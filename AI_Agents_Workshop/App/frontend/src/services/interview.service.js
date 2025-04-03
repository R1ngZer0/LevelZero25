import axios from 'axios';
import authService from './auth.service';

const API_URL = '/api/interviews';

class InterviewService {
  async getInterviews() {
    const response = await axios.get(API_URL, {
      headers: authService.authHeader()
    });
    return response.data;
  }

  async getInterview(id) {
    const response = await axios.get(`${API_URL}/${id}`, {
      headers: authService.authHeader()
    });
    return response.data;
  }

  async createInterview(interviewData) {
    const response = await axios.post(API_URL, interviewData, {
      headers: authService.authHeader()
    });
    return response.data;
  }

  async updateInterview(id, interviewData) {
    const response = await axios.put(`${API_URL}/${id}`, interviewData, {
      headers: authService.authHeader()
    });
    return response.data;
  }

  async deleteInterview(id) {
    await axios.delete(`${API_URL}/${id}`, {
      headers: authService.authHeader()
    });
    return true;
  }
}

const interviewService = new InterviewService();
export default interviewService; 