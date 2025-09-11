import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (credentials) => api.post('/api/v1/auth/login', credentials),
  signup: (userData) => api.post('/api/v1/auth/signup', userData),
  getProfile: () => api.get('/api/v1/auth/me'),
};

export const analysisAPI = {
  analyzeText: (text) => api.post('/api/v1/analysis/text', { text }),
  getSessions: () => api.get('/api/v1/analysis/sessions'),
};

export const chatAPI = {
  sendMessage: (message) => api.post('/api/v1/chat/message', { message }),
};

export default api;