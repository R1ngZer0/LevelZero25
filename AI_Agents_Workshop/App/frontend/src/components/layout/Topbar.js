import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import {
  Button,
  IconButton,
  Avatar,
  Menu,
  MenuItem,
  Divider,
  Typography,
  Box
} from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';

const Topbar = () => {
  const { user, logout } = useAuth();
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    handleClose();
    logout();
  };

  // Generate initial from username or email
  const getInitial = () => {
    if (!user) return 'U';
    
    if (user.username) {
      return user.username.charAt(0).toUpperCase();
    }
    
    if (user.email) {
      return user.email.charAt(0).toUpperCase();
    }
    
    return 'U';
  };

  return (
    <Box>
      <IconButton
        onClick={handleClick}
        size="small"
        aria-controls={open ? 'account-menu' : undefined}
        aria-haspopup="true"
        aria-expanded={open ? 'true' : undefined}
        color="inherit"
      >
        <Avatar sx={{ width: 32, height: 32, bgcolor: 'secondary.main' }}>
          {getInitial()}
        </Avatar>
      </IconButton>
      
      <Menu
        anchorEl={anchorEl}
        id="account-menu"
        open={open}
        onClose={handleClose}
        onClick={handleClose}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        {user && (
          <Box sx={{ px: 2, py: 1 }}>
            <Typography variant="subtitle1">{user.username}</Typography>
            <Typography variant="body2" color="text.secondary">
              {user.role === 'admin' ? 'Administrator' : 'Operator'}
            </Typography>
          </Box>
        )}
        <Divider />
        <MenuItem onClick={handleClose}>
          <AccountCircleIcon fontSize="small" sx={{ mr: 1.5 }} />
          My Profile
        </MenuItem>
        <MenuItem onClick={handleLogout}>
          <ExitToAppIcon fontSize="small" sx={{ mr: 1.5 }} />
          Logout
        </MenuItem>
      </Menu>
    </Box>
  );
};

export default Topbar; 