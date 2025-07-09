import streamlit as st
import csv
import os
import datetime
import pandas as pd

# 🚫 Only allow logged-in users
if not st.session_state.get("logged_in"):
    st.warning("⛔ Please log in to access this page!")
    st.stop()

# 🏠 Title and welcome
st.title("🏠 Home")
st.success(f"Welcome back, {st.session_state.username}!")

# 📅 Current date
today = datetime.date.today().strftime("%B %d, %Y")
st.markdown(f"📅 **Today is:** {today}")

# 🔔 Announcement
st.info("🔔 **Announcement:**\nThe tennis court will be closed for maintenance on July 5.")

# 📂 File path
RESERVATION_FILE = "reservations.csv"
st.divider()

# 👑 Admin view: show all reservations
if st.session_state.get("is_admin"):
    st.subheader("📋 All Reservations (Admin View)")
    st.download_button(
        label="📤 Export All Reservations as CSV",
        data=pd.read_csv(RESERVATION_FILE).to_csv(index=False).encode("utf-8"),
        file_name="all_reservations.csv",
        mime="text/csv"
    )

    # 🧹 Clear all reservations (with confirmation)
    with st.expander("🧹 Clear All Reservations (Admin Only)"):
        st.warning("⚠️ This will permanently delete all reservations. Proceed with caution.")
        confirm = st.checkbox("Yes, I understand and want to clear all reservations.")

        if confirm and st.button("🚨 Confirm and Delete All"):
            os.remove(RESERVATION_FILE)
            st.success("✅ All reservations have been cleared.")
            st.experimental_rerun()

    

    if os.path.exists(RESERVATION_FILE):
        with open(RESERVATION_FILE, newline="") as f:
            reader = csv.DictReader(f)
            data = list(reader)

        if data:
            st.dataframe(data, use_container_width=True)
        else:
            st.info("No reservations found.")
    else:
        st.warning("Reservation file not found.")

# 🙋 Regular user view: show only their own reservations
else:
    st.subheader("📄 My Reservations")

    if os.path.exists(RESERVATION_FILE):
        with open(RESERVATION_FILE, newline="") as f:
            reader = csv.DictReader(f)
            all_data = list(reader)

        # Filter current user's reservations
        user_data = [row for row in all_data if row["user"] == st.session_state.username]

        if user_data:
            for i, row in enumerate(user_data):
                with st.expander(f"📌 {row['venue']} on {row['date']} at {row['time']}"):
                    st.write(f"**Venue:** {row['venue']}")
                    st.write(f"**Date:** {row['date']}")
                    st.write(f"**Time:** {row['time']}")

                    cancel_key = f"cancel_{i}"
                    if st.button("❌ Cancel this reservation", key=cancel_key):
                        # Remove the selected reservation from all_data
                        all_data.remove(row)
                        # Write the updated data back to CSV
                        with open(RESERVATION_FILE, mode="w", newline="") as f:
                            writer = csv.DictWriter(f, fieldnames=["user", "venue", "date", "time"])
                            writer.writeheader()
                            writer.writerows(all_data)

                        st.success("✅ Reservation canceled.")
                        st.experimental_rerun()
        else:
            st.info("You don't have any reservations yet.")
    else:
        st.warning("Reservation file not found.")

