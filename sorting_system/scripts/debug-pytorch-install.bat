@echo off
REM debug-pytorch-install.bat
REM Script to debug PyTorch installation issues on Windows

echo Debugging PyTorch Installation Issues
echo =====================================

REM Check Python version
echo Checking Python version...
python --version

REM Check current torch installation
echo.
echo Checking current torch installation...
pip list | findstr torch

REM Attempt to install PyTorch CPU version
echo.
echo Attempting to install PyTorch CPU version...
pip install torch==2.0.1+cpu torchvision==0.15.2+cpu -f https://download.pytorch.org/whl/torch_stable.html

echo.
echo Installation attempt completed.
echo If you still have issues, try:
echo 1. Checking if the exact version exists in the repository
echo 2. Using a different PyTorch version that is available
echo 3. Installing without the +cpu suffix if needed