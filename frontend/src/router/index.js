import { createRouter, createWebHashHistory } from 'vue-router';
import store from '../store';

const AdminDashboard   = () => import('../views/AdminDashboard.vue');
const StaffDashboard   = () => import('../views/StaffDashboard.vue');
const TrekkerDashboard = () => import('../views/TrekkerDashboard.vue');
const Login            = () => import('../views/Login.vue');
const Register         = () => import('../views/Register.vue');

const routes = [
  { path: '/login',     name: 'Login',           component: Login,            meta: { guest: true } },
  { path: '/register',  name: 'Register',         component: Register,         meta: { guest: true } },
  { path: '/admin',     name: 'AdminDashboard',   component: AdminDashboard,   meta: { requiresAuth: true, role: 'ADMIN'   } },
  { path: '/staff',     name: 'StaffDashboard',   component: StaffDashboard,   meta: { requiresAuth: true, role: 'STAFF'   } },
  { path: '/dashboard', name: 'TrekkerDashboard', component: TrekkerDashboard, meta: { requiresAuth: true, role: 'TREKKER' } },
  {
    path: '/',
    redirect: () => {
      if (!store.isAuthenticated.value) return { name: 'Login' };
      const role = store.state.user?.role;
      if (role === 'ADMIN') return { name: 'AdminDashboard' };
      if (role === 'STAFF') return { name: 'StaffDashboard' };
      return { name: 'TrekkerDashboard' };
    }
  },
  { path: '/:pathMatch(.*)*', redirect: '/' }
];

const router = createRouter({ history: createWebHashHistory(), routes });

router.beforeEach((to, from, next) => {
  const isAuth  = store.isAuthenticated.value;
  const role    = store.state.user?.role;

  if (to.matched.some(r => r.meta.guest)) return next();

  if (to.matched.some(r => r.meta.requiresAuth)) {
    if (!isAuth) return next({ name: 'Login' });

    const required = to.meta.role;
    if (required && role !== required) {
      if (role === 'ADMIN')  return next({ name: 'AdminDashboard' });
      if (role === 'STAFF')  return next({ name: 'StaffDashboard' });
      return next({ name: 'TrekkerDashboard' });
    }
  }

  next();
});

export default router;
