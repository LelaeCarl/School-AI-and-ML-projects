
# --- FILE: tests/test_app.py ---
import json
from app import app

def test_home_route():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

def test_predict_valid():
    payload = {
        "GrLivArea": 1500,
        "TotalBsmtSF": 1000,
        "YearBuilt": 2005,
        "FullBath": 2,
        "GarageCars": 2,
        "OverallQual": 7
    }
    with app.test_client() as client:
        response = client.post('/predict', json=payload)
        assert response.status_code == 200
        data = response.get_json()
        assert 'prediction' in data
