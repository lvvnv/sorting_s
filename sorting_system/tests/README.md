# Backend Testing

This directory contains unit tests for the Django backend application.

## Test Structure

The tests are organized by Django app:

- `api/tests.py` - Tests for API endpoints and views
- `api/tests_serializers.py` - Tests for API serializers
- `core/tests.py` - Tests for core models
- `classification/tests.py` - Tests for classification models
- `detection/tests.py` - Tests for detection models

## Running Tests

To run all tests:
```bash
python manage.py test
```

To run tests for a specific app:
```bash
python manage.py test api
python manage.py test core
python manage.py test classification
python manage.py test detection
```

To run specific test files:
```bash
python manage.py test api.tests
python manage.py test api.tests_serializers
```

## Test Coverage

Current tests cover:

1. **API Endpoint Tests**:
   - GET requests return proper HTTP status codes
   - POST requests with missing data return 400 errors
   - DELETE requests with non-existent IDs return 500 errors (due to current implementation)

2. **Model Tests**:
   - Creation and storage of UploadedImage objects
   - Creation and storage of ClassificationResult objects
   - Creation and storage of DetectionResult objects

3. **Serializer Tests**:
   - Instantiation of all serializer classes

## Writing New Tests

1. Add new test methods to the existing test classes
2. Follow the naming convention: `test_[what_you_are_testing]`
3. Use descriptive method names that explain what is being tested
4. Include assertions to verify expected behavior
5. Use mocks where necessary to isolate units of code

## Test Database

Tests run against a temporary test database that is created and destroyed for each test run. This ensures test isolation and prevents tests from affecting each other.