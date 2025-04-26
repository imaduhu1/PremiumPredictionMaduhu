import streamlit as st
import requests

st.set_page_config(page_title="Health Premium Estimator", layout="centered")

st.title("Health Insurance Premium Predictor by SOMACH.")
st.write("Answer the questions below to estimate your annual health insurance premium.")

# 1. Form input section
with st.form("premium_form", clear_on_submit=False):
    # Inputs
    age = st.number_input("What is your age? (e.g., 35)", min_value=18, max_value=100, format="%d", value=None, step=1)
    height = st.number_input("What is your height in cm? (e.g., 170)", min_value=100.0, max_value=250.0, value=None, step=0.1)
    weight = st.number_input("What is your weight in kg? (e.g., 70)", min_value=30.0, max_value=200.0, value=None, step=0.1)

    def dropdown(label):
        return st.selectbox(label, ["Select an option", "No", "Yes"])

    diabetes = dropdown("Do you have diabetes or any history of diabetes in your family?")
    bp = dropdown("Do you have blood pressure problems?")
    transplants = dropdown("Have you had any organ transplants?")
    chronic = dropdown("Do you have any chronic diseases?")
    allergies = dropdown("Do you have any known allergies?")
    cancer_history = dropdown("Is there a family history of cancer?")

    surgeries = st.number_input("How many major surgeries have you had? (e.g., 2)", min_value=0, max_value=10, value=None, step=1)

    # Submit form to "review" info first
    review_button = st.form_submit_button("📝 Review Information")

# 2. Review and Confirm Section
if review_button:
    if None in [age, height, weight, surgeries] or "Select an option" in [diabetes, bp, transplants, chronic, allergies, cancer_history]:
        st.warning("🚨 Please complete all questions before reviewing.")
    else:
        st.header("🔎 Please Review Your Information")
        st.write(f"**Age:** {age} years")
        st.write(f"**Height:** {height} cm")
        st.write(f"**Weight:** {weight} kg")
        st.write(f"**Diabetes:** {diabetes}")
        st.write(f"**Blood Pressure Problems:** {bp}")
        st.write(f"**Organ Transplants:** {transplants}")
        st.write(f"**Chronic Diseases:** {chronic}")
        st.write(f"**Known Allergies:** {allergies}")
        st.write(f"**Family History of Cancer:** {cancer_history}")
        st.write(f"**Number of Major Surgeries:** {surgeries}")

        confirm = st.button("✅ Confirm and Submit for Estimation")

        if confirm:
            # After confirmation, send to API
            payload = {
                "Age": age,
                "Diabetes": 1 if diabetes == "Yes" else 0,
                "BloodPressureProblems": 1 if bp == "Yes" else 0,
                "AnyTransplants": 1 if transplants == "Yes" else 0,
                "AnyChronicDiseases": 1 if chronic == "Yes" else 0,
                "Height": height,
                "Weight": weight,
                "KnownAllergies": 1 if allergies == "Yes" else 0,
                "HistoryOfCancerInFamily": 1 if cancer_history == "Yes" else 0,
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
                    st.error("⚠️ Unable to retrieve a prediction. Please try again later.")
            except Exception as e:
                st.error(f"⚠️ Something went wrong: {e}")
