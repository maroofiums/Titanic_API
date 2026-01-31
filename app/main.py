from fastapi import FastAPI
from pathlib import Path
import pickle
import pandas as pd
from huggingface_hub import hf_hub_download
from app.models import TitanicInput, TitanicOutput

app = FastAPI(title="Titanic Survival Predictor")

# -----------------------------
# Load model and features from HF Hub
# -----------------------------
# repo_id is where your pkl files are uploaded
REPO_ID = "maroof2424/titanic_model_files"

MODEL_PATH = hf_hub_download(repo_id=REPO_ID, filename="titanic_model.pkl")
FEATURES_PATH = hf_hub_download(repo_id=REPO_ID, filename="titanic_features.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(FEATURES_PATH, "rb") as f:
    feature_cols = pickle.load(f)

# -----------------------------
# Prediction endpoint
# -----------------------------
@app.post("/predict", response_model=TitanicOutput)
def predict(data: TitanicInput):
    # Convert input to DataFrame with correct columns
    df = pd.DataFrame([data.dict()], columns=feature_cols)
    prediction = model.predict(df)[0]
    return {"survived": int(prediction)}
