from pathlib import Path

import json

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
METRICS_PATH = OUTPUT_DIR / "metrics" / "metrics.json"
REPORT_PATH = OUTPUT_DIR / "reports" / "classification_report.txt"
PLOTS_DIR = OUTPUT_DIR / "plots"


def _load_metrics() -> dict:
    if not METRICS_PATH.exists():
        return {}

    with open(METRICS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def _load_report() -> str:
    if not REPORT_PATH.exists():
        return "Classification report is not available yet."

    with open(REPORT_PATH, "r", encoding="utf-8") as file:
        return file.read()


def show() -> None:
    st.title("Model Insights")

    tab_overview, tab_metrics, tab_visualizations = st.tabs(["Overview", "Metrics", "Visualizations"])

    with tab_overview:
        st.subheader("Overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Model", "LSTM")
        with col2:
            st.metric("Dataset", "DSL Strong Password")
        with col3:
            st.metric("Training Samples", "Available")
        with col4:
            st.metric("Validation Samples", "Available")

        col5, col6, col7, col8 = st.columns(4)
        with col5:
            st.metric("Test Samples", "Available")
        with col6:
            st.metric("Epochs", "30")
        with col7:
            st.metric("Training Time", "Logged in training run")
        with col8:
            st.metric("Early Stopping", "Enabled")

    with tab_metrics:
        st.subheader("Metrics")
        metrics = _load_metrics()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Accuracy", f"{metrics.get('accuracy', 0.0) * 100:.2f}%")
        with col2:
            st.metric("Precision", f"{metrics.get('precision', 0.0) * 100:.2f}%")
        with col3:
            st.metric("Recall", f"{metrics.get('recall', 0.0) * 100:.2f}%")
        with col4:
            st.metric("F1 Score", f"{metrics.get('f1_score', 0.0) * 100:.2f}%")

        with st.expander("Classification Report"):
            st.text(_load_report())

    with tab_visualizations:
        st.subheader("Visualizations")
        for image_name in ["accuracy_curve.png", "loss_curve.png", "confusion_matrix.png"]:
            image_path = PLOTS_DIR / image_name
            if image_path.exists():
                st.image(str(image_path), caption=image_name)
            else:
                st.warning(f"{image_name} is not available yet.")


if __name__ == "__main__":
    show()
