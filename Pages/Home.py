import streamlit as st
import csv
import os
import datetime
import pandas as pd

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://tsukatte.com/wp-content/uploads/2020/07/wild-boar.png");
        background-attachment: fixed;
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center top;
        background-color: rgba(255,255,255,0.9);  /* 半透明白背景提升对比度 */
    }
    </style>
    """,
    unsafe_allow_html=True
)


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
# 🧹 Automatically clean expired reservations
def clean_expired_reservations(file_path):
    today = datetime.date.today()
    cleaned = []

    # load and filter reservations
    if os.path.exists(file_path):
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    res_date = datetime.datetime.strptime(row["date"], "%Y-%m-%d").date()
                    if res_date >= today:
                        cleaned.append(row)
                except Exception as e:
                    pass  

        # write cleaned data back
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["user", "venue", "date", "time"])
            writer.writeheader()
            writer.writerows(cleaned)


# 👑 Admin view: show all reservations
if st.session_state.get("is_admin"):
    st.subheader("📋 All Reservations (Admin View)")

    # ✅ Ensure file exists even if just header
    if not os.path.exists(RESERVATION_FILE):
        with open(RESERVATION_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["user", "venue", "date", "time"])

    # Load data
    df = pd.read_csv(RESERVATION_FILE)

    # 📤 Export
    st.download_button(
        label="📤 Export All Reservations as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="all_reservations.csv",
        mime="text/csv"
    )

    # 🔍 Filters
    st.subheader("🔍 Filter Reservations")
    username_filter = st.text_input("Filter by username")
    venue_filter = st.selectbox("Filter by venue", ["All"] + sorted(df["venue"].unique().tolist()))
    start_date = st.date_input("Start date", value=datetime.date.today())
    end_date = st.date_input("End date", value=datetime.date.today() + datetime.timedelta(days=7))

    filtered_df = df.copy()
    if username_filter:
        filtered_df = filtered_df[filtered_df["user"].str.contains(username_filter, case=False)]
    if venue_filter != "All":
        filtered_df = filtered_df[filtered_df["venue"] == venue_filter]
    filtered_df = filtered_df[
        (filtered_df["date"] >= str(start_date)) &
        (filtered_df["date"] <= str(end_date))
    ]

    st.subheader("📊 Filtered Results")
    st.dataframe(filtered_df, use_container_width=True)

    # 🧹 Clear all reservations
    with st.expander("🧹 Clear All Reservations (Admin Only)"):
        st.warning("⚠️ This will permanently delete all reservations. Proceed with caution.")
        confirm = st.checkbox("Yes, I understand and want to clear all reservations.")

        if confirm and st.button("🚨 Confirm and Delete All"):
            with open(RESERVATION_FILE, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["user", "venue", "date", "time"])  # keep header
            st.success("✅ All reservations have been cleared.")
            st.experimental_rerun()

# 🙋 Regular user view
else:
    st.subheader("📄 My Reservations")

    if os.path.exists(RESERVATION_FILE):
        with open(RESERVATION_FILE, newline="") as f:
            reader = csv.DictReader(f)
            all_data = list(reader)

        # Filter user's own data
        user_data = [row for row in all_data if row["user"] == st.session_state.username]

        if user_data:
            for i, row in enumerate(user_data):
                with st.expander(f"📌 {row['venue']} on {row['date']} at {row['time']}"):
                    st.write(f"**Venue:** {row['venue']}")
                    st.write(f"**Date:** {row['date']}")
                    st.write(f"**Time:** {row['time']}")

                    cancel_key = f"cancel_{i}"
                    if st.button("❌ Cancel this reservation", key=cancel_key):
                        # Remove from full list
                        all_data.remove(row)
                        # Rewrite file
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
