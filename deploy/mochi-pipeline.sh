#!/usr/bin/env bash
# mochi-pipeline.sh — weekly data refresh ON the Lightsail server.
# Registered by setup_server_pipeline.sh as a cron job (Tuesdays 00:00 UTC = 09:00 JST).
# Pulls latest engine code, runs the full pipeline, publishes fresh data to the
# live API directory. The API picks up compact_opportunities.json by mtime — no restart.
set -uo pipefail

REPO=/opt/mochi-repo
APP=/opt/mochi
LOG_DIR=$REPO/logs/pipeline_runs
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/run_$(date +%Y-%m-%d_%H%M).log"

{
  echo "=== Mochi weekly pipeline $(date -Is) ==="
  cd "$REPO"
  git pull --ff-only

  # Secrets: the server's existing /opt/mochi/.env (ANTHROPIC + TAVILY keys)
  set -a; source "$APP/.env"; set +a

  # Default: maintenance pipeline (zero API spend). Pass --full for the
  # discovery pipeline (~265-500 Tavily searches + Claude calls).
  if [ "${1:-}" = "--full" ]; then
    "$REPO/venv/bin/python" run_full_mochi_pipeline.py
  else
    "$REPO/venv/bin/python" run_maintenance_pipeline.py
  fi
  STATUS=$?

  if [ $STATUS -eq 0 ]; then
    cp "$REPO/deploy_data/compact_opportunities.json" "$APP/deploy_data/"
    for f in career_strategy_report.json peer_artists.json; do
      [ -f "$REPO/memory/$f" ] && cp "$REPO/memory/$f" "$APP/memory/"
    done
    echo "{\"last_run\":\"$(date -Is)\",\"status\":\"ok\",\"host\":\"server\"}" > "$APP/memory/last_run.json"
    echo "=== OK: data published to $APP ==="
  else
    echo "{\"last_run\":\"$(date -Is)\",\"status\":\"failed\",\"host\":\"server\"}" > "$APP/memory/last_run.json"
    echo "=== FAILED (exit $STATUS) — live data left untouched ==="
  fi
} >> "$LOG" 2>&1
