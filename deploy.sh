#!/usr/bin/env bash
# deploy.sh — build and deploy to Lightsail in one shot.
# Run with: bash deploy.sh
# On Windows: use Git Bash or WSL.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$SCRIPT_DIR/deploy_package"
SSH_KEY="$SCRIPT_DIR/Web/LightsailDefaultKey-us-east-1.pem"
SERVER="ubuntu@18.206.62.200"
SSH_OPTS="-i $SSH_KEY -o StrictHostKeyChecking=no"

# Which frontend to ship: frontend (canonical, default) or frontend2 (the older
# v2 sandbox, whose UX improvements were already ported back into frontend/).
# All active work lives in frontend/ — ship it. Override: MOCHI_FRONTEND=frontend2 bash deploy.sh
FRONTEND_DIR="${MOCHI_FRONTEND:-frontend}"

echo "==> Building React frontend ($FRONTEND_DIR)"
cd "$SCRIPT_DIR/$FRONTEND_DIR"
npm install --silent
npm run build
cd "$SCRIPT_DIR"

echo "==> Assembling deploy package at $OUT"
rm -rf "$OUT"
mkdir -p "$OUT/app" "$OUT/www"

# React build
cp -r "$SCRIPT_DIR/$FRONTEND_DIR/dist/." "$OUT/www/"

# Python API — only the files the server actually needs at runtime
cp "$SCRIPT_DIR/api.py"                  "$OUT/app/"
cp "$SCRIPT_DIR/recommendation_readiness.py" "$OUT/app/"   # api.py imports this at startup — must ship together or mochi-api crashes (502)
cp "$SCRIPT_DIR/requirements-api.txt"    "$OUT/app/"

# Engine modules api.py imports at startup — must ship together or mochi-api
# crashes on import (502), same rule as recommendation_readiness above.
# ibm_email_writer is what the draft-regen launches (not imported by the API).
mkdir -p "$OUT/app/engines"
for e in profile_sync.py regen.py notify.py visit_tracking.py geoip.py backups.py career_strategy_engine.py peppercorn_preference_engine.py ibm_email_writer.py; do
    cp "$SCRIPT_DIR/engines/$e" "$OUT/app/engines/"
done

# Opportunity data (the core dataset the API serves)
mkdir -p "$OUT/app/deploy_data"
cp "$SCRIPT_DIR/deploy_data/compact_opportunities.json" "$OUT/app/deploy_data/"

# Memory files the API reads at request time
mkdir -p "$OUT/app/memory"
for f in \
    feedback.json \
    contact_memory.json \
    peer_artists.json \
    artist_master_profile.json \
    peppercorn_profile.json \
    learned_preferences.json \
    submission_log.json \
    suppressed_opportunities.json \
    career_strategy_report.json \
    translation_cache.json \
    career_events.json \
    exhibition_log.json; do
    src="$SCRIPT_DIR/memory/$f"
    [ -f "$src" ] && cp "$src" "$OUT/app/memory/" || echo "  (skipping missing: $f)"
done

# Config files
cp "$SCRIPT_DIR/deploy/nginx.conf"           "$OUT/"
cp "$SCRIPT_DIR/deploy/mochi-api.service"    "$OUT/"
cp "$SCRIPT_DIR/deploy/install.sh"           "$OUT/"

echo ""
echo "==> Deploying to $SERVER"

# Frontend — scp to staging dir, then rsync on server (avoids scp nesting bug)
ssh $SSH_OPTS "$SERVER" "sudo rm -rf /tmp/mochi-stage && mkdir -p /tmp/mochi-stage"
scp $SSH_OPTS -r "$OUT/www" "$SERVER:/tmp/mochi-stage/"
ssh $SSH_OPTS "$SERVER" bash <<'REMOTE'
  sudo rsync -a --delete /tmp/mochi-stage/www/ /var/www/mochi/
  sudo chown -R www-data:www-data /var/www/mochi
  sudo nginx -s reload
REMOTE

# API + data
ssh $SSH_OPTS "$SERVER" "mkdir -p /tmp/mochi-app-stage"
scp $SSH_OPTS -r "$OUT/app/." "$SERVER:/tmp/mochi-app-stage/"
ssh $SSH_OPTS "$SERVER" bash <<'REMOTE'
  # Back up the server's CURRENT memory (the artist's live edits) before anything
  # touches it — timestamped, kept on the server.
  if [ -d /opt/mochi/memory ]; then
    TS=$(date -u +%Y%m%dT%H%M%SZ)
    sudo mkdir -p "/opt/mochi/memory_backups/$TS"
    sudo rsync -a /opt/mochi/memory/ "/opt/mochi/memory_backups/$TS/"
    echo "  backed up server memory -> /opt/mochi/memory_backups/$TS/"
  fi
  # Update code + data, but DO NOT overwrite the artist's edited memory files.
  sudo rsync -a --checksum --exclude 'memory/' /tmp/mochi-app-stage/ /opt/mochi/
  # Seed only memory files that don't exist yet on the server (never clobber).
  sudo rsync -a --ignore-existing /tmp/mochi-app-stage/memory/ /opt/mochi/memory/
  # Force-update OUR canonical research profile — the exhibition record etc. that
  # we maintain, NOT her interaction data. Without this, --ignore-existing keeps a
  # stale profile on the server and the regen below rebuilds the WRONG career
  # narrative (this is the trap that hid her real solo/museum/international record).
  # The server's memory was backed up above, so this is recoverable.
  # NOTE: once she is actively editing her statement in-app, switch this to a
  # one-time push or a field-merge so her own edits aren't overwritten.
  sudo rsync -a /tmp/mochi-app-stage/memory/artist_master_profile.json /opt/mochi/memory/
  # peer_artists.json is canonical RESEARCH data we maintain (the comparable-artist
  # set), not her interaction data — force-update it too, or --ignore-existing keeps
  # the stale old peer list live (Pip, 2026-06-26).
  sudo rsync -a /tmp/mochi-app-stage/memory/peer_artists.json /opt/mochi/memory/
  sudo chown -R ubuntu:ubuntu /opt/mochi/api.py /opt/mochi/deploy_data /opt/mochi/memory /opt/mochi/engines
  # Regenerate the career-strategy report with the freshly-deployed engine code.
  # deploy preserves her memory (--ignore-existing), so the report file itself is
  # stale until this runs — and the new UI expects the new shape (level block,
  # _zh siblings). Uses her live server-side data. Non-fatal if it hiccups.
  cd /opt/mochi && python3 engines/career_strategy_engine.py || echo "  (career report regen failed — non-fatal, check after)"
  sudo systemctl restart mochi-api
REMOTE

echo ""
echo "==> Verifying..."
sleep 2
HTTP=$(ssh $SSH_OPTS "$SERVER" "curl -sk -o /dev/null -w '%{http_code}' https://localhost/")
API=$(ssh $SSH_OPTS "$SERVER" "curl -s -o /dev/null -w '%{http_code}' http://localhost:8001/api/opportunities")
echo "  Frontend: $HTTP"
echo "  API:      $API"

if [ "$HTTP" = "200" ] && [ "$API" = "200" ]; then
  echo ""
  echo "  Deploy successful. http://18.206.62.200"
else
  echo ""
  echo "  WARNING: one or more services not returning 200 — check logs on server."
fi
