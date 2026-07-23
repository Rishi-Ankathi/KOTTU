import streamlit as st

st.title("ℹ️ About KOTTU")
st.subheader("Behavioral Authentication using Keystroke Dynamics")

st.markdown("---")

# =====================================================
# Project Overview
# =====================================================

st.header("Project Overview")

st.write("""
**KOTTU** is a Behavioral Authentication System that verifies a user's identity
based on their unique typing patterns rather than relying only on passwords.

The project analyzes keystroke dynamics such as key press duration and timing
between consecutive keystrokes. These behavioral characteristics are then used
by a Neural Network model to recognize and authenticate registered users.
""")

st.markdown("---")

# =====================================================
# Why KOTTU
# =====================================================

st.header("Why KOTTU?")

st.write("""
Traditional authentication methods verify **what a user knows** (passwords or PINs).

KOTTU introduces an additional layer of security by verifying **how a user types**.
Since typing behavior is unique to every individual, it becomes significantly
more difficult for an attacker to impersonate another user, even if they know
the correct password.

Behavioral authentication can also be extended to continuous authentication,
allowing systems to verify users throughout an active session.
""")

st.markdown("---")

# =====================================================
# Technology Stack
# =====================================================

st.header("Technology Stack")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
### Frontend
- Streamlit

### Machine Learning
- TensorFlow / Keras
- Scikit-Learn

### Programming
- Python
""")

with col2:
    st.markdown("""
### Data Processing
- Pandas
- NumPy

### Visualization
- Matplotlib

### Model
- Neural Network (Keras)
""")

st.markdown("---")

# =====================================================
# Project Highlights
# =====================================================

st.header("Project Highlights")

st.markdown("""
- Neural Network based behavioral authentication
- Keystroke dynamics feature analysis
- Interactive Streamlit dashboard
- Model evaluation using Accuracy, Precision, Recall and F1 Score
- Visualization of training curves and confusion matrix
- Modular project structure for training and deployment
""")

st.markdown("---")

# =====================================================
# Future Enhancements
# =====================================================

st.header("Future Enhancements")

st.markdown("""
- Real-time keystroke capture from the browser
- Continuous user authentication
- Support for larger user groups
- Improved model accuracy using advanced architectures
- Deployment as a cloud-based authentication service
""")

st.markdown("---")

st.caption("KOTTU v1.0 | Behavioral Authentication System")