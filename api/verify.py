"""
Enrollment + verification.

No model. The 31 timing features are first put on a common scale with the same
StandardScaler the classifier uses (models/scaler.pkl), so every feature is
population unit-variance. A person's profile is then their per-feature mean and
std in that space - a consistent typist has std well below 1. Distance for a new
attempt is a clipped RMS z-score against the profile; the accept threshold is
calibrated leave-one-out from the enrollment attempts.

Calibrated on the CMU benchmark (~15 enrollment attempts / subject): roughly 9%
false-reject and 9% false-accept. Keystroke dynamics on a single short phrase is
a soft signal - this is a demonstrator, not a lock.
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np

# the scaler was fit on a DataFrame; transforming a plain array is fine but noisy
warnings.filterwarnings(
    "ignore", message="X does not have valid feature names", category=UserWarning
)

_SCALER_PATH = Path(__file__).resolve().parent.parent / "models" / "scaler.pkl"

N_FEATURES = 31
MIN_SAMPLES = 8          # fewest attempts we accept; ~15 is the sweet spot
SIGMA_FLOOR = 0.25       # in scaled space, where population std is 1.0
CLIP = 3.0               # cap per-feature z so one fumbled key can't dominate
THRESHOLD_K = 1.0        # accept within mean + K*std of the leave-one-out spread
THRESHOLD_FLOOR = 0.2


@dataclass
class Profile:
    name: str
    mean: list[float]     # length 31, scaled space
    sigma: list[float]    # length 31, scaled space
    threshold: float
    n_samples: int


@lru_cache(maxsize=1)
def _scaler():
    return joblib.load(_SCALER_PATH)


def _scale(rows) -> np.ndarray:
    return _scaler().transform(np.asarray(rows, dtype=float))


def _stats(z: np.ndarray):
    return z.mean(axis=0), np.maximum(z.std(axis=0, ddof=1), SIGMA_FLOOR)


def _distance(z: np.ndarray, mean: np.ndarray, sigma: np.ndarray) -> float:
    r = np.clip((z - mean) / sigma, -CLIP, CLIP)
    return float(np.sqrt(np.mean(r ** 2)))


def enroll(name: str, samples: list[list[float]]) -> Profile:
    raw = np.asarray(samples, dtype=float)

    if raw.ndim != 2 or raw.shape[1] != N_FEATURES:
        raise ValueError(f"each sample must have exactly {N_FEATURES} features")
    if raw.shape[0] < MIN_SAMPLES:
        raise ValueError(f"need at least {MIN_SAMPLES} attempts to enroll")

    z = _scale(raw)
    mean, sigma = _stats(z)

    # leave-one-out: score each attempt against the others for a realistic spread
    loo = []
    for i in range(len(z)):
        m, s = _stats(np.delete(z, i, axis=0))
        loo.append(_distance(z[i], m, s))
    loo = np.asarray(loo)
    threshold = max(THRESHOLD_FLOOR, float(loo.mean() + THRESHOLD_K * loo.std()))

    return Profile(name, mean.tolist(), sigma.tolist(), threshold, int(len(z)))


def verify(profile: Profile, features: list[float]) -> dict:
    x = np.asarray(features, dtype=float)
    if x.shape != (N_FEATURES,):
        raise ValueError(f"expected {N_FEATURES} features, got {x.shape[0]}")

    z = _scale(x.reshape(1, -1))[0]
    distance = _distance(z, np.asarray(profile.mean), np.asarray(profile.sigma))
    accepted = distance <= profile.threshold

    return {
        "accepted": bool(accepted),
        "distance": round(distance, 4),
        "threshold": round(profile.threshold, 4),
        "margin": round(profile.threshold - distance, 4),
    }
