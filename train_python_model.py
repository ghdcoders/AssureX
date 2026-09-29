import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib

def train_and_evaluate():
    print("Loading dataset...")
    df = pd.read_csv('assurex_claims_dataset.csv')

    # 1. Feature Selection
    X = df.drop(columns=['Claim_ID', 'Target_Class', 'Purchase_Date', 'Fault_Date']).copy()
    y = df['Target_Class']

    # 2. Convert boolean features to integers upfront to avoid pandas dtype conflicts
    boolean_features = ['Receipt_Provided', 'Serial_Number_Match', 'Unauthorized_Repair_History']
    for col in boolean_features:
        X[col] = X[col].astype(int)

    # 3. Encode Target Labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    joblib.dump(le, 'label_encoder.joblib')
    print(f"Classes mapped to: {dict(zip(le.classes_, le.transform(le.classes_)))}")

    # 4. Stratified Split (70% Train, 30% Test/Validation)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.30, stratify=y_encoded, random_state=42
    )

    # 5. Data Preprocessing Setup
    categorical_features = ['Product_Category', 'Damage_Type']
    numerical_features = ['Product_Age_Days', 'Warranty_Duration_Months', 'Missing_Documents_Count']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features + boolean_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )

    # 6. Define Three Algorithms for Comparison
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost": XGBClassifier(eval_metric='mlogloss', random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42)
    }

    best_model_name = ""
    best_accuracy = 0
    best_pipeline = None

    print("\n--- Comparing Models ---")
    for name, model in models.items():
        pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', model)])
        pipeline.fit(X_train, y_train)
        
        y_pred = pipeline.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"{name} Accuracy: {acc * 100:.2f}%")
        
        if acc > best_accuracy:
            best_accuracy = acc
            best_model_name = name
            best_pipeline = pipeline

    # 7. Detailed Evaluation of the Best Model
    print(f"\n--- Best Model Selected: {best_model_name} ---")
    y_pred_best = best_pipeline.predict(X_test)
    
    print("\nClassification Report (Precision, Recall, F1-Score):")
    print(classification_report(y_test, y_pred_best, target_names=le.classes_))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred_best))

    # 8. Test Confidence Score Generation
    sample = X_test.iloc[[0]]
    probabilities = best_pipeline.predict_proba(sample)[0]
    print("\n--- Confidence Score Extraction Test ---")
    for cls, prob in zip(le.classes_, probabilities):
        print(f"{cls}: {prob * 100:.2f}% confidence")

    # 9. Export the Model
    joblib.dump(best_pipeline, 'assurex_python_model.joblib')
    print("\nModel saved successfully as 'assurex_python_model.joblib'")

if __name__ == "__main__":
    train_and_evaluate()