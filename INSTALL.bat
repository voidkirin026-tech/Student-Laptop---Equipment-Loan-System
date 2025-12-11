@echo off
REM Equipment Loan System - Automated Installer
REM Single-click installation script for Windows

color 0A
cls
echo.
echo ====================================================
echo   Equipment Loan System - Installation
echo ====================================================
echo.

REM Get the current directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    echo Make sure to check "Add to PATH" during installation
    pause
    exit /b 1
)

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    color 0C
    echo ERROR: requirements.txt not found in current directory
    echo Current directory: %cd%
    pause
    exit /b 1
)

echo [1/5] Python and Node.js found. Proceeding with installation...
echo Current directory: %cd%
echo.

REM Check if venv already exists
if exist "venv" (
    echo [2/5] Virtual environment already exists. Skipping creation...
) else (
    echo [2/5] Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        color 0C
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)
echo.

REM Activate venv and install Python packages
echo [3/5] Installing Python dependencies...
call venv\Scripts\activate.bat
if errorlevel 1 (
    color 0C
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Use full path to requirements.txt
set "REQUIREMENTS_PATH=%cd%\requirements.txt"
echo Installing from: %REQUIREMENTS_PATH%
pip install --upgrade pip
pip install -r "%REQUIREMENTS_PATH%"
if errorlevel 1 (
    color 0C
    echo ERROR: Failed to install Python dependencies
    echo Make sure requirements.txt is in: %cd%
    pause
    exit /b 1
)
echo.

REM Install Node.js dependencies
echo [4/5] Installing Node.js dependencies...
if not exist "frontend" (
    color 0C
    echo ERROR: frontend directory not found
    pause
    exit /b 1
)

cd frontend
call npm install
if errorlevel 1 (
    color 0C
    echo ERROR: Failed to install Node.js dependencies
    cd ..
    pause
    exit /b 1
)
cd ..
echo.

REM Load sample data
echo [5/5] Loading sample data...
python load_sample_data.py
if errorlevel 1 (
    color 0C
    echo WARNING: Sample data loading had an issue, but installation is complete
    echo You may need to set up your database manually
)
echo.

color 0B
echo.
echo ====================================================
echo   Installation Complete! 
echo ====================================================
echo.
echo Your system is ready to use!
echo.
echo To start the application:
echo.
echo  OPTION 1 - Automatic (Recommended):
echo     Run: START.bat
echo.
echo  OPTION 2 - Manual:
echo     Terminal 1 (Backend):
echo        venv\Scripts\activate.bat
echo        python app.py
echo        (Flask runs on http://localhost:5000)
echo.
echo     Terminal 2 (Frontend):
echo        cd frontend
echo        npm run dev
echo        (React runs on http://localhost:3000)
echo.
echo Login Credentials:
echo   Admin:    username=administrator, password=655321
echo   Staff:    username=staff1, password=655322
echo   Borrower: username=borrower1, password=655323
echo.
echo ====================================================
echo.
pause
