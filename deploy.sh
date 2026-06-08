#!/usr/bin/env bash
# deploy.sh — local preparation script (run on your dev machine).
# Builds the React frontend and assembles a self-contained deploy package.
# Run with: bash deploy.sh
# On Windows: use Git Bash or WSL.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$SCRIPT_DIR/deploy_package"

echo "==> Building React frontend"
cd "$SCRIPT_DIR/frontend"
npm install --silent
npm run build
cd "$SCRIPT_DIR"

echo "==> Assembling deploy package at $OUT"
rm -rf "$OUT"
mkdir -p "$OUT/app" "$OUT/www"

# React build
cp -r "$SCRIPT_DIR/frontend/dist/." "$OUT/www/"

# Python API — only the files the server actually needs at runtime
cp "$SCRIPT_DIR/api.py"                  "$OUT/app/"
cp "$SCRIPT_DIR/requirements-api.txt"    "$OUT/app/"

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
    suppressed_opportunities.json; do
    src="$SCRIPT_DIR/memory/$f"
    [ -f "$src" ] && cp "$src" "$OUT/app/memory/" || echo "  (skipping missing: $f)"
done

# Config files
cp "$SCRIPT_DIR/deploy/nginx.conf"           "$OUT/"
cp "$SCRIPT_DIR/deploy/mochi-api.service"    "$OUT/"
cp "$SCRIPT_DIR/deploy/install.sh"           "$OUT/"

echo ""
echo "============================================================"
echo "  Package ready: $OUT"
echo ""
echo "  Upload to your Lightsail server:"
echo "    scp -r deploy_package/ ubuntu@YOUR_IP:/tmp/mochi-deploy"
echo ""
echo "  Then SSH in and run:"
echo "    sudo bash /tmp/mochi-deploy/install.sh"
echo ""
echo "  See README_DEPLOY.md for full step-by-step instructions."
echo "============================================================"
