@echo off
echo ==========================================
echo   LinuxDo Auto Check-in - Quick Start
echo ==========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    pause
    exit /b 1
)

echo Python OK
echo.

REM 设置凭证
set /p username="Enter username: "
set /p password="Enter password: "

echo.
echo Username: %username%
echo Password: ********
echo.

REM 设置环境变量并运行
set "LINUXDO_USERNAME=%username%"
set "LINUXDO_PASSWORD=%password%"

echo Starting optimized version...
python main_optimized.py

echo.
echo Completed
pause
