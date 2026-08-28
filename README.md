# ⌨️ KOTTU

**Behavioral Authentication Using Keystroke Dynamics**

KOTTU verifies a user's identity from *how* they type rather than *what* they type. It analyses the fine‑grained timing of a fixed passphrase — how long each key is held and the intervals between successive keystrokes — and uses a recurrent neural network (LSTM) to recognise the person behind the keyboard. Typing rhythm is hard to imitate, so it adds a behavioral layer on top of a conventional password.

---

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Dataset](#dataset)
- [Model Architecture](#model-architecture)
- [Results](#results)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Train the model](#train-the-model)
  - [Run the web app](#run-the-web-app)
  - [Predict programmatically](#predict-programmatically)
  - [Run the tests](#run-the-tests)
- [Configuration](#configuration)
- [Outputs](#outputs)
- [Tech Stack](#tech-stack)
- [Roadmap](#roadmap)

---

## Overview

Traditional authentication checks **what a user knows** (a password or PIN). KOTTU adds a check on **how a user types**, a biometric signal that is unique to each individual and difficult for an attacker to reproduce even when the password is known.

The repository contains two parts:

1. **A training pipeline** (`src/`, `train.py`) — a modular, class‑based workflow that loads the keystroke dataset, preprocesses it, reshapes each sample into a short sequence, trains an LSTM classifier, evaluates it, and writes metrics and plots to `output/`.
2. **A Streamlit web application** (`app.py`, `pages/`, `ui/`) — a multi‑page dashboard that presents the trained model's performance, an authentication screen, and project documentation.

---

## How It Works

The pipeline in [`src/train.py`](src/train.py) chains the following stages, each implemented as its own class:

| Stage | Module | Responsibility |
|-------|--------|----------------|
| Load | [`src/data_loader.py`](src/data_loader.py) | Read `data/DSL-StrongPasswordData.csv` into a DataFrame. |
| Preprocess | [`src/preprocessing.py`](src/preprocessing.py) | Drop the `subject`, `sessionIndex`, and `rep` columns to form the 31 timing features; label‑encode `subject` and save the encoder to `models/label_encoder.pkl`. |
| Split | [`src/train_test_split.py`](src/train_test_split.py) | Stratified split into train / validation / test (test = 20%, validation = 20% of the remainder, i.e. ≈64 / 16 / 20). `random_state=42`. |
| Scale | [`src/scaler.py`](src/scaler.py) | Fit a `StandardScaler` on the training set, transform all splits, and save the scaler to `models/scaler.pkl`. |
| Sequence | [`src/sequence_generator.py`](src/sequence_generator.py) | Reshape each 31‑feature row into an `11 × 3` sequence (10 full triplets plus a final triplet padded with zeros) so it can be fed to the LSTM. |
| Build & Train | [`src/model.py`](src/model.py) | Build and compile the LSTM, then train for up to 30 epochs (batch size 32) with `EarlyStopping` on `val_loss` (patience 5, best weights restored). |
| Evaluate | [`src/evaluate.py`](src/evaluate.py) | Compute weighted accuracy, precision, recall, and F1; write `output/metrics/metrics.json` and `output/reports/classification_report.txt`; return the confusion matrix. |
| Visualise | [`src/visualisation.py`](src/visualisation.py) | Save the accuracy curve, loss curve, and confusion matrix as PNGs under `output/plots/`. |
| Save | — | Persist the trained model to `models/kottu_model.keras`. |

Inference is handled separately by [`src/predict.py`](src/predict.py): the `Predictor` class loads the saved model, scaler, and label encoder, applies the same scaling and `11 × 3` reshaping to a single 31‑value sample, and returns the predicted user together with a confidence score.

---

## Dataset

KOTTU uses the **CMU keystroke dynamics benchmark**, `data/DSL-StrongPasswordData.csv`.

- **51 subjects**, each typing the password `.tie5Roanl` 400 times (8 sessions × 50 repetitions) → 20,400 samples.
- Identifier columns: `subject`, `sessionIndex`, `rep`.
- **31 timing features** per sample:
  - `H.<key>` — hold time (key‑down to key‑up).
  - `DD.<key1>.<key2>` — down‑to‑down time between two keys.
  - `UD.<key1>.<key2>` — up‑to‑down time between two keys.

All feature values are in seconds.

---

## Model Architecture

Defined in [`src/model.py`](src/model.py) as a Keras `Sequential` model:

```
Input: (11, 3)
 ├─ LSTM(64, return_sequences=True)
 ├─ Dropout(0.3)
 ├─ LSTM(32)
 ├─ Dropout(0.3)
 ├─ Dense(64, activation="relu")
 └─ Dense(num_classes=51, activation="softmax")

Optimizer: adam
Loss:      sparse_categorical_crossentropy
Metric:    accuracy
```

---

## Results

Metrics from the most recent training run (`output/metrics/metrics.json`), evaluated on the 4,080‑sample held‑out test set:

| Metric | Score |
|--------|-------|
| Accuracy | 83.21% |
| Precision (weighted) | 83.49% |
| Recall (weighted) | 83.21% |
| F1 score (weighted) | 83.02% |

The full per‑class breakdown is in [`output/reports/classification_report.txt`](output/reports/classification_report.txt), and the training curves and confusion matrix are in [`output/plots/`](output/plots/).

---

## Project Structure

```
KOTTU/
├── app.py                     # Streamlit entry point (multi-page navigation)
├── train.py                   # Training entry point -> src.train.Trainer
├── requirements.txt
│
├── data/
│   └── DSL-StrongPasswordData.csv
│
├── src/                       # Training / inference pipeline
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── train_test_split.py
│   ├── scaler.py
│   ├── sequence_generator.py
│   ├── model.py
│   ├── train.py               # Trainer: orchestrates the full pipeline
│   ├── evaluate.py
│   ├── visualisation.py
│   └── predict.py             # Predictor: load saved artifacts and classify a sample
│
├── models/                    # Saved artifacts (produced by training)
│   ├── kottu_model.keras
│   ├── scaler.pkl
│   └── label_encoder.pkl
│
├── output/                    # Evaluation artifacts (produced by training)
│   ├── metrics/metrics.json
│   ├── reports/classification_report.txt
│   └── plots/{accuracy_curve,loss_curve,confusion_matrix}.png
│
├── pages/                     # Streamlit pages
│   ├── dashboard.py           # Hero + headline metrics + quick links
│   ├── authentication.py      # Authentication UI (model not yet wired in)
│   ├── model_insights.py      # Metrics, training curves, confusion matrix, report
│   └── about.py               # Project write-up
│
├── ui/
│   ├── components.py          # load_css() helper
│   ├── styles.css             # Global dark theme
│   └── theme.py               # Design constants (colors, spacing, typography)
│
└── tests/
    └── test_artifacts.py      # Unit tests for Evaluator and Visualizer outputs
```

---

## Installation

Requires **Python 3.11**.

```bash
git clone <repository-url>
cd KOTTU

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Dependencies: `tensorflow`, `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `joblib`.

---

## Usage

### Train the model

```bash
python train.py
```

This runs the full pipeline and regenerates every artifact in `models/` and `output/`.

### Run the web app

```bash
streamlit run app.py
```

The app opens with four pages:

- **Dashboard** — project hero banner, headline metrics read from `output/metrics/metrics.json`, and shortcuts to the other pages.
- **Authentication** — the authentication interface. It currently demonstrates the UI only; the model is not connected to this page yet.
- **Model Insights** — metric cards, the accuracy/loss curves, the confusion matrix, and the classification report.
- **About** — project overview, motivation, tech stack, and roadmap.

> The Dashboard and Model Insights pages read files from `output/`, so run training at least once before starting the app.

### Predict programmatically

```python
from src.predict import Predictor

predictor = Predictor()

# 31 keystroke-timing values in the dataset's column order
sample = [0.1491, 0.3979, 0.2488, 0.1069, 0.1674, 0.0605, 0.1169, 0.2212,
          0.1043, 0.1417, 1.1885, 1.0468, 0.1146, 1.6055, 1.4909, 0.1067,
          0.7590, 0.6523, 0.1016, 0.2136, 0.1120, 0.1349, 0.1484, 0.0135,
          0.0932, 0.3515, 0.2583, 0.1338, 0.3509, 0.2171, 0.0742]

result = predictor.predict(sample)
print(result)   # {'user': 's002', 'confidence': 0.97}
```

### Run the tests

```bash
python -m unittest discover -s tests
```

The tests verify that `Evaluator` writes `metrics.json` / `classification_report.txt` and that `Visualizer` writes the three plot PNGs.

---

## Configuration

Common knobs, and where to change them:

| What | Where |
|------|-------|
| Train / validation / test ratios, `random_state` | [`src/train_test_split.py`](src/train_test_split.py) |
| LSTM units, dropout, dense size, optimizer, loss | [`src/model.py`](src/model.py) |
| Epochs, batch size, early-stopping patience | [`src/train.py`](src/train.py) |
| Sequence shape (`11 × 3`) | [`src/sequence_generator.py`](src/sequence_generator.py) and [`src/predict.py`](src/predict.py) |
| Dataset path | [`src/data_loader.py`](src/data_loader.py) |
| App colors, typography, spacing | [`ui/theme.py`](ui/theme.py) and [`ui/styles.css`](ui/styles.css) |

---

## Outputs

Produced by `python train.py`:

| Path | Contents |
|------|----------|
| `models/kottu_model.keras` | Trained LSTM. |
| `models/scaler.pkl` | Fitted `StandardScaler`. |
| `models/label_encoder.pkl` | Fitted `LabelEncoder` (subject ↔ class index). |
| `output/metrics/metrics.json` | Accuracy, precision, recall, F1. |
| `output/reports/classification_report.txt` | Per‑class precision / recall / F1. |
| `output/plots/accuracy_curve.png` | Training accuracy per epoch. |
| `output/plots/loss_curve.png` | Training loss per epoch. |
| `output/plots/confusion_matrix.png` | Test‑set confusion matrix. |

---

## Tech Stack

- **Language:** Python 3.11
- **Machine learning:** TensorFlow / Keras (LSTM), scikit‑learn (splitting, scaling, label encoding, metrics)
- **Data:** pandas, NumPy
- **Visualization:** matplotlib (`Agg` backend)
- **Persistence:** joblib, Keras native format
- **Web app:** Streamlit (multi‑page via `st.navigation` / `st.Page`)

---

## Roadmap

- Wire the trained model into the **Authentication** page for live predictions.
- Real‑time keystroke capture in the browser.
- Continuous (session‑long) authentication.
- Support for larger user groups and stronger architectures.
- Deployment as a cloud authentication service.

---

_KOTTU v1.0 — Behavioral Authentication System_
