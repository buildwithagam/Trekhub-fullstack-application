# TrekHub — Trekking Management Application (TMA v2)

A full-stack web application for managing trekking operations, bookings, staff, and trekker profiles. Built with Flask (backend) and Vue.js 3 (frontend), served as a single application at `http://127.0.0.1:5000/`.

---

## Project Structure

```
submission/
│
├── backend/                        # Flask REST API
│   ├── app.py                      # App factory, serves Vue frontend from /dist
│   ├── config.py                   # DB, JWT, Redis, Celery config (auto-detects Redis)
│   ├── extensions.py               # Flask extensions: db, jwt, cache, celery
│   ├── seed.py                     # Pre-creates Admin, Staff, Trekker, and sample treks
│   ├── requirements.txt            # Python dependencies
│   │
│   ├── models/
│   │   ├── user.py                 # User model — roles: ADMIN / STAFF / TREKKER
│   │   ├── trek.py                 # Trek model — name, location, difficulty, slots, status
│   │   ├── booking.py              # Booking model — user FK, trek FK, status, payment
│   │   ├── staff_profile.py        # StaffProfile — experience, certifications (1-to-1 User)
│   │   └── notification.py         # Notification model — user FK, message, is_read
│   │
│   ├── routes/
│   │   ├── auth.py                 # /api/auth/* — login, register, refresh, reset-password
│   │   ├── admin.py                # /api/admin/* — staff, treks, users, bookings, reports
│   │   ├── staff.py                # /api/staff/* — assigned treks, slots, status, participants
│   │   └── trekker.py              # /api/trekker/* — browse, book, cancel, history, export
│   │
│   ├── tasks/
│   │   └── celery_worker.py        # Daily reminders, monthly HTML report, CSV export
│   │
│   └── utils/
│       └── decorators.py           # @role_required decorator for JWT role enforcement
│
├── frontend/                       # Vue.js 3 SPA (Vue CLI)
│   ├── package.json
│   ├── vue.config.js               # Dev proxy: /api -> http://127.0.0.1:5000
│   │
│   └── src/
│       ├── main.js
│       ├── App.vue                 # Root shell: Navbar + router-view + ToastContainer
│       ├── style.css               # TMA design system — CSS variables, components
│       ├── router/index.js         # Hash-mode router with role-based navigation guards
│       ├── store/index.js          # Reactive auth store (localStorage persistence)
│       ├── services/api.js         # Axios instance with JWT interceptor + auto-refresh
│       │
│       ├── components/
│       │   ├── common/
│       │   │   ├── Navbar.vue      # Sticky navbar: user pill, role badge, notifications
│       │   │   ├── ToastContainer.vue
│       │   │   └── LoadingSpinner.vue
│       │   └── trek/
│       │       └── TrekCard.vue    # Trek card: metadata, slot progress bar, Book button
│       │
│       └── views/
│           ├── Login.vue           # Role selector (Admin/Staff/Trekker) + credential form
│           ├── Register.vue        # Trekker self-registration
│           ├── AdminDashboard.vue  # Tabbed: Stats, Staff, Treks, Users, Bookings, Reports
│           ├── StaffDashboard.vue  # Assigned treks, participant list, status management
│           └── TrekkerDashboard.vue # Explore trails, My Bookings, Profile
│
└── .venv/                          # Python virtual environment (excluded from git)
```

---

## How to Run

### Prerequisites
- Python 3.11+
- Node.js 18+

### Step 1 — Create virtual environment and install dependencies
```powershell
cd "MAD2 Project/submission"
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

### Step 2 — Build the frontend
```powershell
cd frontend
npm install
npm run build
cd ..
```

### Step 3 — Start the backend (serves API + frontend)
```powershell
cd backend
python app.py
```

### Step 4 — Open browser
Navigate to: **http://127.0.0.1:5000/**

> Redis is optional. Without it, Celery tasks run synchronously (eager mode) and caching uses SimpleCache. The app is fully functional either way.

---

## Default Login Credentials

| Role    | Email           | Password |
|---------|-----------------|----------|
| Admin   | admin@tma.com   | pass123  |
| Staff   | staff@tma.com   | pass123  |
| Trekker | trekker@tma.com | pass123  |

On the login page, click the **Admin / Staff / Trekker** role button to select your role, then enter your credentials. The app enforces that the submitted credentials match the selected role.

---

## Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Backend   | Flask 3 (Python 3.11)             |
| Database  | SQLite via SQLAlchemy ORM         |
| Auth      | Flask-JWT-Extended (access + refresh tokens) |
| Cache     | Flask-Caching (Redis / SimpleCache fallback) |
| Tasks     | Celery 5 + Redis (eager fallback) |
| Frontend  | Vue.js 3 + Vue CLI                |
| State     | Custom reactive store             |
| HTTP      | Axios (with auto token refresh)   |
| Charts    | Chart.js (doughnut, pie, bar)     |

---

## Features

### Admin
- Dashboard: total treks, staff, trekkers, bookings, active/completed treks
- Create, edit, delete trek trails; assign staff guides
- Trek status management: Pending → Approved → Open → Closed → Completed
- Add, edit, activate, deactivate, and blacklist staff members
- View and search all trekker accounts; blacklist or deactivate users
- View full bookings log with search by user or trek name
- Analytics charts: difficulty breakdown, booking status, monthly booking volume
- Trigger monthly HTML report — auto-downloads in browser

### Staff
- View only assigned treks (ownership enforced server-side)
- Update available slots for assigned treks
- Open or close a trek; mark as completed (cascades booking statuses)
- View full participant list for each assigned trek

### Trekker
- Self-register and log in
- Browse open treks with filters: location, difficulty, duration, start date
- Book a trek (blocked if slots full, trek not open, or already booked)
- Cancel a booking (slot restored automatically)
- View personal booking history with status and payment info
- Export trek history as CSV (async task, in-app notification on completion)
- Receive in-app notifications for upcoming trek reminders
- Update profile (name, phone) and reset password

---

## Background Jobs (Celery)

| Task | Trigger | Description |
|------|---------|-------------|
| Daily reminder | Every day at 18:00 UTC | Logs email reminders for treks starting within 3 days |
| Monthly report | 1st of month at 09:00 UTC | Generates HTML summary report in `backend/reports/` |
| CSV export | User-triggered | Exports personal trek history; notifies user when ready |

---

## API Endpoints Summary

| Method | Endpoint | Role | Description |
|--------|----------|------|-------------|
| POST | /api/auth/login | Public | Login, returns JWT tokens |
| POST | /api/auth/register | Public | Trekker self-registration |
| POST | /api/auth/refresh | Auth | Refresh access token |
| POST | /api/auth/reset-password | Auth | Reset password |
| GET | /api/admin/dashboard | Admin | Dashboard statistics |
| GET/POST | /api/admin/staff | Admin | List / add staff |
| PUT/DELETE | /api/admin/staff/\<id\> | Admin | Edit / delete staff |
| GET/POST | /api/admin/trek | Admin | List / create trek |
| PUT/DELETE | /api/admin/trek/\<id\> | Admin | Edit / delete trek |
| GET | /api/admin/users | Admin | List trekkers |
| GET | /api/admin/bookings | Admin | All bookings |
| POST | /api/admin/reports/trigger | Admin | Generate + download HTML report |
| GET | /api/staff/dashboard | Staff | Assigned treks stats |
| GET | /api/staff/treks | Staff | Assigned treks |
| PUT | /api/staff/trek/\<id\>/slots | Staff | Update available slots |
| PUT | /api/staff/trek/\<id\>/status | Staff | Update trek status |
| GET | /api/treks | Trekker | Browse open treks (with filters) |
| POST | /api/trekker/book/\<id\> | Trekker | Book a trek |
| POST | /api/trekker/cancel/\<id\> | Trekker | Cancel booking |
| GET | /api/trekker/bookings | Trekker | Personal booking history |
| POST | /api/trekker/export-history | Trekker | Trigger CSV export |
