@echo off
REM ci-validate.bat
REM Script to validate CI setup locally on Windows

echo Validating CI setup locally...

REM Check if we're in the right directory
if not exist "sorting_system" (
    echo Error: sorting_system directory not found
    exit /b 1
)

if not exist "frontend" (
    echo Error: frontend directory not found
    exit /b 1
)

echo ✓ Project directory structure verified

REM Test backend setup
echo Testing backend setup...
cd sorting_system

REM Check Python availability
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found
    exit /b 1
)

echo ✓ Python available

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo Error: requirements.txt not found
    exit /b 1
)

echo ✓ requirements.txt found

REM Test Django setup
python -c "import django" >nul 2>&1
if errorlevel 1 (
    echo Warning: Django not installed. Please install dependencies.
) else (
    echo ✓ Django available
)

REM Check if manage.py exists
if not exist "manage.py" (
    echo Error: manage.py not found
    exit /b 1
)

echo ✓ manage.py found

REM Try to run Django check
python manage.py check >nul 2>&1
if errorlevel 1 (
    echo Warning: Django configuration check failed
) else (
    echo ✓ Django configuration valid
)

echo Backend validation completed.

REM Test frontend setup
echo Testing frontend setup...
cd ..\frontend

REM Check if package.json exists
if not exist "package.json" (
    echo Error: package.json not found
    exit /b 1
)

echo ✓ package.json found

REM Check Node.js availability
node --version >nul 2>&1
if errorlevel 1 (
    echo Warning: Node.js not found. Frontend tests will not run.
) else (
    echo ✓ Node.js available
    
    REM Check if node_modules exists
    if exist "node_modules" (
        echo ✓ node_modules directory found
    ) else (
        echo Info: node_modules not found. Run 'npm install' to install dependencies.
    )
)

echo Frontend validation completed.

cd ..

echo CI validation completed successfully!
echo.
echo To run the full CI pipeline locally:
echo 1. Backend tests: cd sorting_system ^&^& python manage.py test
echo 2. Frontend tests: cd frontend ^&^& npm test
echo.
echo For GitHub Actions, push your changes to trigger the CI pipeline.