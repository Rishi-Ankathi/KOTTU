"""
=========================================
Module : preprocessing.py
Project: KOTTU
Purpose: Data Preprocessing
=========================================
"""

from pathlib import Path

import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler

from .data_loader import DataLoader


PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODELS_DIR = PROJECT_ROOT / "models"


class DataPreprocessor:

    def __init__(self):

        self.loader = DataLoader()

        self.scaler = StandardScaler()

        self.label_encoder = LabelEncoder()

    def preprocess(self):

        df = self.loader.load_dataset()

        # Features
        X = df.drop(columns=["subject", "sessionIndex", "rep"])

        # Labels
        y = df["subject"]

        # Encode labels
        y = self.label_encoder.fit_transform(y)

        # Scale features
        X = self.scaler.fit_transform(X)

        # Save objects
        joblib.dump(self.scaler, MODELS_DIR / "scaler.pkl")
        joblib.dump(self.label_encoder, MODELS_DIR / "label_encoder.pkl")

        return X, y