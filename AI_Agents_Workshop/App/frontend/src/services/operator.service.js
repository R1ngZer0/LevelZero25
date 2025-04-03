import axios from 'axios';
import authService from './auth.service';

const API_URL = '/api/operators';

class OperatorService {
  async getOperators() {
    const response = await axios.get(API_URL, {
      headers: authService.authHeader()
    });
    return response.data;
  }

  async getOperator(id) {
    const response = await axios.get(`${API_URL}/${id}`, {
      headers: authService.authHeader()
    });
    return response.data;
  }

  async createOperator(operatorData) {
    const response = await axios.post(API_URL, operatorData, {
      headers: authService.authHeader()
    });
    return response.data;
  }

  async updateOperator(id, operatorData) {
    const response = await axios.put(`${API_URL}/${id}`, operatorData, {
      headers: authService.authHeader()
    });
    return response.data;
  }

  async deleteOperator(id) {
    await axios.delete(`${API_URL}/${id}`, {
      headers: authService.authHeader()
    });
    return true;
  }
}

const operatorService = new OperatorService();
export default operatorService; 