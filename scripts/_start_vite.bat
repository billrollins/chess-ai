@echo off
REM Chess frontend - port 5174 (dev.bat Vite uses 5173)
cd /d "%~dp0..\frontend"
call npm run dev
