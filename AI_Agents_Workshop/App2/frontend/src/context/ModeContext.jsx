import React, { createContext, useState, useContext } from 'react';

const ModeContext = createContext();

export const useMode = () => useContext(ModeContext);

export const ModeProvider = ({ children }) => {
  // Default to 'cloud' or read from localStorage if persisted
  const [mode, setMode] = useState(localStorage.getItem('appMode') || 'cloud');

  const changeMode = (newMode) => {
    if (newMode === 'cloud' || newMode === 'local') {
      setMode(newMode);
      localStorage.setItem('appMode', newMode); // Persist selection
      // Potentially notify backend or reload parts of the app if needed
      console.log(`Switched mode to: ${newMode}`);
    }
  };

  return (
    <ModeContext.Provider value={{ mode, changeMode }}>
      {children}
    </ModeContext.Provider>
  );
}; 