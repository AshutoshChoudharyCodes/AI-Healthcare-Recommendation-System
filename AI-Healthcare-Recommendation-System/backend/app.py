from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import joblib

from backend.recommendations import recommendations
from backend.database import predictions_collection

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-healthcare-recommendation-system.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML Model
model = joblib.load("backend/disease_model.pkl")


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

    disease = prediction[0]

    result = {
        "predicted_disease": disease,
        "medicine": recommendations[disease]["medicine"],
        "doctor": recommendations[disease]["doctor"],
        "precaution": recommendations[disease]["precaution"]
    }

    predictions_collection.insert_one({
        "name": symptoms.name,
        "age": symptoms.age,
        "timestamp": datetime.now().isoformat(),
        "fever": symptoms.fever,
        "cough": symptoms.cough,
        "headache": symptoms.headache,
        "fatigue": symptoms.fatigue,
        **result
    })

    return result


@app.get("/history")
def get_history():
    data = list(
        predictions_collection.find({}, {"_id": 0})
    )
    return data