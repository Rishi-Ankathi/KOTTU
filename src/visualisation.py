"""
=========================================
Module : visualisation.py
Project: KOTTU
Purpose: Generate training visualizations
=========================================
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
PLOTS_DIR = OUTPUT_DIR / "plots"


class Visualizer:

    def plot_accuracy(self, history):

        PLOTS_DIR.mkdir(parents=True, exist_ok=True)

        plt.figure(figsize=(8, 5))
        plt.plot(history.get("accuracy", []), label="accuracy")
        plt.xlabel("Epoch")
        plt.ylabel("Accuracy")
        plt.title("Accuracy Curve")
        plt.legend()
        plt.tight_layout()
        plt.savefig(PLOTS_DIR / "accuracy_curve.png")
        plt.close()

    def plot_loss(self, history):

        PLOTS_DIR.mkdir(parents=True, exist_ok=True)

        plt.figure(figsize=(8, 5))
        plt.plot(history.get("loss", []), label="loss")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.title("Loss Curve")
        plt.legend()
        plt.tight_layout()
        plt.savefig(PLOTS_DIR / "loss_curve.png")
        plt.close()

    def plot_confusion_matrix(self, matrix):

        PLOTS_DIR.mkdir(parents=True, exist_ok=True)

        plt.figure(figsize=(6, 6))
        ConfusionMatrixDisplay(matrix).plot(cmap="Blues")
        plt.title("Confusion Matrix")
        plt.tight_layout()
        plt.savefig(PLOTS_DIR / "confusion_matrix.png")
        plt.close()

    def generate_all(self, history, matrix):

        self.plot_accuracy(history)
        self.plot_loss(history)
        self.plot_confusion_matrix(matrix)
