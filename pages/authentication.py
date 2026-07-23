import streamlit as st

st.title("🔐 Authentication")
st.subheader("Behavioral Authentication using Keystroke Dynamics")

st.markdown("---")

st.write(
    "Enter the passphrase below. The authentication model will be "
    "connected in the next phase of the project."
)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:

    user = st.selectbox(
        "Select User",
        [
            "User 1",
            "User 2",
            "User 3",
            "User 4"
        ]
    )

    passphrase = st.text_input(
        "Passphrase",
        placeholder="Type the passphrase here..."
    )

    authenticate = st.button(
        "🔐 Authenticate",
        use_container_width=True
    )

with col2:

    st.markdown(
        """
        ### Instructions

        - Select the registered user.
        - Type the predefined passphrase.
        - Press **Authenticate**.
        - Model integration will be added later.
        """
    )

st.markdown("---")

if authenticate:

    if passphrase.strip() == "":
        st.warning("Please enter the passphrase.")

    else:
        st.info(
            "Authentication model is not connected yet.\n\n"
            "This page currently demonstrates the user interface."
        )