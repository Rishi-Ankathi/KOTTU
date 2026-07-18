"""
=========================================
Module : predict.py
Project: KOTTU
Purpose: Load pretrained model and predict labels
=========================================
"""

from pathlib import Path

import joblib
import numpy as np
from tensorflow.keras.models import load_model


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"


class Predictor:

    def __init__(self):

        self.model_path = MODELS_DIR / "kottu_model.keras"
        self.scaler_path = MODELS_DIR / "scaler.pkl"
        self.label_encoder_path = MODELS_DIR / "label_encoder.pkl"

        self.model = load_model(self.model_path)
        self.scaler = joblib.load(self.scaler_path)
        self.label_encoder = joblib.load(self.label_encoder_path)

    def predict(self, sample):

        sample_array = np.array(sample, dtype=float).reshape(1, -1)
        sample_scaled = self.scaler.transform(sample_array)

        sample_sequence = np.array([
            [sample_scaled[0, 0], sample_scaled[0, 1], sample_scaled[0, 2]],
            [sample_scaled[0, 3], sample_scaled[0, 4], sample_scaled[0, 5]],
            [sample_scaled[0, 6], sample_scaled[0, 7], sample_scaled[0, 8]],
            [sample_scaled[0, 9], sample_scaled[0, 10], sample_scaled[0, 11]],
            [sample_scaled[0, 12], sample_scaled[0, 13], sample_scaled[0, 14]],
            [sample_scaled[0, 15], sample_scaled[0, 16], sample_scaled[0, 17]],
            [sample_scaled[0, 18], sample_scaled[0, 19], sample_scaled[0, 20]],
            [sample_scaled[0, 21], sample_scaled[0, 22], sample_scaled[0, 23]],
            [sample_scaled[0, 24], sample_scaled[0, 25], sample_scaled[0, 26]],
            [sample_scaled[0, 27], sample_scaled[0, 28], sample_scaled[0, 29]],
            [sample_scaled[0, 30], 0.0, 0.0]
        ]).reshape(1, 11, 3)

        probabilities = self.model.predict(sample_sequence, verbose=0)[0]
        class_idx = int(np.argmax(probabilities))
        confidence = float(np.max(probabilities))
        label = self.label_encoder.inverse_transform([class_idx])[0]

        return {
            "user": str(label),
            "confidence": confidence
        }