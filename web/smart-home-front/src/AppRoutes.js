import React from 'react';
import { Devices } from './components/Devices';
import { Home } from './components/Home';
import { Routes, Route, Navigate } from 'react-router-dom';

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/home" />} />
      <Route path="/devices/:id" element={<Devices />} />
      <Route path="/home" element={<Home />} />
      {/* Add more routes if needed */}
    </Routes>
  );
};  

export default AppRoutes;
