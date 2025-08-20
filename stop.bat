@echo off
REM stop.bat
REM Script to stop the application on Windows

echo Stopping the waste sorting application...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed.
    exit /b 1
)

REM Stop the services
echo Stopping services...
docker-compose down

echo Services have been stopped.