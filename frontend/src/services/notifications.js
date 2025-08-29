import api from './api';

export const notificationAPI = {
  getNotifications: (params = {}) => api.get('/notifications', { params }),
  markAsRead: (notificationId) => api.patch(`/notifications/${notificationId}/read`),
  markAllAsRead: () => api.patch('/notifications/read-all'),
  deleteNotification: (notificationId) => api.delete(`/notifications/${notificationId}`),
  
  // Push notification subscription
  subscribe: (subscription) => api.post('/notifications/push/subscribe', { subscription }),
  unsubscribe: () => api.post('/notifications/push/unsubscribe'),
  
  // Scheduling
  schedule: (notificationData) => api.post('/notifications/schedule', notificationData),
  
  // Settings
  getSettings: () => api.get('/notifications/settings'),
  updateSettings: (settings) => api.put('/notifications/settings', settings),
  
  // Test notification
  sendTest: () => api.post('/notifications/test'),
};

export default notificationAPI;