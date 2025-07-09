import streamlit as st
import datetime
import csv
import os

# Check if user is logged in
if not st.session_state.get("logged_in"):
    st.warning("⛔ Please log in to access this page.")
    st.stop()

st.title("📅 Sports Facility Reservation")

# CSV file path to store all reservations
RESERVATION_FILE = "reservations.csv"

# Venue and time slot options
venues = ["🏸 Badminton Court", "⚽ Soccer Field", "🎾 Tennis Court"]
time_slots = ["09:00 - 10:00", "10:00 - 11:00", "14:00 - 15:00", "15:00 - 16:00"]

# Create the file and header if it doesn't exist
if not os.path.exists(RESERVATION_FILE):
    with open(RESERVATION_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user", "venue", "date", "time"])

# Load all reservation records from CSV
def load_reservations():
    with open(RESERVATION_FILE, mode="r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

# Save a new reservation into the CSV file
def save_reservation(user, venue, date, time):
    with open(RESERVATION_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([user, venue, date, time])

# Delete a reservation by row index
def delete_reservation_by_index(index_to_remove):
    rows = load_reservations()
    with open(RESERVATION_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user", "venue", "date", "time"])  # write header
        for i, row in enumerate(rows):
            if i != index_to_remove:
                writer.writerow([row["user"], row["venue"], row["date"], row["time"]])

# Reservation form
with st.form("reservation_form"):
    venue = st.selectbox("🏟 Select Venue", venues)
    date = st.date_input("📅 Select Date", min_value=datetime.date.today())
    time = st.selectbox("⏰ Select Time Slot", time_slots)
    submit = st.form_submit_button("Reserve")

# Handle reservation submission
if submit:
    current_user = st.session_state.username
    reservations = load_reservations()

    # Check for conflicts (same venue, date, and time)
    conflict = any(
        r["venue"] == venue and r["date"] == str(date) and r["time"] == time
        for r in reservations
    )

    if conflict:
        st.warning("⚠️ This time slot at the venue is already booked.")
    else:
        save_reservation(current_user, venue, str(date), time)
        st.success("✅ Reservation successful!")

# Display current user's reservation records
st.subheader("📖 My Reservations")

reservations = load_reservations()
user_reservations = [
    (i, r) for i, r in enumerate(reservations)
    if r["user"] == st.session_state.username
]

if user_reservations:
    for i, r in user_reservations:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"- {r['date']} | {r['time']} @ {r['venue']}")
        with col2:
            if st.button("❌ Cancel", key=f"cancel_{i}"):
                delete_reservation_by_index(i)
                st.success("Reservation canceled.")
                st.experimental_rerun()
else:
    st.info("No reservations yet.")
