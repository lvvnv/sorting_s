import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ResultPage from '../pages/ClassificationResultPage';

const AppRoutes = () => (
  <Router>
    <Routes>
      <Route path="/classify/result" element={<ResultPage />} />
    </Routes>
  </Router>
);

export default AppRoutes;
