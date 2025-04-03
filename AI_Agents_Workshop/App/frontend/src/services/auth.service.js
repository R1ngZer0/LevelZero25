import axios from 'axios';

const API_URL = '/api';

class AuthService {
  async login(username, password) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await axios.post(`${API_URL}/token`, formData);
    
    if (response.data.access_token) {
      localStorage.setItem('token', JSON.stringify(response.data));
      // After login, get the user's information
      return this.getCurrentUser();
    }
    
    return response.data;
  }

  logout() {
    localStorage.removeItem('token');
  }

  async getCurrentUser() {
    const token = this.getToken();
    if (!token) {
      throw new Error('No token found');
    }

    try {
      const response = await axios.get(`${API_URL}/me`, {
        headers: this.authHeader()
      });
      return response.data;
    } catch (error) {
      this.logout();
      throw error;
    }
  }

  getToken() {
    const tokenString = localStorage.getItem('token');
    if (!tokenString) return null;
    
    try {
      const token = JSON.parse(tokenString);
      return token;
    } catch (e) {
      return null;
    }
  }

  authHeader() {
    const token = this.getToken();
    if (token?.access_token) {
      return { Authorization: `Bearer ${token.access_token}` };
    } else {
      return {};
    }
  }

  isAdmin() {
    // Function to check if user is admin - would check role in JWT or make API call
    // This is a placeholder implementation
    return false;
  }
}

const authService = new AuthService();
export default authService; 