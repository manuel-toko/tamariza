import streamlit as st

if not st.session_state.get("logged_in"):
    st.warning("⛔ Please log in to access this page!")
    st.stop()

st.title("⚙️ Settings")
st.write("Here you can modify your preferences.")
