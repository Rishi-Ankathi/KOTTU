"""
One-time export for the slim serving path.

Run this on a machine that has the training TensorFlow installed (the same
environment that produced ``models/kottu_model.keras``). It writes two files the
API loads instead of the full Keras model, so the deployed service needs neither
``tensorflow`` nor ``scikit-learn``:

    models/kottu_model.tflite   the model, converted for the TF-Lite runtime
    models/serving_params.json  StandardScaler mean/scale + the label classes,
                                lifted out of scaler.pkl / label_encoder.pkl

Re-run it whenever you retrain (``python train.py``).

    python scripts/export_serving.py
"""

from __future__ import annotations

import json
import os
from pathlib import Path

# keep TF's math deterministic so the parity check has a stable reference
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import joblib  # noqa: E402
import numpy as np  # noqa: E402
import tensorflow as tf  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MODELS = ROOT / "models"


def export_tflite() -> None:
    """Convert the Keras model to a float32 TF-Lite flatbuffer (built-in ops only)."""
    model = tf.keras.models.load_model(MODELS / "kottu_model.keras")

    # Pin the input to (1, 11, 3). With a static timestep count the LSTM unrolls
    # at conversion time, so it maps onto built-in TF-Lite ops - no dynamic
    # tensor-list ops, no dependency on the heavyweight Flex (full-TF) runtime.
    @tf.function(input_signature=[tf.TensorSpec([1, 11, 3], tf.float32, name="sequence")])
    def serve(sequence):
        return model(sequence, training=False)

    concrete = serve.get_concrete_function()
    converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete], model)
    # no quantization: stay in float32 so the output matches the .keras model
    converter.optimizations = []
    # fail loudly if anything still needs Flex ops - that is exactly the case
    # where we would fall back to a NumPy implementation
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS]

    flatbuffer = converter.convert()

    out = MODELS / "kottu_model.tflite"
    out.write_bytes(flatbuffer)
    print(f"wrote {out.relative_to(ROOT)}  ({len(flatbuffer) / 1024:.1f} KB)")


def export_params() -> None:
    """Lift the scaler statistics and label classes into a plain JSON file."""
    scaler = joblib.load(MODELS / "scaler.pkl")
    encoder = joblib.load(MODELS / "label_encoder.pkl")

    params = {
        "scaler_mean": np.asarray(scaler.mean_, dtype=float).tolist(),
        "scaler_scale": np.asarray(scaler.scale_, dtype=float).tolist(),
        "classes": [str(c) for c in encoder.classes_],
    }

    out = MODELS / "serving_params.json"
    out.write_text(json.dumps(params, indent=2) + "\n")
    print(
        f"wrote {out.relative_to(ROOT)}  "
        f"({len(params['classes'])} classes, {len(params['scaler_mean'])} features)"
    )


if __name__ == "__main__":
    export_tflite()
    export_params()
    print("\ndone. next: python scripts/check_parity.py")
