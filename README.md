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
git clone [https://github.com/yourusername/AssureX.git](https://github.com/yourusername/AssureX.git)
cd AssureX