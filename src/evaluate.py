"""
=========================================
Module : evaluate.py
Project: KOTTU
Purpose: Evaluate LSTM Model
=========================================
"""

"""
    Evaluates the trained model on the test dataset.

    Returns:
        metrics (dict): Accuracy, Precision, Recall and F1-score.
        report (str): Classification report.
        confusion_matrix_data (ndarray): Confusion matrix.
"""

from pathlib import Path
import json

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
)

# -----------------------------
# Project Paths
# -----------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_DIR = PROJECT_ROOT / "output"

METRICS_DIR = OUTPUT_DIR / "metrics"

REPORTS_DIR = OUTPUT_DIR / "reports"

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
            predicted_labels,
            digits=4
        )

        matrix = confusion_matrix(
            y_test,
            predicted_labels
        )

        precision = precision_score(
            y_test,
            predicted_labels,
            average="weighted"
        )

        recall = recall_score(
            y_test,
            predicted_labels,
            average="weighted"
        )

        f1 = f1_score(
            y_test,
            predicted_labels,
            average="weighted"
        )

        metrics = {
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1_score": float(f1)
        }

        METRICS_DIR.mkdir(parents=True, exist_ok=True)
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        with open(
            METRICS_DIR / "metrics.json",
            "w"
        ) as file:
            json.dump(
                metrics,
                file,
                indent=4
            )

        with open(
            REPORTS_DIR / "classification_report.txt",
            "w"
        ) as file:
            file.write(report)

        return metrics, report, matrix