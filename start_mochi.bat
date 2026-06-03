@echo off
start "Mochi API" powershell -NoExit -Command "cd /d '%~dp0'; python api.py"
start "Mochi Dev" powershell -NoExit -Command "cd /d '%~dp0frontend'; npm run dev"
timeout /t 3 /nobreak >nul
start http://localhost:5177
