from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from backend.recommendations import recommendations

app = FastAPI()

# Load trained model
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

    return {
        "predicted_disease": disease,
        "medicine": recommendations[disease]["medicine"],
        "doctor": recommendations[disease]["doctor"],
        "precaution": recommendations[disease]["precaution"]
    }