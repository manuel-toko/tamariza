import streamlit as st
import csv
import os

# === Page title ===
st.title("📝 Register New Account")

# === Admin invite code for privileged users ===
def load_invite_codes(file="admin_codes.txt"):
    if not os.path.exists(file):
        return set()
    with open(file) as f:
        return set(line.strip() for line in f if line.strip())

# === User file location ===
USER_FILE = "users.csv"

# === Ensure user file exists ===
if not os.path.exists(USER_FILE):
    with open(USER_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password", "is_admin"])  # CSV header

# === Registration Form ===
with st.form("register_form"):
    new_username = st.text_input("👤 Username")
    new_password = st.text_input("🔒 Password", type="password")
    confirm_password = st.text_input("✅ Confirm Password", type="password")
    invite_code = st.text_input("🔑 Admin Invite Code (optional)")
    submit = st.form_submit_button("Register")

# === Handle form submission ===
if submit:
    if not new_username or not new_password:
        st.warning("⚠️ Please fill in all fields.")
    elif new_password != confirm_password:
        st.warning("⚠️ Passwords do not match.")
    else:
        # Check for duplicate username
        with open(USER_FILE, mode="r", newline="") as f:
            reader = csv.DictReader(f)
            if any(row["username"] == new_username for row in reader):
                st.error("🚫 Username already exists.")
            else:
                # Determine if admin access is granted
                VALID_CODES = load_invite_codes()
                is_admin = False
                if invite_code in VALID_CODES:
                    is_admin = True

                # Save the new user to the file
                with open(USER_FILE, mode="a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([new_username, new_password, is_admin])

                # Success message and redirect
                st.success("✅ Registration successful! Redirecting to login...")
                if is_admin:
                    st.info("👑 Admin privileges granted.")

                # Auto-redirect after a short delay (1 second)
                st.session_state.registration_success = True
                st.rerun()

# === After rerun: redirect if registration was successful ===
if st.session_state.get("registration_success"):
    del st.session_state["registration_success"]
    st.switch_page("app")  
