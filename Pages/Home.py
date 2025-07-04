import streamlit as st

if not st.session_state.get("logged_in"):
    st.warning("⛔ Please log in to access this page!")
    st.stop()

st.title("🏠 Home")
st.write(f"Welcome, {st.session_state.username}!")
