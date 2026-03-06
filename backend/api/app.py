from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import os
from api.logger import log_prediction

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load model
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
        df = df[["Age","MonthlyIncome","JobSatisfaction","WorkLifeBalance",
                 "YearsAtCompany","OverTime","DistanceFromHome"]]

        prediction = model.predict(df)[0]
        risk_score = (data["OverTime"]*30 + (4-data["JobSatisfaction"])*20 +
                      (4-data["WorkLifeBalance"])*15 + data["DistanceFromHome"]*2)
        reasons = []
        if data["OverTime"]: reasons.append("Employee works overtime frequently")
        if data["JobSatisfaction"] <= 2: reasons.append("Low job satisfaction")
        if data["WorkLifeBalance"] <= 2: reasons.append("Poor work-life balance")
        if data["DistanceFromHome"] > 15: reasons.append("Long commute distance")

        log_prediction(data, prediction, risk_score)
        return {"attrition_prediction": int(prediction),
                "risk_score": int(risk_score),
                "ai_explanation": reasons}
    except Exception as e:
        return {"error": str(e)}

@app.get("/analytics")
def analytics():
    try:
        if not os.path.exists("prediction_log.csv"):
            return {"message":"No prediction data yet"}
        df = pd.read_csv("prediction_log.csv")
        return {
            "total_predictions": len(df),
            "predicted_attrition_cases": int(df["Prediction"].sum()),
            "high_risk_employees": int(df[df["RiskScore"] > 70].shape[0]),
            "average_employee_income": int(df["MonthlyIncome"].mean())
        }
    except Exception as e:
        return {"error": str(e)}