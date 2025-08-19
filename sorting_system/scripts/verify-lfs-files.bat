@echo off
REM verify-lfs-files.bat
REM Script to verify Git LFS files are properly downloaded (Windows version)

echo Verifying Git LFS Files
echo =======================

REM Check if git-lfs is installed
git-lfs --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: git-lfs is not installed
    echo This may cause issues with large file handling
) else (
    echo ✓ git-lfs is installed
    git-lfs version
)

REM Check current directory
echo.
echo Current directory: %CD%

REM Look for common model file patterns
echo.
echo Looking for model files...

set FOUND_FILES=0
for /r %%f in (*.pth *.pt *.h5 *.onnx *.weights) do (
    if exist "%%f" (
        set /a FOUND_FILES+=1
        echo Found: %%f
        
        REM Check file size
        for %%A in ("%%f") do (
            set "FILESIZE=%%~zA"
            echo   Size: %%~zA bytes
        )
        
        REM Check if file is suspiciously small
        for %%A in ("%%f") do (
            if %%~zA LSS 200 (
                echo   ⚠️  WARNING: File is very small - might be a pointer file
                echo   First 100 characters:
                powershell -Command "& {Get-Content '%%f' -Head 1 | Out-String}" 2>nul
                echo.
            )
        )
        
        echo.
    )
)

if %FOUND_FILES%==0 (
    echo No model files found
    exit /b 0
)

echo Verification complete
echo ✓ Found %FOUND_FILES% model files

REM Note: More detailed verification would require PowerShell scripting
REM This basic version just confirms files exist and aren't tiny