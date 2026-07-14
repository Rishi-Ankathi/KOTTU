"""
=========================================
Module : train.py
Project: KOTTU
Purpose: Train LSTM Model
=========================================
"""

from pathlib import Path

from tensorflow.keras.callbacks import EarlyStopping

from .preprocessing import DataPreprocessor
from .sequence_generator import SequenceGenerator
from .train_test_split import DatasetSplitter
from .model import KOTTUModel


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"


class Trainer:

    def __init__(self):

        self.preprocessor = DataPreprocessor()

        self.generator = SequenceGenerator()

        self.splitter = DatasetSplitter()

        self.model_builder = KOTTUModel()

    def train(self):

        # Load and preprocess data
        X, y = self.preprocessor.preprocess()

        # Convert into LSTM sequences
        X = self.generator.generate_sequences(X)

        # Split dataset
        X_train, X_test, y_train, y_test = self.splitter.split(X, y)

        # Build model
        model = self.model_builder.build_model(
            input_shape=X_train.shape[1:],
            num_classes=len(set(y))
        )

        # Prevent overfitting
        early_stopping = EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True
        )

        # Train model
        history = model.fit(
            X_train,
            y_train,
            validation_data=(X_test, y_test),
            epochs=30,
            batch_size=32,
            callbacks=[early_stopping]
        )

        # Save model
        model.save(MODELS_DIR / "kottu_model.keras")

        return history, model, X_test, y_test