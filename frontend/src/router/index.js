import { createRouter, createWebHashHistory } from 'vue-router';
import store from '../store';

// Lazy load views for optimization
const Login = () => import('../views/Login.vue');
const Register = () => import('../views/Register.vue');
const AdminDashboard = () => import('../views/AdminDashboard.vue');
const StaffDashboard = () => import('../views/StaffDashboard.vue');
const TrekkerDashboard = () => import('../views/TrekkerDashboard.vue');

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
      if (!store.isAuthenticated.value) return { name: 'Login' };
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

// Guard checks before navigating to a route
router.beforeEach((to, from, next) => {
  const isAuth = store.isAuthenticated.value;
  const user = store.state.user;

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuth) {
      next({ name: 'Login' });
    } else {
      const requiredRole = to.meta.role;
      if (requiredRole && user.role !== requiredRole) {
        if (user.role === 'ADMIN') {
          next({ name: 'AdminDashboard' });
        } else if (user.role === 'STAFF') {
          next({ name: 'StaffDashboard' });
        } else {
          next({ name: 'TrekkerDashboard' });
        }
      } else {
        next();
      }
    }
  } else if (to.matched.some(record => record.meta.guest)) {
    if (isAuth) {
      if (user.role === 'ADMIN') {
        next({ name: 'AdminDashboard' });
      } else if (user.role === 'STAFF') {
        next({ name: 'StaffDashboard' });
      } else {
        next({ name: 'TrekkerDashboard' });
      }
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
