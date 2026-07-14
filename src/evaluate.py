"""
=========================================
Module : evaluate.py
Project: KOTTU
Purpose: Evaluate LSTM Model
=========================================
"""

import numpy as np

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


class Evaluator:

    def evaluate(
        self,
        model,
        X_test,
        y_test
    ):

        predictions = model.predict(X_test)

        predicted_labels = np.argmax(
            predictions,
            axis=1
        )

        accuracy = accuracy_score(
            y_test,
            predicted_labels
        )

        report = classification_report(
            y_test,
            predicted_labels
        )

        matrix = confusion_matrix(
            y_test,
            predicted_labels
        )

        print("\nAccuracy")
        print(accuracy)

        print("\nClassification Report")
        print(report)

        return accuracy, report, matrix