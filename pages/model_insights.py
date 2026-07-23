import json
from pathlib import Path

import streamlit as st

st.title("📊 Model Insights")
st.subheader("Performance Evaluation")

st.markdown("---")

# ------------------------
# Load Metrics
# ------------------------

with open("output/metrics/metrics.json", "r") as f:
    metrics = json.load(f)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Accuracy", f"{metrics['accuracy']*100:.2f}%")

with col2:
    st.metric("Precision", f"{metrics['precision']*100:.2f}%")

with col3:
    st.metric("Recall", f"{metrics['recall']*100:.2f}%")

with col4:
    st.metric("F1 Score", f"{metrics['f1_score']*100:.2f}%")

st.markdown("---")

st.header("Training Curves")

col1, col2 = st.columns(2)

with col1:
    st.image(
        "output/plots/accuracy_curve.png",
        caption="Accuracy Curve",
        use_container_width=True,
    )

with col2:
    st.image(
        "output/plots/loss_curve.png",
        caption="Loss Curve",
        use_container_width=True,
    )

st.markdown("---")

st.header("Confusion Matrix")

st.image(
    "output/plots/confusion_matrix.png",
    use_container_width=True,
)

st.markdown("---")

st.header("Classification Report")

report_path = Path("output/reports/classification_report.txt")

with open(report_path, "r") as f:
    report = f.read()

st.code(report)