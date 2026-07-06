from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import pandas as pd

app = FastAPI(title="API de Scoring Crédit")
model = joblib.load("model.pkl")

class ClientData(BaseModel):
    RevolvingUtilizationOfUnsecuredLines: float
    age: int
    NumberOfTime30_59DaysPastDueNotWorse: int = Field(alias="NumberOfTime30-59DaysPastDueNotWorse")
    DebtRatio: float
    MonthlyIncome: float
    NumberOfOpenCreditLinesAndLoans: int
    NumberOfTimes90DaysLate: int
    NumberRealEstateLoansOrLines: int
    NumberOfTime60_89DaysPastDueNotWorse: int = Field(alias="NumberOfTime60-89DaysPastDueNotWorse")
    NumberOfDependents: float
    DebtToIncome: float

    class Config:
        populate_by_name = True

@app.get("/")
def home():
    return {"message": "API de scoring en ligne."}

@app.post("/predict")
def predict(data: ClientData):
    df = pd.DataFrame([data.dict(by_alias=True)])
    proba = model.predict_proba(df)[0][1]
    prediction = int(proba > 0.5)
    return {"probabilite_defaut": float(proba), "prediction": prediction}