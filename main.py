import streamlit as st

USER_CREDENTIALS = {
    "admin": "123456",
    "guest": "password"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""


def login(username, password):
    return USER_CREDENTIALS.get(username) == password

if not st.session_state.logged_in:
    st.title("🔐 Please Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful! Please select a page on the left 👈")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password. Please try again.")
else:
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    st.sidebar.page_link("pages/Home.py", label="🏠 Home")
    st.sidebar.page_link("pages/Reservation.py", label="📅 Reservation")
    st.sidebar.page_link("pages/Settings.py", label="⚙️ Settings")
    
    # 添加登出按钮
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()

    st.write("Please select a feature page from the left 👈")
