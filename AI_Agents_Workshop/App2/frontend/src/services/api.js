// Handles communication with the backend API.
import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000', // Default if not set in .env
  headers: {
    'Content-Type': 'application/json',
  },
});

// You can add interceptors here if needed (e.g., for auth tokens)

// --- File Management --- 
export const getFiles = (mode) => apiClient.get('/files', { params: { mode } });
export const uploadFile = (formData, mode) => apiClient.post('/files/upload', formData, {
  headers: { 'Content-Type': 'multipart/form-data' },
  params: { mode },
});
export const deleteFile = (filename, mode) => apiClient.delete(`/files/${encodeURIComponent(filename)}`, { params: { mode } });
// Note: Download link is constructed directly in the component

// --- Document Creation --- 
export const createDocument = (prompt, mode) => apiClient.post('/documents/create', { prompt }, { params: { mode } });

// --- Chat & Conversation Management --- 
export const getConversations = () => apiClient.get('/chats');

export const getConversationMessages = (conversationId) => apiClient.get(`/chats/${encodeURIComponent(conversationId)}`);

export const sendMessage = (conversationId, content, mode) => {
  const payload = { content, mode };
  return apiClient.post(`/chats/${encodeURIComponent(conversationId)}/messages`, payload);
};

export default apiClient; 