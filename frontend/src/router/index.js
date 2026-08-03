import { createRouter, createWebHashHistory } from 'vue-router';
import store from '../store';
import api from '../services/api';

const AdminDashboard   = () => import('../views/AdminDashboard.vue');
const StaffDashboard   = () => import('../views/StaffDashboard.vue');
const TrekkerDashboard = () => import('../views/TrekkerDashboard.vue');
const Login            = () => import('../views/Login.vue');
const Register         = () => import('../views/Register.vue');

async function autoLoginAsTrekker() {
  try {
    const res = await api.post('/api/auth/login', {
      email: 'trekker@tma.com',
      password: 'pass123'
    });
    store.login(res.data.user, res.data.access_token, res.data.refresh_token);
    return true;
  } catch (e) {
    return false;
  }
}

const routes = [
  { path: '/login',     name: 'Login',            component: Login,            meta: { guest: true } },
  { path: '/register',  name: 'Register',          component: Register,         meta: { guest: true } },
  { path: '/admin',     name: 'AdminDashboard',    component: AdminDashboard,   meta: { requiresAuth: true, role: 'ADMIN'   } },
  { path: '/staff',     name: 'StaffDashboard',    component: StaffDashboard,   meta: { requiresAuth: true, role: 'STAFF'   } },
  { path: '/dashboard', name: 'TrekkerDashboard',  component: TrekkerDashboard, meta: { requiresAuth: true, role: 'TREKKER' } },
  {
    path: '/',
    redirect: () => {
      if (!store.isAuthenticated.value) return { name: 'TrekkerDashboard' };
      const role = store.state.user?.role;
      if (role === 'ADMIN') return { name: 'AdminDashboard' };
      if (role === 'STAFF') return { name: 'StaffDashboard' };
      return { name: 'TrekkerDashboard' };
    }
  },
  { path: '/:pathMatch(.*)*', redirect: '/' }
];

const router = createRouter({ history: createWebHashHistory(), routes });

router.beforeEach(async (to, from, next) => {
  // Always allow guest routes
  if (to.matched.some(r => r.meta.guest)) return next();

  if (to.matched.some(r => r.meta.requiresAuth)) {
    // Not logged in → auto-login as trekker then go to correct dashboard
    if (!store.isAuthenticated.value) {
      const ok = await autoLoginAsTrekker();
      if (!ok) return next({ name: 'Login' });
    }

    // Now check role — if user's role matches the target route, allow it
    const userRole = store.state.user?.role;
    const requiredRole = to.meta.role;

    // Role matches — allow navigation
    if (userRole === requiredRole) return next();

    // Role mismatch — send to correct dashboard for this user
    if (userRole === 'ADMIN')  return next({ name: 'AdminDashboard' });
    if (userRole === 'STAFF')  return next({ name: 'StaffDashboard' });
    return next({ name: 'TrekkerDashboard' });
  }

  next();
});

export default router;
