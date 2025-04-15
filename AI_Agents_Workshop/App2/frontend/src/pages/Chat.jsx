// Placeholder for the Chat page
import React, { useState, useEffect, useRef } from 'react';
import {
  Typography,
  Box,
  TextField,
  Button,
  Paper,
  CircularProgress,
  Alert,
  List,
  ListItem,
  ListItemText,
  Avatar,
  Divider,
  Snackbar
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import PersonIcon from '@mui/icons-material/Person';
import SmartToyIcon from '@mui/icons-material/SmartToy'; // Icon for AI
import CreateIcon from '@mui/icons-material/Create'; // Icon for Create Document
import { useParams, useNavigate } from 'react-router-dom'; // Import useParams and useNavigate
import { v4 as uuidv4 } from 'uuid'; // Import uuid
import { getConversationMessages, sendMessage, createDocument } from '../services/api'; // Import specific API functions
import { useMode } from '../context/ModeContext';

function Chat() {
  const { conversationId: conversationIdFromUrl } = useParams(); // Get ID from URL
  const navigate = useNavigate();
  const [currentConversationId, setCurrentConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false); // For messages list loading
  const [sending, setSending] = useState(false); // For sending message state
  const [error, setError] = useState(null);
  const [docPrompt, setDocPrompt] = useState(''); // State for document prompt
  const [docCreating, setDocCreating] = useState(false); // State for doc creation loading
  const [docError, setDocError] = useState(null); // State for doc creation error
  const [snackbarOpen, setSnackbarOpen] = useState(false); // State for feedback snackbar
  const [snackbarMessage, setSnackbarMessage] = useState(''); // State for feedback message
  const { mode } = useMode();
  const messagesEndRef = useRef(null); // Ref to scroll to bottom

  // Effect to handle conversation ID changes from URL
  useEffect(() => {
    const validId = conversationIdFromUrl || uuidv4(); // Use URL ID or generate new one
    if (conversationIdFromUrl) {
        console.log(`Loading conversation: ${conversationIdFromUrl}`);
        setCurrentConversationId(conversationIdFromUrl);
        fetchMessages(conversationIdFromUrl);
    } else {
        // If no ID in URL, navigate to the new chat URL
        console.log(`No conversation ID in URL, starting new chat: ${validId}`);
        navigate(`/chat/${validId}`, { replace: true }); 
        setCurrentConversationId(validId);
        setMessages([]); // Start with empty messages for new chat
        setLoading(false);
        setError(null);
    }
  }, [conversationIdFromUrl, navigate]); // Re-run when URL ID changes

  // Function to fetch messages for the current conversation
  const fetchMessages = async (id) => {
    setLoading(true);
    setError(null);
    try {
      const response = await getConversationMessages(id);
      // Assuming response.data is the ConversationDetailOutput schema
      setMessages(response.data.messages || []); 
    } catch (err) {
      // Handle 404 specifically: It means a new chat or invalid ID
      if (err.response && err.response.status === 404) {
        console.log(`Conversation ${id} not found (or is new), starting empty.`);
        setMessages([]); // Treat as empty chat
        setError(null); // Ensure no error is shown for 404
      } else {
        // Handle other errors as before
        console.error(`Error fetching messages for ${id}:`, err);
        setError(`Failed to load messages: ${err.response?.data?.detail || err.message}`);
        setMessages([]); // Clear messages on error
      }
    } finally {
      setLoading(false);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim() || !currentConversationId || sending) return;

    const userMessage = { 
        id: Date.now(), // Temporary client-side ID for key prop
        role: 'user', 
        content: input, 
        conversation_id: currentConversationId, 
        created_at: new Date().toISOString()
    };
    // Optimistically add user message
    setMessages((prevMessages) => [...prevMessages, userMessage]); 
    const messageToSend = input;
    setInput('');
    setSending(true); // Use separate state for sending operation
    setError(null);

    try {
        // Call the updated API service function
        const response = await sendMessage(currentConversationId, messageToSend, mode);
      
        // Create assistant message object matching schema (assuming response.data is AssistantMessageOutput)
        const assistantMessage = { 
            id: Date.now() + 1, // Temporary client-side ID
            role: 'assistant', 
            content: response.data.content, 
            conversation_id: currentConversationId, 
            created_at: new Date().toISOString()
        };
        
        // Replace optimistic user message with potential DB ID later if needed,
        // For now, just append the assistant response
        setMessages((prevMessages) => [...prevMessages, assistantMessage]);

        // Optionally, refetch messages to get server-generated IDs/timestamps?
        // fetchMessages(currentConversationId);

    } catch (err) {
      console.error("Error sending message:", err);
      setError(`Failed to send message: ${err.response?.data?.detail || err.message}`);
      // Remove the optimistically added user message on error
      setMessages((prevMessages) => prevMessages.filter(msg => msg.id !== userMessage.id));
    } finally {
      setSending(false);
    }
  };

  const handleInputChange = (event) => {
    setInput(event.target.value);
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  // --- Document Creation Logic ---
  const handleDocPromptChange = (event) => {
    setDocPrompt(event.target.value);
  };

  const handleCreateDocument = async () => {
    if (!docPrompt.trim()) return;
    setDocCreating(true);
    setDocError(null);
    setSnackbarMessage('');
    try {
      // Use the imported createDocument function
      const response = await createDocument(docPrompt, mode);
      setSnackbarMessage(response.data.message || 'Document created successfully!');
      setSnackbarOpen(true);
      setDocPrompt('');
    } catch (err) {
      console.error("Error creating document:", err);
      setDocError(`Failed to create document: ${err.response?.data?.detail || err.message}`);
    } finally {
      setDocCreating(false);
    }
  };

  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setSnackbarOpen(false);
  };
  // --- End Document Creation Logic ---

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 64px - 48px)', /* Adjust based on layout padding */ }}>
      <Typography variant="h4" gutterBottom sx={{ p: 2, pb: 0 }}>
        Chat {currentConversationId ? `(${currentConversationId.substring(0, 8)}...)` : '(New)'}
      </Typography>

      {/* Message Display Area */}
      <Box
        sx={{
          flexGrow: 1,
          overflowY: 'auto',
          p: 2,
          mb: 2,
          border: '1px solid',
          borderColor: 'divider',
          borderRadius: 1
        }}
      >
        {loading && <CircularProgress sx={{ display: 'block', mx: 'auto' }} />}
        {error && <Alert severity="error" sx={{ m: 1 }}>{error}</Alert>}
        {!loading && (
          <List>
            {messages.map((msg, index) => (
              // Use msg.id from DB if available, otherwise index or temp ID
              <ListItem key={msg.id || index} sx={{ py: 1, display: 'flex', alignItems: 'flex-start' }}> 
                <Avatar sx={{ bgcolor: msg.role === 'user' ? 'primary.main' : 'secondary.main', mr: 1.5 }}>
                  {msg.role === 'user' ? <PersonIcon /> : <SmartToyIcon />}
                </Avatar>
                <ListItemText
                  primary={msg.content}
                  // secondary={new Date(msg.created_at).toLocaleTimeString()} // Optional: Show time
                  sx={{
                    bgcolor: msg.role === 'user' ? 'grey.200' : 'grey.100',
                    p: 1.5,
                    borderRadius: 2,
                    maxWidth: '80%',
                    wordBreak: 'break-word',
                    ml: msg.role === 'assistant' ? 0 : 'auto',
                    mr: msg.role === 'user' ? 0 : 'auto',
                  }}
                />
              </ListItem>
            ))}
            {/* Sending indicator (subtle) */}
            {sending && (
              <ListItem sx={{ justifyContent: 'center', opacity: 0.6 }}>
                <CircularProgress size={20} />
              </ListItem>
            )}
            <div ref={messagesEndRef} />
          </List>
        )}
      </Box>

      {/* Input Area */}
      <Paper elevation={3} sx={{ p: 2, mt: 'auto', display: 'flex', alignItems: 'center' }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Type your message..."
          value={input}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          disabled={sending || loading} // Disable if loading history or sending
          multiline
          maxRows={4} // Allow multi-line input up to 4 rows
          sx={{ mr: 1 }}
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleSendMessage}
          disabled={sending || loading || !input.trim() || !currentConversationId} // Disable if no ID
          endIcon={sending ? <CircularProgress size={20} color="inherit"/> : <SendIcon />}
        >
          {sending ? 'Sending...' : 'Send'}
        </Button>
      </Paper>

      {/* --- Input Areas Container --- */}
      <Paper elevation={3} sx={{ mt: 'auto' }}>
        {/* Document Creation Input Area */}
        <Box sx={{ p: 2 }}>
          <Typography variant="subtitle1" gutterBottom>Create Document</Typography>
          {docError && (
            <Alert severity="error" sx={{ mb: 1 }}>{docError}</Alert>
          )}
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
             <TextField
               fullWidth
               variant="outlined"
               placeholder="Enter prompt for document creation..."
               value={docPrompt}
               onChange={handleDocPromptChange}
               disabled={docCreating}
               multiline
               rows={2} // Start with 2 rows
               sx={{ mr: 1 }}
             />
             <Button
               variant="contained"
               color="secondary"
               onClick={handleCreateDocument}
               disabled={docCreating || !docPrompt.trim()}
               endIcon={docCreating ? <CircularProgress size={20} color="inherit"/> : <CreateIcon />}
               sx={{ height: 'fit-content'}} // Align button height with TextField
             >
               {docCreating ? 'Creating...' : 'Create'}
             </Button>
           </Box>
        </Box>
      </Paper>
       {/* --- End Input Areas Container --- */}

       {/* Feedback Snackbar */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={6000} // Hide after 6 seconds
        onClose={handleSnackbarClose}
        message={snackbarMessage}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      />
    </Box>
  );
}

export default Chat; 