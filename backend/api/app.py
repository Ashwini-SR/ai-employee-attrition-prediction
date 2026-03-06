from fastapi import FastAPI
import pandas as pd
import joblib
import os
from api.logger import log_prediction
app = FastAPI()

# Load trained model safely
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "attrition_model.pkl")

model = joblib.load(MODEL_PATH)


@app.get("/")
def home():
    return {"message": "AI Employee Attrition Prediction API Running"}


@app.post("/predict")
def predict(data: dict):

    try:

        df = pd.DataFrame([data])

        df = df[[
            "Age",
            "MonthlyIncome",
            "JobSatisfaction",
            "WorkLifeBalance",
            "YearsAtCompany",
            "OverTime",
            "DistanceFromHome"
        ]]

        prediction = model.predict(df)[0]

        # Risk score (simple logic for hackathon)
        risk_score = int(
            (data["OverTime"] * 30) +
            ((4 - data["JobSatisfaction"]) * 20) +
            ((4 - data["WorkLifeBalance"]) * 15) +
            (data["DistanceFromHome"] * 2)
        )

        # AI explanation
        reasons = []

        if data["OverTime"] == 1:
            reasons.append("Employee works overtime frequently")

        if data["JobSatisfaction"] <= 2:
            reasons.append("Low job satisfaction")

        if data["WorkLifeBalance"] <= 2:
            reasons.append("Poor work-life balance")

        if data["DistanceFromHome"] > 15:
            reasons.append("Long commute distance")
        log_prediction(data, prediction, risk_score)
        return {
            "attrition_prediction": int(prediction),
            "risk_score": risk_score,
            "ai_explanation": reasons
        }

    except Exception as e:
        return {"error": str(e)}