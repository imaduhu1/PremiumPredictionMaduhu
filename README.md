#  Medical Premium Prediction Project Description

This is an interactive system that allows users to obtain personalized health insurance premium estimates based on their medical and demographic information. Built using **Streamlit**, **scikit-learn**, and a custom API layer, the system integrates a user-friendly interface with a machine learning backend to deliver real-time premium predictions.

---

## 🚀 Launch the App (Streamlit)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://premiumpredictionmaduhu-acwpryu8wy33ctvtaiqhmy.streamlit.app/)

---

## 🧾 Project Description

This project delivers an end-to-end workflow for premium estimation:

### 🔹 Streamlit Interface

The frontend app (`frontend_app_clean_online.py`) allows users to:
- Enter age, height, weight, and answer health-related questions.
- Validate all inputs with clear prompts and drop-down menus.
- Confirm details before submitting for a prediction.
- Receive a real-time premium estimate via an integrated API.

Includes a scrolling welcome banner, organized layout, and error handling for incomplete inputs or API issues.

---

### 🔹 API Layer

The API layer receives user input in JSON format and returns a premium estimate. It:
- Loads a **trained Random Forest model** from a serialized `.pkl` file.
- Uses key features such as: age, BMI (auto-calculated from height and weight), history of diabetes, cancer, major surgeries, and other chronic conditions.
- Is designed to handle live requests from the Streamlit app and respond with accurate premium values.


---

### 🔹 Model Training

The model is trained using the script `main.py`, which:
- Loads `Medicalpremium.csv`
- Engineers a `BMI` feature
- Defines key features such as:
  - Age, Diabetes, Blood Pressure Problems, Organ Transplants, Chronic Diseases
  - Known Allergies, Cancer History in Family, Number of Major Surgeries
- Trains a **RandomForestRegressor** with 100 trees
- Exports the trained model using `joblib` as `premium_model.pkl`

Example training logic:

```python
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)
joblib.dump(model, "premium_model.pkl")
