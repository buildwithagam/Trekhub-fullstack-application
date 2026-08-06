import axios from 'axios';

const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://127.0.0.1:5000',
  timeout: 15000
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    // Don't send demo placeholder token — let request go unauthenticated
    if (token && token !== 'demo-token') {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const refreshToken = localStorage.getItem('refresh_token');

    // Only attempt refresh with a real refresh token
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      refreshToken &&
      refreshToken !== 'demo-refresh'
    ) {
      originalRequest._retry = true;
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
    return Promise.reject(error);
  }
);

export function markAuthReady() {}
export function resetAuthReady() {}

export default api;
