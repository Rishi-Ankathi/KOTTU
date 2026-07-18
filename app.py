import streamlit as st

st.set_page_config(
    page_title="KOTTU",
    page_icon="⌨️",
    layout="wide"
)

st.sidebar.title("Navigation")
st.sidebar.page_link("pages/dashboard.py", label="Dashboard")
st.sidebar.page_link("pages/authentication.py", label="Authentication")
st.sidebar.page_link("pages/modelInsights.py", label="Model Insights")
st.sidebar.page_link("pages/about.py", label="About")

st.title("⌨️ KOTTU")
st.subheader("Behavioral Authentication System")

st.markdown("---")
st.write("Use the navigation panel to explore the saved model, authentication workflow, and performance artifacts.")