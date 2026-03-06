# backend/api/logger.py
import csv, os
from datetime import datetime

FILE_NAME = "prediction_log.csv"

def log_prediction(data, prediction, risk_score):
    file_exists = os.path.isfile(FILE_NAME)
    with open(FILE_NAME, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "timestamp","Age","MonthlyIncome","JobSatisfaction",
                "WorkLifeBalance","YearsAtCompany","OverTime",
                "DistanceFromHome","Prediction","RiskScore"
            ])
        writer.writerow([
            datetime.now(),
            data["Age"],
            data["MonthlyIncome"],
            data["JobSatisfaction"],
            data["WorkLifeBalance"],
            data["YearsAtCompany"],
            data["OverTime"],
            data["DistanceFromHome"],
            prediction,
            risk_score
        ])