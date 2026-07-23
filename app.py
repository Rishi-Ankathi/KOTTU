import streamlit as st

from ui.components import load_css

st.set_page_config(
    page_title="KOTTU",
    page_icon="⌨️",
    layout="wide"
)

load_css()

dashboard = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    icon="🏠",
    default=True
)

authentication = st.Page(
    "pages/authentication.py",
    title="Authentication",
    icon="🔐"
)

insights = st.Page(
    "pages/model_insights.py",
    title="Model Insights",
    icon="📊"
)

about = st.Page(
    "pages/about.py",
    title="About",
    icon="ℹ️"
)

pg = st.navigation(
    [
        dashboard,
        authentication,
        insights,
        about
    ]
)

pg.run()