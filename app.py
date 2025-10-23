import streamlit as st
import pickle
import numpy as np

# Load model
model = pickle.load(open('model.pkl', 'rb'))

st.set_page_config(page_title="Prediksi Customer Churn", page_icon="📊", layout="centered")

# Judul
st.markdown(
    """
    <h1 style='text-align: center; color: #003366;'>📊 Prediksi Customer Churn</h1>
    <p style='text-align: center;'>Masukkan detail pelanggan untuk memprediksi kemungkinan churn.</p>
    <hr>
    """,
    unsafe_allow_html=True
)

# --- INPUT FORM ---
with st.form("churn_form"):
    col1, col2 = st.columns(2)

    with col1:
        MonthlyCharges = st.number_input("Monthly Charges", min_value=0.0, step=1.0)
        TotalCharges = st.number_input("Total Charges", min_value=0.0, step=1.0)
        tenure = st.number_input("Tenure (bulan)", min_value=0)
        gender = st.selectbox("Gender", ("Female", "Male"))
        Partner = st.selectbox("Partner", ("No", "Yes"))
        Dependents = st.selectbox("Dependents", ("No", "Yes"))
        PhoneService = st.selectbox("Phone Service", ("No", "Yes"))
        MultipleLines = st.selectbox("Multiple Lines", ("No", "Yes"))

    with col2:
        OnlineSecurity = st.selectbox("Online Security", ("No", "Yes"))
        OnlineBackup = st.selectbox("Online Backup", ("No", "Yes"))
        DeviceProtection = st.selectbox("Device Protection", ("No", "Yes"))
        TechSupport = st.selectbox("Tech Support", ("No", "Yes"))
        StreamingTV = st.selectbox("Streaming TV", ("No", "Yes"))
        StreamingMovies = st.selectbox("Streaming Movies", ("No", "Yes"))
        PaperlessBilling = st.selectbox("Paperless Billing", ("No", "Yes"))
        InternetService = st.selectbox("Internet Service", ("No", "DSL", "Fiber optic"))
        Contract = st.selectbox("Contract", ("Month-to-month", "One year", "Two year"))
        PaymentMethod = st.selectbox(
            "Payment Method",
            ("Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)")
        )
        SeniorCitizen = st.selectbox("Senior Citizen", ("No", "Yes"))

    submitted = st.form_submit_button("Prediksi Churn")

# --- ENCODING ---
if submitted:
    mapping = {
        "gender": {"Female": 0, "Male": 1},
        "Partner": {"No": 0, "Yes": 1},
        "Dependents": {"No": 0, "Yes": 1},
        "PhoneService": {"No": 0, "Yes": 1},
        "MultipleLines": {"No": 0, "Yes": 1},
        "OnlineSecurity": {"No": 0, "Yes": 1},
        "OnlineBackup": {"No": 0, "Yes": 1},
        "DeviceProtection": {"No": 0, "Yes": 1},
        "TechSupport": {"No": 0, "Yes": 1},
        "StreamingTV": {"No": 0, "Yes": 1},
        "StreamingMovies": {"No": 0, "Yes": 1},
        "PaperlessBilling": {"No": 0, "Yes": 1},
        "InternetService": {"No": 0, "DSL": 1, "Fiber optic": 2},
        "Contract": {"Month-to-month": 0, "One year": 1, "Two year": 2},
        "PaymentMethod": {
            "Electronic check": 0,
            "Mailed check": 1,
            "Bank transfer (automatic)": 2,
            "Credit card (automatic)": 3,
        },
        "SeniorCitizen": {"No": 0, "Yes": 1},
    }

    # Transform input sesuai urutan fitur model
    data = np.array([
        MonthlyCharges,
        mapping["Contract"][Contract],
        TotalCharges,
        tenure,
        mapping["InternetService"][InternetService],
        mapping["PaymentMethod"][PaymentMethod],
        mapping["PhoneService"][PhoneService],
        mapping["OnlineSecurity"][OnlineSecurity],
        mapping["OnlineBackup"][OnlineBackup],
        mapping["TechSupport"][TechSupport],
        mapping["StreamingTV"][StreamingTV],
        mapping["StreamingMovies"][StreamingMovies],
        mapping["gender"][gender],
        mapping["DeviceProtection"][DeviceProtection],
        mapping["Partner"][Partner],
        mapping["MultipleLines"][MultipleLines],
        mapping["Dependents"][Dependents],
        mapping["PaperlessBilling"][PaperlessBilling],
        mapping["SeniorCitizen"][SeniorCitizen]
    ]).reshape(1, -1)

    # Prediksi
    prediction = model.predict(data)[0]

    if prediction == 1:
        st.success("💡 Hasil Prediksi: **CHURN** — Pelanggan berpotensi berhenti berlangganan.")
    else:
        st.info("✅ Hasil Prediksi: **TIDAK CHURN** — Pelanggan diperkirakan tetap berlangganan.")

# --- FOOTER ---
st.markdown(
    """
    <hr>
    <p style='text-align:center; color: gray; font-size: 13px;'>
    © 2025 Prediksi Churn Streamlit App | Dibuat oleh Salzi
    </p>
    """,
    unsafe_allow_html=True
)

