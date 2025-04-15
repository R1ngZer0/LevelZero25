import React, { useState, useEffect } from 'react';
import { Link as RouterLink, Outlet, useNavigate, useLocation } from 'react-router-dom';
import { 
    AppBar, Box, CssBaseline, Drawer, List, ListItem, ListItemButton, 
    ListItemIcon, ListItemText, Toolbar, Typography, Button, Divider, 
    CircularProgress, Alert 
} from '@mui/material';
import ChatIcon from '@mui/icons-material/Chat';
import FolderIcon from '@mui/icons-material/Folder';
import SettingsIcon from '@mui/icons-material/Settings';
import AddCommentIcon from '@mui/icons-material/AddComment';
import ForumIcon from '@mui/icons-material/Forum';
import { v4 as uuidv4 } from 'uuid';
import { getConversations } from '../services/api';

const drawerWidth = 240;

function Layout() {
  const navigate = useNavigate();
  const location = useLocation();
  const [conversations, setConversations] = useState([]);
  const [loadingConvos, setLoadingConvos] = useState(false);
  const [errorConvos, setErrorConvos] = useState(null);

  const fetchConversations = async () => {
    setLoadingConvos(true);
    setErrorConvos(null);
    try {
      const response = await getConversations();
      setConversations(response.data || []);
    } catch (err) {
      console.error("Error fetching conversations:", err);
      setErrorConvos("Failed to load conversations.");
    } finally {
      setLoadingConvos(false);
    }
  };

  useEffect(() => {
    fetchConversations();
  }, []);

  const handleNewChat = () => {
    const newChatId = uuidv4();
    navigate(`/chat/${newChatId}`);
  };

  const menuItems = [
    { text: 'Knowledge Base', icon: <FolderIcon />, path: '/knowledge-base' },
    { text: 'Settings', icon: <SettingsIcon />, path: '/settings' },
  ];

  const currentPath = location.pathname;
  const activeConversationId = currentPath.startsWith('/chat/') 
      ? currentPath.split('/chat/')[1] 
      : null;

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{ width: `calc(100% - ${drawerWidth}px)`, ml: `${drawerWidth}px` }}
      >
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            Multi-Agent AI App
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
        variant="permanent"
        anchor="left"
      >
        <Toolbar />
        <List>
          {menuItems.map((item) => (
            <ListItem key={item.text} disablePadding>
              <ListItemButton component={RouterLink} to={item.path}>
                <ListItemIcon>
                  {item.icon}
                </ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>

        <Divider sx={{ my: 1 }}/>

        <Box sx={{ px: 2, py: 1 }}>
          <Button 
            fullWidth 
            variant="contained" 
            startIcon={<AddCommentIcon />} 
            onClick={handleNewChat}
          >
            New Chat
          </Button>
        </Box>

        <Divider sx={{ my: 1 }}/>

        <Typography variant="overline" sx={{ px: 2, mt: 1 }}>Conversations</Typography>
        {loadingConvos && <CircularProgress size={20} sx={{ mx: 'auto', display:'block'}}/>}
        {errorConvos && <Alert severity="error" sx={{ mx: 2 }}>{errorConvos}</Alert>}
        <List sx={{ overflowY: 'auto'}}> 
          {conversations.map((convo) => (
            <ListItem key={convo.id} disablePadding>
              <ListItemButton 
                component={RouterLink} 
                to={`/chat/${convo.id}`}
                selected={activeConversationId === convo.id}
              >
                <ListItemIcon>
                  <ForumIcon fontSize="small"/>
                </ListItemIcon>
                <ListItemText 
                    primary={`Chat ${convo.id.substring(0, 8)}...`}
                    secondary={new Date(convo.created_at).toLocaleString()} 
                    primaryTypographyProps={{ sx: { overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' } }}/>
              </ListItemButton>
            </ListItem>
          ))}
          {conversations.length === 0 && !loadingConvos && !errorConvos && (
             <ListItem>
               <ListItemText secondary="No past conversations found." />
             </ListItem>
          )}
        </List>

      </Drawer>
      <Box
        component="main"
        sx={{ flexGrow: 1, bgcolor: 'background.default', p: 3, marginTop: '64px' /* Height of AppBar */ }}
      >
        <Outlet />
      </Box>
    </Box>
  );
}

export default Layout; 