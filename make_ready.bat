@echo off
rem ============================================================================
rem make_ready.bat — "she's getting it today" — one command from dormant to live.
rem
rem Run this the day you decide to send Mochi to her. It:
rem   1. Pre-flight checks (API keys present, server key present)
rem   2. Runs the FULL discovery pipeline (fresh opportunities — costs
rem      ~265-500 Tavily searches + Claude calls; needs API credits)
rem   3. Generates tailored email drafts for every Immediate Best Move
rem   4. Deploys the v2 app + fresh data to the Lightsail server
rem   5. Smoke-tests the live site
rem
rem Expected runtime: 1-2 hours, mostly unattended. Read docs\HANDOFF.md first.
rem ============================================================================
cd /d "%~dp0"
echo.
echo === MOCHI HANDOFF — pre-flight ===

if not exist .env (
  echo FAIL: .env missing at repo root. Needs ANTHROPIC_API_KEY and TAVILY_API_KEY.
  exit /b 1
)
if not exist "Web\LightsailDefaultKey-us-east-1.pem" (
  echo FAIL: Lightsail SSH key missing at Web\LightsailDefaultKey-us-east-1.pem
  exit /b 1
)
python -c "import anthropic, dotenv; dotenv.load_dotenv(); import os, sys; k=os.environ.get('ANTHROPIC_API_KEY'); sys.exit(0 if k else 1)" || (
  echo FAIL: ANTHROPIC_API_KEY not loadable from .env
  exit /b 1
)
echo Pre-flight OK. Remember: this run spends Tavily + Claude credits.
echo.

echo === STEP 1/4: full discovery pipeline ===
python run_full_mochi_pipeline.py
if errorlevel 1 (
  echo PIPELINE FAILED — fix before handoff. Live data untouched.
  exit /b 1
)

echo.
echo === STEP 2/4: tailored email drafts for all Immediate Best Moves ===
python engines\ibm_email_writer.py --limit 20

echo.
echo === STEP 3/4: deploy v2 + fresh data to the server ===
bash deploy.sh
if errorlevel 1 (
  echo DEPLOY FAILED — check output above. See docs\HANDOFF.md troubleshooting.
  exit /b 1
)

echo.
echo === STEP 4/4: smoke test ===
python -c "import urllib.request,json,sys; d=json.load(urllib.request.urlopen('http://18.206.62.200/api/today',timeout=20)); ok=all(d.get(k) for k in ('quick_win','high_impact','stretch_goal')); print('Today slots:', 'OK' if ok else 'MISSING'); sys.exit(0 if ok else 1)"
if errorlevel 1 (
  echo SMOKE TEST FAILED — do not send yet.
  exit /b 1
)

echo.
echo ============================================================
echo   MOCHI IS READY. Send her: http://18.206.62.200
echo   (Walk through docs\HANDOFF.md "final once-over" first.)
echo ============================================================
