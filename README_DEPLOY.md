# Mochi — Deployment Guide

Target: Amazon Lightsail, Ubuntu 22.04 LTS.  
Stack: nginx (static + reverse proxy) + uvicorn/FastAPI (port 8001, local only).

---

## 1. On your dev machine — build the package

```bash
bash deploy.sh
```

This produces `deploy_package/` containing the React build, API files,
data, nginx config, systemd service, and install script.

On Windows, run from Git Bash or WSL.

---

## 2. Upload to the server

Replace `YOUR_IP` with your Lightsail public IP (find it in the Lightsail console).

```bash
scp -r deploy_package/ ubuntu@YOUR_IP:/tmp/mochi-deploy
```

If you have a `.pem` key file (Lightsail default):

```bash
scp -i ~/path/to/key.pem -r deploy_package/ ubuntu@YOUR_IP:/tmp/mochi-deploy
```

---

## 3. SSH into the server

```bash
ssh ubuntu@YOUR_IP
# or with key:
ssh -i ~/path/to/key.pem ubuntu@YOUR_IP
```

---

## 4. Run the install script

```bash
sudo bash /tmp/mochi-deploy/install.sh
```

This installs nginx, creates the Python virtualenv at `/opt/mochi/venv`,
installs API dependencies, copies the React build to `/var/www/mochi`,
enables the nginx site, and registers the systemd service.

---

## 5. Add secrets

The `.env` file is never uploaded. Create it manually on the server:

```bash
sudo nano /opt/mochi/.env
```

Paste exactly:

```
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE
TAVILY_API_KEY=tvly-YOUR_KEY_HERE
```

Save: `Ctrl-O`, `Enter`, `Ctrl-X`.

Set permissions:

```bash
sudo chown ubuntu:ubuntu /opt/mochi/.env
chmod 600 /opt/mochi/.env
```

---

## 6. Start the API service

```bash
sudo systemctl start mochi-api
sudo systemctl status mochi-api   # should show "active (running)"
```

Check the logs if it doesn't start:

```bash
sudo journalctl -u mochi-api -n 50
```

---

## 7. Verify everything works

```bash
# API health check (from the server itself)
curl http://127.0.0.1:8001/api/health

# Full stack via nginx (from your laptop)
curl http://YOUR_IP/api/health

# Open in browser:
# http://YOUR_IP
```

---

## File layout on the server

```
/opt/mochi/
├── api.py                        # FastAPI app
├── requirements-api.txt
├── .env                          # secrets — never committed
├── venv/                         # Python virtualenv
├── deploy_data/
│   └── compact_opportunities.json
└── memory/
    ├── feedback.json
    ├── contact_memory.json
    ├── peer_artists.json
    ├── artist_master_profile.json
    ├── learned_preferences.json
    ├── submission_log.json
    ├── suppressed_opportunities.json
    └── peppercorn_profile.json   # optional — API generates defaults if missing

/var/www/mochi/                   # React static build
└── (index.html, assets/, ...)

/etc/nginx/sites-enabled/mochi    # nginx config
/etc/systemd/system/mochi-api.service
```

---

## Lightsail firewall — open port 80

In the Lightsail console → your instance → **Networking** tab:

- Add rule: **Custom TCP**, port **80**, source `0.0.0.0/0`

Port 8001 stays closed to the internet — nginx proxies to it internally.

---

## Updating the app after changes

**Data only** (re-run pipeline on dev, push updated JSON):

```bash
scp deploy_data/compact_opportunities.json ubuntu@YOUR_IP:/opt/mochi/deploy_data/
```

**Full redeploy** (code + data change):

```bash
bash deploy.sh
scp -r deploy_package/ ubuntu@YOUR_IP:/tmp/mochi-deploy
ssh ubuntu@YOUR_IP "sudo bash /tmp/mochi-deploy/install.sh && sudo systemctl restart mochi-api"
```

---

## HTTPS (optional, after DNS is pointed)

Once you have a domain and DNS pointed at your Lightsail IP:

```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

Certbot patches the nginx config and sets up auto-renewal.

---

## Troubleshooting

| Symptom | Check |
|---|---|
| `502 Bad Gateway` | `sudo systemctl status mochi-api` — API not running |
| `curl: (7) Failed to connect` | Lightsail firewall port 80 not open |
| API starts then crashes | `sudo journalctl -u mochi-api -n 100` — usually a missing `.env` |
| React loads but API calls fail | Check `/api/` proxy in nginx: `sudo nginx -t` |
| Old data showing | Re-upload `compact_opportunities.json`, no restart needed |
| `deploy.sh` prints "(skipping missing: peppercorn_profile.json)" | Expected — this file doesn't exist until the artist saves their first profile. The API generates safe defaults from `artist_master_profile.json`. |
| Peppercorn page shows empty preferences on first load | Normal on a fresh deploy. Once the artist submits their profile it persists to disk. |
