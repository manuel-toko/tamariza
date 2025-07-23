import streamlit as st
import csv
import os

# 📂 File paths
USER_FILE = "users.csv"
LOGIN_STATE_FILE = "login_state.csv"

# 🔁 Load previous login state (if exists)
def load_login_state():
    if os.path.exists(LOGIN_STATE_FILE):
        with open(LOGIN_STATE_FILE, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                return row["username"], row["is_admin"] == "True"
    return None, False

# 💾 Save login state to file
def save_login_state(username, is_admin):
    with open(LOGIN_STATE_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "is_admin"])
        writer.writerow([username, str(is_admin)])

# ❌ Clear login state file
def clear_login_state():
    if os.path.exists(LOGIN_STATE_FILE):
        os.remove(LOGIN_STATE_FILE)

# 🚀 Auto-login if state file exists
prev_user, prev_admin = load_login_state()
if prev_user and "logged_in" not in st.session_state:
    st.session_state.logged_in = True
    st.session_state.username = prev_user
    st.session_state.is_admin = prev_admin

# 🧠 Initialize session state if missing
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

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
            save_login_state(username, st.session_state.is_admin)  # ✅ Save login state
            st.success(f"Welcome, {username}!")
            st.stop()
        else:
            st.error("Invalid username or password.")

    st.info("Don't have an account?")
    st.page_link("pages/Register.py", label="📝 Go to Register")

# ✅ After Login
else:
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    
    # Admin-specific navigation
    if st.session_state.is_admin:
        st.sidebar.page_link("pages/Home.py", label="🧑‍⚖️ Admin Dashboard")
    else:
        st.sidebar.page_link("pages/Home.py", label="🏠 Home")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.is_admin = False
        clear_login_state()  # ✅ Clear saved login
        st.experimental_rerun()

    st.write("Please select a feature page from the left 👈")
