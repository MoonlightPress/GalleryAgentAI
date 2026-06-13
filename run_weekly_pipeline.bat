@echo off
rem Weekly Mochi pipeline run — registered as Windows scheduled task "MochiWeeklyPipeline".
rem 1. Runs the full pipeline, logging to logs\pipeline_runs\
rem 2. Writes memory\last_run.json (status ok/failed)
rem 3. On success, publishes refreshed data to the Lightsail server (no restart
rem    needed — the API reloads compact_opportunities.json on mtime change).
cd /d "%~dp0"
if not exist logs\pipeline_runs mkdir logs\pipeline_runs
set TS=%date:~10,4%-%date:~4,2%-%date:~7,2%_%time:~0,2%%time:~3,2%
set TS=%TS: =0%
python run_full_mochi_pipeline.py > "logs\pipeline_runs\run_%TS%.log" 2>&1
if %errorlevel%==0 (
  python -c "import json,datetime;json.dump({'last_run':datetime.datetime.now().isoformat(),'status':'ok'},open('memory/last_run.json','w'))"
  rem ── Publish data to server (best-effort; skipped if key or network missing) ──
  if exist "Web\LightsailDefaultKey-us-east-1.pem" (
    scp -i "Web\LightsailDefaultKey-us-east-1.pem" -o StrictHostKeyChecking=no -o ConnectTimeout=15 deploy_data\compact_opportunities.json ubuntu@18.206.62.200:/opt/mochi/deploy_data/ >> "logs\pipeline_runs\run_%TS%.log" 2>&1
    scp -i "Web\LightsailDefaultKey-us-east-1.pem" -o StrictHostKeyChecking=no -o ConnectTimeout=15 memory\career_strategy_report.json memory\peer_artists.json ubuntu@18.206.62.200:/opt/mochi/memory/ >> "logs\pipeline_runs\run_%TS%.log" 2>&1
  )
) else (
  python -c "import json,datetime;json.dump({'last_run':datetime.datetime.now().isoformat(),'status':'failed'},open('memory/last_run.json','w'))"
)
