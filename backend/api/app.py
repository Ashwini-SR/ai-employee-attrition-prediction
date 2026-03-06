from fastapi import FastAPI
import pandas as pd
import joblib
import os

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

        # Ensure correct column order
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

        return {"attrition_prediction": int(prediction)}

    except Exception as e:
        return {"error": str(e)}