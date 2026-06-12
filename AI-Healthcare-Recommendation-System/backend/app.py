from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib

from backend.recommendations import recommendations

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML model
model = joblib.load("backend/disease_model.pkl")

# Temporary history storage
history = []


class Symptoms(BaseModel):
    name: str
    age: int
    fever: int
    cough: int
    headache: int
    fatigue: int


@app.get("/")
def home():
    return {
        "message": "AI Healthcare Recommendation System API is running"
    }


@app.post("/predict")
def predict(symptoms: Symptoms):

    prediction = model.predict([[
        symptoms.fever,
        symptoms.cough,
        symptoms.headache,
        symptoms.fatigue
    ]])

    disease = str(prediction[0])

    recommendation = recommendations.get(
        disease,
        {
            "medicine": "Consult Doctor",
            "doctor": "General Physician",
            "precaution": "Take Rest"
        }
    )

    result = {
        "name": symptoms.name,
        "age": symptoms.age,
        "predicted_disease": disease,
        "medicine": recommendation["medicine"],
        "doctor": recommendation["doctor"],
        "precaution": recommendation["precaution"]
    }

    history.append(result)

    return result


@app.get("/history")
def get_history():
    return history