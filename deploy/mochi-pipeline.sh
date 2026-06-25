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
    # Best-effort Discord alert so a server-side failure isn't silent. MOCHI_DISCORD_WEBHOOK
    # comes from the .env sourced above. Wrapped (|| true) so the alert can never abort the run.
    "$REPO/venv/bin/python" -c "from engines.notify import notify_discord; notify_discord('Mochi server pipeline run FAILED (exit $STATUS) at $(date -Is). Live data left untouched (not stale yet), but the refresh did not run — check the newest log in $LOG_DIR.', status='failure')" || true
  fi
} >> "$LOG" 2>&1

# Log hygiene: prune run logs older than 30 days. Guarded so it can never abort the run.
find "$LOG_DIR" -name 'run_*.log' -mtime +30 -delete 2>/dev/null || true
