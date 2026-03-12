@echo off
cd /d "%~dp0"

call "%~dp0scripts\kill_servers.bat" nopause

echo Starting Chess AI...
start "Chess Backend" cmd /k "%~dp0scripts\_start_backend.bat"
start "Chess Frontend" cmd /k "%~dp0scripts\_start_vite.bat"

echo Waiting for dev server to start...
timeout /t 5 /nobreak >nul

start http://localhost:5174

echo.
echo Chess AI: Backend http://localhost:8001  Frontend http://localhost:5174
