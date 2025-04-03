import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Box,
  Typography,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Paper,
  Alert,
  CircularProgress,
  Grid
} from '@mui/material';
import { useAuth } from '../../hooks/useAuth';
import interviewService from '../../services/interview.service';
import operatorService from '../../services/operator.service';

const initialFormState = {
  workflow: '',
  environment: '',
  tools_used: '',
  concerns_risks: '',
  safety_challenges: '',
  additional_notes: '',
  operator_id: ''
};

const InterviewForm = () => {
  const { id } = useParams(); // If id exists, we're editing an existing interview
  const isEditMode = !!id;
  const [formData, setFormData] = useState(initialFormState);
  const [operators, setOperators] = useState([]);
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(isEditMode);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  const navigate = useNavigate();
  const { user } = useAuth();

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch operators for dropdown
        const operatorsData = await operatorService.getOperators();
        setOperators(operatorsData);
        
        // If editing, fetch the interview data
        if (isEditMode) {
          const interviewData = await interviewService.getInterview(id);
          setFormData(interviewData);
        }
      } catch (error) {
        console.error('Error fetching initial data:', error);
        setError('Failed to load data. Please try again.');
      } finally {
        setInitialLoading(false);
      }
    };

    fetchData();
  }, [id, isEditMode]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.operator_id) {
      setError('Please select an operator');
      return;
    }
    
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      if (isEditMode) {
        await interviewService.updateInterview(id, formData);
        setSuccess('Interview updated successfully!');
      } else {
        await interviewService.createInterview(formData);
        setSuccess('Interview submitted successfully!');
        // Clear form after successful submission
        setFormData(initialFormState);
      }
    } catch (error) {
      console.error('Error submitting interview:', error);
      setError(error.response?.data?.detail || 'Failed to submit interview. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (initialLoading) {
    return (
      <Box display="flex" justifyContent="center" my={4}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {isEditMode ? 'Edit Interview' : 'New Interview'}
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      
      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {success}
        </Alert>
      )}
      
      <Paper sx={{ p: 3 }}>
        <Box component="form" onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            {/* Operator Selection */}
            <Grid item xs={12}>
              <FormControl fullWidth required>
                <InputLabel id="operator-label">Operator</InputLabel>
                <Select
                  labelId="operator-label"
                  id="operator_id"
                  name="operator_id"
                  value={formData.operator_id}
                  onChange={handleChange}
                  label="Operator"
                  disabled={loading}
                >
                  {operators.map((operator) => (
                    <MenuItem key={operator.operator_id} value={operator.operator_id}>
                      {operator.name} - {operator.role}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            {/* Workflow Field */}
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Workflow Description"
                name="workflow"
                multiline
                rows={4}
                value={formData.workflow}
                onChange={handleChange}
                placeholder="Describe the operator's daily workflow and processes..."
                disabled={loading}
              />
            </Grid>
            
            {/* Environment Field */}
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Work Environment"
                name="environment"
                multiline
                rows={4}
                value={formData.environment}
                onChange={handleChange}
                placeholder="Describe the operator's work environment, including machinery, software used..."
                disabled={loading}
              />
            </Grid>
            
            {/* Tools Used Field */}
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Tools Used"
                name="tools_used"
                multiline
                rows={4}
                value={formData.tools_used}
                onChange={handleChange}
                placeholder="List and describe the tools and technologies the operator uses..."
                disabled={loading}
              />
            </Grid>
            
            {/* Concerns/Risks Field */}
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Concerns and Risks"
                name="concerns_risks"
                multiline
                rows={4}
                value={formData.concerns_risks}
                onChange={handleChange}
                placeholder="Describe any concerns or risks the operator has mentioned..."
                disabled={loading}
              />
            </Grid>
            
            {/* Safety Challenges Field */}
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Safety Challenges"
                name="safety_challenges"
                multiline
                rows={4}
                value={formData.safety_challenges}
                onChange={handleChange}
                placeholder="Describe any safety challenges the operator faces..."
                disabled={loading}
              />
            </Grid>
            
            {/* Additional Notes Field */}
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Additional Notes"
                name="additional_notes"
                multiline
                rows={4}
                value={formData.additional_notes}
                onChange={handleChange}
                placeholder="Any other relevant information..."
                disabled={loading}
              />
            </Grid>
            
            {/* Form Buttons */}
            <Grid item xs={12}>
              <Box display="flex" justifyContent="flex-end" gap={2}>
                <Button
                  variant="outlined"
                  onClick={() => navigate(-1)}
                  disabled={loading}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  variant="contained"
                  disabled={loading}
                >
                  {loading ? <CircularProgress size={24} /> : (isEditMode ? 'Update Interview' : 'Submit Interview')}
                </Button>
              </Box>
            </Grid>
          </Grid>
        </Box>
      </Paper>
    </Box>
  );
};

export default InterviewForm; 