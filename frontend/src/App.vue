<template>
  <div class="app-container">

    <!-- Global loading screen while auto-login runs -->
    <div v-if="appLoading"
      class="fixed inset-0 bg-white flex flex-col items-center justify-center z-50"
      style="font-family:'Inter',sans-serif">
      <div class="flex flex-col items-center gap-6">
        <!-- Logo -->
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 bg-green-600 rounded-2xl flex items-center justify-center shadow-lg">
            <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M3 17l5-10 4 8 3-5 4 7H3z"/>
            </svg>
          </div>
          <span class="text-2xl font-bold text-gray-900" style="font-family:'Poppins',sans-serif">
            Trek<span class="text-green-600">Hub</span>
          </span>
        </div>
        <!-- Spinner -->
        <div class="flex flex-col items-center gap-3">
          <svg class="w-8 h-8 animate-spin text-green-600" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
          </svg>
          <p class="text-gray-500 text-sm">{{ loadingMessage }}</p>
          <p v-if="countdown > 0" class="text-gray-400 text-xs">Timeout in {{ countdown }}s</p>
        </div>
      </div>
    </div>

    <!-- Main app (only shown after loading) -->
    <template v-else>
      <AppNavbar
        v-if="showLegacyNav"
        :user="user"
        :is-authenticated="isAuthenticated"
        :notification-count="notificationCount"
        :notifications="state.notifications"
        @logout="handleLogout"
        @load-notifications="loadNotifications"
        @mark-read="markRead"
      />
      <main :class="isDashboardRoute ? '' : 'tma-main'">
        <router-view></router-view>
      </main>
    </template>

    <ToastContainer :toasts="toasts" @remove="removeToast" />
  </div>
</template>

<script>
import { computed, ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import store from './store';
import api from './services/api';
import AppNavbar from './components/common/Navbar.vue';
import ToastContainer from './components/common/ToastContainer.vue';

export default {
  components: { AppNavbar, ToastContainer },
  setup() {
    const router = useRouter();
    const route  = useRoute();
    const user   = computed(() => store.state.user);
    const isAuthenticated  = store.isAuthenticated;
    const notificationCount = store.notificationCount;
    const state  = store.state;
    const toasts = ref([]);
    const appLoading     = ref(false);
    const loadingMessage = ref('');
    const countdown      = ref(0);

    const DASHBOARD_ROUTES = ['TrekkerDashboard', 'AdminDashboard', 'StaffDashboard'];
    const isDashboardRoute = computed(() => DASHBOARD_ROUTES.includes(route.name));
    const showLegacyNav    = computed(() => !isDashboardRoute.value);

    const loadNotifications = () => store.fetchNotifications();
    const markRead = (id) => store.markNotificationRead(id);
    const handleLogout = () => { store.logout(); router.push({ name: 'Login' }); };

    const triggerToast = (message, type = 'success') => {
      const id = Date.now();
      toasts.value.push({ id, message, type });
      setTimeout(() => removeToast(id), 5000);
    };
    const removeToast = (id) => { toasts.value = toasts.value.filter(t => t.id !== id); };

    onMounted(async () => {
      window.triggerToast = triggerToast;

      // Already has a real session — go straight to dashboard
      if (store.isAuthenticated.value) {
        appLoading.value = false;
        const role = store.state.user?.role;
        if (role === 'ADMIN')      router.push({ name: 'AdminDashboard' });
        else if (role === 'STAFF') router.push({ name: 'StaffDashboard' });
        else                       router.push({ name: 'TrekkerDashboard' });
        return;
      }

      // Inject a demo trekker session INSTANTLY so dashboard shows right away
      // Real API token will be fetched silently in background
      const demoUser = { id: 3, name: 'John Trekker', email: 'trekker@tma.com', role: 'TREKKER', phone: '1234567890' };
      store.login(demoUser, 'demo-token', 'demo-refresh');
      appLoading.value = false;
      router.push({ name: 'TrekkerDashboard' });

      // Silent background auth — replaces demo token with real one when Render wakes
      const silentLogin = async () => {
        try {
          const res = await Promise.race([
            api.post('/api/auth/login', { email: 'trekker@tma.com', password: 'pass123' }),
            new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 60000))
          ]);
          store.login(res.data.user, res.data.access_token, res.data.refresh_token);
        } catch (e) {
          // Retry after 15s (Render cold start can take up to 50s)
          setTimeout(silentLogin, 15000);
        }
      };
      silentLogin();

      // Background notification polling
      setInterval(() => {
        if (isAuthenticated.value && store.state.user?.role === 'TREKKER') {
          store.fetchNotifications();
        }
      }, 15000);
    });

    return {
      user, isAuthenticated, notificationCount, state,
      loadNotifications, markRead, handleLogout,
      toasts, removeToast,
      isDashboardRoute, showLegacyNav,
      appLoading, loadingMessage, countdown,
    };
  }
};
</script>

<style scoped>
.app-container { min-height: 100vh; }
</style>
