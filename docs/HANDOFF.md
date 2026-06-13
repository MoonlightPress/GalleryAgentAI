# HANDOFF.md — giving Mochi to her

This document exists so that on any future day — next week or next year — you can
take Mochi from dormant to in-her-hands in one sitting, without rebuilding context.

## The short version

```
make_ready.bat        ← run this, wait 1-2 hours, follow what it prints
```

It pre-flights your keys, runs the full discovery pipeline (fresh opportunities),
generates a tailored email draft for every Immediate Best Move, deploys the v2 app
and data to the Lightsail server, and smoke-tests the live site. If every step
passes, the URL is ready to send.

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

## State as of 2026-06-13

- v2 frontend (`frontend2/`, three-companion build) complete and verified; v1
  untouched at `frontend/`. Both run locally (5177/5178); server still has v1
  until the next `bash deploy.sh` (which now ships v2 by default).
- Backend trust fixes live locally: stale-deadline gates, Tier-4 guard,
  follow-up nudges (14-day), 26k follower correction.
- Known remaining gaps (acceptable for handoff, tracked in
  `reports/ux_pass_2026-06/04_LOGIC_EFFECTIVENESS.md`): server-side strategy
  strings render English-only in zh/ja mode; deep deadline *extraction* (reading
  dates off venue pages) not yet built — the verification agent checks
  liveness/format, the maintenance pipeline keeps it honest.
- Her zh/ja UI strings were machine-written with care but not native-reviewed.
  Her first session is the QA pass; expect small wording notes.
