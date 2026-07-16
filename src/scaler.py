"""
=========================================
Module : scaler.py
Project: KOTTU
Purpose: Feature Scaling
=========================================
"""

from pathlib import Path

import joblib
from sklearn.preprocessing import StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODELS_DIR = PROJECT_ROOT / "models"


class DataScaler:

    def __init__(self):

        self.scaler = StandardScaler()

    def fit_transform(self, X_train):

        X_train = self.scaler.fit_transform(X_train)

        joblib.dump(
            self.scaler,
            MODELS_DIR / "scaler.pkl"
        )

        return X_train

    def transform(self, X):

        return self.scaler.transform(X)