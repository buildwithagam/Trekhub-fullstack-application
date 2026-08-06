import axios from 'axios';
import api from './api';
import store from '../store';

export const DEMO_ROLES = [
  { role: 'TREKKER', label: 'Trekker', email: 'trekker@tma.com', icon: '🥾', bg: 'bg-green-100',  route: 'TrekkerDashboard' },
  { role: 'STAFF',   label: 'Staff',   email: 'staff@tma.com',   icon: '🧑‍💼', bg: 'bg-orange-100', route: 'StaffDashboard'   },
  { role: 'ADMIN',   label: 'Admin',   email: 'admin@tma.com',   icon: '🛡',  bg: 'bg-red-100',    route: 'AdminDashboard'   },
];

// Demo user objects — no API call needed
const DEMO_USERS = {
  TREKKER: { id: 3, name: 'John Trekker',      email: 'trekker@tma.com', role: 'TREKKER', phone: '1234567890' },
  STAFF:   { id: 2, name: 'Trek Guide 1',       email: 'staff@tma.com',   role: 'STAFF',   phone: '9876543210' },
  ADMIN:   { id: 1, name: 'TMA Administrator',  email: 'admin@tma.com',   role: 'ADMIN',   phone: '' },
};

export async function switchToRole(role, router) {
  const target = DEMO_ROLES.find(r => r.role === role);
  if (!target) return false;

  // Switch instantly using demo data — no backend needed
  const demoUser = DEMO_USERS[role];
  store.login(demoUser, 'demo-token', 'demo-refresh');
  await router.push({ name: target.route });

  // Try to get a real token in background (non-blocking)
  axios.post(
    `${api.defaults.baseURL}/api/auth/login`,
    { email: demoUser.email, password: 'pass123' },
    { timeout: 30000 }
  ).then(res => {
    store.login(res.data.user, res.data.access_token, res.data.refresh_token);
    window.dispatchEvent(new Event('auth-ready'));
  }).catch(() => {
    // Backend still sleeping — dashboard still works with demo data
  });

  return true;
}
