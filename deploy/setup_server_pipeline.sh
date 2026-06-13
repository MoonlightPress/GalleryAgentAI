#!/usr/bin/env bash
# setup_server_pipeline.sh — ONE-TIME setup of the self-running pipeline on Lightsail.
# Run on the server: sudo bash /tmp/mochi-deploy/setup_server_pipeline.sh
#
# After this, the server refreshes its own data every Tuesday with no laptop,
# no Claude, no human. Requires /opt/mochi/.env to already hold ANTHROPIC_API_KEY
# (with credits) and TAVILY_API_KEY.
set -euo pipefail

REPO=/opt/mochi-repo
GIT_URL=https://github.com/MoonlightPress/GalleryAgentAI.git

echo "==> Cloning/updating repo at $REPO"
if [ -d "$REPO/.git" ]; then
  sudo -u ubuntu git -C "$REPO" pull --ff-only
else
  sudo -u ubuntu git clone --depth 1 "$GIT_URL" "$REPO"
fi

echo "==> Python venv + full pipeline requirements"
sudo -u ubuntu python3 -m venv "$REPO/venv"
sudo -u ubuntu "$REPO/venv/bin/pip" install -q --upgrade pip
sudo -u ubuntu "$REPO/venv/bin/pip" install -q -r "$REPO/requirements.txt"

echo "==> Installing pipeline runner"
cp "$REPO/deploy/mochi-pipeline.sh" /usr/local/bin/mochi-pipeline.sh
chmod +x /usr/local/bin/mochi-pipeline.sh
chown ubuntu:ubuntu /usr/local/bin/mochi-pipeline.sh

echo "==> Registering cron (ubuntu user): Tuesdays 00:00 UTC (= 09:00 JST)"
( sudo -u ubuntu crontab -l 2>/dev/null | grep -v mochi-pipeline ;
  echo "0 0 * * 2 /usr/local/bin/mochi-pipeline.sh" ) | sudo -u ubuntu crontab -

echo "==> Done. First run can be triggered manually to supervise it once:"
echo "    sudo -u ubuntu /usr/local/bin/mochi-pipeline.sh && tail -50 $REPO/logs/pipeline_runs/*.log"
