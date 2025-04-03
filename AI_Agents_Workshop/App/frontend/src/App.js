import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

// Components
import Login from './components/auth/Login';
import Layout from './components/layout/Layout';
import Dashboard from './components/dashboard/Dashboard';
import OperatorList from './components/operators/OperatorList';
import OperatorDetail from './components/operators/OperatorDetail';
import InterviewList from './components/interviews/InterviewList';
import InterviewForm from './components/interviews/InterviewForm';
import InterviewDetail from './components/interviews/InterviewDetail';
import AnalysisList from './components/analyses/AnalysisList';
import AnalysisDetail from './components/analyses/AnalysisDetail';

// Auth
import { useAuth } from './hooks/useAuth';
import PrivateRoute from './components/auth/PrivateRoute';

// Create theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#0066cc',
    },
    secondary: {
      main: '#6c757d',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/"
          element={
            <PrivateRoute>
              <Layout />
            </PrivateRoute>
          }
        >
          <Route index element={<Dashboard />} />
          
          {/* Operators */}
          <Route path="operators" element={<OperatorList />} />
          <Route path="operators/new" element={<OperatorDetail />} />
          <Route path="operators/:id" element={<OperatorDetail />} />
          
          {/* Interviews */}
          <Route path="interviews" element={<InterviewList />} />
          <Route path="interviews/new" element={<InterviewForm />} />
          <Route path="interviews/:id" element={<InterviewDetail />} />
          <Route path="interviews/:id/edit" element={<InterviewForm />} />
          
          {/* Analyses */}
          <Route path="analyses" element={<AnalysisList />} />
          <Route path="analyses/:id" element={<AnalysisDetail />} />
          
          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </ThemeProvider>
  );
}

export default App; 