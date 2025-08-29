import api from './api';
import Cookies from 'js-cookie';

class AuthService {
  constructor() {
    this.token = null;
    this.user = null;
  }

  async login(email, password) {
    try {
      const response = await api.post('/auth/login', {
        email,
        password,
      });

      const { token, user } = response.data;
      this.setToken(token);
      this.user = user;

      return { token, user };
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Login failed');
    }
  }

  async signup(userData) {
    try {
      const response = await api.post('/auth/signup', userData);
      
      const { token, user } = response.data;
      this.setToken(token);
      this.user = user;

      return { token, user };
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Signup failed');
    }
  }

  async logout() {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      this.removeToken();
      this.user = null;
    }
  }

  async getCurrentUser() {
    try {
      const response = await api.get('/auth/me');
      this.user = response.data;
      return this.user;
    } catch (error) {
      this.removeToken();
      throw new Error('Failed to get current user');
    }
  }

  async refreshToken() {
    try {
      const response = await api.post('/auth/refresh');
      const { token } = response.data;
      this.setToken(token);
      return token;
    } catch (error) {
      this.removeToken();
      throw new Error('Token refresh failed');
    }
  }

  setToken(token) {
    this.token = token;
    // Store in httpOnly cookie for security
    Cookies.set('auth_token', token, { 
      expires: 7, // 7 days
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict'
    });
    // Also set in localStorage as backup for API calls
    localStorage.setItem('auth_token', token);
  }

  getToken() {
    if (this.token) return this.token;
    
    // Try cookie first, then localStorage
    this.token = Cookies.get('auth_token') || localStorage.getItem('auth_token');
    return this.token;
  }

  removeToken() {
    this.token = null;
    Cookies.remove('auth_token');
    localStorage.removeItem('auth_token');
  }

  isAuthenticated() {
    const token = this.getToken();
    if (!token) return false;

    try {
      // Basic JWT validation (check if token is not expired)
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.exp * 1000 > Date.now();
    } catch {
      return false;
    }
  }

  async updateProfile(userData) {
    try {
      const response = await api.put('/auth/profile', userData);
      this.user = { ...this.user, ...response.data };
      return this.user;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Profile update failed');
    }
  }

  async changePassword(currentPassword, newPassword) {
    try {
      await api.put('/auth/change-password', {
        current_password: currentPassword,
        new_password: newPassword,
      });
      return { success: true };
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Password change failed');
    }
  }

  async resetPassword(email) {
    try {
      await api.post('/auth/reset-password', { email });
      return { success: true };
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Password reset failed');
    }
  }
}

export const authService = new AuthService();