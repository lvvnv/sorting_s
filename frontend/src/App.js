// frontend/src/App.js
import React from 'react';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import ClassificationUploadPage from './pages/ClassificationUploadPage';
import ClassificationResultPage from './pages/ClassificationResultPage';
import ErrorPage from './pages/ErrorPage';
import NoDetectionsPage from './pages/NoDetectionsPage';
import DetectionUploadPage from './pages/DetectionUploadPage';
import DetectionResultPage from './pages/DetectionResultPage';

import { createBrowserRouter, RouterProvider } from 'react-router-dom';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: "about", element: <AboutPage /> },
      { path: "classify", element: <ClassificationUploadPage /> },
      { path: "classify/result", element: <ClassificationResultPage /> },
      { path: "detect", element: <DetectionUploadPage />},
      { path: "detect/results", element: <DetectionResultPage />},
      { path: "error", element: <ErrorPage /> },
      { path: "no-detections", element: <NoDetectionsPage /> }
    ]
  }
], {
  future: {
    v7_relativeSplatPath: true,
    v7_startTransition: true
  }
});

function App() {
  return <RouterProvider router={router} />;
}

export default App;
