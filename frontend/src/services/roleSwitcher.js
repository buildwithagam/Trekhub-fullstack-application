import axios from 'axios';
import api, { markAuthReady, resetAuthReady } from './api';
import store from '../store';

export const DEMO_CREDS = {
  TREKKER: { email: 'trekker@tma.com', password: 'pass123' },
  STAFF:   { email: 'staff@tma.com',   password: 'pass123' },
  ADMIN:   { email: 'admin@tma.com',   password: 'pass123' },
};

export const DEMO_ROLES = [
  { role: 'TREKKER', label: 'Trekker', email: 'trekker@tma.com', icon: '🥾', bg: 'bg-green-100',  route: 'TrekkerDashboard' },
  { role: 'STAFF',   label: 'Staff',   email: 'staff@tma.com',   icon: '🧑‍💼', bg: 'bg-orange-100', route: 'StaffDashboard'   },
  { role: 'ADMIN',   label: 'Admin',   email: 'admin@tma.com',   icon: '🛡',  bg: 'bg-red-100',    route: 'AdminDashboard'   },
];

export async function switchToRole(role, router) {
  const creds = DEMO_CREDS[role];
  if (!creds) return false;
  try {
    // Use axios directly — bypass the auth-ready queue since we're switching auth
    const res = await axios.post(
      `${api.defaults.baseURL}/api/auth/login`,
      creds,
      { timeout: 30000 }
    );
    const { user, access_token, refresh_token } = res.data;
    store.login(user, access_token, refresh_token);
    // Reset and immediately mark ready — new role has a real token
    resetAuthReady();
    markAuthReady();
    const target = DEMO_ROLES.find(r => r.role === role);
    await router.push({ name: target.route });
    return true;
  } catch (e) {
    console.error('Role switch failed', e);
    return false;
  }
}
