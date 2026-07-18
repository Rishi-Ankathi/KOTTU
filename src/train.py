"""
=========================================
Module : train.py
Project: KOTTU
Purpose: Train LSTM Model
=========================================
"""

from pathlib import Path

from tensorflow.keras.callbacks import EarlyStopping
from .scaler import DataScaler

from .preprocessing import DataPreprocessor
from .sequence_generator import SequenceGenerator
from .train_test_split import DatasetSplitter
from .model import KOTTUModel
from .evaluate import Evaluator
from .visualisation import Visualizer


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)


class Trainer:

    def __init__(self):

        self.preprocessor = DataPreprocessor()

        self.scaler = DataScaler()

        self.generator = SequenceGenerator()

        self.splitter = DatasetSplitter()

        self.model_builder = KOTTUModel()
        self.evaluator = Evaluator()
        self.visualizer = Visualizer()

    def train(self):

        # Load dataset
        X, y = self.preprocessor.preprocess()

        # Split dataset
        (
            X_train,
            X_validation,
            X_test,
            y_train,
            y_validation,
            y_test
        ) = self.splitter.split(X, y)

        # Scale
        X_train = self.scaler.fit_transform(X_train)

        X_validation = self.scaler.transform(X_validation)

        X_test = self.scaler.transform(X_test)

        # Generate sequences
        X_train = self.generator.generate_sequences(X_train)

        X_validation = self.generator.generate_sequences(X_validation)

        X_test = self.generator.generate_sequences(X_test)

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
            validation_data=(X_validation, y_validation),
            epochs=30,
            batch_size=32,
            callbacks=[early_stopping]
        )

        # Evaluate
        metrics, report, matrix = self.evaluator.evaluate(
            model,
            X_test,
            y_test
        )

        # Generate visuals
        self.visualizer.generate_all(
            history.history,
            matrix
        )

        # Save model
        model.save(MODELS_DIR / "kottu_model.keras")

        return history, model, X_test, y_test, metrics, report