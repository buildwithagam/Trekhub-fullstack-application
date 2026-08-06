// Shared role-switcher used by all 3 dashboards
import api from './api';
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
    const res = await api.post('/api/auth/login', creds);
    const { user, access_token, refresh_token } = res.data;
    // Update store first before navigation so guard sees correct role
    store.login(user, access_token, refresh_token);
    const target = DEMO_ROLES.find(r => r.role === role);
    await router.push({ name: target.route });
    return true;
  } catch (e) {
    console.error('Role switch failed', e);
    return false;
  }
}
