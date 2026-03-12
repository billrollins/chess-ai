@echo off
REM Chess backend - port 8001 (dev.bat Django uses 8000)
cd /d "%~dp0..\backend"
call venv\Scripts\activate.bat
uvicorn main:app --reload --host 0.0.0.0 --port 8001
