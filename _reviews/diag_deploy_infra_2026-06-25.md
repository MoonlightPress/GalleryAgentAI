# Mochi — Deploy / Infra / Durability diagnostic (read-only)

_2026-06-25 · scope: local config & scripts only · no prod writes, no paid runs_

Live app: https://twilightdreamworks.com/mochi/ on Lightsail `ubuntu@18.206.62.200`.
`api.py` runs as systemd `mochi-api` with `EnvironmentFile=/opt/mochi/.env`; app updates via `deploy.sh`.

This pass cross-checked the seven investigation areas. Several previously-known issues are now
**FIXED** (money gate, memory preservation, frontend ship target, `_load_json`). The remaining live
risks cluster around **server autonomy/staleness** and the **install.sh nginx footgun**.

Severity legend: **HIGH** = can break the site or silently fail the artist · **MED** = his-risk /
operational landmine · **LOW** = defense-in-depth / cosmetic.

---

## HIGH

### H1 — No data-staleness signal; refresh is laptop-only and its last run FAILED
- **Evidence:** `memory/last_run.json` = `{"status":"failed","last_run":"2026-06-23T09:00:01"}` (no `host`
  key → a laptop run via `run_weekly_pipeline.bat:22`, not the server runner which stamps `"host":"server"`
  in `deploy/mochi-pipeline.sh:39`). The server-side cron exists only as an **un-run installer**
  (`deploy/setup_server_pipeline.sh` registers `0 0 * * 2` cron at line 32) — there is no evidence it was
  ever run on the box. `api.py` has **no `/api/last_run` or staleness endpoint** (grep for `last_run`/`stale`
  in `api.py` returns only deadline logic, never data-freshness), and the frontend has **no "data may be
  stale" banner** (`frontend/src/**` has no last_run/staleness consumer). The only failure surface is
  `reports/NEEDS_ATTENTION.md`, written by `scripts/check_attention.py` — a file on **Scott's laptop**, not
  anything the artist sees.
- **Impact:** Laptop off (or task failing, as it is now) → the artist silently views frozen data with zero
  on-screen signal. This is the durability promise breaking.
- **One-line fix:** Run `setup_server_pipeline.sh` on the box to make refresh server-resident, OR add a
  `last_updated` field to an API response + a dismissible "updated N days ago" banner; and investigate the
  6/23 failure (check `logs/pipeline_runs/`).

### H2 — `install.sh` installs the WRONG nginx config → white-screens the site and drops SSL
- **Evidence:** `deploy/install.sh:31` copies `deploy/nginx.conf` to `sites-available/mochi`. That file
  (`deploy/nginx.conf:6,10,16`) serves the app at **`/` with `root /var/www/mochi`, listen 80, no SSL**.
  But the live config is `deploy/nginx-mochi.conf` (`/mochi/` + `root /var/www`, `listen 443 ssl`, Certbot,
  lines 18-41) and the Vite build is hard-baked to `base:'/mochi/'` (`frontend/vite.config.js:6`). A
  full `install.sh` run would publish a `/mochi/`-based SPA under a `/`-root server → **blank page**, and
  drop HTTPS.
- **Impact:** Any "reinstall from scratch" (or anyone trusting install.sh as the source of truth) bricks
  the site for a non-technical user who can't recover. `deploy.sh` itself does NOT run install.sh and only
  reloads nginx (so routine app deploys are safe) — but the wrong config is shipped in the package
  (`deploy.sh:68` copies `nginx.conf` into `deploy_package/`), keeping the landmine armed.
- **One-line fix:** Point `install.sh:31` (and `deploy.sh:68`) at `nginx-mochi.conf`, and delete/retire
  `deploy/nginx.conf` so the wrong one can't be installed.

---

## MEDIUM

### M2 — `make_ready.bat` smoke test hits HTTP/IP and will FALSE-FAIL on a healthy deploy
- **Evidence:** `make_ready.bat:55` smoke-tests `http://18.206.62.200/api/today`. Under the live
  `nginx-mochi.conf`, port 80 for that host returns `404` (Certbot block, `nginx-mochi.conf:53-55`), and
  the app is HTTPS at `twilightdreamworks.com`. The success banner even prints `http://18.206.62.200`
  (`make_ready.bat:63`). `deploy.sh`'s own verify is correct (`curl -sk https://localhost/`, line 107).
- **Impact:** The "she's getting it today" one-shot reports DEPLOY/SMOKE FAILED on a perfectly good deploy
  → Scott aborts a working handoff, or learns to ignore the smoke test.
- **One-line fix:** Change the smoke test URL to `https://twilightdreamworks.com/mochi/` (and `-k`/host as
  needed) and fix the final echo URL.

### M3 — `scheduler.py` + `deep_verification_agent.py` are orphaned Claude/Tavily spenders
- **Evidence:** grep across `*.py/*.bat/*.sh` (excluding worktrees) shows `scheduler.py` is referenced only
  by itself; it imports `smart_pipeline_runner.run_pipeline` and (per prior audit) drives the
  Claude-using `deep_verification_agent`. Not wired to any `.bat`, `deploy/*.sh`, or cron.
- **Impact:** Unreachable today (so no *silent* spend), but a live, un-gated paid path one manual
  `python scripts/scheduler.py` away. It is NOT covered by `PAID_STEPS` gating (that only protects the
  `run_*_pipeline` path).
- **One-line fix:** Move both to `archive/dead_code/` or add an explicit `--i-will-pay` guard at the top.

### M4 — `_load_json` crash-safety added but only partially applied (43 raw `json.load*` remain)
- **Evidence:** `api.py:57` defines a crash-safe `_load_json` (returns default on `JSONDecodeError`), used in
  **11** sites — but **43** raw `json.load(`/`json.loads(` call sites remain in `api.py`. A file that
  *exists but is malformed* (e.g. an interrupted self-write to a `memory/` JSON) on an un-migrated hot
  reader → `JSONDecodeError` → HTTP 500 on page load.
- **Impact:** Low-probability (needs a torn write) but page-killing; the artist sees a 500, not a graceful
  empty.
- **One-line fix:** Route the remaining hot GET readers (`/api/opportunities`, `/api/saffron`,
  `/api/contacts`, `/api/peppercorn`) through `_load_json`.

---

## LOW

### L1 — `/webhook/deploy` skips signature check when `MOCHI_WEBHOOK_SECRET` is empty
- **Evidence:** `api.py:3243` `if WEBHOOK_SECRET:` — when the env var is unset, signature verification is
  bypassed entirely and any POST with `X-GitHub-Event: push` triggers `_run_deploy()` →
  `scripts/deploy_from_git.sh` (`api.py:3236-3250`). Mitigation: nginx only proxies `location /api/`
  (`nginx-mochi.conf:27`), so `/webhook/deploy` is **not externally reachable** — only on `localhost:8001`.
- **Impact:** Defense-in-depth only, given the nginx scoping. But a future nginx change exposing `/webhook/`
  would turn this into an unauthenticated remote deploy trigger.
- **One-line fix:** Confirm `MOCHI_WEBHOOK_SECRET` is set in `/opt/mochi/.env` (or make the handler hard-fail
  closed when it's empty).

### L2 — Frontend publish is rsync-atomic, but the upstream scp is not transactional
- **Evidence:** `deploy.sh:77` `scp -r www → /tmp/mochi-stage/www`, then `deploy.sh:79`
  `rsync -a --delete /tmp/mochi-stage/www/ /var/www/mochi/`. The **publish** (rsync from a fully-staged
  dir) lands `index.html` + all hashed chunks together — so the lazy-loaded `SaffronPage-<hash>.js` /
  `PeppercornPage-<hash>.js` chunks (`App.jsx:13-14`) deploy atomically. BUT if the `scp` dies mid-transfer,
  the staging dir is partial and rsync then publishes that partial set (the prior "Saffron blank" 404).
- **Impact:** Small residual partial-deploy window on a flaky network; the documented prior blank most
  likely came from a manual partial scp, not this code path.
- **One-line fix:** Gate the rsync on scp success (`set -e` already on; add an explicit
  `index.html` + chunk-count sanity check on the staging dir before publishing).

---

## VERIFIED GOOD — do not re-chase

- **Engine ship list is complete.** `api.py` imports `engines.{profile_sync, regen, notify, visit_tracking,
  backups}` (lines 16-20) + `engines.career_strategy_engine` (line 104, lazy); `deploy.sh:40` ships exactly
  those six plus `ibm_email_writer`. Transitive imports check out: `regen.py` launches
  `engines/ibm_email_writer.py` as a **subprocess** (`regen.py:19`, relative to WorkingDirectory `/opt/mochi`),
  and `ibm_email_writer` imports only `profile_sync` + `notify` (`ibm_email_writer.py:26-27`) — both shipped.
  `recommendation_readiness.py` (api.py:15) is shipped (`deploy.sh:33`). **No import gap → no 502-on-import.**
- **Money gate is closed (the 6/30 risk).** The four translation engines ARE in `PAID_STEPS`
  (`run_full_mochi_pipeline.py:138-141`), and the enabled `MochiWeeklyPipeline` task runs
  `run_maintenance_pipeline.py` (`run_weekly_pipeline.bat:13`), which excludes `PAID_STEPS`
  (`run_maintenance_pipeline.py:11`). The unattended weekly task **cannot spend Claude/Tavily**.
- **Memory preservation is safe.** `deploy.sh:90-99` snapshots `/opt/mochi/memory` → `memory_backups/<ts>/`
  before any touch, rsyncs code with `--exclude 'memory/'` (line 97), and seeds memory `--ignore-existing`
  (line 99) → never clobbers her edits. Caveat: `--ignore-existing` also means a **legitimate data update to
  an already-present memory file will NOT be pushed by deploy** (by design — that's the pipeline's job via
  `mochi-pipeline.sh:32-34`, which copies specific files). Acceptable, but worth knowing.
- **Secrets hygiene clean.** `.gitignore` covers `.env`, `.env.*`, `*.env`, `*.pem`, `Web/*.pem` (lines 2-11);
  `git ls-files` finds no tracked `.env`/`.pem`/secret/credential file.
- **`_load_json` is genuinely crash-safe** for the 11 readers it covers (api.py:57-70).

---

## Priority order to act
1. **H2** nginx footgun — one-line config swap, removes a site-bricking landmine. (free, no prod)
2. **H1** staleness — run the server cron installer OR add a staleness banner; investigate 6/23 failure.
3. **M2** make_ready smoke-test URL — stops false-fails on a real handoff.
4. **M3 / M4 / L1 / L2** — cleanup / defense-in-depth, no urgency.

_Read-only diagnostic. No production writes, no paid runs, no SSH-write performed._
