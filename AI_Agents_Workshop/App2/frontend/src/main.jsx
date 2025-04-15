import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css'; // Keep or remove based on styling needs
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { ModeProvider } from './context/ModeContext'; // Import ModeProvider

// Define a default theme (can be customized later)
const theme = createTheme();

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <ModeProvider> {/* Wrap App with ModeProvider */}
        <CssBaseline /> {/* Normalize CSS and apply background color */}
        <App />
      </ModeProvider>
    </ThemeProvider>
  </React.StrictMode>,
);
