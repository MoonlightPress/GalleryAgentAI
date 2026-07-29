@echo off
rem Weekly Mochi pipeline run — registered as Windows scheduled task "MochiWeeklyPipeline".
rem 1. Runs the MAINTENANCE pipeline (zero Tavily/Claude spend), logging to logs\pipeline_runs\
rem 2. Writes memory\last_run.json (status ok/failed)
rem 3. On success, publishes refreshed data to the Lightsail server (no restart
rem    needed — the API reloads compact_opportunities.json on mtime change).
cd /d "%~dp0"
if not exist logs\pipeline_runs mkdir logs\pipeline_runs
rem Log hygiene: prune run logs older than 30 days (no-op if none match; errors suppressed)
forfiles /p logs\pipeline_runs /m run_*.log /d -30 /c "cmd /c del @path" 2>nul
rem Locale-proof timestamp. The old %date% slicing assumed "Tue 07/28/2026"
rem (weekday first); this machine renders "07/28/2026 Tue", so TS came out as
rem "0Tue-8/-02_..." — a path with "/" in it. The redirect below then failed
rem before python ever started, every weekly run since 2026-07-14 died in
rem under a second, and check_attention fired a Discord failure alert each
rem time. Found 2026-07-28 after "a lot of errors on discord".
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HHmm"') do set TS=%%i
if "%TS%"=="" set TS=unknown_time
python run_maintenance_pipeline.py > "logs\pipeline_runs\run_%TS%.log" 2>&1
if %errorlevel%==0 (
  python -c "import json,datetime;json.dump({'last_run':datetime.datetime.now().isoformat(),'status':'ok'},open('memory/last_run.json','w'))"
  rem ── Publish data to server (best-effort; skipped if key or network missing) ──
  rem ATOMIC upload (2026-07-29): scp writes in place while the live API
  rem hot-reloads the file on mtime change — an in-place scp let the API read
  rem a half-written JSON and serve an EMPTY site (observed today). Upload to
  rem a temp name, validate it parses on the server, then mv (atomic rename).
  if exist "Web\LightsailDefaultKey-us-east-1.pem" (
    scp -i "Web\LightsailDefaultKey-us-east-1.pem" -o StrictHostKeyChecking=no -o ConnectTimeout=15 deploy_data\compact_opportunities.json ubuntu@18.206.62.200:/opt/mochi/deploy_data/compact_opportunities.json.new >> "logs\pipeline_runs\run_%TS%.log" 2>&1
    ssh -i "Web\LightsailDefaultKey-us-east-1.pem" -o StrictHostKeyChecking=no -o ConnectTimeout=15 ubuntu@18.206.62.200 "python3 -c 'import json; json.load(open(\"/opt/mochi/deploy_data/compact_opportunities.json.new\"))' && mv /opt/mochi/deploy_data/compact_opportunities.json.new /opt/mochi/deploy_data/compact_opportunities.json" >> "logs\pipeline_runs\run_%TS%.log" 2>&1
    scp -i "Web\LightsailDefaultKey-us-east-1.pem" -o StrictHostKeyChecking=no -o ConnectTimeout=15 memory\career_strategy_report.json memory\peer_artists.json ubuntu@18.206.62.200:/opt/mochi/memory/ >> "logs\pipeline_runs\run_%TS%.log" 2>&1
  )
) else (
  python -c "import json,datetime;json.dump({'last_run':datetime.datetime.now().isoformat(),'status':'failed'},open('memory/last_run.json','w'))"
)
rem Always check whether anything needs the maintainer (her reports, failed runs)
python scripts\check_attention.py
