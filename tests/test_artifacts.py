import unittest
from pathlib import Path

import numpy as np

from src.evaluate import Evaluator
from src.visualisation import Visualizer


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
PLOTS_DIR = OUTPUT_DIR / "plots"
METRICS_DIR = OUTPUT_DIR / "metrics"
REPORTS_DIR = OUTPUT_DIR / "reports"


class DummyModel:
    def predict(self, X):
        return np.array(
            [[0.9, 0.1], [0.2, 0.8]],
            dtype=float
        )


class ArtifactTests(unittest.TestCase):
    def test_evaluator_writes_metrics_and_report(self):
        evaluator = Evaluator()
        metrics, report, matrix = evaluator.evaluate(
            DummyModel(),
            np.zeros((2, 1)),
            np.array([0, 1])
        )

        self.assertEqual(
            set(metrics.keys()),
            {"accuracy", "precision", "recall", "f1_score"}
        )
        self.assertTrue((METRICS_DIR / "metrics.json").exists())
        self.assertTrue((REPORTS_DIR / "classification_report.txt").exists())
        self.assertEqual(matrix.shape, (2, 2))
        self.assertIn("precision", report)

    def test_visualizer_saves_plot_files(self):
        visualizer = Visualizer()
        history = {"accuracy": [0.6, 0.8], "loss": [0.9, 0.4]}
        matrix = np.array([[2, 0], [0, 2]])

        visualizer.generate_all(history, matrix)

        self.assertTrue((PLOTS_DIR / "accuracy_curve.png").exists())
        self.assertTrue((PLOTS_DIR / "loss_curve.png").exists())
        self.assertTrue((PLOTS_DIR / "confusion_matrix.png").exists())


if __name__ == "__main__":
    unittest.main()
