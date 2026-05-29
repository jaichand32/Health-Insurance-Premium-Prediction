import streamlit as st
from prediction_helper import predict

# Configure Streamlit Page
st.set_page_config(
    page_title="Health Insurance Premium Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Premium CSS Injection
st.markdown("""
<style>
/* Import Outfit Google Font */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

/* Apply font across Streamlit elements */
html, body, [class*="css"], .stMarkdown {
    font-family: 'Outfit', sans-serif;
}

/* Squeeze the main container to the middle */
.main .block-container {
    max-width: 1050px !important;
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    margin: 0 auto !important;
}

/* Page Titles */
.main-title {
    font-weight: 700;
    background: linear-gradient(90deg, #0F172A 0%, #2563EB 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5rem;
    margin-bottom: 0.2rem;
    text-align: center;
}

.sub-title {
    font-weight: 400;
    color: #475569;
    font-size: 1.05rem;
    margin-bottom: 2rem;
    text-align: center;
}

/* Card/Container Styling (Forced Light Theme) */
div[data-testid="stVerticalBlockBorder"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

div[data-testid="stVerticalBlockBorder"]:hover {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.03) !important;
}

/* Card Section Headers (Vibrant Sky Blue bottom border & Dark Text) */
.section-header {
    display: flex;
    align-items: center;
    font-size: 1.2rem;
    font-weight: 600;
    color: #0F172A !important;
    margin-bottom: 18px;
    border-bottom: 2.5px solid #3B82F6 !important;
    padding-bottom: 8px;
}

/* Button Custom Styling */
.stButton > button {
    background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    padding: 12px 32px !important;
    border-radius: 12px !important;
    border: none !important;
    box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.25) !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
    height: 50px !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px 0 rgba(37, 99, 235, 0.35) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Result Dashboard Card */
.result-card {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
    color: white;
    padding: 24px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.25);
    margin-top: 24px;
}

.result-val {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 8px 0;
}
</style>
""", unsafe_allow_html=True)

# Main Titles
st.markdown('<div class="main-title">🏥 Health Insurance Premium Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Complete the demographics, lifestyle, and health inputs below for a tailored premium forecast</div>', unsafe_allow_html=True)

# Select options dictionary - exact matching with original keys and lists
categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer', ''],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease', 'Diabetes', 'High blood pressure', 'Diabetes & High blood pressure',
        'Thyroid', 'Heart disease', 'High blood pressure & Heart disease', 'Diabetes & Thyroid',
        'Diabetes & Heart disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}

# Create three modern dashboard columns
col1, col2, col3 = st.columns(3)

# Demographic Card
with col1:
    with st.container(border=True):
        st.markdown('<div class="section-header">👤 Demographic Details</div>', unsafe_allow_html=True)
        gender = st.selectbox('Gender', categorical_options['Gender'])
        age = st.number_input('Age', min_value=18, step=1, max_value=100)
        marital_status = st.selectbox('Marital Status', categorical_options['Marital Status'])
        number_of_dependants = st.number_input('Number of Dependants', min_value=0, step=1, max_value=20)

# Lifestyle & Occupation Card
with col2:
    with st.container(border=True):
        st.markdown('<div class="section-header">💼 Lifestyle & Income</div>', unsafe_allow_html=True)
        income_lakhs = st.number_input('Income in Lakhs', step=1, min_value=0, max_value=200)
        employment_status = st.selectbox('Employment Status', categorical_options['Employment Status'])
        bmi_category = st.selectbox('BMI Category', categorical_options['BMI Category'])
        smoking_status = st.selectbox('Smoking Status', categorical_options['Smoking Status'])

# Coverage & Health Card
with col3:
    with st.container(border=True):
        st.markdown('<div class="section-header">🛡️ Coverage & Health</div>', unsafe_allow_html=True)
        insurance_plan = st.selectbox('Insurance Plan', categorical_options['Insurance Plan'])
        region = st.selectbox('Region', categorical_options['Region'])
        genetical_risk = st.number_input('Genetical Risk', step=1, min_value=0, max_value=5)
        medical_history = st.selectbox('Medical History', categorical_options['Medical History'])

# Mapping of variables to prediction keys - exact matching
input_dict = {
    'Age': age,
    'Number of Dependants': number_of_dependants,
    'Income in Lakhs': income_lakhs,
    'Genetical Risk': genetical_risk,
    'Insurance Plan': insurance_plan,
    'Employment Status': employment_status,
    'Gender': gender,
    'Marital Status': marital_status,
    'BMI Category': bmi_category,
    'Smoking Status': smoking_status,
    'Region': region,
    'Medical History': medical_history
}

st.write("") # Layout spacer

# Center-aligned Predict Button
col_b1, col_b2, col_b3 = st.columns([1, 1, 1])
with col_b2:
    predict_btn = st.button('Predict')

# Display Predict Results in a beautiful Card
if predict_btn:
    prediction = predict(input_dict)
    st.markdown(f"""
    <div class="result-card">
        <div style="font-size: 1.1rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">Estimated Annual Premium</div>
        <div class="result-val">₹{prediction:,}</div>
        <div style="font-size: 0.9rem; opacity: 0.85;">Based on your demographic profile & calculated medical risk</div>
    </div>
    """, unsafe_allow_html=True)
