import axios from 'axios';

const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://127.0.0.1:5000'
});

// Request interceptor to add authorization header
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh automatically
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const res = await axios.post(`${api.defaults.baseURL}/api/auth/refresh`, {}, {
            headers: { 'Authorization': `Bearer ${refreshToken}` }
          });
          const newAccessToken = res.data.access_token;
          localStorage.setItem('access_token', newAccessToken);
          originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
          return api(originalRequest);
        } catch (refreshError) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user');
          window.location.href = '#/login'; // Hash router login link
          return Promise.reject(refreshError);
        }
      }
    }
    return Promise.reject(error);
  }
);

export default api;
