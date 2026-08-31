"""
Parity check for the slim serving path.

Runs real dataset samples through both:

    old  src/predict.py    full TensorFlow, the current /identify path
    new  api/infer.py       TF-Lite runtime, the replacement

and passes only if every sample gives the same predicted user and the 51 class
probabilities agree within a small tolerance. Run this after
``scripts/export_serving.py`` and before switching the API over.

    python scripts/check_parity.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")  # deterministic TF reference
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.predict import Predictor  # noqa: E402  (full TensorFlow)
from api.infer import probabilities  # noqa: E402  (TF-Lite runtime)

N_SAMPLES = 40
TOL = 1e-4


def old_probabilities(predictor: Predictor, feats: np.ndarray) -> np.ndarray:
    """src/predict.py's internal softmax vector, from its own scaler + model."""
    scaled = predictor.scaler.transform(np.asarray(feats, dtype=float).reshape(1, -1))
    seq = np.zeros((1, 11, 3))
    seq.reshape(1, -1)[0, :31] = scaled[0]
    return predictor.model.predict(seq, verbose=0)[0]


def main() -> int:
    df = pd.read_csv(ROOT / "data" / "DSL-StrongPasswordData.csv")
    rows = df.sample(N_SAMPLES, random_state=0)
    predictor = Predictor()

    worst = 0.0
    mismatches = 0
    for _, row in rows.iterrows():
        feats = row.iloc[3:34].to_numpy(dtype=float)  # 31 features after the id cols

        p_old = old_probabilities(predictor, feats)
        p_new = probabilities(feats)
        worst = max(worst, float(np.max(np.abs(p_old - p_new))))

        if int(np.argmax(p_old)) != int(np.argmax(p_new)):
            mismatches += 1
            print(f"  MISMATCH  subject={row['subject']}  "
                  f"old={np.argmax(p_old)}  new={np.argmax(p_new)}")

    print(f"\nsamples          {N_SAMPLES}")
    print(f"user mismatches  {mismatches}")
    print(f"max |d prob|     {worst:.3e}  (tol {TOL:.0e})")

    ok = mismatches == 0 and worst <= TOL
    print("\nPARITY OK" if ok else "\nPARITY FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
