
import React from 'react';
import ReactDOM from 'react-dom/client'; // Updated import for React 18
import App from './App';
import '../css/main.css'; // Import your CSS file here

// Create a root element and render the App component
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
