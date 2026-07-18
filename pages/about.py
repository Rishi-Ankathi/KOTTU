import streamlit as st


def show() -> None:
    st.title("About KOTTU")
    st.markdown("---")
    st.write("KOTTU is a behavioral authentication system built around keystroke dynamics.")
    st.write("It uses a long short-term memory model to learn typing patterns and verify users based on their behavior rather than only passwords.")
    st.write("The project uses the DSL Strong Password Dataset, which contains typing samples that capture timing-based keystroke signals.")
    st.write("The LSTM model is trained offline and the Streamlit interface only consumes saved model and evaluation artifacts.")
    st.write("Authentication is performed by loading the saved model, scaling the input sample, and using the learned classifier to return a predicted user and confidence score.")


if __name__ == "__main__":
    show()
