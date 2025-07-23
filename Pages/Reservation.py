import streamlit as st
import datetime
import csv
import os

# 🚫 Only allow logged-in users
if not st.session_state.get("logged_in"):
    st.warning("⛔ Please log in to access this page.")
    st.stop()

st.title("📅 Sports Facility Reservation")

# 📂 CSV file paths
RESERVATION_FILE = "reservations.csv"
VENUE_FILE = "venues.csv"

# 🏟 Load venues into dictionary for enrichment
venue_dict = {}
venue_names = []
if os.path.exists(VENUE_FILE):
    with open(VENUE_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            venue_dict[row["name"]] = row
            venue_names.append(row["name"])
else:
    st.error("❗ Venue file not found. Please contact admin.")
    st.stop()

# ⏰ Time slots
time_slots = ["09:00 - 10:00", "10:00 - 11:00", "14:00 - 15:00", "15:00 - 16:00"]

# 📌 Create reservation file if missing
if not os.path.exists(RESERVATION_FILE):
    with open(RESERVATION_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user", "venue", "date", "time"])

# 📤 Load all reservations
def load_reservations():
    with open(RESERVATION_FILE, mode="r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

# ✅ Save new reservation
def save_reservation(user, venue, date, time):
    with open(RESERVATION_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([user, venue, date, time])

# ❌ Cancel reservation by index
def delete_reservation_by_index(index_to_remove):
    rows = load_reservations()
    with open(RESERVATION_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user", "venue", "date", "time"])
        for i, row in enumerate(rows):
            if i != index_to_remove:
                writer.writerow([row["user"], row["venue"], row["date"], row["time"]])

# 📋 Reservation form
with st.form("reservation_form"):
    venue = st.selectbox("🏟 Select Venue", venue_names)
    date = st.date_input("📅 Select Date", min_value=datetime.date.today())
    time = st.selectbox("⏰ Select Time Slot", time_slots)
    submit = st.form_submit_button("Reserve")

# 🧠 Conflict check
if submit:
    current_user = st.session_state.username
    reservations = load_reservations()

    conflict = any(
        r["venue"] == venue and r["date"] == str(date) and r["time"] == time
        for r in reservations
    )

    if conflict:
        st.warning("⚠️ This time slot at the venue is already booked.")
    else:
        save_reservation(current_user, venue, str(date), time)
        st.success("✅ Reservation successful!")

# 📖 My Reservations
st.subheader("📖 My Reservations")

reservations = load_reservations()
user_reservations = [
    (i, r) for i, r in enumerate(reservations)
    if r["user"] == st.session_state.username
]

if user_reservations:
    for i, r in user_reservations:
        venue_info = venue_dict.get(r["venue"], {})
        location = venue_info.get("location", "Unknown")
        capacity = venue_info.get("capacity", "N/A")
        notes = venue_info.get("notes", "")

        with st.expander(f"📌 {r['venue']} | {r['date']} @ {r['time']}"):
            st.write(f"**Location:** {location}")
            st.write(f"**Capacity:** {capacity}")
            st.write(f"**Notes:** {notes}")
            col1, col2 = st.columns([5, 1])
            with col1:
                st.caption(f"Reserved by **{r['user']}**")
            with col2:
                if st.button("❌ Cancel", key=f"cancel_{i}"):
                    delete_reservation_by_index(i)
                    st.success("✅ Reservation canceled.")
                    st.experimental_rerun()
else:
    st.info("You don't have any reservations yet.")
