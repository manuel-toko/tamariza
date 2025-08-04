import streamlit as st
import csv
import os
import datetime
import pandas as pd

# ---------- Style ----------
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://tsukatte.com/wp-content/uploads/2020/07/wild-boar.png");
        background-attachment: fixed;
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center top;
        background-color: rgba(0,0,0,0.9);  
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Constants ----------
RESERVATION_FILE = "reservations.csv"
ANNOUNCEMENT_FILE = "announcements.csv"

# ---------- Login Check ----------
if not st.session_state.get("logged_in"):
    st.warning("⛔ Please log in to access this page!")
    st.stop()

# ---------- Title ----------
st.title("🏠 Home")
st.success(f"Welcome back, {st.session_state.username}!")
today = datetime.date.today().strftime("%B %d, %Y")
st.markdown(f"📅 **Today is:** {today}")

# ---------- Load Data ----------
def load_csv(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def save_csv(file_path, data, fieldnames):
    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# ---------- Reservation Cleanup ----------
def clean_expired_reservations():
    today = datetime.date.today()
    cleaned = []
    if os.path.exists(RESERVATION_FILE):
        with open(RESERVATION_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    res_date = datetime.datetime.strptime(row["date"], "%Y-%m-%d").date()
                    if res_date >= today:
                        cleaned.append(row)
                except:
                    continue
        save_csv(RESERVATION_FILE, cleaned, ["user", "venue", "date", "time"])

clean_expired_reservations()

# ---------- Announcement Area ----------
st.subheader("📢 Announcements")

# Auto-generated announcements (next 3 days)
today_date = datetime.date.today()
upcoming_reservations = [row for row in load_csv(RESERVATION_FILE) if datetime.datetime.strptime(row["date"], "%Y-%m-%d").date() <= today_date + datetime.timedelta(days=3)]

if upcoming_reservations:
    with st.expander("🕒 Upcoming Reservations (Next 3 Days)", expanded=False):
        df_upcoming = pd.DataFrame(upcoming_reservations)
        st.dataframe(df_upcoming, use_container_width=True)

# Admin announcements
admin_announcements = load_csv(ANNOUNCEMENT_FILE)
if admin_announcements:
    with st.expander("📌 Admin Announcements", expanded=True):
        for idx, ann in enumerate(admin_announcements):
            st.info(f"**{ann['title']}**\n{ann['message']}")
            if st.session_state.get("is_admin") and st.button(f"🗑 Delete", key=f"delete_ann_{idx}"):
                admin_announcements.pop(idx)
                save_csv(ANNOUNCEMENT_FILE, admin_announcements, ["title", "message"])
                st.rerun()

# Admin Add Announcement
if st.session_state.get("is_admin"):
    st.markdown("---")
    st.subheader("➕ Add Admin Announcement")
    with st.form("add_announcement"):
        title = st.text_input("Title")
        message = st.text_area("Message")
        submitted = st.form_submit_button("✅ Publish")
        if submitted and title.strip() and message.strip():
            admin_announcements.append({"title": title.strip(), "message": message.strip()})
            save_csv(ANNOUNCEMENT_FILE, admin_announcements, ["title", "message"])
            st.success("Announcement published!")
            st.rerun()

# ---------- Admin View ----------
if st.session_state.get("is_admin"):
    st.subheader("📋 All Reservations (Admin View)")

    if not os.path.exists(RESERVATION_FILE):
        save_csv(RESERVATION_FILE, [], ["user", "venue", "date", "time"])

    df = pd.read_csv(RESERVATION_FILE)

    st.download_button("📤 Export CSV", data=df.to_csv(index=False).encode("utf-8"), file_name="reservations.csv")

    st.subheader("🔍 Filter Reservations")
    username_filter = st.text_input("Filter by username")
    venue_filter = st.selectbox("Venue", ["All"] + sorted(df["venue"].unique().tolist()))
    start_date = st.date_input("Start", value=datetime.date.today())
    end_date = st.date_input("End", value=datetime.date.today() + datetime.timedelta(days=7))

    filtered_df = df.copy()
    if username_filter:
        filtered_df = filtered_df[filtered_df["user"].str.contains(username_filter, case=False)]
    if venue_filter != "All":
        filtered_df = filtered_df[filtered_df["venue"] == venue_filter]
    filtered_df = filtered_df[
        (filtered_df["date"] >= str(start_date)) &
        (filtered_df["date"] <= str(end_date))
    ]

    st.subheader("📊 Results")
    st.dataframe(filtered_df, use_container_width=True)

    selected_rows = st.multiselect(
        "Select rows to delete",
        options=filtered_df.index.tolist(),
        format_func=lambda x: f"{filtered_df.loc[x, 'user']} - {filtered_df.loc[x, 'venue']} - {filtered_df.loc[x, 'date']} {filtered_df.loc[x, 'time']}"
    )

    if selected_rows and st.button("❌ Delete Selected"):
        df.drop(index=selected_rows, inplace=True)
        df.to_csv(RESERVATION_FILE, index=False)
        st.success("Selected reservations deleted.")
        st.rerun()

    with st.expander("🧹 Clear All Reservations"):
        st.warning("⚠️ This will delete all reservations!")
        if st.checkbox("Yes, I'm sure") and st.button("🚨 Confirm Delete"):
            df.iloc[0:0].to_csv(RESERVATION_FILE, index=False)
            st.success("✅ All cleared.")
            st.rerun()

# ---------- User View ----------
else:
    st.subheader("📄 My Reservations")
    if os.path.exists(RESERVATION_FILE):
        all_data = load_csv(RESERVATION_FILE)
        user_data = [row for row in all_data if row["user"] == st.session_state.username]

        if user_data:
            df_user = pd.DataFrame(user_data)
            st.dataframe(df_user, use_container_width=True)
            selected_rows = st.multiselect(
                "Select rows to cancel",
                options=df_user.index.tolist(),
                format_func=lambda x: f"{df_user.loc[x, 'venue']} - {df_user.loc[x, 'date']} {df_user.loc[x, 'time']}"
            )

            if selected_rows and st.button("❌ Cancel Selected"):
                new_data = [row for i, row in enumerate(user_data) if i not in selected_rows]
                others = [r for r in all_data if r["user"] != st.session_state.username]
                save_csv(RESERVATION_FILE, new_data + others, ["user", "venue", "date", "time"])
                st.success("✅ Selected reservations canceled.")
                st.rerun()
        else:
            st.info("You don't have any reservations yet.")
    else:
        st.warning("Reservation file not found.")
