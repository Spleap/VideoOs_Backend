@echo off
title VideoOs Backend Server
echo ===================================================
echo Starting VideoOs Backend Server...
echo Host: 0.0.0.0 (Accessible via LAN)
echo Port: 8000
echo ===================================================

:: Switch to the script's directory (Project Root)
cd /d "%~dp0"

:: Check if venv exists
if not exist "venv" (
    echo Error: Virtual environment 'venv' not found!
    echo Please run: python -m venv venv
    pause
    exit /b
)

:: Activate Virtual Environment
call venv\Scripts\activate

:: Run the server
echo Activating virtual environment and starting Uvicorn...
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
