# Frontend Testing

This directory contains unit tests for the frontend components.

## Running Tests

To run all tests once:
```bash
npm test -- --watchAll=false
```

To run tests in watch mode:
```bash
npm test
```

## Test Structure

- `src/App.test.js` - Tests for the main App component
- `src/__tests__/App.test.js` - Additional tests for the App component
- `src/__tests__/basic.test.js` - Basic sanity tests to verify the testing environment

## Adding New Tests

1. Create new test files in the `src/__tests__` directory
2. Follow the naming convention: `[ComponentName].test.js`
3. Use Jest and React Testing Library for writing tests
4. Run tests to ensure they pass before committing

## Test Coverage

Currently, we have basic tests to verify the testing environment is working. More comprehensive tests for individual components can be added as needed.