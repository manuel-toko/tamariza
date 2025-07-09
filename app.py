import streamlit as st
import csv
import os

# Path to user data
USER_FILE = "users.csv"

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# Read users from CSV into a dictionary
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

users = load_users()

# Login interface
if not st.session_state.logged_in:
    st.title("🔐 Please Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.is_admin = users[username]["is_admin"]
            st.success(f"Welcome, {username}!")
            st.stop()
        else:
            st.error("Invalid username or password.")

    # Link to Register page
    st.info("Don't have an account?")
    st.page_link("pages/Register.py", label="📝 Go to Register")

else:
      # ✅ Only show Admin page if user is admin
    if st.session_state.is_admin:
        st.sidebar.page_link("pages/Home.py", label="🧑‍⚖️ Admin Dashboard")


    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.is_admin = False
        st.experimental_rerun()

    st.write("Please select a feature page from the left 👈")
