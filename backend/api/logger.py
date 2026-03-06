import csv
from datetime import datetime
import os

FILE_NAME = "prediction_log.csv"

def log_prediction(data, prediction, risk_score):

    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Header (created only once)
        if not file_exists:
            writer.writerow([
                "timestamp",
                "Age",
                "MonthlyIncome",
                "JobSatisfaction",
                "WorkLifeBalance",
                "YearsAtCompany",
                "OverTime",
                "DistanceFromHome",
                "Prediction",
                "RiskScore"
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