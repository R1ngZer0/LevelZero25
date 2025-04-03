import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Grid,
  Paper,
  Typography,
  Button,
  Box,
  Card,
  CardContent,
  CardActions,
  CircularProgress
} from '@mui/material';
import PeopleIcon from '@mui/icons-material/People';
import QuestionAnswerIcon from '@mui/icons-material/QuestionAnswer';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import AddIcon from '@mui/icons-material/Add';

import operatorService from '../../services/operator.service';
import interviewService from '../../services/interview.service';
import analysisService from '../../services/analysis.service';
import { useAuth } from '../../hooks/useAuth';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    operators: 0,
    interviews: 0,
    analyses: 0,
    recentInterviews: [],
    recentAnalyses: []
  });
  const { isAdmin } = useAuth();

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Get counts
        const operators = await operatorService.getOperators();
        const interviews = await interviewService.getInterviews();
        const analyses = await analysisService.getAnalyses();
        
        // Get recent data (last 5)
        const recentInterviews = interviews.slice(0, 5);
        const recentAnalyses = analyses.slice(0, 5);
        
        setStats({
          operators: operators.length,
          interviews: interviews.length,
          analyses: analyses.length,
          recentInterviews,
          recentAnalyses
        });
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" my={4}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Dashboard</Typography>
        {isAdmin && (
          <Button
            variant="contained"
            color="primary"
            startIcon={<AddIcon />}
            component={Link}
            to="/interviews/new"
          >
            New Interview
          </Button>
        )}
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={4}>
          <Paper
            elevation={2}
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              bgcolor: 'primary.light',
              color: 'white'
            }}
          >
            <PeopleIcon sx={{ fontSize: 48, mb: 1 }} />
            <Typography variant="h4">{stats.operators}</Typography>
            <Typography variant="subtitle1">Operators</Typography>
          </Paper>
        </Grid>
        
        <Grid item xs={12} sm={4}>
          <Paper
            elevation={2}
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              bgcolor: 'secondary.light',
              color: 'white'
            }}
          >
            <QuestionAnswerIcon sx={{ fontSize: 48, mb: 1 }} />
            <Typography variant="h4">{stats.interviews}</Typography>
            <Typography variant="subtitle1">Interviews</Typography>
          </Paper>
        </Grid>
        
        <Grid item xs={12} sm={4}>
          <Paper
            elevation={2}
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              bgcolor: 'success.light',
              color: 'white'
            }}
          >
            <AnalyticsIcon sx={{ fontSize: 48, mb: 1 }} />
            <Typography variant="h4">{stats.analyses}</Typography>
            <Typography variant="subtitle1">Analyses</Typography>
          </Paper>
        </Grid>
      </Grid>

      {/* Recent Activity */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Typography variant="h6" gutterBottom>
            Recent Interviews
          </Typography>
          
          {stats.recentInterviews.length === 0 ? (
            <Paper sx={{ p: 2, bgcolor: 'background.paper' }}>
              <Typography variant="body1">No interviews found</Typography>
            </Paper>
          ) : (
            stats.recentInterviews.map((interview) => (
              <Card 
                key={interview.interview_id} 
                sx={{ mb: 2, bgcolor: 'background.paper' }}
              >
                <CardContent>
                  <Typography variant="h6">
                    {interview.operator?.name || 'Unknown Operator'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {new Date(interview.created_at).toLocaleDateString()}
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button 
                    size="small" 
                    component={Link} 
                    to={`/interviews/${interview.interview_id}`}
                  >
                    View Details
                  </Button>
                </CardActions>
              </Card>
            ))
          )}
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Typography variant="h6" gutterBottom>
            Recent Analyses
          </Typography>
          
          {stats.recentAnalyses.length === 0 ? (
            <Paper sx={{ p: 2, bgcolor: 'background.paper' }}>
              <Typography variant="body1">No analyses found</Typography>
            </Paper>
          ) : (
            stats.recentAnalyses.map((analysis) => (
              <Card 
                key={analysis.analysis_id} 
                sx={{ mb: 2, bgcolor: 'background.paper' }}
              >
                <CardContent>
                  <Typography variant="subtitle1">
                    {analysis.analysis_type === 'individual'
                      ? 'Individual Analysis'
                      : 'Cross-Section Analysis'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {new Date(analysis.created_at).toLocaleDateString()}
                  </Typography>
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    {analysis.summary?.substring(0, 100)}
                    {analysis.summary?.length > 100 ? '...' : ''}
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button 
                    size="small" 
                    component={Link} 
                    to={`/analyses/${analysis.analysis_id}`}
                  >
                    View Full Analysis
                  </Button>
                </CardActions>
              </Card>
            ))
          )}
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 