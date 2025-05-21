
# --- FILE: app.py ---
from flask import Flask, request, jsonify, render_template
from services.predict_service import predict_price
from services.schema_validator import validate_input
from marshmallow.exceptions import ValidationError
from config import Config
import logging
import os

app = Flask(__name__)
logging.basicConfig(filename=os.path.join(Config.LOG_DIR, 'app.log'), level=logging.INFO)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('predict.html')

    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        validated = validate_input(data)
        result = predict_price(validated)
        return jsonify({'prediction': result})
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400
    except Exception as e:
        logging.exception("Prediction error")
        return jsonify({'error': str(e)}), 500


@app.route('/eda')
def eda():
    return render_template('eda.html')

if __name__ == '__main__':
    app.run(debug=True)
