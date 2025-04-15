import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Chat from './pages/Chat';
import KnowledgeBase from './pages/KnowledgeBase';
import Settings from './pages/Settings';
import './App.css'; // Keep or remove based on styling needs

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          {/* Redirect base path to /chat */}
          <Route index element={<Navigate to="/chat" replace />} /> 
          {/* Route for specific chat sessions */}
          <Route path="chat/:conversationId" element={<Chat />} />
          {/* Route for starting a new chat (will likely redirect in Layout/Chat) */}
          <Route path="chat" element={<Chat />} /> 
          <Route path="knowledge-base" element={<KnowledgeBase />} />
          <Route path="settings" element={<Settings />} />
          {/* Add other routes here if needed */}
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
