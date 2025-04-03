import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import {
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  Typography,
  Box
} from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import PeopleIcon from '@mui/icons-material/People';
import QuestionAnswerIcon from '@mui/icons-material/QuestionAnswer';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { isAdmin } = useAuth();

  const menuItems = [
    {
      text: 'Dashboard',
      icon: <DashboardIcon />,
      path: '/',
      adminOnly: false
    },
    {
      text: 'Operators',
      icon: <PeopleIcon />,
      path: '/operators',
      adminOnly: false
    },
    {
      text: 'Interviews',
      icon: <QuestionAnswerIcon />,
      path: '/interviews',
      adminOnly: false
    },
    {
      text: 'Analyses',
      icon: <AnalyticsIcon />,
      path: '/analyses',
      adminOnly: false
    },
    // Admin section could be expanded
    {
      text: 'Admin Panel',
      icon: <AdminPanelSettingsIcon />,
      path: '/admin',
      adminOnly: true
    }
  ];

  return (
    <>
      <Box sx={{ p: 2 }}>
        <Typography variant="subtitle2" color="text.secondary">
          MAIN NAVIGATION
        </Typography>
      </Box>
      <List>
        {menuItems.map((item) => {
          // Skip admin items for non-admin users
          if (item.adminOnly && !isAdmin) {
            return null;
          }

          return (
            <ListItem key={item.text} disablePadding>
              <ListItemButton
                selected={location.pathname === item.path}
                onClick={() => navigate(item.path)}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItemButton>
            </ListItem>
          );
        })}
      </List>
      
      <Divider sx={{ my: 2 }} />
      
      <Box sx={{ p: 2 }}>
        <Typography variant="body2" color="text.secondary">
          v1.0.0
        </Typography>
      </Box>
    </>
  );
};

export default Sidebar; 