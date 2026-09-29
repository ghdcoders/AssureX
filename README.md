# 🛡️ AssureX Claim Engine
**AI-Powered Document Ops & Warranty Validation**  
*Techwiz 7th Edition | Category 5: NextWave AI and ML*

The AssureX Claim Engine automates and optimizes warranty claim evaluations for manufacturers and service centers. By combining a Python-based machine learning classification model with a Google Teachable Machine vision model, AssureX cross-verifies structured claim data against visual evidence to deliver rapid, consistent, and highly accurate adjudication.

---

## 🚀 The Development Team (GHD Coders)
Developed with precision at **Aptech Gulshan-e-Hadeed Center**:
* **Abdul Sattar** – Lead Software Engineer 
* **Muhammad Hasnain** – AI/ML Architect
* **Marium Kamran** – Data Preprocessing Lead
* **Ujala** – Rule Engine & Quality Assurance

---

## 🧠 System Architecture
AssureX utilizes a dual-model consensus architecture to prevent fraud and minimize human error:
1. **Python Classification Model (Structured Data):** Evaluates product age, warranty duration, damage type, and service history using an XGBoost/Scikit-Learn pipeline.
2. **Google Teachable Machine (Visual Data):** Analyzes the visual Claim Summary Card to independently verify the claim classification (Valid, Invalid, or Manual Review).
3. **Business Rule Engine:** Validates hard constraints (e.g., missing receipts, unauthorized repairs, expired warranties).
4. **Adjudication Logic:** Computes the confidence delta between the two AI models and applies rule constraints to output a final unified decision.

---

## ⚙️ Prerequisites & Installation

**Supported OS:** Windows 10/11, macOS, Linux  
**Required Python Version:** Python 3.10 to 3.14  

### 1. Clone the Repository
```bash
git clone [https://github.com/ghdcoders/AssureX.git](https://github.com/ghdcoders/AssureX.git)
cd AssureX

2. Create and Activate a Virtual Environment
Bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
(Dependencies include: streamlit, pandas, numpy, scikit-learn, xgboost, tensorflow, plotly, Pillow)

4. Model Placement Configuration
Ensure your exported models and assets are placed exactly in the following structure before execution:

assurex_python_model.joblib (Root directory)

label_encoder.joblib (Root directory)

converted_savedmodel/ (Must contain the saved_model.pb and variables folder from Google Teachable Machine)

assets/ (Must contain team photos and logo.png)

🖥️ Execution Instructions
To launch the AssureX Claim Engine interface, run the following command in your activated virtual environment:

Bash
streamlit run app.py
Navigating the Application:
Input Claim Details: Use the left panel to input the product category, age, warranty duration, and damage type.

Apply Verification Checks: Check the boxes for receipt availability, serial number matches, and unauthorized repairs.

Upload Visual Evidence: Drag and drop the generated Claim Summary Card (PNG/JPG) into the right panel.

Execute Dual-AI Evaluation: Click the primary evaluation button. The system will run OCR simulations, duplicate detection, and execute both the Python and Vision models.

Review Telemetry: The interface will display the max validity confidence, individual model predictions, the model convergence delta, and the final adjudication (Valid, Invalid, or Manual Review).

📁 Project Structure
Plaintext
AssureX/
│
├── app.py                      # Main Streamlit Dashboard Application
├── inference_engine.py         # Dual-AI loading, comparison, and rule validation logic
├── dataset_generator.py        # Script used to generate the 1,500+ CSV claim records
├── card_generator.py           # Script used to convert CSV records into Summary Card images
├── train_python_model.py       # Scikit-learn/XGBoost training pipeline
│
├── assets/                     # Team photos and application logo
├── dataset/                    # Generated CSV and Test Images
├── converted_savedmodel/       # Exported Google Teachable Machine model
└── policies/                   # JSON configurations for warranty rules
🔒 Security & Privacy
AssureX relies on localized model inference. Uploaded Claim Summary Cards are temporarily processed in memory/local storage and purged immediately following the evaluation to ensure data privacy and compliance.

Created for Techwiz 7. For evaluation purposes only.