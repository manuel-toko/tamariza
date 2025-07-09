import streamlit as st
import csv
import os

st.title("📝 Register New Account")

# CSV file to store users
USER_FILE = "users.csv"

# Ensure users.csv exists
if not os.path.exists(USER_FILE):
    with open(USER_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password", "is_admin"])  # header

# Input form
with st.form("register_form"):
    new_username = st.text_input("👤 Username")
    new_password = st.text_input("🔒 Password", type="password")
    confirm_password = st.text_input("✅ Confirm Password", type="password")
    is_admin = st.checkbox("Grant admin access")
    submit = st.form_submit_button("Register")

# Handle form submission
if submit:
    if not new_username or not new_password:
        st.warning("Please fill in all fields.")
    elif new_password != confirm_password:
        st.warning("Passwords do not match.")
    else:
        # Check for existing user
        with open(USER_FILE, mode="r", newline="") as f:
            reader = csv.DictReader(f)
            if any(row["username"] == new_username for row in reader):
                st.error("Username already exists.")
            else:
                # Append new user to file
                with open(USER_FILE, mode="a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([new_username, new_password, is_admin])
                st.success("✅ Registration successful! You can now log in.")
