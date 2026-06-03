#!/usr/bin/env bash
# install.sh — runs ON the Lightsail server after files are uploaded.
# Usage: sudo bash /tmp/mochi-deploy/install.sh
set -euo pipefail

APP_DIR=/opt/mochi
WWW_DIR=/var/www/mochi

echo "==> Installing system packages"
apt-get update -qq
apt-get install -y -qq python3 python3-pip python3-venv nginx

echo "==> Creating app directory at $APP_DIR"
mkdir -p "$APP_DIR"

echo "==> Copying application files"
cp -r /tmp/mochi-deploy/app/. "$APP_DIR/"
chown -R ubuntu:ubuntu "$APP_DIR"

echo "==> Creating Python virtualenv"
sudo -u ubuntu python3 -m venv "$APP_DIR/venv"
sudo -u ubuntu "$APP_DIR/venv/bin/pip" install -q --upgrade pip
sudo -u ubuntu "$APP_DIR/venv/bin/pip" install -q -r "$APP_DIR/requirements-api.txt"

echo "==> Copying React build to $WWW_DIR"
mkdir -p "$WWW_DIR"
cp -r /tmp/mochi-deploy/www/. "$WWW_DIR/"
chown -R www-data:www-data "$WWW_DIR"

echo "==> Installing nginx config"
cp /tmp/mochi-deploy/nginx.conf /etc/nginx/sites-available/mochi
ln -sf /etc/nginx/sites-available/mochi /etc/nginx/sites-enabled/mochi
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

echo "==> Installing systemd service"
cp /tmp/mochi-deploy/mochi-api.service /etc/systemd/system/mochi-api.service
systemctl daemon-reload
systemctl enable mochi-api

echo ""
echo "============================================================"
echo "  Install complete. One step left:"
echo ""
echo "  Create the secrets file:"
echo "    sudo nano $APP_DIR/.env"
echo ""
echo "  Paste:"
echo "    ANTHROPIC_API_KEY=sk-ant-..."
echo "    TAVILY_API_KEY=tvly-..."
echo ""
echo "  Then start the API:"
echo "    sudo systemctl start mochi-api"
echo "    sudo systemctl status mochi-api"
echo "============================================================"
