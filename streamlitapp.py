import streamlit as st
import pandas as pd
import joblib

# Set_page_configuration
# Welcome message
st.markdown(
    """
    <marquee behavior="scroll" direction="left" style="color:blue; font-size:40px; font-weight:bold;">
    Welcome to Maduhu Health Insurance Company Premium Calculator
    </marquee>
    """,
    unsafe_allow_html=True
)
 
st.title("Health Insurance Premium Predictor by Maduhu.")
st.write("Answer the questions below to estimate your annual health insurance premium.")

# Load the trained model locally
model = joblib.load("premium_model.pkl")

# Numeric inputs
age = st.number_input("What is your age? (e.g., 35)", min_value=18, max_value=100, format="%d", value=None, step=1)
height = st.number_input("What is your height in cm? (e.g., 170)", min_value=100.0, max_value=250.0, value=None, step=0.1)
weight = st.number_input("What is your weight in kg? (e.g., 70)", min_value=30.0, max_value=200.0, value=None, step=0.1)

# Dropdown helper function
def dropdown(label):
    return st.selectbox(label, ["Select an option", "No", "Yes"])

diabetes = dropdown("Do you have diabetes or any history of diabetes in your family?")
bp = dropdown("Do you have blood pressure problems?")
transplants = dropdown("Have you had any organ transplants?")
chronic = dropdown("Do you have any chronic diseases?")
allergies = dropdown("Do you have any known allergies?")
cancer_history = dropdown("Is there a family history of cancer?")
surgeries = st.number_input("How many major surgeries have you had?(e.g.,2)", min_value=0, max_value=10, value=None, step=1)

# Convert Yes/No to binary
def to_binary(answer): return 1 if answer == "Yes" else 0

# Validate all fields completed
def all_fields_completed():
    return all(ans in ["Yes", "No"] for ans in [diabetes, bp, transplants, chronic, allergies, cancer_history]) \
        and age is not None and height is not None and weight is not None

# Initialize session state
if 'confirm' not in st.session_state:
    st.session_state.confirm = False

# Main submit button
if st.button("\ud83d\udca1 Click here to get your premium estimate"):
    if not all_fields_completed():
        st.warning("\ud83d\udea8 Please answer all questions before getting your premium estimate.")
    else:
        st.session_state.confirm = True

# Placeholder for confirmation and premium result
confirm_placeholder = st.empty()
result_placeholder = st.empty()

# Confirmation prompt
if st.session_state.confirm:
    with confirm_placeholder.container():
        st.info("Are you sure you want to submit?")
        col1, col2 = st.columns(2)
        with col1:
            confirm_yes = st.button("Yes, I'm sure")
        with col2:
            confirm_no = st.button("No, I want to review my details")

    if 'confirm_yes' not in st.session_state:
        st.session_state.confirm_yes = False

    if confirm_yes:
        st.session_state.confirm_yes = True
        st.session_state.confirm = False
        confirm_placeholder.empty()

    if confirm_no:
        st.session_state.confirm = False
        confirm_placeholder.empty()

# Display premium estimate after confirmation
if st.session_state.get('confirm_yes', False):
    bmi = weight / ((height / 100) ** 2)
    input_df = pd.DataFrame({
        "Age": [age],
        "Diabetes": [to_binary(diabetes)],
        "BloodPressureProblems": [to_binary(bp)],
        "AnyTransplants": [to_binary(transplants)],
        "AnyChronicDiseases": [to_binary(chronic)],
        "BMI": [bmi],
        "KnownAllergies": [to_binary(allergies)],
        "HistoryOfCancerInFamily": [to_binary(cancer_history)],
        "NumberOfMajorSurgeries": [surgeries]
    })

    try:
        premium = model.predict(input_df)[0]
        with result_placeholder.container():
            st.subheader("Quotation from your Health Insurance Provider:")
            st.success(f"Your annual premium is: **Rs. {premium:,.2f}**")
    except Exception:
        st.error("Something went wrong while making the prediction. Please try again later.")

    st.session_state.confirm_yes = False
