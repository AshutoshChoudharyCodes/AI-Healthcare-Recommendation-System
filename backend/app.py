from fastapi import FastAPI
from pydantic import BaseModel
import joblib

from backend.recommendations import recommendations
from backend.database import predictions_collection

app = FastAPI()

model = joblib.load("backend/disease_model.pkl")


class Symptoms(BaseModel):
    fever: int
    cough: int
    headache: int
    fatigue: int


@app.get("/")
def home():
    return {"message": "AI Healthcare Recommendation System API is running"}


@app.post("/predict")
def predict(symptoms: Symptoms):

    prediction = model.predict([[
        symptoms.fever,
        symptoms.cough,
        symptoms.headache,
        symptoms.fatigue
    ]])

    disease = prediction[0]

    result = {
        "predicted_disease": disease,
        "medicine": recommendations[disease]["medicine"],
        "doctor": recommendations[disease]["doctor"],
        "precaution": recommendations[disease]["precaution"]
    }

    predictions_collection.insert_one({
        "fever": symptoms.fever,
        "cough": symptoms.cough,
        "headache": symptoms.headache,
        "fatigue": symptoms.fatigue,
        **result
    })

    return result


@app.get("/history")
def get_history():
    data = list(predictions_collection.find({}, {"_id": 0}))
    return data