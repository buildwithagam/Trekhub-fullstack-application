import { createRouter, createWebHashHistory } from 'vue-router';
import store from '../store';
import api from '../services/api';

const AdminDashboard    = () => import('../views/AdminDashboard.vue');
const StaffDashboard    = () => import('../views/StaffDashboard.vue');
const TrekkerDashboard  = () => import('../views/TrekkerDashboard.vue');
const Login             = () => import('../views/Login.vue');
const Register          = () => import('../views/Register.vue');

// Auto-login helper — signs in with demo trekker credentials silently
async function autoLoginAsTrekker() {
  try {
    const res = await api.post('/api/auth/login', {
      email: 'trekker@tma.com',
      password: 'pass123'
    });
    const { user, access_token, refresh_token } = res.data;
    store.login(user, access_token, refresh_token);
    return true;
  } catch (e) {
    return false;
  }
}

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { guest: true }
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'ADMIN' }
  },
  {
    path: '/staff',
    name: 'StaffDashboard',
    component: StaffDashboard,
    meta: { requiresAuth: true, role: 'STAFF' }
  },
  {
    path: '/dashboard',
    name: 'TrekkerDashboard',
    component: TrekkerDashboard,
    meta: { requiresAuth: true, role: 'TREKKER' }
  },
  {
    path: '/',
    redirect: () => {
      const user = store.state.user;
      if (!store.isAuthenticated.value) return { name: 'TrekkerDashboard' };
      if (user?.role === 'ADMIN') return { name: 'AdminDashboard' };
      if (user?.role === 'STAFF') return { name: 'StaffDashboard' };
      return { name: 'TrekkerDashboard' };
    }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
});

router.beforeEach(async (to, from, next) => {
  const isAuth = store.isAuthenticated.value;
  const user   = store.state.user;

  // Guest routes (login/register) — just allow
  if (to.matched.some(r => r.meta.guest)) {
    return next();
  }

  // Protected route — not authenticated → auto-login as trekker
  if (to.matched.some(r => r.meta.requiresAuth)) {
    if (!isAuth) {
      const ok = await autoLoginAsTrekker();
      if (!ok) return next({ name: 'Login' });
      // After auto-login, redirect to correct dashboard for their role
      const u = store.state.user;
      if (u?.role === 'ADMIN')  return next({ name: 'AdminDashboard' });
      if (u?.role === 'STAFF')  return next({ name: 'StaffDashboard' });
      return next({ name: 'TrekkerDashboard' });
    }

    // Wrong role for this route → redirect to correct dashboard
    const requiredRole = to.meta.role;
    if (requiredRole && user.role !== requiredRole) {
      if (user.role === 'ADMIN')  return next({ name: 'AdminDashboard' });
      if (user.role === 'STAFF')  return next({ name: 'StaffDashboard' });
      return next({ name: 'TrekkerDashboard' });
    }
  }

  next();
});

export default router;
