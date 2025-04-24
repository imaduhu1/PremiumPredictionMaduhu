
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Load data
data = pd.read_csv("Medicalpremium.csv")

# Define features and target
features = ['Age', 'Diabetes', 'BloodPressureProblems', 'AnyTransplants',
            'AnyChronicDiseases', 'Height', 'Weight', 'KnownAllergies',
            'HistoryOfCancerInFamily', 'NumberOfMajorSurgeries']
target = 'PremiumPrice'

X = data[features]
y = data[target]

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# FastAPI app
app = FastAPI()

class PatientInfo(BaseModel):
    Age: int
    Diabetes: int
    BloodPressureProblems: int
    AnyTransplants: int
    AnyChronicDiseases: int
    Height: float
    Weight: float
    KnownAllergies: int
    HistoryOfCancerInFamily: int
    NumberOfMajorSurgeries: int

@app.get("/")
def root():
    return {"message": "Health Premium API is running!"}

@app.post("/predict_premium/")
def predict_premium(info: PatientInfo):
    bmi = round(info.Weight / ((info.Height / 100) ** 2), 2)
    input_data = pd.DataFrame([[info.Age, info.Diabetes, info.BloodPressureProblems,
                                info.AnyTransplants, info.AnyChronicDiseases,
                                info.Height, info.Weight, info.KnownAllergies,
                                info.HistoryOfCancerInFamily, info.NumberOfMajorSurgeries]],
                              columns=features)
    prediction = model.predict(input_data)[0]
    return {"estimated_premium_usd": round(prediction, 2)}
