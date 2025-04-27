import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load data
data = pd.read_csv("Medicalpremium.csv")

# Calculate BMI
data['BMI'] = data['Weight'] / ((data['Height'] / 100) ** 2)

# Define features and target
features = ['Age', 'Diabetes', 'BloodPressureProblems', 'AnyTransplants',
            'AnyChronicDiseases', 'BMI', 'KnownAllergies',
            'HistoryOfCancerInFamily', 'NumberOfMajorSurgeries']
target = 'PremiumPrice'

X = data[features]
y = data[target]

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Save trained model for use in Streamlit app
joblib.dump(model, "premium_model.pkl")

print("Model trained and saved successfully.")
