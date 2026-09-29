import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def generate_dataset(num_records=1500):
    data = []
    # Enforce the strict 500/500/500 split required by the SRS
    statuses = ['Valid Claim'] * 500 + ['Invalid Claim'] * 500 + ['Manual Review'] * 500
    random.shuffle(statuses)

    for status in statuses:
        claim_id = f"CLM-{fake.unique.random_int(min=10000, max=99999)}"
        product_age_days = random.randint(10, 1000)
        
        # Base logical defaults
        warranty_duration_months = random.choice([12, 24, 36])
        receipt_provided = True
        serial_match = True
        unauthorized_repair = False
        damage_type = random.choice(["Hardware Failure", "Software Glitch", "Screen Defect", "Battery Issue"])
        
        # Inject realistic rule-breaking anomalies for Invalid Claims
        if status == 'Invalid Claim':
            condition = random.choice(['expired', 'no_receipt', 'serial_mismatch', 'unauthorized'])
            if condition == 'expired':
                product_age_days = (warranty_duration_months * 30) + random.randint(10, 200)
            elif condition == 'no_receipt':
                receipt_provided = False
            elif condition == 'serial_mismatch':
                serial_match = False
            elif condition == 'unauthorized':
                unauthorized_repair = True
                
        # Inject borderline cases for Manual Review
        elif status == 'Manual Review':
            condition = random.choice(['borderline_date', 'missing_doc', 'suspicious_fault'])
            if condition == 'borderline_date':
                # Claim submitted just days before warranty expiry
                product_age_days = (warranty_duration_months * 30) - random.randint(1, 5) 
            elif condition == 'missing_doc':
                receipt_provided = random.choice([True, False])
            elif condition == 'suspicious_fault':
                damage_type = "Water Damage" 

        # Calculate logical dates
        purchase_date = datetime.now() - timedelta(days=product_age_days)
        fault_date = purchase_date + timedelta(days=random.randint(1, product_age_days))

        data.append({
            "Claim_ID": claim_id,
            "Product_Category": random.choice(["Laptop", "Smartphone", "Washing Machine", "Refrigerator"]),
            "Product_Age_Days": product_age_days,
            "Warranty_Duration_Months": warranty_duration_months,
            "Purchase_Date": purchase_date.strftime("%Y-%m-%d"),
            "Fault_Date": fault_date.strftime("%Y-%m-%d"),
            "Receipt_Provided": receipt_provided,
            "Serial_Number_Match": serial_match,
            "Unauthorized_Repair_History": unauthorized_repair,
            "Damage_Type": damage_type,
            "Missing_Documents_Count": 0 if receipt_provided else random.randint(1, 3),
            "Target_Class": status
        })

    df = pd.DataFrame(data)
    df.to_csv('assurex_claims_dataset.csv', index=False)
    print("Dataset generated successfully: assurex_claims_dataset.csv")
    return df

if __name__ == "__main__":
    generate_dataset(1500)