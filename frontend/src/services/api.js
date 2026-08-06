import axios from 'axios';

const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://127.0.0.1:5000'
});

// ── Auth-readiness promise ──────────────────────────────────────────────────
// Resolves once a real JWT token is available.
// All API calls wait on this before sending, so nothing fires with the fake
// demo token and nothing redirects to /login prematurely.
let _resolveReady;
let _authReady = new Promise(resolve => { _resolveReady = resolve; });

export function markAuthReady() {
  _resolveReady();
}

export function resetAuthReady() {
  _authReady = new Promise(resolve => { _resolveReady = resolve; });
}

// ── Request interceptor ─────────────────────────────────────────────────────
api.interceptors.request.use(
  async (config) => {
    // Skip waiting for auth on the login endpoint itself
    const isLoginCall = config.url?.includes('/api/auth/login') ||
                        config.url?.includes('/api/auth/refresh');
    if (!isLoginCall) {
      await _authReady; // wait until real token is set
    }
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ── Response interceptor ────────────────────────────────────────────────────
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('refresh_token');
      // Only try refresh if it's a real token (not the demo placeholder)
      if (refreshToken && refreshToken !== 'demo-refresh') {
        try {
          const res = await axios.post(
            `${api.defaults.baseURL}/api/auth/refresh`, {},
            { headers: { Authorization: `Bearer ${refreshToken}` } }
          );
          const newToken = res.data.access_token;
          localStorage.setItem('access_token', newToken);
          originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
          return api(originalRequest);
        } catch {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user');
          window.location.href = '#/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

export default api;
