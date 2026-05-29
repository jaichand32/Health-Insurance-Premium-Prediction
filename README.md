# Health Insurance Premium Predictor

An interactive, machine learning-powered web application built with **Streamlit** to predict health insurance premiums based on individual demographic, lifestyle, medical, and socio-economic factors.

The project features a segmented model architecture that dynamically selects the best prediction pipeline based on the user's demographic cohort (specifically age group), and calculates an engineered medical risk profile from their medical history.

---

## Key Features

* **Interactive Web Interface**: Built using Streamlit, providing a clean, response-driven, and easy-to-use user form.
* **Dual-Model Predictive Pipeline**: Dynamically routes prediction requests to different machine learning models depending on whether the individual is in the young cohort (≤ 25 years old) or adult/senior cohort (> 25 years old).
* **Engineered Medical Risk Score**: Automatically parses and normalizes compound medical history conditions into a normalized risk score between 0.0 and 1.0.
* **Instant Predictions**: Generates premium predictions in real time as the user fills out the form.

---

## Tech Stack & Libraries

* **Frontend Framework**: [Streamlit](https://streamlit.io/) (v1.57.0)
* **Machine Learning & Serialization**: [Scikit-Learn](https://scikit-learn.org/) (v1.8.0), [XGBoost](https://xgboost.readthedocs.io/) (v3.2.0), [Joblib](https://joblib.readthedocs.io/) (v1.5.3)
* **Data Manipulation**: [Pandas](https://pandas.pydata.org/) (v3.0.3), [Numpy](https://numpy.org/) (v2.4.4)
* **Python Runtime**: Python 3.x

---

## Model Architecture & Logic

### 1. Cohort Segmentation (Age-based Routing)
Demographic and medical data analysis indicates that individuals aged 25 and under present different premium risk profiles compared to older age brackets. Thus, the system loads and routes predictions through separate preprocessing scalers and predictive models:

* **Young Cohort (Age ≤ 25)**: Utilizes `scaler_young.joblib` and `model_young.joblib`.
* **Standard/Adult Cohort (Age > 25)**: Utilizes `scaler_rest.joblib` and `model_rest.joblib`.

### 2. Medical History Risk Normalization
Medical conditions are mapped to predefined risk values:

| Condition | Risk Score |
| :--- | :---: |
| **Heart Disease** | 8 |
| **Diabetes** | 6 |
| **High Blood Pressure** | 6 |
| **Thyroid** | 5 |
| **No Disease / None** | 0 |

#### Risk Score Calculation & Normalization Formula:
1. **Splitting & Parsing**: Compound medical histories (e.g., `"Diabetes & High blood pressure"`) are parsed and split by the `&` delimiter.
2. **Summing**: The raw risk scores for all present conditions are summed:
   $$\text{Raw Risk} = \sum \text{Risk Score}(\text{condition})$$
3. **Normalization**: The raw risk is normalized to a $[0, 1]$ scale. The maximum possible raw risk score is set to $14$ (which corresponds to Heart Disease (8) + the next highest risk condition (6), i.e., Diabetes or High Blood Pressure):
   $$\text{Normalized Risk Score} = \frac{\text{Raw Risk} - 0}{14}$$

---

## Project Directory Structure

```text
Healthcare-Premium-Prediction/
│
├── artifacts/                  # Serialized ML models and scalers
│   ├── model_rest.joblib       # XGBoost/Sklearn model for Age > 25
│   ├── model_young.joblib      # XGBoost/Sklearn model for Age <= 25
│   ├── scaler_rest.joblib      # StandardScaler/Scaler metadata for Age > 25
│   └── scaler_young.joblib     # StandardScaler/Scaler metadata for Age <= 25
│
├── main.py                     # Streamlit frontend application
├── prediction_helper.py        # Input preprocessing, feature engineering & prediction logic
├── requirements.txt            # Python package dependencies
├── LICENSE                     # Project License (Apache 2.0)
└── README.md                   # Project documentation (this file)
```

---

## Installation & Setup

Follow these steps to run the application locally on your machine:

### Prerequisites
Make sure you have **Python 3.8+** installed.

### 1. Clone or Navigate to the Directory
Ensure you are in the project's root folder:
```bash
cd Healthcare-Premium-Prediction
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
Create and activate a virtual environment to isolate the project dependencies:
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows (Command Prompt)
venv\Scripts\activate
# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
Install all required libraries using the package manager `pip`:
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
Start the Streamlit local development server:
```bash
streamlit run main.py
```
This will start a server and open the web application automatically in your default browser at `http://localhost:8501`.

---

## Usage Guide

Provide the application with the following inputs in the form:
1. **Age**: Select your age (18 - 100).
2. **Number of Dependants**: Choose the number of dependents (0 - 20).
3. **Income in Lakhs**: Enter annual income in Lakhs (0 - 200).
4. **Genetical Risk**: Risk factors rating (0 - 5).
5. **Insurance Plan**: Choose your tier (**Bronze**, **Silver**, or **Gold**).
6. **Employment Status**: **Salaried**, **Self-Employed**, **Freelancer**, or leave blank.
7. **Gender**: **Male** or **Female**.
8. **Marital Status**: **Married** or **Unmarried**.
9. **BMI Category**: Choose from **Underweight**, **Normal**, **Overweight**, or **Obesity**.
10. **Smoking Status**: **No Smoking**, **Occasional**, or **Regular**.
11. **Region**: **Northeast**, **Northwest**, **Southeast**, or **Southwest**.
12. **Medical History**: Select pre-existing conditions or choose **No Disease**.

Click the **Predict** button to view the estimated premium value instantly.

---

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](file:///c:/Code/Notebook/ML/HealthCarePremiumPrediction/Healthcare-Premium-Prediction/LICENSE) file for details.
