"""
Slim inference for /identify: the trained 51-way LSTM, run through the TF-Lite
runtime instead of full TensorFlow.

Loads two files produced by ``scripts/export_serving.py``:

    models/kottu_model.tflite   the converted model
    models/serving_params.json  StandardScaler mean/scale + label classes

Only ``numpy`` and a TF-Lite interpreter are needed at runtime. The scaling and
the 11x3 zero-padded reshape mirror ``src/predict.py``; ``scripts/check_parity.py``
verifies the outputs match.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import numpy as np

try:  # production: the standalone ~5 MB runtime
    from tflite_runtime.interpreter import Interpreter
except ModuleNotFoundError:  # dev box with full TensorFlow installed
    import tensorflow as _tf  # type: ignore

    Interpreter = _tf.lite.Interpreter

_MODELS = Path(__file__).resolve().parent.parent / "models"
_TFLITE = _MODELS / "kottu_model.tflite"
_PARAMS = _MODELS / "serving_params.json"

N_FEATURES = 31


class ModelUnavailable(RuntimeError):
    """The exported serving artifacts (.tflite / .json) are missing."""


@lru_cache(maxsize=1)
def _params():
    if not _PARAMS.exists():
        raise ModelUnavailable(f"missing {_PARAMS.name}; run scripts/export_serving.py")
    p = json.loads(_PARAMS.read_text())
    return (
        np.asarray(p["scaler_mean"], dtype=np.float32),
        np.asarray(p["scaler_scale"], dtype=np.float32),
        list(p["classes"]),
    )


@lru_cache(maxsize=1)
def _interpreter():
    if not _TFLITE.exists():
        raise ModelUnavailable(f"missing {_TFLITE.name}; run scripts/export_serving.py")
    interp = Interpreter(model_path=str(_TFLITE))
    interp.allocate_tensors()
    return interp


def probabilities(features) -> np.ndarray:
    """One passphrase attempt (31 timing features) -> the 51-way softmax vector."""
    x = np.asarray(features, dtype=np.float32)
    if x.shape != (N_FEATURES,):
        raise ValueError(f"expected {N_FEATURES} features, got {tuple(x.shape)}")

    mean, scale, _ = _params()
    seq = np.zeros(33, dtype=np.float32)
    seq[:N_FEATURES] = (x - mean) / scale  # trailing two slots stay 0 (the training pad)
    seq = seq.reshape(1, 11, 3)

    interp = _interpreter()
    interp.reset_all_variables()  # the fused LSTM keeps state between invokes
    interp.set_tensor(interp.get_input_details()[0]["index"], seq)
    interp.invoke()
    return interp.get_tensor(interp.get_output_details()[0]["index"])[0]


def identify(features) -> dict:
    """One passphrase attempt -> {"user", "confidence"} for the closest of 51 typists."""
    _, _, classes = _params()
    probs = probabilities(features)
    idx = int(np.argmax(probs))
    return {"user": str(classes[idx]), "confidence": float(np.max(probs))}
