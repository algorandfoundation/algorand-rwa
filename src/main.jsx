import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';

// Set a default theme on first load; can be toggled later if needed
if (!document.documentElement.dataset.theme) {
  document.documentElement.dataset.theme = 'dark';
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
