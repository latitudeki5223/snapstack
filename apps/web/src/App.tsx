import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import AdminLayout from './admin/AdminLayout';
import Dashboard from './admin/Dashboard';
import ParserStudio from './admin/ParserStudio';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Redirect root to admin */}
        <Route path="/" element={<Navigate to="/admin" replace />} />
        
        {/* Admin routes */}
        <Route path="/admin" element={<AdminLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="parser" element={<ParserStudio />} />
          <Route path="api-monitor" element={<ApiMonitorPlaceholder />} />
          <Route path="users" element={<UsersPlaceholder />} />
          <Route path="finance" element={<FinancePlaceholder />} />
          <Route path="settings" element={<SettingsPlaceholder />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

// Placeholder components
const ApiMonitorPlaceholder = () => (
  <div className="p-6">
    <h2 className="text-2xl font-bold mb-4">API Monitor</h2>
    <p className="text-gray-600">Coming soon...</p>
  </div>
);

const UsersPlaceholder = () => (
  <div className="p-6">
    <h2 className="text-2xl font-bold mb-4">User Management</h2>
    <p className="text-gray-600">Coming soon...</p>
  </div>
);

const FinancePlaceholder = () => (
  <div className="p-6">
    <h2 className="text-2xl font-bold mb-4">Finance Dashboard</h2>
    <p className="text-gray-600">Coming soon...</p>
  </div>
);

const SettingsPlaceholder = () => (
  <div className="p-6">
    <h2 className="text-2xl font-bold mb-4">Settings</h2>
    <p className="text-gray-600">Coming soon...</p>
  </div>
);

export default App;