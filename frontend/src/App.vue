<template>
  <div class="app-container">
    <!-- Navbar only on non-dashboard routes (dashboards have their own sidebar) -->
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

    <!-- Dashboard routes get no wrapper padding; others keep tma-main -->
    <main :class="isDashboardRoute ? '' : 'tma-main'">
      <router-view></router-view>
    </main>

    <!-- Global Toast Container -->
    <ToastContainer :toasts="toasts" @remove="removeToast" />
  </div>
</template>

<script>
import { computed, ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import store from './store';
import AppNavbar from './components/common/Navbar.vue';
import ToastContainer from './components/common/ToastContainer.vue';

export default {
  components: {
    AppNavbar,
    ToastContainer
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const user = computed(() => store.state.user);
    const isAuthenticated = store.isAuthenticated;

    const DASHBOARD_ROUTES = ['TrekkerDashboard', 'AdminDashboard', 'StaffDashboard'];
    const isDashboardRoute = computed(() => DASHBOARD_ROUTES.includes(route.name));
    const showLegacyNav = computed(() => !isDashboardRoute.value);
    const notificationCount = store.notificationCount;
    const state = store.state;
    const toasts = ref([]);

    const loadNotifications = () => {
      store.fetchNotifications();
    };

    const markRead = (id) => {
      store.markNotificationRead(id);
    };

    const handleLogout = () => {
      store.logout();
      router.push({ name: 'Login' });
    };

    const triggerToast = (message, type = 'success') => {
      const id = Date.now();
      toasts.value.push({ id, message, type });
      setTimeout(() => {
        removeToast(id);
      }, 5000);
    };

    const removeToast = (id) => {
      toasts.value = toasts.value.filter(t => t.id !== id);
    };

    onMounted(() => {
      window.triggerToast = triggerToast;
      // Start background polling for notifications for trekkers
      setInterval(() => {
        if (isAuthenticated.value && store.state.user?.role === 'TREKKER') {
          store.fetchNotifications();
        }
      }, 15000);
    });

    return {
      user,
      isAuthenticated,
      notificationCount,
      state,
      loadNotifications,
      markRead,
      handleLogout,
      toasts,
      removeToast,
      isDashboardRoute,
      showLegacyNav,
    };
  }
};
</script>

<style scoped>
.app-container {
  min-height: 100vh;
}
</style>
