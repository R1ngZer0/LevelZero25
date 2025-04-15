// Placeholder for the Knowledge Base page
import React, { useState, useEffect, useRef } from 'react';
import {
  Typography,
  Box,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
  CircularProgress,
  Alert,
  Link
} from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import DownloadIcon from '@mui/icons-material/Download';
import DeleteIcon from '@mui/icons-material/Delete';
import apiClient from '../services/api'; // Import the API client
import { useMode } from '../context/ModeContext'; // To pass mode if needed later

function KnowledgeBase() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null); // Ref for the hidden file input
  const { mode } = useMode(); // Get current mode

  // Function to fetch files
  const fetchFiles = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.get('/files', {
        params: { mode: mode } // Pass mode as query param
      });
      setFiles(response.data.files || []); // Assuming backend returns { files: [...] }
    } catch (err) {
      console.error("Error fetching files:", err);
      setError('Failed to fetch files. Please ensure the backend is running.');
      setFiles([]); // Clear files on error
    } finally {
      setLoading(false);
    }
  };

  // Fetch files on component mount and when mode changes
  useEffect(() => {
    fetchFiles();
  }, [mode]); // Re-fetch if mode changes

  // Function to handle file upload
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', file);

    try {
      await apiClient.post('/files/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        params: { mode: mode } // Pass mode as query param
      });
      // Refresh file list after successful upload
      fetchFiles();
    } catch (err) {
      console.error("Error uploading file:", err);
      setError(`Failed to upload file: ${err.response?.data?.detail || err.message}`);
    } finally {
      setUploading(false);
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  // Function to handle file deletion
  const handleFileDelete = async (filename) => {
    // Optional: Add confirmation dialog here
    // if (!confirm(`Are you sure you want to delete ${filename}?`)) {
    //   return;
    // }

    setError(null);
    try {
      await apiClient.delete(`/files/${encodeURIComponent(filename)}`, {
        params: { mode: mode } // Pass mode as query param
      });
      // Refresh file list after successful deletion
      fetchFiles();
    } catch (err) {
      console.error("Error deleting file:", err);
      setError(`Failed to delete file: ${err.response?.data?.detail || err.message}`);
    }
  };

  // Trigger hidden file input click
  const handleUploadButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Typography variant="h4" gutterBottom>
        Knowledge Base
      </Typography>

      {/* Hidden file input */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileUpload}
        style={{ display: 'none' }}
        accept=".txt,.pdf,.docx" // Specify acceptable file types
      />

      {/* Upload Button */}
      <Button
        variant="contained"
        startIcon={<UploadFileIcon />}
        onClick={handleUploadButtonClick}
        disabled={uploading || loading}
        sx={{ mb: 2 }}
      >
        {uploading ? 'Uploading...' : 'Upload File'}
      </Button>
      {uploading && <CircularProgress size={24} sx={{ ml: 1 }} />}

      {/* Error Display */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* File List */}
      {loading && !uploading ? (
        <CircularProgress />
      ) : (
        <List>
          {files.length === 0 && !loading && (
            <ListItem>
              <ListItemText primary="No files found in the knowledge base." />
            </ListItem>
          )}
          {files.map((filename) => (
            <ListItem
              key={filename}
              secondaryAction={
                <>
                  {/* Download Link/Button */}
                  <IconButton
                     edge="end"
                     aria-label="download"
                     href={`${apiClient.defaults.baseURL}/files/download/${encodeURIComponent(filename)}?mode=${mode}`}
                     target="_blank" // Open in new tab
                     rel="noopener noreferrer" // Security best practice
                     download // Suggests browser should download
                   >
                    <DownloadIcon />
                  </IconButton>
                  {/* Delete Button */}
                  <IconButton
                    edge="end"
                    aria-label="delete"
                    onClick={() => handleFileDelete(filename)}
                    sx={{ ml: 1 }}
                  >
                    <DeleteIcon />
                  </IconButton>
                </>
              }
            >
              <ListItemText primary={filename} />
            </ListItem>
          ))}
        </List>
      )}
    </Box>
  );
}

export default KnowledgeBase; 