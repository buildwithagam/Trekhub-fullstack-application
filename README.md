# TrekHub — Trekking Management Application

A full-stack web application for managing trekking operations, bookings, staff, and trekker profiles. Built with **Flask** (backend) and **Vue.js 3 + Tailwind CSS** (frontend).

---

## Screenshots

### Login Page
![Login](screenshots/login.png)

### Register Page
![Register](screenshots/register.png)

### Trekker Dashboard
![Trekker Dashboard](screenshots/trekker-dashboard.png)

### Admin Dashboard
![Admin Dashboard](screenshots/admin-dashboard.png)

### Staff Dashboard
![Staff Dashboard](screenshots/staff-dashboard.png)

---

## Live Demo

- **Frontend:** [Deploy on Vercel]
- **Backend:** [Deploy on Render]

### Demo Credentials

| Role    | Email             | Password |
|---------|-------------------|----------|
| Trekker | trekker@tma.com   | pass123  |
| Staff   | staff@tma.com     | pass123  |
| Admin   | admin@tma.com     | pass123  |

> On the login page click **"🔑 Demo Credentials"** to auto-fill any role.

---

## Tech Stack

| Layer     | Technology                                    |
|-----------|-----------------------------------------------|
| Frontend  | Vue.js 3, Tailwind CSS, Chart.js, Axios       |
| Backend   | Flask 3, SQLAlchemy, Flask-JWT-Extended       |
| Database  | SQLite                                        |
| Auth      | JWT (access + refresh tokens)                 |
| Cache     | Flask-Caching (Redis / SimpleCache fallback)  |
| Tasks     | Celery 5 + Redis (eager fallback)             |
| Hosting   | Vercel (frontend) + Render (backend)          |

---

## Features

### Trekker
- Browse treks with filters (location, difficulty, duration)
- Book & cancel treks — slot management automatic
- View booking history with payment status
- Real-time in-app notifications
- Export trek history as CSV
- Update profile and reset password

### Staff
- View assigned treks only
- Manage slot availability
- Open / close / complete treks
- View full participant list per trek

### Admin
- Full metrics dashboard with charts (difficulty, bookings, monthly volume)
- Create, edit, delete trek trails — assign staff guides
- Full trek lifecycle: Pending → Approved → Open → Closed → Completed
- Manage staff members (add, edit, blacklist, deactivate)
- Manage trekkers (search, blacklist, deactivate)
- Bookings log with search
- Generate & download monthly HTML report

---

## Project Structure

```
├── backend/
│   ├── app.py              # App factory
│   ├── config.py           # DB, JWT, Redis config
│   ├── seed.py             # Default users + sample treks
│   ├── models/             # User, Trek, Booking, StaffProfile, Notification
│   ├── routes/             # auth, admin, staff, trekker blueprints
│   ├── tasks/              # Celery background jobs
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── views/          # Login, Register, TrekkerDashboard, AdminDashboard, StaffDashboard
    │   ├── components/     # Navbar, TrekCard, ToastContainer
    │   ├── router/         # Role-based navigation guards
    │   ├── store/          # Reactive auth store
    │   └── services/api.js # Axios with auto token refresh
    ├── tailwind.config.js
    └── vue.config.js
```

---

## How to Run Locally

### Prerequisites
- Python 3.11+
- Node.js 18+

```bash
# 1. Clone the repo
git clone https://github.com/buildwithagam/Trekhub-fullstack-application.git
cd Trekhub-fullstack-application

# 2. Backend setup
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# 3. Frontend setup
cd ../frontend
npm install
npm run dev                   # Runs on http://localhost:8080

# 4. Start backend (separate terminal)
cd ../backend
python app.py                 # Runs on http://127.0.0.1:5000
```

Open **http://localhost:8080** in your browser.

---

## API Endpoints

| Method | Endpoint | Role | Description |
|--------|----------|------|-------------|
| POST | /api/auth/login | Public | Login, returns JWT tokens |
| POST | /api/auth/register | Public | Trekker self-registration |
| GET | /api/admin/dashboard | Admin | Dashboard statistics |
| GET/POST | /api/admin/staff | Admin | List / add staff |
| GET/POST | /api/admin/trek | Admin | List / create trek |
| GET | /api/staff/treks | Staff | Assigned treks |
| GET | /api/treks | Trekker | Browse open treks |
| POST | /api/trekker/book/\<id\> | Trekker | Book a trek |
| POST | /api/trekker/cancel/\<id\> | Trekker | Cancel booking |

---

## Background Jobs

| Task | Schedule | Description |
|------|----------|-------------|
| Daily reminder | 18:00 UTC daily | Reminders for treks starting in 3 days |
| Monthly report | 1st of month 09:00 UTC | HTML summary report |
| CSV export | User-triggered | Personal trek history export |
