import pandas as pd
import numpy as np
import joblib
import json
import tensorflow as tf
from PIL import Image, ImageOps
import os

class AssureXEngine:
    def __init__(self):
        # 1. Load the Python Model & Preprocessor
        print("Loading Python Model...")
        self.python_model = joblib.load('assurex_python_model.joblib')
        self.label_encoder = joblib.load('label_encoder.joblib')
        
        # 2. Load the Google Teachable Machine Model (SavedModel Format)
        print("Loading Teachable Machine Model...")
        np.set_printoptions(suppress=True)
        
        model_dir = 'converted_savedmodel'
        
        # Load the frozen execution graph directly
        self.tm_model = tf.saved_model.load(model_dir)
        self.tm_infer = self.tm_model.signatures['serving_default']
        
        # Load Teachable Machine Labels
        self.keras_labels = []
        with open(os.path.join(model_dir, 'labels.txt'), 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    self.keras_labels.append(line.split(' ', 1)[1])

        # 3. Load Business Rules
        with open('policies/warranty_rules.json', 'r') as f:
            self.rules = json.load(f)

    def evaluate_python_model(self, claim_data: dict):
        df = pd.DataFrame([claim_data])
        
        boolean_features = ['Receipt_Provided', 'Serial_Number_Match', 'Unauthorized_Repair_History']
        for col in boolean_features:
            df[col] = df[col].astype(int)
            
        probabilities = self.python_model.predict_proba(df)[0]
        pred_idx = np.argmax(probabilities)
        
        return {
            "prediction": self.label_encoder.classes_[pred_idx],
            "confidence": float(probabilities[pred_idx] * 100),
            "all_scores": {cls: float(prob * 100) for cls, prob in zip(self.label_encoder.classes_, probabilities)}
        }

    def evaluate_keras_model(self, image_path: str):
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image = Image.open(image_path).convert('RGB')
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data[0] = normalized_image_array
        
        # Run inference using the SavedModel signature
        tensor_data = tf.convert_to_tensor(data)
        prediction_dict = self.tm_infer(tensor_data)
        
        # Extract the prediction array from the dictionary
        prediction = list(prediction_dict.values())[0].numpy()
        pred_idx = np.argmax(prediction)
        
        return {
            "prediction": self.keras_labels[pred_idx],
            "confidence": float(prediction[0][pred_idx] * 100),
            "all_scores": {cls: float(prob * 100) for cls, prob in zip(self.keras_labels, prediction[0])}
        }

    def rule_validation(self, claim_data: dict):
        category = claim_data.get("Product_Category", "Laptop")
        policy = self.rules["policies"].get(category, self.rules["policies"]["Laptop"])
        
        violations = []
        if claim_data["Product_Age_Days"] > policy["max_age_days_extended"]:
            violations.append("Warranty Expired")
        if claim_data["Damage_Type"] in policy["exclusions"]:
            violations.append(f"Excluded Damage: {claim_data['Damage_Type']}")
        if policy["requires_receipt"] and not claim_data["Receipt_Provided"]:
            violations.append("Missing Purchase Receipt")
        if policy["requires_serial_match"] and not claim_data["Serial_Number_Match"]:
            violations.append("Serial Number Mismatch")
        if not policy["allow_unauthorized_repair"] and claim_data["Unauthorized_Repair_History"]:
            violations.append("Unauthorized Repair Detected")
            
        return violations

    def process_unified_claim(self, claim_data: dict, summary_card_path: str):
        py_result = self.evaluate_python_model(claim_data)
        tm_result = self.evaluate_keras_model(summary_card_path)
        violations = self.rule_validation(claim_data)
        
        conf_diff = abs(py_result["confidence"] - tm_result["confidence"])
        classes_match = (py_result["prediction"] == tm_result["prediction"])
        
        thresh = self.rules["confidence_thresholds"]
        if not classes_match:
            consistency = "Model Disagreement"
        elif conf_diff <= thresh["strong_match_diff"]:
            consistency = "Strong Match"
        elif conf_diff <= thresh["acceptable_match_diff"]:
            consistency = "Acceptable Match"
        else:
            consistency = "Weak Match"

        if consistency == "Model Disagreement" or len(violations) > 0 or not classes_match:
            final_decision = "Manual Review Required"
        elif py_result["prediction"] == "Valid Claim" and py_result["confidence"] > thresh["minimum_valid_confidence"]:
            final_decision = "Likely Valid"
        elif py_result["prediction"] == "Invalid Claim":
            final_decision = "Likely Invalid"
        else:
            final_decision = "Manual Review Required"

        return {
            "python_model": py_result,
            "keras_model": tm_result,
            "rule_violations": violations,
            "confidence_difference": round(conf_diff, 2),
            "model_consistency": consistency,
            "final_decision": final_decision
        }