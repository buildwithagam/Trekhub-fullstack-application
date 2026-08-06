# TrekHub — Frontend

Vue.js 3 + Tailwind CSS frontend for the TrekHub Trekking Management Platform.

## Live Demo
🔗 [trekhub.vercel.app](https://trekhub.vercel.app)

## Tech Stack
- Vue.js 3
- Tailwind CSS
- Chart.js
- Axios (JWT auto-refresh)
- Vue Router (role-based guards)

## Features
- Auto-login demo — lands directly on Trekker Dashboard
- 🔄 Switch Role dropdown — instantly switch between Trekker, Staff and Admin dashboards
- Trekker Dashboard with booking overview, charts, trek cards
- Admin Dashboard — manage staff, treks, users, bookings, reports
- Staff Dashboard — assigned treks, participants, slot management

## Run Locally
```bash
npm install
npm run dev
```

## Demo Credentials
| Role | Email | Password |
|---|---|---|
| Trekker | trekker@tma.com | pass123 |
| Staff | staff@tma.com | pass123 |
| Admin | admin@tma.com | pass123 |
