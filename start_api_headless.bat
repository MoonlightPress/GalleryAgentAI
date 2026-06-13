@echo off
rem Headless API starter — registered as scheduled task "MochiAPI" (at logon).
rem Keeps the local API on :8001 alive without any terminal or Claude session.
cd /d "%~dp0"
if not exist logs mkdir logs
python api.py >> logs\api_headless.log 2>&1
