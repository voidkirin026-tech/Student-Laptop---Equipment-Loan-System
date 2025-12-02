@echo off
REM Copy script to prepare project for USB transfer
REM This excludes venv, cache, and other unnecessary files

setlocal enabledelayedexpansion

set SOURCE=%cd%
set DEST=%1

if "%DEST%"=="" (
    echo Usage: copy_to_usb.bat D:\
    echo Example: copy_to_usb.bat "E:\Project Backup\"
    exit /b 1
)

echo Copying project files to USB (excluding venv and cache)...
echo.

REM Create destination folder if it doesn't exist
if not exist "%DEST%Equipment_Loan_System\" mkdir "%DEST%Equipment_Loan_System\"

REM Copy all files EXCEPT venv and cache
robocopy "%SOURCE%" "%DEST%Equipment_Loan_System\" /S /E ^
    /XD venv __pycache__ .git node_modules ^
    /XF *.pyc .DS_Store thumbs.db ^
    /NP /R:1 /W:1

echo.
echo ✓ Project copied successfully!
echo.
echo Location: %DEST%Equipment_Loan_System\
echo.
echo Next steps on the new computer:
echo 1. Open Command Prompt in the project folder
echo 2. Run: python -m venv venv
echo 3. Run: venv\Scripts\activate (Windows) or source venv/bin/activate (Mac/Linux)
echo 4. Run: pip install -r requirements.txt
echo 5. Run: python app.py
echo.
pause
