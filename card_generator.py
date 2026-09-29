import pandas as pd
import os
from PIL import Image, ImageDraw, ImageFont
from sklearn.model_selection import train_test_split

def create_folders():
    base_dir = "dataset"
    splits = ["train", "validation", "test"]
    classes = ["Valid Claim", "Invalid Claim", "Manual Review"]
    
    for split in splits:
        for cls in classes:
            os.makedirs(os.path.join(base_dir, split, cls), exist_ok=True)
    return base_dir

def generate_card_image(record, output_path, variation="light"):
    # Dimensions and color schemes for variations
    width, height = 600, 400
    if variation == "light":
        bg_color, text_color = (255, 255, 255), (0, 0, 0)
    else:
        bg_color, text_color = (30, 30, 30), (255, 255, 255)

    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Text formatting (using default PIL font for universal compatibility)
    y_text = 40
    lines = [
        f"Claim ID: {record['Claim_ID']}",
        f"Product Category: {record['Product_Category']}",
        f"Product Age (Days): {record['Product_Age_Days']}",
        f"Warranty Duration: {record['Warranty_Duration_Months']} Months",
        f"Purchase Date: {record['Purchase_Date']}",
        f"Fault Date: {record['Fault_Date']}",
        f"Receipt Provided: {record['Receipt_Provided']}",
        f"Serial Number Match: {record['Serial_Number_Match']}",
        f"Unauthorized Repair: {record['Unauthorized_Repair_History']}",
        f"Damage Type: {record['Damage_Type']}",
        f"Missing Documents: {record['Missing_Documents_Count']}"
    ]
    
    # Title
    draw.text((20, 10), "ASSUREX CLAIM SUMMARY CARD", fill=text_color)
    draw.line((20, 30, 580, 30), fill=text_color, width=2)

    # Content
    for line in lines:
        draw.text((20, y_text), line, fill=text_color)
        y_text += 30

    img.save(output_path)

def process_dataset(csv_path):
    df = pd.read_csv(csv_path)
    base_dir = create_folders()
    
    # Stratified split: 70% Train, 30% Temp (Val/Test)
    train_df, temp_df = train_test_split(df, test_size=0.30, stratify=df['Target_Class'], random_state=42)
    # Split Temp into 15% Validation, 15% Testing
    val_df, test_df = train_test_split(temp_df, test_size=0.50, stratify=temp_df['Target_Class'], random_state=42)

    def process_split(data, split_name, generate_variations=False):
        count = 0
        for _, row in data.iterrows():
            target_dir = os.path.join(base_dir, split_name, row['Target_Class'])
            
            if generate_variations:
                # Generate two variations for training to hit the 2,100+ requirement
                generate_card_image(row, os.path.join(target_dir, f"{row['Claim_ID']}_v1.png"), "light")
                generate_card_image(row, os.path.join(target_dir, f"{row['Claim_ID']}_v2.png"), "dark")
                count += 2
            else:
                generate_card_image(row, os.path.join(target_dir, f"{row['Claim_ID']}.png"), "light")
                count += 1
        print(f"Generated {count} images for {split_name} split.")

    print("Generating Claim Summary Cards...")
    process_split(train_df, "train", generate_variations=True)
    process_split(val_df, "validation", generate_variations=False)
    process_split(test_df, "test", generate_variations=False)
    print("All image generation complete. Ready for Google Teachable Machine.")

if __name__ == "__main__":
    process_dataset('assurex_claims_dataset.csv')