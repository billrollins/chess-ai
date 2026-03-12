@echo off
cd /d "%~dp0.."

set "MSG_FILE=scripts\commit_message.txt"

if not exist "%MSG_FILE%" (
    echo ERROR: %MSG_FILE% not found.
    pause
    exit /b 1
)

set /p MSG=<"%MSG_FILE%"

if "%MSG%"=="" (
    echo ERROR: Commit message is empty. Write a message to %MSG_FILE% first.
    pause
    exit /b 1
)

if "%MSG%"=="---" (
    echo ERROR: Commit message is still the placeholder. Write a real message to %MSG_FILE% first.
    pause
    exit /b 1
)

echo Committing with message: %MSG%
echo.

git add .
if errorlevel 1 (
    echo ERROR: git add failed.
    pause
    exit /b 1
)

git commit -m "%MSG%"
if errorlevel 1 (
    echo ERROR: git commit failed.
    pause
    exit /b 1
)

>"%MSG_FILE%" echo ---

echo.
echo Committed and reset commit_message.txt.
if "%~1" neq "nopause" timeout /t 3 /nobreak >nul
