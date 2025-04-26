import streamlit as st
import requests

st.set_page_config(page_title="Health Premium Estimator", layout="centered")

st.title("Health Insurance Premium Predictor by SOMACH.")
st.write("Answer the questions below to estimate your annual health insurance premium.")

# Numeric inputs with placeholder-like prompts using label only
age = st.number_input("What is your age? (e.g., 35)", min_value=18, max_value=100, format="%d", value=None, step=1)
height = st.number_input("What is your height in cm? (e.g., 170)", min_value=100.0, max_value=250.0, value=None, step=0.1)
weight = st.number_input("What is your weight in kg? (e.g., 70)", min_value=30.0, max_value=200.0, value=None, step=0.1)

# Dropdowns with placeholder

def dropdown(label):
    return st.selectbox(label, ["Select an option", "No", "Yes"])

diabetes = dropdown("Do you have diabetes or any history of diabetes in your family?")
bp = dropdown("Do you have blood pressure problems?")
transplants = dropdown("Have you had any organ transplants?")
chronic = dropdown("Do you have any chronic diseases?")
allergies = dropdown("Do you have any known allergies?")
cancer_history = dropdown("Is there a family history of cancer?")

# Surgeries at the end
surgeries = st.number_input("How many major surgeries have you had?(e.g.,2)", min_value=0, max_value=10, value=None, step=1)

# Convert Yes/No to 1/0
def to_binary(answer): return 1 if answer == "Yes" else 0

# Validation
def all_fields_completed():
    return all(ans in ["Yes", "No"] for ans in [diabetes, bp, transplants, chronic, allergies, cancer_history]) \
        and age is not None and height is not None and weight is not None

# Submit logic
if st.button("💡 Click here to get your premium estimate"):
    if not all_fields_completed():
        st.warning("🚨 Please answer all questions before getting your premium estimate.")
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
                premium = result.get("estimated_premium_usd") or result.get("estimated_premium")
                if premium is not None:
                    st.subheader("📦 Quotation from your Health Insurance Provider:")
                    st.success(f"💰 Your annual premium is: **Rs. {premium:,.2f}**")
                else:
                    st.error("⚠️ We couldn’t calculate your premium at this time. Please review your inputs and try again.")
            else:
                st.write("Unable to retrieve a prediction at the moment. Did you complete all the fields?")
        except Exception:
            st.write("Something went wrong. Try again later.")
