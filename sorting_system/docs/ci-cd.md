# CI/CD Pipeline Documentation

## Overview

This project uses GitHub Actions for Continuous Integration and Continuous Deployment (CI/CD). The pipeline automates testing, building, and deployment processes to ensure code quality and reliability.

## Workflow Files

### 1. Django CI (`django.yml`)
- **Trigger**: Push or pull request to main/develop branches
- **Purpose**: Test Django backend with multiple Python versions
- **Stages**:
  1. Setup Python environment
  2. Install dependencies
  3. Run Django migrations
  4. Execute backend tests

### 2. Sorting System CI/CD (`ci-cd.yml`)
- **Trigger**: Push or pull request to main/develop branches
- **Purpose**: Comprehensive CI/CD pipeline for both frontend and backend
- **Stages**:
  1. Backend testing
  2. Frontend testing
  3. Build and deployment preparation

## Pipeline Stages

### 1. Setup Phase
- Checkout repository code
- Setup Python environment (3.10)
- Setup Node.js environment (18.x)
- Install system dependencies

### 2. Backend Testing
- Install Python dependencies from `requirements.txt`
- Setup Django environment with test settings
- Run Django database migrations
- Execute Django tests using `python manage.py test`

### 3. Frontend Testing
- Install Node.js dependencies with `npm ci`
- Run frontend tests with `npm test`

### 4. Build Phase
- Build frontend application with `npm run build`
- Prepare backend for deployment
- Package artifacts for deployment

## Environment Variables

The pipeline uses the following environment variables:

```bash
SECRET_KEY=django-insecure-test-key-for-ci
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

These are automatically set in the CI environment and do not require secrets.

## Dependencies

### Backend Dependencies
- Python 3.10
- Django 5.2+
- PyTorch (CPU version for CI speed)
- OpenCV (headless version)
- Pillow
- NumPy

### Frontend Dependencies
- Node.js 18.x
- React 18+
- Testing Library
- Jest

## Test Execution

### Backend Tests
```bash
cd sorting_system
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test -- --watchAll=false
```

## Artifacts

The pipeline generates the following artifacts:
1. **Frontend build** - Compiled React application
2. **Backend application** - Django application ready for deployment

## Deployment

Deployment steps are prepared but not automatically executed. The artifacts are uploaded and can be deployed manually or through additional deployment workflows.

## Troubleshooting

### Common Issues

1. **Dependency Installation Failures**
   - Check `requirements.txt` for incompatible versions
   - Ensure PyTorch CPU version is used for faster builds

2. **Database Migration Errors**
   - Verify Django settings in CI environment
   - Check that all apps are properly registered in `INSTALLED_APPS`

3. **Test Failures**
   - Run tests locally with same environment
   - Check for race conditions in tests
   - Ensure test database isolation

### Debugging CI Issues

1. Enable verbose logging:
   ```bash
   python manage.py test --verbosity=2
   ```

2. Check Django configuration:
   ```bash
   python manage.py check
   ```

3. Verify database connectivity:
   ```bash
   python manage.py migrate --dry-run
   ```

## Customization

To customize the pipeline:

1. **Add new Python versions**: Modify the `python-version` matrix
2. **Add new Node.js versions**: Modify the `node-version` in setup steps
3. **Add new test stages**: Create additional jobs in the workflow files
4. **Add deployment steps**: Extend the build-and-deploy job with deployment commands

## Security Considerations

- No secrets are required for test environment
- Dependencies are pinned to specific versions
- PyTorch CPU version reduces attack surface
- All dependencies are regularly updated