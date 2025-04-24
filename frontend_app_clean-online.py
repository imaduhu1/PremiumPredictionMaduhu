
import streamlit as st
import requests
import datetime
import pandas as pd

st.set_page_config(page_title="Health Premium Estimator", layout="wide")

st.title("🩺 Health Insurance Premium Estimator Dashboard")
st.markdown("Estimate your **annual premium** and track predictions below.")

# Sidebar input section
st.sidebar.header("Enter your health info:")

age = st.sidebar.number_input("Age (years)", min_value=0, max_value=100, value=0)
height = st.sidebar.number_input("Height (cm)", min_value=100.0, max_value=250.0)
weight = st.sidebar.number_input("Weight (kg)", min_value=30.0, max_value=200.0)
surgeries = st.sidebar.slider("Major surgeries", 0, 10, 0)

# Selectbox options with default placeholders
def dropdown(label):
    return st.sidebar.selectbox(label, ["Select an option", "No", "Yes"])

diabetes = dropdown("Do you have diabetes?")
bp = dropdown("Do you have blood pressure problems?")
transplants = dropdown("Have you had any organ transplants?")
chronic = dropdown("Do you have any chronic diseases?")
allergies = dropdown("Do you have any known allergies?")
cancer_history = dropdown("Family history of cancer?")

# Helper to convert yes/no to binary
def to_binary(ans): return 1 if ans == "Yes" else 0

def all_valid():
    checks = [age > 18, height > 100, weight > 40] +              [v != "Select an option" for v in [diabetes, bp, transplants, chronic, allergies, cancer_history]]
    return all(checks)

# Predict button
if st.sidebar.button("💡 Predict Premium"):
    if not all_valid():
        st.warning("🚨 Please complete all fields before submitting.")
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
                premium = result.get("estimated_premium") or result.get("estimated_premium_usd")

                # Calculate BMI
                bmi = round(weight / ((height / 100) ** 2), 2)

                # Display results
                st.subheader("📊 Quotation Summary")
                col1, col2 = st.columns(2)
                col1.metric("💰 Annual Premium", f"Rs. {premium:,.2f}")
                col2.metric("📏 BMI", f"{bmi} kg/m²")

                # Save to CSV for download
                record = {
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Age": age, "BMI": bmi, "Premium": premium
                }
                df = pd.DataFrame([record])
                df.to_csv("premium_predictions_log.csv", mode='a', header=not pd.io.common.file_exists("premium_predictions_log.csv"), index=False)
                st.success("Prediction saved.")

            else:
                st.warning("Unable to retrieve prediction.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
