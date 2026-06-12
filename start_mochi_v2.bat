@echo off
start "Mochi API" /d "%~dp0" powershell -NoExit -Command "python api.py"
start "Mochi v2 Dev" /d "%~dp0frontend2" powershell -NoExit -Command "npm run dev"
timeout /t 5 /nobreak >nul
start http://localhost:5178
