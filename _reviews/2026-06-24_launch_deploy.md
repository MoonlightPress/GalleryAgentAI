# Mochi — Launch Readiness / Deploy / Server Autonomy Review
**Date:** 2026-06-24
**Reviewer facet:** Launch readiness, deployment, server autonomy
**Mode:** Read-only. No deploys, no SSH, no paid pipeline runs. Secret *values* never inspected — only presence.

---

## Summary

The app build and deploy path are basically sound, and one previously-flagged launch trap
(deploy.sh shipping the `frontend2/` sandbox) is genuinely fixed. Data was freshly regenerated
on 2026-06-24, so what ships today is current.

**The headline answer to Pip's concern — "is it only as current as Scott's last pipeline run?" — is YES, with one caveat.** As wired *today*, the production server does **not** refresh its own data.
The only thing that keeps the live site current is a **Windows Scheduled Task on Scott's laptop**
(`MochiWeeklyPipeline`, Tuesdays 09:00, runs `run_weekly_pipeline.bat`) that runs the *free*
maintenance pipeline and SCPs the JSON up. If Scott's laptop is off, asleep, or he stops the task,
the live data silently stops updating. The intended server-side self-refresh
(`deploy/setup_server_pipeline.sh` → server cron) is **written but unverified / not confirmed
installed**, and even if installed it defaults to the *maintenance* pipeline (no new discovery) —
so genuinely new opportunities still depend on a manual paid `make_ready.bat` run.

There is also one concrete deploy hazard: **the deploy/install scripts ship and install the WRONG
nginx config** (`nginx.conf`, which serves the app at `/` with no SSL) while the live, canonical
config is `nginx-mochi.conf` (app at `/mochi/`, SSL). Re-running `install.sh` would overwrite the
live config and break the site, because the Vite build is hard-coded to `base: '/mochi/'`.

Verdict: **NO-GO until server autonomy is confirmed switched on (or consciously accepted as
laptop-driven) and the nginx-config mismatch is resolved.** Neither is a large fix; both are
launch-blocking as stated in CURRENT_STATE's own open list.

---

## Deploy correctness

**Frontend shipped is now correct (the launch trap is fixed).**
`deploy.sh` line 16: `FRONTEND_DIR="${MOCHI_FRONTEND:-frontend}"` — defaults to the canonical
`frontend/`. Confirmed end-to-end: the staged `deploy_package/www/index.html` references
`/mochi/assets/index-*.js` and `/mochi/favicon.svg`, i.e. it was built with `base: '/mochi/'`.
So the build artifact is the canonical app at the correct base path. Good.

**Vite base path is consistent with the live nginx.** `frontend/vite.config.js` sets
`base: '/mochi/'`. The live config `deploy/nginx-mochi.conf` serves the SPA at `location /mochi/`
with `try_files $uri $uri/ /mochi/index.html`, immutable caching on `/mochi/assets/`, root `/`
serving `landing/index.html`, and `/api/` proxied to `127.0.0.1:8001`. This trio is internally
consistent and matches CURRENT_STATE's description of production.

**HAZARD — two divergent nginx configs; the deploy scripts ship the wrong one.**
- `deploy/nginx-mochi.conf` = the **live, canonical** config (app at `/mochi/`, `root /var/www`,
  SSL 443 via Certbot, landing page at `/`). Per CURRENT_STATE it was applied **manually via SSH**.
- `deploy/nginx.conf` = an **older, wrong** config (app at `/`, `root /var/www/mochi`, listen 80
  only, no SSL, no `/mochi/` prefix).
- `deploy.sh` line 60 copies **`deploy/nginx.conf`** into the package; `install.sh` lines 31-33
  install **`nginx.conf`** to `/etc/nginx/sites-available/mochi` and reload nginx.
- Because the Vite build is hard-baked to `/mochi/`, installing `nginx.conf` (which serves at `/`)
  would serve an app whose asset URLs (`/mochi/assets/...`) 404 → **white screen**. It would also
  drop SSL and the landing page.

Mitigating fact: the normal update path (`deploy.sh`) only `rsync`s the build + API + data and
reloads nginx; it does **not** install the nginx config. So routine `deploy.sh` runs are safe.
The danger is specifically **re-running `install.sh`** (a full redeploy per README_DEPLOY.md §"Full
redeploy") or anyone treating README_DEPLOY.md as current — it would clobber the live config.
**Fix:** make `deploy.sh`/`install.sh` ship `nginx-mochi.conf`, or delete/retire `nginx.conf` so
there is one source of truth.

**README_DEPLOY.md is stale vs. reality.** It documents a generic Lightsail "YOUR_IP" first-install
at `/` with no `/mochi/` prefix and no landing page, and its "Full redeploy" step calls
`install.sh` (which would trigger the nginx hazard above). It predates the `/mochi/` move. Not
launch-blocking but should be reconciled with `nginx-mochi.conf` to avoid a future foot-gun.

**Other deploy details that are correct:**
- `deploy.sh` ships `recommendation_readiness.py` alongside `api.py` (commented: api imports it at
  startup or mochi-api 502s) — good, this is a real prior failure being guarded.
- systemd unit `mochi-api.service` is `Restart=on-failure`, `EnvironmentFile=/opt/mochi/.env`,
  binds `127.0.0.1:8001` only (nginx proxies). Correct and minimal.
- Data publish is mtime-based (no API restart needed for data-only refresh) — matches the runners.

---

## Server autonomy — will the data refresh itself? (concrete answer)

**Concrete answer: NO, not on the server as currently confirmed. Production is laptop-driven.**

What actually keeps the live site fresh today:
1. **`MochiWeeklyPipeline` Windows Scheduled Task — CONFIRMED PRESENT on this machine.**
   State `Ready`, weekly trigger Tuesdays 09:00 (DaysOfWeek=4), last run 2026-06-23 09:00
   (LastTaskResult 0), next run 2026-06-30. It executes `run_weekly_pipeline.bat`, which runs the
   **free maintenance pipeline** (re-verify URLs/deadlines, re-score, re-bucket — zero API spend),
   then **SCPs `compact_opportunities.json` + `career_strategy_report.json` + `peer_artists.json`
   to the server** using the bundled Lightsail key. The API picks up the new JSON by mtime.
   → This is the *only* mechanism currently proven to refresh production. **It requires Scott's
   laptop to be powered on at the scheduled time.** Laptop off/asleep = no refresh, silently.

2. **Server-side cron (`deploy/setup_server_pipeline.sh` → `mochi-pipeline.sh`) — WRITTEN, NOT
   CONFIRMED INSTALLED.** This script *would* register a cron (`0 0 * * 2`, Tuesdays 00:00 UTC =
   09:00 JST) on the Lightsail box that pulls the repo and runs the pipeline server-side with no
   laptop. **But:** (a) HANDOFF.md itself lists "confirm the cron is registered" as an *open,
   unverified* SSH check — i.e. nobody has confirmed it's switched on; (b) I am read-only / no-SSH,
   so I cannot confirm it from here; (c) even when it runs, `mochi-pipeline.sh` **defaults to the
   maintenance pipeline** (`run_maintenance_pipeline.py`) — `--full` (paid discovery) is opt-in. So
   even a healthy server cron would *re-verify and re-score existing opps but never discover new
   ones automatically.*

3. **Local `last_run.json` reads `{"status":"failed"}` (2026-06-23).** This file was written by the
   *laptop* path (it lacks the `"host":"server"` field the server cron writes), so the most recent
   recorded maintenance attempt is marked failed even though the Scheduled Task exited 0 and a
   pipeline log shows "PIPELINE COMPLETE". Worth a quick look before launch — the local refresh
   loop is the one keeping production current, and its own status file says its last run failed.

4. **GitHub webhook auto-deploy — IMPLEMENTED, OFF by default.** `api.py` has
   `POST /webhook/deploy` (HMAC-verified against `MOCHI_WEBHOOK_SECRET`, fires
   `scripts/deploy_from_git.sh` on a `push` event). `MOCHI_WEBHOOK_SECRET` is **not** in the local
   `.env` (only `ANTHROPIC_API_KEY` + `TAVILY_API_KEY` present), and it's a code-deploy hook, not a
   data-refresh mechanism. Irrelevant to data staleness.

**Net:** Pip is right. Without the server cron verified on, the live data is exactly "as current as
Scott's laptop's last successful Tuesday run." New *discovery* is even more manual — it only happens
when Scott deliberately runs the paid `make_ready.bat` / `--full`. The pieces to fix this exist
(`setup_server_pipeline.sh`); they are just not confirmed wired, and the default tier wouldn't add
new opportunities anyway.

---

## Pre-launch open items status (from CURRENT_STATE "Real / open before launch")

**(a) Visual smoke-test Peppercorn + Saffron — DEPENDENCY, not mine.**
Owned by another reviewer (the visual/UX facet). Noting the dependency only: HANDOFF "final
once-over" and CURRENT_STATE both flag that the recent hook-order/refactor changes to
`PeppercornPage`/`SaffronPage` and the new People view have **not** been visually verified in a
running browser. Launch should not proceed until that reviewer signs off.

**(b) Live verification pass + email-draft generation (PAID) — CONFIRMED, NOT RUN.**
Command/path: **`make_ready.bat`** (repo root). It runs, in order: pre-flight key check →
`python run_full_mochi_pipeline.py` (full discovery) → `python engines\ibm_email_writer.py
--limit 20` (drafts) → `bash deploy.sh` → live smoke test of `/api/today`.
Cost (per HANDOFF.md / make_ready header): **~265–500 Tavily searches** + Claude calls for the
draft writer & why-it-fits engine (a few dollars). **Requires Scott's go and funded API credits**
(the key was out of credits on 2026-06-13; the 2026-06-24 monthly pass hit the Tavily cap ⅓ in).
**I did not run it.** Known limitation to flag: email drafts are write-once
(`ibm_email_writer` only fills *missing* `email_ja`/`email_en`), and Peppercorn saves the statement
to `peppercorn_profile.json` while the writer reads `artist_master_profile.json` — so editing her
statement will not refresh existing drafts.

**(c) Confirm server autonomy switched on — NOT CONFIRMED (blocking).**
As above: the server cron is written but unverified; production currently depends on the laptop
task; `last_run.json` reads failed. This is the single most important pre-launch verification and
it requires the SSH checks in HANDOFF.md ("Verify the server is actually autonomous"):
`crontab -l | grep mochi-pipeline`, `systemctl is-enabled mochi-api`, and `/opt/mochi/.env` holds
funded keys.

---

## Secrets / config hygiene

**Good:**
- `.env` is present at repo root (201 bytes) and holds both required keys
  (`ANTHROPIC_API_KEY`, `TAVILY_API_KEY` — names only; values not inspected).
- `.gitignore` correctly excludes `.env`, `.env.*`, `*.env`, `*.pem`, `Web/*.pem`, `logs/`,
  `deploy_package/`, `__pycache__`, backups.
- `git ls-files` for `.env` / `.pem` / `secret` returns **nothing** — no secrets are tracked. Clean.
- Server secrets model is correct: `.env` is never uploaded by `deploy.sh`; it's created by hand on
  the box (README §5), `chmod 600`, loaded via systemd `EnvironmentFile`. The server cron sources
  the same `/opt/mochi/.env`.
- API binds localhost only; port 8001 not exposed; webhook is HMAC-verified.

**Watch items (not blocking, worth noting):**
- The Lightsail private key `Web/LightsailDefaultKey-us-east-1.pem` lives in the working tree
  (gitignored, so not committed — correct). It is bundled into the laptop-driven refresh and
  `deploy.sh`. Ensure this machine's disk is the trust boundary you intend; it is the root of
  production access.
- `deploy_package/` (gitignored) currently contains a built artifact + the **wrong** `nginx.conf`.
  Harmless while it stays local, but it's the source of the install hazard above.
- Data freshness: `deploy_data/compact_opportunities.json` rebuilt 2026-06-24 (the monthly pass) —
  so what would deploy today is current. Note the monthly pass hit the Tavily cap, so the back ⅔ of
  opportunities degraded to the Watch List (absorbed gracefully; actionable surface stayed verified).

---

## Go / No-Go checklist (ordered — must be true before sending to GEGYjiji)

1. **Resolve the nginx config mismatch (BLOCKING).** Point `deploy.sh`/`install.sh` at
   `nginx-mochi.conf`, or delete `nginx.conf`, so a full redeploy can never overwrite the live
   `/mochi/` + SSL config with the root-serving one. One source of truth.
2. **Confirm server autonomy is switched on, or consciously accept laptop-driven (BLOCKING).**
   Run the HANDOFF SSH checks: cron registered (`crontab -l | grep mochi-pipeline`),
   `systemctl is-enabled mochi-api` = enabled, `/opt/mochi/.env` keys present + funded. If the
   server cron is NOT installed and you accept laptop-driven refresh, that is a documented decision
   — but then the laptop task must be reliable (see #3) and Scott must know the site goes stale when
   the laptop is off.
3. **Fix / explain the `last_run.json` "failed" status (BLOCKING-ish).** The laptop refresh is
   currently the only thing keeping production current and its last recorded run is marked failed.
   Confirm the most recent maintenance run actually published, or you're shipping on a refresh loop
   whose own status file says it's broken.
4. **Visual smoke-test Peppercorn + Saffron (BLOCKING — other reviewer).** Sign-off required after
   the recent hook/refactor changes; mobile + 中文.
5. **Run the paid `make_ready.bat` with Scott's go and funded credits (REQUIRED before send).**
   This generates fresh discovery + the email drafts that are "the single most important artifact in
   the product." Raise the Tavily pay-as-you-go limit first so verification doesn't degrade ⅔ in.
6. **Do the HANDOFF "final once-over" by hand (REQUIRED).** Live site on a phone, switch to 中文,
   read Today's Focus aloud (no past deadlines in the 3 slots), Copy-email on the top Best Move and
   read it, confirm Peppercorn shows her saved statement, confirm Saffron's "From up here" is
   accurate.
7. **Reconcile README_DEPLOY.md with reality (NICE-TO-HAVE).** Update it to the `/mochi/` + SSL +
   landing-page layout and the `nginx-mochi.conf` filename so the next operator doesn't re-introduce
   the hazard.
8. **(Optional, recommended) Set `MOCHI_WEBHOOK_SECRET` + GitHub webhook** only if you want
   push-to-deploy; not required for launch and unrelated to data freshness.

Only when 1–6 are green should this be flipped live to GEGYjiji.
