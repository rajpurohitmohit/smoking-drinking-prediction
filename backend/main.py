from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import os

app = FastAPI(
    title="Smoking & Drinking Prediction API",
    description="API for predicting if a person is a drinker based on health metrics.",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Models at Startup
try:
    # Ensure they are loaded when starting the server
    model = joblib.load('model.pkl')
    scaler = joblib.load('scaler.pkl')
except Exception as e:
    print(f"Warning: Model or scaler not found. Run train.py first. Error: {e}")
    model = None
    scaler = None

class HealthData(BaseModel):
    gender: str # 'Male' or 'Female'
    age: float
    height_cm: float
    weight_kg: float
    waist_cm: float
    vision_left: float
    vision_right: float
    systolic_bp: float
    diastolic_bp: float
    total_cholesterol: float
    hdl_cholesterol: float
    ldl_cholesterol: float
    triglycerides: float
    hemoglobin: float
    creatinine: float
    liver_ast: float
    liver_alt: float
    gamma_gtp: float
    smoking_status: float

@app.get("/")
def read_root():
    return {"status": "API is running. Models loaded: " + str(model is not None)}

@app.post("/predict")
def predict(data: HealthData):
    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Models not loaded on server.")

    try:
        # Preprocessing user input
        # 1. Feature Engineering
        liver_enzyme_ratio = data.liver_ast / data.liver_alt if data.liver_alt != 0 else 0
        anemia_threshold = 12.0
        anemia_indicator = 1 if data.hemoglobin < anemia_threshold else 0
        
        # 2. Gender Encoding (Male=1, Female=0 as per LabelEncoder in train.py)
        gender_encoded = 1 if data.gender.lower() == 'male' else 0

        # Construct raw array in the exact order as training:
        # 'gender', 'age', 'height_cm', 'weight_kg', 'waist_cm',
        # 'vision_left', 'vision_right', 'systolic_bp', 'diastolic_bp',
        # 'total_cholesterol', 'hdl_cholesterol', 'ldl_cholesterol',
        # 'triglycerides', 'hemoglobin', 'creatinine', 'liver_ast',
        # 'liver_alt', 'gamma_gtp', 'smoking_status',
        # 'Liver_Enzyme_Ratio', 'Anemia_Indicator'
        
        features = [
            gender_encoded, data.age, data.height_cm, data.weight_kg, data.waist_cm,
            data.vision_left, data.vision_right, data.systolic_bp, data.diastolic_bp,
            data.total_cholesterol, data.hdl_cholesterol, data.ldl_cholesterol,
            data.triglycerides, data.hemoglobin, data.creatinine, data.liver_ast,
            data.liver_alt, data.gamma_gtp, data.smoking_status,
            liver_enzyme_ratio, anemia_indicator
        ]
        
        features_array = np.array(features).reshape(1, -1)
        
        # Scale
        scaled_features = scaler.transform(features_array)
        
        # Predict
        prediction = model.predict(scaled_features)[0]
        
        # In the original notebook: is_drinker LabelEncoder fit on ['N', 'Y']
        # 'N' = 0, 'Y' = 1
        result = "Drinker" if prediction == 1 else "Not a Drinker"
        
        # Also get probability (if the stacking classifier provides it)
        try:
            probabilities = model.predict_proba(scaled_features)[0]
            confidence = probabilities[prediction]
        except:
            confidence = None

        return {
            "prediction": result,
            "prediction_code": int(prediction),
            "confidence": float(confidence) if confidence else None
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
