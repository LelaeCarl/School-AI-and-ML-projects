
# --- FILE: config.py ---
import os

class Config:
    MODEL_VERSION = "v1"
    MODEL_DIR = os.path.join("model", "versioned")
    MODEL_PATH = os.path.join(MODEL_DIR, f"model_{MODEL_VERSION}.pkl")
    LOG_DIR = "logs"
    DATA_DIR = "data"

# Ensure directories exist
os.makedirs(Config.MODEL_DIR, exist_ok=True)
os.makedirs(Config.LOG_DIR, exist_ok=True)