@echo off
REM Equipment Loan System - Uninstaller
REM Removes virtual environment and node_modules

color 0C
cls
echo.
echo ====================================================
echo   Equipment Loan System - Uninstall
echo ====================================================
echo.

setlocal enabledelayedexpansion

echo This will remove:
echo   - Python virtual environment (venv)
echo   - Node.js modules (node_modules)
echo   - Database will be reset on next install
echo.
set /p confirm="Are you sure? (yes/no): "

if /i not "%confirm%"=="yes" (
    echo Uninstall cancelled.
    pause
    exit /b 0
)

echo.
echo Removing virtual environment...
if exist "venv" (
    rmdir /s /q venv
    echo   ✓ venv removed
) else (
    echo   - venv not found
)

echo.
echo Removing Node.js modules...
if exist "frontend\node_modules" (
    rmdir /s /q frontend\node_modules
    echo   ✓ node_modules removed
) else (
    echo   - node_modules not found
)

echo.
echo Removing lock files...
if exist "frontend\package-lock.json" (
    del frontend\package-lock.json
    echo   ✓ package-lock.json removed
)

echo.
color 0A
echo ====================================================
echo   Uninstall Complete!
echo ====================================================
echo.
echo To reinstall, run: INSTALL.bat
echo.
pause
