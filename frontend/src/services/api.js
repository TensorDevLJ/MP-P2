import axios from 'axios';
import { API_BASE_URL } from '../utils/constants';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
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
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
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
  login: (credentials) => api.post('/auth/login', credentials),
  signup: (userData) => api.post('/auth/signup', userData),
  logout: () => api.post('/auth/logout'),
  verify: () => api.get('/auth/verify'),
};

export const eegAPI = {
  uploadInit: (metadata) => api.post('/eeg/upload:init', metadata),
  process: (data) => api.post('/eeg/process', data),
  getResult: (jobId) => api.get(`/eeg/result/${jobId}`),
  listSessions: (params) => api.get('/eeg/sessions', { params }),
};

export const textAPI = {
  analyze: (data) => api.post('/text/analyze', data),
};

export const analysisAPI = {
  combined: (data) => api.post('/analysis/combined', data),
  getSummary: (sessionId) => api.get(`/analysis/summary/${sessionId}`),
};

export const chatAPI = {
  sendMessage: (data) => api.post('/chat', data),
  getHistory: (limit = 50) => api.get('/chat/history', { params: { limit } }),
};

export const careAPI = {
  findNearby: (params) => api.get('/care/nearby', { params }),
  getProviderDetails: (providerId) => api.get(`/care/provider/${providerId}`),
};

export const notificationAPI = {
  subscribe: (token) => api.post('/notify/subscribe', { token }),
  schedule: (data) => api.post('/notify/schedule', data),
  getSettings: () => api.get('/notify/settings'),
  updateSettings: (settings) => api.put('/notify/settings', settings),
};

export const reportsAPI = {
  getSession: (sessionId) => api.get(`/reports/session/${sessionId}`),
  getSummary: (params) => api.get('/reports/summary', { params }),
  export: (params) => api.get('/reports/export', { params, responseType: 'blob' }),
};

export default api;