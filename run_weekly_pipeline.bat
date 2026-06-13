@echo off
rem Weekly Mochi pipeline run — registered as Windows scheduled task "MochiWeeklyPipeline".
rem Logs to logs\pipeline_runs\ with timestamp; writes memory\last_run.json on success.
cd /d "%~dp0"
if not exist logs\pipeline_runs mkdir logs\pipeline_runs
set TS=%date:~10,4%-%date:~4,2%-%date:~7,2%_%time:~0,2%%time:~3,2%
set TS=%TS: =0%
python run_full_mochi_pipeline.py > "logs\pipeline_runs\run_%TS%.log" 2>&1
if %errorlevel%==0 (
  python -c "import json,datetime;json.dump({'last_run':datetime.datetime.now().isoformat(),'status':'ok'},open('memory/last_run.json','w'))"
) else (
  python -c "import json,datetime;json.dump({'last_run':datetime.datetime.now().isoformat(),'status':'failed'},open('memory/last_run.json','w'))"
)
