import { reactive, computed } from 'vue';
import api from '../services/api';

const state = reactive({
  user: JSON.parse(localStorage.getItem('user')) || null,
  access_token: localStorage.getItem('access_token') || null,
  refresh_token: localStorage.getItem('refresh_token') || null,
  notifications: []
});

const isAuthenticated = computed(() => !!state.access_token);
const notificationCount = computed(() => state.notifications.filter(n => !n.is_read).length);

const store = {
  state,
  isAuthenticated,
  notificationCount,
  
  login(user, access_token, refresh_token) {
    state.user = user;
    state.access_token = access_token;
    state.refresh_token = refresh_token;
    
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
  },
  
  logout() {
    state.user = null;
    state.access_token = null;
    state.refresh_token = null;
    state.notifications = [];
    
    localStorage.removeItem('user');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },
  
  updateUser(name, phone) {
    if (state.user) {
      state.user.name = name;
      state.user.phone = phone;
      localStorage.setItem('user', JSON.stringify(state.user));
    }
  },
  
  async fetchNotifications() {
    if (!isAuthenticated.value) return;
    try {
      const res = await api.get('/api/trekker/notifications');
      state.notifications = res.data;
    } catch (err) {
      console.error("Error fetching notifications", err);
    }
  },
  
  async markNotificationRead(id) {
    try {
      await api.put(`/api/trekker/notifications/${id}/read`);
      const n = state.notifications.find(n => n.id === id);
      if (n) n.is_read = true;
    } catch (err) {
      console.error("Error marking notification read", err);
    }
  }
};

export default store;
