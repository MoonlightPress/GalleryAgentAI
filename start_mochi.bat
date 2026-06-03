@echo off
start "Mochi API" /d "%~dp0" powershell -NoExit -Command "python api.py"
start "Mochi Dev" /d "%~dp0frontend" powershell -NoExit -Command "npm run dev"
timeout /t 5 /nobreak >nul
start http://localhost:5177
