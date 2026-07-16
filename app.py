import streamlit as st

from src.train import Trainer
from src.evaluate import Evaluator

st.set_page_config(
    page_title="KOTTU",
    page_icon="⌨️",
    layout="wide"
)

st.title("⌨️ KOTTU")
st.subheader("Behavioral Biometrics using LSTM")

st.markdown("---")

if "trained" not in st.session_state:
    st.session_state.trained = False

if st.button("Train Model"):

    with st.spinner("Training KOTTU..."):

        trainer = Trainer()

        history, model, X_test, y_test = trainer.train()

        evaluator = Evaluator()

        accuracy, report, matrix = evaluator.evaluate(
            model,
            X_test,
            y_test
        )

        st.session_state.trained = True
        st.session_state.history = history
        st.session_state.model = model
        st.session_state.accuracy = accuracy
        st.session_state.report = report

if st.session_state.trained:

    st.success("Training Complete!")

    st.metric(
        "Test Accuracy",
        f"{st.session_state.accuracy*100:.2f}%"
    )

    st.text(st.session_state.report)