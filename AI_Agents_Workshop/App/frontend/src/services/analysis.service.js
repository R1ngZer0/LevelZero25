import axios from 'axios';
import authService from './auth.service';

const API_URL = '/api/analyses';

class AnalysisService {
  async getAnalyses(filter = {}) {
    // Create query params for filtering if needed
    const params = new URLSearchParams();
    if (filter.analysisType) {
      params.append('analysis_type', filter.analysisType);
    }
    if (filter.interviewId) {
      params.append('interview_id', filter.interviewId);
    }
    
    const response = await axios.get(`${API_URL}?${params.toString()}`, {
      headers: authService.authHeader()
    });
    return response.data;
  }

  async getAnalysis(id) {
    const response = await axios.get(`${API_URL}/${id}`, {
      headers: authService.authHeader()
    });
    return response.data;
  }

  async triggerIndividualAnalysis(interviewId) {
    const response = await axios.post(`${API_URL}/trigger/individual/${interviewId}`, {}, {
      headers: authService.authHeader()
    });
    return response.data;
  }

  async triggerCrossSectionAnalysis(operatorIds = null) {
    const payload = operatorIds ? { operator_ids: operatorIds } : {};
    
    const response = await axios.post(`${API_URL}/trigger/cross-section`, payload, {
      headers: authService.authHeader()
    });
    return response.data;
  }
}

const analysisService = new AnalysisService();
export default analysisService; 