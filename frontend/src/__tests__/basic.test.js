import React from 'react';
import { render, screen } from '@testing-library/react';

// A very simple test to verify the testing environment is working
test('basic test environment works', () => {
  expect(1 + 1).toBe(2);
});

// A simple component test
const SimpleComponent = () => <div>Hello World</div>;

test('renders simple component', () => {
  render(<SimpleComponent />);
  expect(screen.getByText('Hello World')).toBeInTheDocument();
});