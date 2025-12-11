@echo off
REM Equipment Loan System - Application Launcher
REM Starts both backend and frontend automatically

color 0A
cls
echo.
echo ====================================================
echo   Equipment Loan System
echo ====================================================
echo.

REM Check if venv exists
if not exist "venv" (
    color 0C
    echo ERROR: Virtual environment not found!
    echo Please run INSTALL.bat first
    pause
    exit /b 1
)

echo Starting backend and frontend...
echo.
echo Backend will run on: http://localhost:5000
echo Frontend will run on: http://localhost:3000
echo.
echo Press Ctrl+C in either terminal to stop
echo.

REM Start backend in new terminal
start cmd /k "venv\Scripts\activate.bat && python app.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak

REM Start frontend in new terminal
start cmd /k "cd frontend && npm run dev"

echo.
echo Both applications are starting...
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak

REM Try to open browser
start http://localhost:3000

echo.
echo ====================================================
echo Applications are running!
echo Frontend: http://localhost:3000
echo Backend: http://localhost:5000
echo ====================================================
echo.
pause
