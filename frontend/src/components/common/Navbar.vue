<template>
  <nav v-if="isAuthenticated" class="tma-navbar tma-navbar--enhanced">
    <a class="tma-brand" href="#/">
      <div class="tma-brand-icon">🏔</div>
      <span>Trek<span class="highlight">Hub</span></span>
    </a>

    <div class="navbar-user-info">
      <!-- Notification Bell (Trekkers only) -->
      <div class="notif-wrapper" v-if="user?.role === 'TREKKER'" ref="notifRef">
        <button class="notif-btn" @click="toggleNotif">
          <span class="notif-icon">🔔</span>
          <span v-if="notificationCount > 0" class="notif-badge">{{ notificationCount }}</span>
        </button>
        <div v-if="notifOpen" class="notif-dropdown">
          <div class="notif-header">Notifications</div>
          <div v-if="notifications.length === 0" class="notif-empty">No notifications</div>
          <div
            v-for="n in notifications"
            :key="n.id"
            class="notif-item"
            :class="{ unread: !n.is_read }"
          >
            <div class="notif-msg" v-html="n.message"></div>
            <div class="notif-meta">
              <span class="notif-time">{{ n.created_at }}</span>
              <button v-if="!n.is_read" class="notif-mark" @click.stop="$emit('mark-read', n.id)">Mark read</button>
            </div>
          </div>
        </div>
      </div>

      <!-- User pill -->
      <div class="user-pill">
        <div class="user-avatar">{{ userInitial }}</div>
        <span class="user-name">{{ user?.name }}</span>
        <span class="role-badge" :class="user?.role?.toLowerCase()">{{ user?.role }}</span>
      </div>

      <button @click="$emit('logout')" class="btn-logout">Sign out</button>
    </div>
  </nav>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'AppNavbar',
  props: {
    user: { type: Object, default: null },
    isAuthenticated: { type: Boolean, default: false },
    notificationCount: { type: Number, default: 0 },
    notifications: { type: Array, default: () => [] }
  },
  emits: ['logout', 'load-notifications', 'mark-read'],
  setup(props, { emit }) {
    const notifOpen = ref(false);
    const notifRef = ref(null);

    const userInitial = ref('');

    const toggleNotif = () => {
      notifOpen.value = !notifOpen.value;
      if (notifOpen.value) emit('load-notifications');
    };

    return { notifOpen, notifRef, toggleNotif, userInitial };
  },
  computed: {
    userInitial() {
      return this.user?.name?.charAt(0).toUpperCase() || '?';
    }
  }
};
</script>

<style scoped>
.notif-wrapper {
  position: relative;
}

.notif-btn {
  background: var(--dark-card2);
  border: 1px solid var(--dark-border);
  border-radius: 8px;
  padding: 7px 10px;
  cursor: pointer;
  position: relative;
  display: flex;
  align-items: center;
  transition: var(--transition);
  color: var(--text-secondary);
}
.notif-btn:hover {
  border-color: var(--dark-border-hover);
  color: var(--text-primary);
}
.notif-icon { font-size: 1rem; }
.notif-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: var(--danger);
  color: white;
  font-size: 0.65rem;
  font-weight: 700;
  min-width: 17px;
  height: 17px;
  border-radius: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
}

.notif-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 320px;
  background: var(--dark-card);
  border: 1px solid var(--dark-border-hover);
  border-radius: var(--radius-lg);
  box-shadow: 0 16px 48px rgba(0,0,0,0.6);
  z-index: 1100;
  overflow: hidden;
  animation: slideUp 0.15s ease;
}
.notif-header {
  padding: 12px 16px;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.6px;
  border-bottom: 1px solid var(--dark-border);
}
.notif-empty {
  padding: 20px 16px;
  text-align: center;
  font-size: 0.85rem;
  color: var(--text-muted);
}
.notif-item {
  padding: 12px 16px;
  border-bottom: 1px solid var(--dark-border);
  transition: background 0.15s;
}
.notif-item:last-child { border-bottom: none; }
.notif-item.unread { background: rgba(200,121,65,0.04); }
.notif-msg { font-size: 0.85rem; color: var(--text-primary); margin-bottom: 4px; }
.notif-meta { display: flex; justify-content: space-between; align-items: center; }
.notif-time { font-size: 0.75rem; color: var(--text-muted); }
.notif-mark {
  background: none;
  border: none;
  font-size: 0.75rem;
  color: var(--accent);
  cursor: pointer;
  padding: 0;
  text-decoration: underline;
}

/* ── Enhanced navbar ── */
.tma-navbar--enhanced {
  background: rgba(13, 10, 8, 0.92);
  border-bottom: 1px solid rgba(200, 121, 65, 0.15);
  box-shadow: 0 1px 0 rgba(200, 121, 65, 0.08), 0 4px 24px rgba(0,0,0,0.4);
}
.tma-navbar--enhanced .tma-brand-icon {
  box-shadow: 0 0 16px rgba(200, 121, 65, 0.35);
}
.tma-navbar--enhanced .user-pill {
  background: rgba(28, 22, 17, 0.9);
  border-color: rgba(200, 121, 65, 0.2);
  transition: border-color 0.25s;
}
.tma-navbar--enhanced .user-pill:hover {
  border-color: rgba(200, 121, 65, 0.5);
}
.tma-navbar--enhanced .user-avatar {
  box-shadow: 0 0 10px rgba(200, 121, 65, 0.3);
}
</style>
