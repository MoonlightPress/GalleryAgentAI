# HANDOFF.md — giving Mochi to her

This document exists so that on any future day — next week or next year — you can
take Mochi from dormant to in-her-hands in one sitting, without rebuilding context.

## The short version

```
make_ready.bat        ← run this, wait 1-2 hours, follow what it prints
```

It pre-flights your keys, runs the full discovery pipeline (fresh opportunities),
generates a tailored email draft for every Immediate Best Move, deploys the canonical
React app (`frontend/`) and data to the Lightsail server, and smoke-tests the live site.
If every step passes, the URL is ready to send.

## What it costs (the only money in the process)

- **Tavily:** ~265–500 searches, one time (the four discovery engines).
- **Claude API:** the draft writer + why-it-fits engine — a few dollars at most.
  Check credits first: console.anthropic.com → Plans & Billing. The key in `.env`
  was out of credits on 2026-06-13.

## While dormant (no action needed)

- Windows task **MochiWeeklyPipeline** (Tuesdays 09:00, if the PC is on) runs the
  free maintenance pipeline: re-verifies URLs/deadlines, re-buckets, re-scores,
  applies feedback. Zero API spend. Logs: `logs\pipeline_runs\`.
- The server keeps serving whatever was last deployed (systemd + nginx).
- Nothing anywhere runs the paid discovery pipeline automatically.

## The final once-over before sending (15 minutes, by hand)

1. Open the live site on your **phone** — she'll open it on hers.
2. Switch to **中文** — that's the language she'll use. Read Today's Focus aloud:
   does each of the three items make sense *today*? No past deadlines?
3. Click **Copy email** on the top Best Move; paste it somewhere and read it.
   This is the single most important artifact in the product — it speaks as her.
4. Peppercorn page: confirm her artist statement and answered questions show
   (this is her data from before; it should feel like the system remembered her).
5. Saffron page: does "From up here" describe her position accurately?

## What to say when you send it (suggestion)

The product introduces itself — three companions, three questions. You don't need
to explain features. One line and the URL is enough.

## If something breaks

- **Live site down:** `ssh -i Web\LightsailDefaultKey-us-east-1.pem ubuntu@18.206.62.200`
  → `sudo systemctl restart mochi-api` · logs: `sudo journalctl -u mochi-api -n 50`
- **Pipeline fails mid-run:** live data is untouched (publish happens only on
  success). Check the newest log in `logs\pipeline_runs\`.
- **Stale "Today's Focus":** three independent guards filter dead deadlines
  (bucket engine, /api/today gates, client-side). If something still looks wrong,
  run `python run_maintenance_pipeline.py` — free, ~30 min.
- **Full context for any future Claude session:** `reports/ux_pass_2026-06/`
  (00_PROGRESS.md is the index) + CLAUDE.md.

## State as of 2026-06-19

- **`frontend/` is the canonical app** (port 5177). The old `frontend2/` sandbox's
  UX improvements were ported back into it, and **`deploy.sh` now ships `frontend/`
  by default** (it previously defaulted to `frontend2/` — a fixed launch trap; all
  active work lives in `frontend/`).
- Recent work, all in `frontend/`: a **"People to reach out to" view** (surfaces the
  52 researched relationship contacts), **past-deadline verification** (103 stale
  "verified" deadlines now flagged, incl. one that was in Immediate Best Moves), and
  a clean `npm run lint`. Tests pass: 33 Python, 15 frontend.
- **Not yet done (deliberate):**
  - **Visual smoke-test the Peppercorn + Saffron pages** after recent hook/refactor
    changes — fold into the "final once-over" below before sending.
  - The **paid** live-verification pass (fill missing fees/contacts, re-check dead
    URLs) + email-draft generation — both cost a little; `make_ready.bat` runs them.
  - zh/ja UI strings machine-written, not native-reviewed; her first session is the QA pass.

## Verify the server is actually autonomous (one-time, by SSH)

`deploy/setup_server_pipeline.sh` is meant to make the server self-refresh weekly with
no laptop. Confirm it's actually switched on:

- **Cron registered:** `ssh -i Web\LightsailDefaultKey-us-east-1.pem ubuntu@18.206.62.200 'sudo -u ubuntu crontab -l | grep mochi-pipeline'`
- **API starts on boot:** `… 'systemctl is-enabled mochi-api'` → should say `enabled`
- **Keys present + funded:** `/opt/mochi/.env` holds `ANTHROPIC_API_KEY` (with credits) + `TAVILY_API_KEY`
- **Auto-deploy on git push (optional):** `MOCHI_WEBHOOK_SECRET` set in `.env` and a GitHub
  webhook pointed at `/webhook/deploy` — then a `git push` redeploys with no laptop.

If the cron isn't registered, run once on the server: `sudo bash /opt/mochi-repo/deploy/setup_server_pipeline.sh`.
