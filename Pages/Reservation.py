import streamlit as st
import datetime
import csv
import os

# 🚫 Require login
if not st.session_state.get("logged_in"):
    st.warning("⛔ Please log in to access this page.")
    st.stop()

st.title("📅 Sports Facility Reservation")

# 📂 File paths
RESERVATION_FILE = "reservations.csv"
VENUE_FILE = "venues.csv"

# 📍 Load venue data
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

# ❌ Delete by index
def delete_reservation_by_index(index_to_remove):
    rows = load_reservations()
    with open(RESERVATION_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user", "venue", "date", "time"])
        for i, row in enumerate(rows):
            if i != index_to_remove:
                writer.writerow([row["user"], row["venue"], row["date"], row["time"]])

# ✏️ Replace reservation by index
def update_reservation(index, new_venue, new_date, new_time):
    rows = load_reservations()
    rows[index] = {
        "user": st.session_state.username,
        "venue": new_venue,
        "date": new_date,
        "time": new_time
    }
    with open(RESERVATION_FILE, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["user", "venue", "date", "time"])
        writer.writeheader()
        writer.writerows(rows)

# 🧾 Reservation form
with st.form("reservation_form"):
    venue = st.selectbox("🏟 Select Venue", venue_names)
    date = st.date_input("📅 Select Date", min_value=datetime.date.today())
    time = st.selectbox("⏰ Select Time Slot", time_slots)
    submit = st.form_submit_button("Reserve")

if submit:
    current_user = st.session_state.username
    reservations = load_reservations()
    conflict = any(r["venue"] == venue and r["date"] == str(date) and r["time"] == time for r in reservations)

    if conflict:
        st.warning("⚠️ This time slot at the venue is already booked.")
    else:
        save_reservation(current_user, venue, str(date), time)
        st.success(f"✅ Reserved **{venue}** on **{date}** at **{time}**")

# 📖 My Reservations
st.subheader("📖 My Reservations")

reservations = load_reservations()
user_reservations = [
    (i, r) for i, r in enumerate(reservations)
    if r["user"] == st.session_state.username
]

# ✅ Sort by date and time
user_reservations.sort(key=lambda x: (x[1]["date"], x[1]["time"]))

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

            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                if st.button("❌ Cancel", key=f"cancel_{i}"):
                    delete_reservation_by_index(i)
                    st.success("✅ Reservation canceled.")
                    st.rerun()

            with col2:
                if st.button("✏️ Edit", key=f"edit_{i}"):
                    st.session_state.edit_index = i
                    st.session_state.editing = r
                    st.rerun()

# ✏️ Edit form (after button press)
if "edit_index" in st.session_state and "editing" in st.session_state:
    st.subheader("✏️ Modify Reservation")
    edit = st.session_state.editing
    with st.form("edit_form"):
        new_venue = st.selectbox("🏟 New Venue", venue_names, index=venue_names.index(edit["venue"]))
        new_date = st.date_input("📅 New Date", value=datetime.datetime.strptime(edit["date"], "%Y-%m-%d").date())
        new_time = st.selectbox("⏰ New Time", time_slots, index=time_slots.index(edit["time"]))
        submit_edit = st.form_submit_button("Confirm Change")

    if submit_edit:
        update_reservation(st.session_state.edit_index, new_venue, str(new_date), new_time)
        del st.session_state["edit_index"]
        del st.session_state["editing"]
        st.success(f"✅ Updated reservation to **{new_venue}** on **{new_date}** at **{new_time}**")
        st.rerun()
