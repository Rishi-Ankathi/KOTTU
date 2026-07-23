import streamlit as st
import json


st.markdown("""
<div class="hero">

<h1>⌨️ KOTTU</h1>

<h3>Behavioral Authentication Using Keystroke Dynamics</h3>

<p>
Authenticate users through their typing behavior using
Keystroke Dynamics and Machine Learning.
</p>

</div>
""", unsafe_allow_html=True)

with open("output/metrics/metrics.json", "r") as f:
    metrics = json.load(f)

accuracy = metrics["accuracy"] * 100
precision = metrics["precision"] * 100
recall = metrics["recall"] * 100
f1 = metrics["f1_score"] * 100

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🔐 Authenticate", use_container_width=True):
        st.switch_page("pages/authentication.py")

with col2:
    if st.button("📊 Model Insights", use_container_width=True):
        st.switch_page("pages/model_insights.py")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

cards = [
    (f"{accuracy:.2f}%", "Accuracy"),
    (f"{precision:.2f}%", "Precision"),
    (f"{recall:.2f}%", "Recall"),
    (f"{f1:.2f}%", "F1 Score"),
]

for col, (value, label) in zip([col1, col2, col3, col4], cards):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{value}</h2>
            <p>{label}</p>
        </div>
        """, unsafe_allow_html=True)