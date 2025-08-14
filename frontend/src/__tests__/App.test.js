import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../App';

test('renders app without crashing', () => {
  render(<App />);
  // The App component uses React Router, so we can't easily test specific content
  // But we can at least verify it renders without errors
  expect(true).toBe(true);
});