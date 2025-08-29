import { authAPI } from './api';

class AuthService {
  constructor() {
    this.token = localStorage.getItem('auth_token');
    this.user = null;
  }

  async login(credentials) {
    try {
      const response = await authAPI.login(credentials);
      const { token, user } = response.data;
      
      this.token = token;
      this.user = user;
      localStorage.setItem('auth_token', token);
      
      return { success: true, user };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.message || 'Login failed' 
      };
    }
  }

  async signup(userData) {
    try {
      const response = await authAPI.signup(userData);
      const { token, user } = response.data;
      
      this.token = token;
      this.user = user;
      localStorage.setItem('auth_token', token);
      
      return { success: true, user };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.message || 'Signup failed' 
      };
    }
  }

  async logout() {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      this.token = null;
      this.user = null;
      localStorage.removeItem('auth_token');
    }
  }

  async verifyToken() {
    if (!this.token) return false;
    
    try {
      const response = await authAPI.verify();
      this.user = response.data.user;
      return true;
    } catch (error) {
      this.logout();
      return false;
    }
  }

  isAuthenticated() {
    return !!this.token;
  }

  getUser() {
    return this.user;
  }
}

export default new AuthService();