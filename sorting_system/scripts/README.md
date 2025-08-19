# CI/CD Scripts

This directory contains scripts to help validate and test the CI/CD setup locally.

## Scripts

### 1. ci-validate.sh
A bash script to validate the CI setup on Unix-like systems (Linux, macOS).

**Usage:**
```bash
./ci-validate.sh
```

### 2. ci-validate.bat
A Windows batch script to validate the CI setup on Windows.

**Usage:**
```cmd
ci-validate.bat
```

## What the Scripts Check

1. **Project Structure**
   - Verifies the presence of required directories (`sorting_system`, `frontend`)

2. **Backend Validation**
   - Checks Python availability
   - Verifies `requirements.txt` exists
   - Confirms Django is available
   - Validates Django configuration with `manage.py check`

3. **Frontend Validation**
   - Checks Node.js availability
   - Verifies `package.json` exists
   - Confirms `node_modules` directory (if dependencies are installed)

## Running Locally

To validate your local development environment before pushing changes:

### On Linux/macOS:
```bash
./scripts/ci-validate.sh
```

### On Windows:
```cmd
scripts\ci-validate.bat
```

## Running Tests Locally

### Backend Tests:
```bash
cd sorting_system
python manage.py test
```

### Frontend Tests:
```bash
cd frontend
npm test -- --watchAll=false
```

## CI Pipeline

The GitHub Actions pipelines automatically run these validations on every push or pull request to the main branches. You can find the workflow files in `.github/workflows/`.