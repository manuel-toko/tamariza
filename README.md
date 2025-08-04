# tamariza
# 🏟 Sports Facility Reservation System (Kyushu University)

This project is a **web-based sports facility reservation system** built with **Streamlit**.  
It supports both **general users** (students/staff) and **administrators** with full functionality for **venue reservations, announcements, and account management**.

---

## 🚀 Features

### 👤 User Functions
- **User Registration & Login**
  - Standard accounts and admin accounts (with invite code)
- **Make Reservations**
  - Choose venue, date, and time slot
  - Prevent double-booking
- **Manage Reservations**
  - View your own reservations
  - Cancel or edit existing bookings
- **Auto-clean Expired Reservations**
  - Past events are automatically removed from active reservations
- **Password Management**
  - Change password from settings

### 👑 Admin Functions
- **Admin Announcements**
  - Post notices for all users
  - View, edit, and delete announcements
- **Admin Reservation Management**
  - View all reservations
  - Filter by user, venue, and date range
  - Export all reservations to CSV
  - Delete selected or all reservations

### 📅 Calendar View
- **All reservations displayed in a calendar** (FullCalendar via `streamlit-calendar`)
- Users can quickly see all booked slots

---

## 📂 File Structure

project/
│── app.py # Main Streamlit entry point (multi-page)
│── pages/
│ ├── 1_Home.py # Home dashboard (Announcements + Upcoming)
│ ├── 2_Reserve.py # Make and manage reservations
│ ├── 3_Admin.py # Admin-only view
│ ├── 4_Settings.py # Password change & help
│── users.csv # User accounts (username, password, is_admin)
│── venues.csv # Venue data (name, location, capacity, notes)
│── reservations.csv # Reservation records (user, venue, date, time)
│── announcements.csv # Admin announcements
│── README.md # This document


---

## 🛠 Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourname/sports-reservation.git
cd sports-reservation

2️⃣ Install Dependencies

pip install -r requirements.txt

Requirements:

    streamlit

    pandas

    streamlit-calendar

3️⃣ Prepare CSV Files

At minimum:

# users.csv
username,password,is_admin
admin,admin123,True
testuser,test123,False

# venues.csv
name,location,capacity,notes
Main Gym,Building A,100,Indoor gym
Multipurpose Ground,Building B,200,Outdoor field

▶️ Running the App

streamlit run app.py

Open in browser:

http://localhost:8501

🔑 Default Login

    Admin
    Username: admin
    Password: admin123

    User
    Username: testuser
    Password: test123

(You can change these in users.csv)
📸 Screenshots (Recommended to Add)

    Login Screen

    User Dashboard with Announcements

    Reservation Form

    Admin Panel (Filtering + CSV Export)

    Calendar View

📌 Notes

    Past reservations are automatically removed on each login.

    venues.csv defines available venues, time slots are fixed in code.

    Admin invite code (for creating admin accounts) can be set in Register page code:

ADMIN_INVITE_CODE = "KYOUSHI2025"
