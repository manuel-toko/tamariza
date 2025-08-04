import streamlit as st
import csv
import os

USER_FILE = "users.csv"

# 🚫 Only allow logged-in users
if not st.session_state.get("logged_in"):
    st.warning("⛔ Please log in to access this page!")
    st.stop()

st.title("⚙️ Settings")

# ========== 🔐 1. Change Password ==========
st.header("🔐 Change Password")

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

def save_users(users_dict):
    with open(USER_FILE, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["username", "password", "is_admin"])
        writer.writeheader()
        for username, info in users_dict.items():
            writer.writerow({
                "username": username,
                "password": info["password"],
                "is_admin": str(info["is_admin"])
            })

users = load_users()
current_user = st.session_state.username

with st.form("change_password_form"):
    old_pw = st.text_input("Current Password", type="password")
    new_pw = st.text_input("New Password", type="password")
    confirm_pw = st.text_input("Confirm New Password", type="password")
    submitted = st.form_submit_button("Update Password")

    if submitted:
        if users[current_user]["password"] != old_pw:
            st.error("❌ Current password is incorrect.")
        elif new_pw != confirm_pw:
            st.error("❌ New passwords do not match.")
        elif len(new_pw) < 4:
            st.warning("⚠️ Password should be at least 4 characters.")
        else:
            users[current_user]["password"] = new_pw
            save_users(users)
            st.success("✅ Password updated successfully!")

# ========== ℹ️ 9. About & Help ==========
st.header("ℹ️ About & Help")

st.markdown("""
This system is designed to manage sports facility reservations at **Kyushu University**.  
It supports both **users** and **administrators**, including features such as:
- 📅 Reservation creation & cancellation
- 📊 Admin filtering and CSV export
- 🧹 Auto-clean expired reservations
- 🔐 Password management

If you encounter issues or have suggestions, feel free to contact the developer.

📧 **Contact:** kyoso_project_group@kyushu-u.ac.jp  
📘 **Source Code:** _Available upon request_  
""")
