from pathlib import Path

import streamlit as st

from src.predict import Predictor


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"


PASSWORD = "tie5Roanl"


def show() -> None:
    st.title("Authentication")
    st.subheader("Verify a typing sample")

    st.markdown("---")
    st.write(f"Password: {PASSWORD}")

    if not (MODELS_DIR / "kottu_model.keras").exists():
        st.warning("Model artifacts are not available yet. Train the model first.")
        return

    sample_input = st.text_input("Type the password", value="", placeholder="Enter the typing pattern")

    if st.button("Verify"):
        if not sample_input.strip():
            st.warning("Please provide a typing sample before verifying.")
            return

        predictor = Predictor()
        result = predictor.predict([0.0] * 31)

        st.metric("Predicted User", result["user"])
        st.metric("Confidence", f"{result['confidence'] * 100:.2f}%")

        if result["confidence"] >= 0.5:
            st.success("Authentication Status: Verified")
        else:
            st.error("Authentication Status: Rejected")


if __name__ == "__main__":
    show()
