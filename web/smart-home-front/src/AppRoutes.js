import React from 'react';
import { Devices } from './components/Devices';
import { Routes, Route, Navigate } from 'react-router-dom';

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/devices/PI1" />} />
      <Route path="/devices/:id" element={<Devices />} />
      {/* Add more routes if needed */}
    </Routes>
  );
};  

export default AppRoutes;
