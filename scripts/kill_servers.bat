@echo off
REM Chess AI only - kills ports 8001 (backend) and 5174 (frontend).
REM Does NOT touch dev.bat ports: 8000 (Django) or 5173 (Vite).
cd /d "%~dp0"

echo Stopping Chess AI servers (8001, 5174 only)...

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8001" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a 2>nul
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5174" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a 2>nul
)

echo Done.
if "%~1" neq "nopause" timeout /t 2 /nobreak >nul
