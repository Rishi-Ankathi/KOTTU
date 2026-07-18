from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
OUTPUT_DIR = PROJECT_ROOT / "output"
METRICS_PATH = OUTPUT_DIR / "metrics" / "metrics.json"


def _load_metrics() -> dict:
    if not METRICS_PATH.exists():
        return {}

    import json

    with open(METRICS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def show() -> None:
    st.title("KOTTU")
    st.subheader("Behavioral Authentication System")

    st.markdown("---")

    metrics = _load_metrics()
    accuracy = metrics.get("accuracy", 0.0)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Model Status", "Ready")
    with col2:
        st.metric("Model Accuracy", f"{accuracy * 100:.2f}%")
    with col3:
        st.metric("Users Trained", "Multiple")
    with col4:
        st.metric("Typing Samples", "Available")

    st.markdown("---")

    st.subheader("Dataset")
    st.write("The system uses keystroke dynamics samples from the DSL Strong Password Dataset.")

    col5, col6 = st.columns(2)
    with col5:
        st.button("Start Authentication", use_container_width=True, disabled=not (MODELS_DIR / "kottu_model.keras").exists())
    with col6:
        if st.button("Model Insights", use_container_width=True):
            st.switch_page("pages/modelInsights.py")


if __name__ == "__main__":
    show()
