import streamlit as st
import pandas as pd
from PIL import Image
import os
import time
import base64
import plotly.graph_objects as go
from inference_engine import AssureXEngine

# --- Helper Functions ---
def get_image_path(base_name):
    """Safely fetch images regardless of duplicate extensions."""
    paths = [f"assets/{base_name}", f"assets/{base_name}.png", f"assets/{base_name}.jpg", 
             f"assets/{base_name}.png.png", f"assets/{base_name}.jpg.jpg"]
    for path in paths:
        if os.path.exists(path): return path
    return None

def img_to_base64(img_path):
    """Converts images to Base64 to prevent Streamlit from breaking HTML div structures."""
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# --- UI Configuration ---
# Load the logo image for the browser tab
logo_path = get_image_path("logo.png")
tab_icon = Image.open(logo_path) if logo_path else "🛡️"

st.set_page_config(
    page_title="AssureX Claim Engine", 
    page_icon=tab_icon, 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- Clean SRS Light Theme CSS ---
st.markdown("""
<style>
    /* Force Light Mode Background & Text */
    .stApp { 
        background-color: #ffffff !important;
        color: #1e293b !important; 
    }
    
    /* Clean Light Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8fafc !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    /* Input Fields & File Uploader */
    .stSelectbox div[data-baseweb="select"], .stNumberInput input, div[data-testid="stFileUploader"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        color: #0f172a !important;
        border-radius: 6px !important;
    }
    
    /* Main SRS Red Evaluate Button */
    div.stButton > button:first-child {
        background-color: #ef4444 !important;
        color: #ffffff !important;
        width: 100%;
        border-radius: 6px;
        border: none !important;
        font-weight: 700;
        font-size: 18px;
        padding: 10px;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.2) !important;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        background-color: #dc2626 !important;
        box-shadow: 0 10px 15px -3px rgba(239, 68, 68, 0.3) !important;
    }
    
    /* Typography Overrides */
    h1, h2, h3, h4, p, label, span, .stCheckbox > label { 
        color: #0f172a !important; 
        font-family: 'Inter', sans-serif;
    }
    
    /* Status Pill */
    .status-pill {
        background: #dcfce7;
        color: #166534 !important;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        border: 1px solid #86efac;
        font-size: 14px;
    }

    /* Sidebar Team Cards */
    .team-member {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 12px;
        text-align: center;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    .team-member img {
        width: 100%;
        border-radius: 6px;
    }
    .team-name { font-weight: 800; color: #0f172a !important; font-size: 15px; margin-top: 10px;}
    .team-role { color: #2563eb !important; font-size: 12px; font-weight: 700; text-transform: uppercase;}
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Load the AI Engine ---
@st.cache_resource
def load_engine():
    return AssureXEngine()

engine = load_engine()

# --- Sidebar: Competition, Team & Contacts ---
with st.sidebar:
    if logo_path:
        logo_b64 = img_to_base64(logo_path)
        st.markdown(f"<img src='data:image/png;base64,{logo_b64}' style='width:100%; max-width:180px; display:block; margin:0 auto 15px auto;'>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align:center; color:#2563eb !important;'>🛡️ AssureX</h2>", unsafe_allow_html=True)
        
    st.markdown("<div style='text-align:center; color:#64748b; margin-bottom:20px; font-weight:600;'>Techwiz 7th Edition<br>Category 5: AI & ML</div>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("<h4 style='text-align:center;'>DEVELOPMENT TEAM</h4>", unsafe_allow_html=True)
    
    team_data = [
        {"name": "Abdul Sattar", "role": "Lead Software Engineer", "img": "abdul.png"},
        {"name": "Muhammad Hasnain", "role": "AI/ML Architect", "img": "hasnain.png"},
        {"name": "Marium Kamran", "role": "Data Preprocessing Lead", "img": "marium.png"},
        {"name": "Ujala", "role": "Rule Engine & QA", "img": "ujala.png"}
    ]
    
    for member in team_data:
        img_path = get_image_path(member["img"])
        if img_path:
            img_b64 = img_to_base64(img_path)
            st.markdown(f"""
            <div class='team-member'>
                <img src="data:image/png;base64,{img_b64}">
                <div class='team-name'>{member['name']}</div>
                <div class='team-role'>{member['role']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; text-align: center; margin-top: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>
        <span style='color:#64748b; font-size:12px; font-weight:800;'>GHD CODERS</span><br><br>
        <a href='mailto:info@ghdcoders.com' style='color:#2563eb; text-decoration:none; font-weight:bold; display:block; margin:5px 0;'>info@ghdcoders.com</a>
        <a href='tel:03046585559' style='color:#2563eb; text-decoration:none; font-weight:bold; display:block; margin:5px 0;'>0304 6585559</a>
        <a href='https://facebook.com/ghdcoders' target='_blank' style='color:#2563eb; text-decoration:none; font-weight:bold; display:block; margin:5px 0;'>fb.com/ghdcoders</a>
    </div>
    """, unsafe_allow_html=True)

# --- Main Interface ---
head_col1, head_col2 = st.columns([4, 1])
with head_col1:
    if logo_path:
        logo_b64 = img_to_base64(logo_path)
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:15px;'>
            <img src="data:image/png;base64,{logo_b64}" style="width:60px; object-fit:contain;">
            <h2 style='margin:0;'>AssureX Claim Engine</h2>
        </div>
        <span style='color:#64748b; font-size: 16px; font-weight:500; display:block; margin-top:5px;'>AI-Powered Document Ops & Warranty Validation</span>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='margin-top:-10px;'>AssureX Claim Engine</h2><span style='color:#64748b; font-size: 16px; font-weight:500;'>AI-Powered Document Ops & Warranty Validation</span>", unsafe_allow_html=True)
with head_col2:
    st.markdown("<br><div style='text-align: right;'><span class='status-pill'>SYSTEM ONLINE</span></div>", unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 1. Enter Claim Details")
    with st.container(border=True):
        r1c1, r1c2 = st.columns(2)
        with r1c1:
            product_category = st.selectbox("Product Category", ["Laptop", "Smartphone", "Washing Machine", "Refrigerator"])
            warranty_duration = st.selectbox("Warranty Duration (Months)", [12, 24, 36])
        with r1c2:
            product_age = st.number_input("Product Age (Days)", min_value=0, max_value=2000, value=150)
            damage_type = st.selectbox("Damage Type", ["Hardware Failure", "Software Glitch", "Screen Defect", "Battery Issue", "Water Damage"])
        
        st.markdown("<hr style='margin: 15px 0; border-color: #e2e8f0;'>", unsafe_allow_html=True)
        st.markdown("**Verification Checks**")
        check_col1, check_col2 = st.columns(2)
        with check_col1:
            receipt_provided = st.checkbox("Receipt Provided", value=True)
            serial_match = st.checkbox("Serial Number Matches", value=True)
        with check_col2:
            unauthorized_repair = st.checkbox("Unauthorized Repair Detected", value=False)
            duplicate_check = st.checkbox("Run Duplicate Scan", value=True)

with col2:
    st.markdown("### 2. Upload Claim Summary Card")
    with st.container(border=True):
        st.info("Upload a visual Claim Summary Card to be evaluated by the Google Teachable Machine model.", icon="ℹ️")
        uploaded_file = st.file_uploader("Choose a summary card image (PNG/JPG)", type=["png", "jpg", "jpeg"])
        
        temp_path = None
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            temp_path = os.path.join("dataset", "temp_upload.png")
            os.makedirs("dataset", exist_ok=True)
            image.save(temp_path)
            st.image(image, caption="Ready for Analysis", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
evaluate_clicked = st.button("Evaluate Claim")
st.markdown("<br>", unsafe_allow_html=True)

# --- Evaluation Engine Results ---
st.markdown("### 3. Claim Decision")

if not evaluate_clicked:
    with st.container(border=True):
        st.markdown("<div style='text-align:center; padding: 40px; color:#94a3b8; font-weight:600; font-size: 16px;'>AWAITING CLAIM SUBMISSION...</div>", unsafe_allow_html=True)
else:
    if uploaded_file is None:
        st.error("Please upload a Claim Summary Card image before evaluating.")
    else:
        with st.spinner("Processing AssureX Dual-AI Verification..."):
            time.sleep(1)
            
            claim_data = {
                "Product_Category": product_category,
                "Product_Age_Days": product_age,
                "Warranty_Duration_Months": warranty_duration,
                "Receipt_Provided": receipt_provided,
                "Serial_Number_Match": serial_match,
                "Unauthorized_Repair_History": unauthorized_repair,
                "Damage_Type": damage_type,
                "Missing_Documents_Count": 0 if receipt_provided else 1
            }
            
            result = engine.process_unified_claim(claim_data, temp_path)
            
            with st.container(border=True):
                res_col1, res_col2 = st.columns([1.2, 2])
                
                with res_col1:
                    final_conf = max(result['python_model']['confidence'], result['keras_model']['confidence'])
                    color = "#22c55e" if result['final_decision'] == "Likely Valid" else ("#ef4444" if result['final_decision'] == "Likely Invalid" else "#f59e0b")
                    
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = final_conf,
                        title = {'text': "Confidence Score", 'font': {'color': '#475569', 'size': 16}},
                        number = {'suffix': "%", 'font': {'color': '#0f172a', 'size': 45}},
                        gauge = {
                            'axis': {'range': [None, 100], 'visible': False},
                            'bar': {'color': color},
                            'bgcolor': "#f1f5f9",
                            'borderwidth': 0
                        }
                    ))
                    fig.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig, use_container_width=True)

                with res_col2:
                    st.markdown("<h4 style='color:#0f172a; margin-top:10px;'>Model Diagnostics</h4>", unsafe_allow_html=True)
                    
                    def draw_progress(label, value, bar_color, prediction):
                        st.markdown(f"""
                        <div style='margin-bottom: 12px;'>
                            <div style='display:flex; justify-content:space-between; margin-bottom:4px;'>
                                <span style='color:#475569; font-size:14px; font-weight:600;'>{label}</span>
                                <span style='color:{bar_color}; font-size:14px; font-weight:bold;'>{prediction} ({value:.1f}%)</span>
                            </div>
                            <div style='background-color:#f1f5f9; border-radius:6px; height:8px; width:100%; border: 1px solid #e2e8f0;'>
                                <div style='background-color:{bar_color}; height:6px; border-radius:6px; width:{value}%;'></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    draw_progress("Python AI Model (Structured Data)", result['python_model']['confidence'], "#3b82f6", result['python_model']['prediction'])
                    draw_progress("Image AI Model (Teachable Machine)", result['keras_model']['confidence'], "#8b5cf6", result['keras_model']['prediction'])
                    draw_progress("Model Confidence Comparison", 100 - result['confidence_difference'], color, result['model_consistency'])

            if result['final_decision'] == "Likely Valid":
                st.success(f"### VALID CLAIM\nApproved based on model confidence and business rules.")
            elif result['final_decision'] == "Likely Invalid":
                st.error(f"### INVALID CLAIM\nDoes not meet policy terms or model validity thresholds.")
            else:
                st.warning(f"### MANUAL REVIEW\nRequires further assessment due to low confidence or rule violations.")
                
            if result['rule_violations']:
                st.error(f"**Policy Exclusions Detected:** {', '.join(result['rule_violations'])}")

    if evaluate_clicked and temp_path and os.path.exists(temp_path):
        os.remove(temp_path)