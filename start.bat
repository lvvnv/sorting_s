@echo off
REM start.bat
REM Script to start the application with Docker on Windows

echo Starting the waste sorting application...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed. Please install Docker Desktop first.
    exit /b 1
)

REM Check if docker-compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo Error: docker-compose is not installed. Please install Docker Desktop which includes docker-compose.
    exit /b 1
)

REM Build and start the services
echo Building and starting services...
docker-compose up --build -d

REM Wait a moment for services to start
timeout /t 10 /nobreak >nul

REM Check if services are running
docker ps | findstr "sorting_s_backend_1" >nul
if errorlevel 1 (
    echo Warning: Backend service may not be running properly
) else (
    echo Backend service is running on http://localhost:8000
)

docker ps | findstr "sorting_s_frontend_1" >nul
if errorlevel 1 (
    echo Warning: Frontend service may not be running properly
) else (
    echo Frontend service is running on http://localhost:3000
)

echo.
echo You can access the application at:
echo   Frontend: http://localhost:3000
echo   Backend API: http://localhost:8000/api/
echo.
echo To stop the services, run: docker-compose down