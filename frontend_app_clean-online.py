
import streamlit as st
import requests

st.set_page_config(page_title="Health Premium Estimator", layout="centered")

st.title("🩺 Health Insurance Premium Predictor © Maduhu, Chloe and Sonia")
st.write("Answer the questions below to estimate your annual health insurance premium.")

# Collect inputs
age = st.number_input("What is your age?", min_value=18, max_value=100, value=30)

diabetes = st.selectbox("Do you have diabetes?", [" ", "No", "Yes"])
bp = st.selectbox("Do you have blood pressure problems?", [" ", "No", "Yes"])
transplants = st.selectbox("Have you had any organ transplants?", [" ", "No", "Yes"])
chronic = st.selectbox("Do you have any chronic diseases?", [" ", "No", "Yes"])

height = st.number_input("What is your height in cm?", min_value=100.0, max_value=250.0, value=170.0)
weight = st.number_input("What is your weight in kg?", min_value=30.0, max_value=200.0, value=70.0)

allergies = st.selectbox("Do you have any known allergies?", [" ", "No", "Yes"])
cancer_history = st.selectbox("Is there a family history of cancer?", [" ", "No", "Yes"])
surgeries = st.slider("How many major surgeries have you had?", 0, 10, 0)

def to_binary(answer):
    return 1 if answer == "Yes" else 0

if st.button("💡 Predict Premium"):
    payload = {
        "Age": age,
        "Diabetes": to_binary(diabetes),
        "BloodPressureProblems": to_binary(bp),
        "AnyTransplants": to_binary(transplants),
        "AnyChronicDiseases": to_binary(chronic),
        "Height": height,
        "Weight": weight,
        "KnownAllergies": to_binary(allergies),
        "HistoryOfCancerInFamily": to_binary(cancer_history),
        "NumberOfMajorSurgeries": surgeries
    }

    try:
        response = requests.post("https://premiumpredictionfastapi-3.onrender.com/predict_premium/", json=payload)

        if response.status_code == 200:
            result = response.json()

            premium = result.get("estimated_premium") or premium = result.get("estimated_premium")

            if premium is not None:
                st.subheader("📦 Quotation from your Health Insurance Provider:")
                st.success(f"💰 Your annual premium is: **Rs. {premium:,.2f}**")
            else:
                st.write("Premium calculation was not successful. Please check your inputs or try again.")
        else:
            st.write("Unable to retrieve a prediction at the moment.")
    except Exception:
        st.write("Something went wrong. Try again later.")
