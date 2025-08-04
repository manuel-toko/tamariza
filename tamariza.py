import streamlit as st
import csv
import os

# 📂 File path for users
USER_FILE = "users.csv"

# 🧾 Load users from CSV
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, mode="r", newline="") as f:
        reader = csv.DictReader(f)
        return {
            row["username"]: {
                "password": row["password"],
                "is_admin": row["is_admin"] == "True"
            }
            for row in reader
        }

# 🚀 Initialize session state (do not persist across devices)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

users = load_users()

# 🔐 Login Interface
if not st.session_state.logged_in:
    st.title("🔐 Please Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.is_admin = users[username]["is_admin"]

            # ✅ Redirect immediately to Home
            if st.session_state.is_admin:
                st.switch_page("pages/Home.py")
            else:
                st.switch_page("pages/Home.py")
        else:
            st.error("Invalid username or password.")

    st.info("Don't have an account?")
    st.page_link("pages/Register.py", label="📝 Go to Register")

# ✅ After Login
else:
    st.sidebar.success(f"Logged in as: {st.session_state.username}")

    # Admin/General Navigation
    st.sidebar.page_link("pages/Home.py", label="🏠 Home" if not st.session_state.is_admin else "🧑‍⚖️ Admin Dashboard")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.is_admin = False
        st.experimental_rerun()

    st.write("Please select a feature page from the left 👈")
