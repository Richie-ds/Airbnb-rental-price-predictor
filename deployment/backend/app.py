
import os
import joblib
import pandas as pd
import numpy as np # Ensure numpy is imported
from flask import Flask, request, jsonify

app = Flask(__name__)

# Path to the serialized model (copied into the Docker image)
MODEL_PATH = 'rental_price_prediction_model_v1_0.joblib'

# Load the model once when the app starts
try:
    saved_model = joblib.load(MODEL_PATH)
    print(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model: {e}")
    saved_model = None

@app.route('/predict', methods=['POST'])
def predict():
    if saved_model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.get_json(force=True)
        df = pd.DataFrame(data)

        predictions_log_prices = saved_model.predict(df)
        predictions_actual_prices = round(pd.Series(predictions_log_prices).apply(np.exp),2)

        return jsonify(predictions_actual_prices.tolist())

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict_single', methods=['POST'])
def predict_single():
    if saved_model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.get_json(force=True)
        # Ensure data is a single dictionary, wrap it in a list for DataFrame
        if not isinstance(data, dict):
            return jsonify({'error': 'Input for /predict_single must be a single JSON object'}), 400

        df = pd.DataFrame([data]) # Wrap single dict in a list for DataFrame creation

        predictions_log_prices = saved_model.predict(df)
        predictions_actual_price = round(np.exp(predictions_log_prices[0]), 2) # Get the single prediction

        return jsonify(float(predictions_actual_price)) # Return single float

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/')
def health_check():
    return jsonify({'status': 'ok', 'message': 'Flask backend is running'})
