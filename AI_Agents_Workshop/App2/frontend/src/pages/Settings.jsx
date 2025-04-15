// Placeholder for the Settings page
import React from 'react';
import { Typography, Box, FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import { useMode } from '../context/ModeContext'; // Import the context hook

function Settings() {
  const { mode, changeMode } = useMode(); // Use the context

  const handleModeChange = (event) => {
    changeMode(event.target.value);
  };

  return (
    <Box sx={{ width: '100%', maxWidth: 500 }}>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>

      <FormControl fullWidth margin="normal">
        <InputLabel id="mode-select-label">Application Mode</InputLabel>
        <Select
          labelId="mode-select-label"
          id="mode-select"
          value={mode}
          label="Application Mode"
          onChange={handleModeChange}
        >
          <MenuItem value="cloud">Cloud (OpenAI)</MenuItem>
          <MenuItem value="local">Local (Ollama)</MenuItem>
        </Select>
      </FormControl>

      {/* Add other settings here later */}
    </Box>
  );
}

export default Settings; 