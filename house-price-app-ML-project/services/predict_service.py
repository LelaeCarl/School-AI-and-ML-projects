
# --- FILE: services/predict_service.py ---
import pandas as pd
import joblib
from config import Config

model = joblib.load(Config.MODEL_PATH)

def predict_price(payload: dict):
    input_df = pd.DataFrame([payload])
    prediction = model.predict(input_df)[0]
    return round(prediction, 2)
