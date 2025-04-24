import streamlit as st
import requests

st.set_page_config(page_title="Health Premium Estimator", layout="centered")

st.title("🩺 Health Insurance Premium Predictor © Maduhu, Chloe and Sonia")
st.write("Answer the questions below to estimate your annual health insurance premium.")

# Collect inputs
age = st.number_input("What is your age?", min_value=18, max_value=100)
height = st.number_input("What is your height in cm?", min_value=100.0, max_value=250.0)
weight = st.number_input("What is your weight in kg?", min_value=30.0, max_value=200.0)

# Dropdowns with initial blank option
def dropdown(label):
    return st.selectbox(label, ["Select an option", "No", "Yes"])

diabetes = dropdown("Do you have diabetes?")
bp = dropdown("Do you have blood pressure problems?")
transplants = dropdown("Have you had any organ transplants?")
chronic = dropdown("Do you have any chronic diseases?")
allergies = dropdown("Do you have any known allergies?")
cancer_history = dropdown("Is there a family history of cancer?")

# Move surgeries to the end
surgeries = st.slider("How many major surgeries have you had?", 0, 10, 0)

# Helper
def to_binary(answer): return 1 if answer == "Yes" else 0

def all_valid():
    dropdowns = [diabetes, bp, transplants, chronic, allergies, cancer_history]
    return all(ans in ["Yes", "No"] for ans in dropdowns)

submit = st.button("💡 Predict Premium", disabled=not all_valid())

if submit:
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
            st.write("📦 Raw Response for Debugging:", result)  # TEMPORARY: Remove after debugging

            premium = result.get("estimated_premium")
            if premium is not None:
                st.subheader("📦 Quotation from your Health Insurance Provider:")
                st.success(f"💰 Your annual premium is: **Rs. {premium:,.2f}**")
            else:
                st.error("⚠️ Premium calculation was not successful. Please check your inputs or try again.")
        else:
            st.error("❌ Server error: failed to retrieve a prediction.")
    except Exception as e:
        st.error(f"🚨 Something went wrong: {e}")
