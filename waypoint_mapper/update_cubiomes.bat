@echo off
REM Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed. Please install Git first.
    exit /b 1
)

REM Navigate to the cubiomes directory
cd /d "%~dp0\cubiomes"

REM Check if the directory is a Git repository
git rev-parse --is-inside-work-tree >nul 2>&1
if %errorlevel% neq 0 (
    echo The cubiomes directory is not a Git repository.
    exit /b 1
)

REM Pull the latest updates from the repository
echo Pulling the latest updates from the cubiomes repository...
git pull origin master

REM Navigate back to the original directory
cd /d "%~dp0"

echo Update complete.
pause
