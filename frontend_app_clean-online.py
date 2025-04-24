
import streamlit as st
import requests

st.set_page_config(page_title="Health Premium Estimator", layout="centered")

st.title("🩺 Health Insurance Premium Predictor © Maduhu, Chloe and Sonia")
st.write("Answer the questions below to estimate your annual health insurance premium.")

# Collect inputs
age = st.number_input("What is your age?", min_value=18, max_value=100, value=0)
height = st.number_input("What is your height in cm?", min_value=100.0, max_value=250.0)
weight = st.number_input("What is your weight in kg?", min_value=30.0, max_value=200.0)
surgeries = st.slider("How many major surgeries have you had?", 0, 10, 0)

# Dropdowns with blank option first
def dropdown(label):
    return st.selectbox(label, [" ", "No", "Yes"])

diabetes = dropdown("Do you have diabetes?")
bp = dropdown("Do you have blood pressure problems?")
transplants = dropdown("Have you had any organ transplants?")
chronic = dropdown("Do you have any chronic diseases?")
allergies = dropdown("Do you have any known allergies?")
cancer_history = dropdown("Is there a family history of cancer?")

# Conversion
def to_binary(answer):
    return 1 if answer == "Yes" else 0

# Check if all required fields are filled
def all_valid():
    dropdowns = [diabetes, bp, transplants, chronic, allergies, cancer_history]
    return age > 0 and height > 0 and weight > 0 and all(v.strip() in ["Yes", "No"] for v in dropdowns)

# Submit button
if st.button("💡 Predict Premium"):
    if not all_valid():
        st.warning("🚨 Please complete all fields before getting your premium estimate.")
    else:
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
                premium = result.get("estimated_premium")
                if premium is not None:
                    st.subheader("📦 Quotation from your Health Insurance Provider:")
                    st.success(f"💰 Your annual premium is: **Rs. {premium:,.2f}**")
                else:
                    st.write("Premium calculation was not successful. Please check your inputs or try again.")
            else:
                st.write("Unable to retrieve a prediction at the moment.")
        except Exception:
            st.write("Something went wrong. Try again later.")
