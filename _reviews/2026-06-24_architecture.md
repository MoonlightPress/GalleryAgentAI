# Mochi — Pre-launch Architecture Review (Architecture / Sprawl / Money-risk)

_Reviewer posture: pragmatic tech lead, consolidation over expansion. READ-ONLY review — nothing was run, moved, or edited._
_Date: 2026-06-24_

---

## Summary

The architecture is fundamentally sound for launch: there is **one true read surface** (`api.py` serves opportunities from `deploy_data/compact_opportunities.json` only), **one true write path** (`run_full_mochi_pipeline.py` → its `PIPELINE` list), and a money-safe **maintenance** variant of that path that the weekly automation actually runs. The danger the project carries is not a broken pipeline — it is **enormous surface-area sprawl** (150 root `.py`, 105 `engines/*.py`, 114 `README*.md`, 62 already-archived dead files, two React apps, a retired Streamlit, and an *orphaned* second scheduler) in which it is easy to edit, schedule, or trust the wrong file.

**The money-risk headline: there IS an active, enabled Windows scheduled task (`MochiWeeklyPipeline`) that fires weekly and ran as recently as 2026-06-23.** It does **not** run the Claude/Tavily scheduler. It runs the maintenance pipeline, which is designed to be zero-spend. But "zero spend" is **not strictly guaranteed** — three Claude translation engines run inside the maintenance pipeline and are only kept free by an incremental cache gate. See the next section; this is the one thing to verify before you stop worrying.

The single most useful prediction this review makes: **as long as `compact_opportunities.json` and the translation/contact caches stay fully translated, the weekly task spends $0. The moment any source prose changes without those caches being refreshed, the next Thursday 09:00 run will silently spend a small amount of Claude money.** That is the only live money channel, and it is small — but it is real and it is unattended.

---

## Money-risk finding — is anything spending money right now?

**Short answer: ALMOST CERTAINLY NO net spend today, but the channel is LIVE and only one cache-gate away from spending. Treat as "low, unattended, fix-before-you-forget."**

### What is actually scheduled (verified on this machine)

A Windows Scheduled Task exists and is **enabled**:

- **Task:** `MochiWeeklyPipeline` — State `Ready`, `Settings.Enabled = True`.
- **Action:** `C:\ScottStuff\GalleryAgentAI\run_weekly_pipeline.bat` (no args).
- **Trigger:** Weekly, **Thursdays 09:00**, `WeeksInterval = 1`, start boundary 2026-06-13.
- **Last run:** 2026-06-23 09:00, **LastTaskResult = 0** (the `.bat` itself exited clean).
- **Next run:** 2026-06-30 09:00. It *will* fire again unattended.

This directly **contradicts the stale prior audit** (`reports/ux_pass_2026-06/04_LOGIC_EFFECTIVENESS.md`), which claimed "the scheduler has never executed — `memory/last_run.json` does not exist, and no Windows scheduled task references Mochi." Both halves are now false: `memory/last_run.json` exists (written 2026-06-23 09:00) and the scheduled task exists and is enabled. Do not rely on that audit for the money question.

### What the scheduled task runs (the chain)

`run_weekly_pipeline.bat` → `python run_maintenance_pipeline.py` → `run_full_mochi_pipeline.PIPELINE` **minus** `PAID_STEPS` → then `python scripts\check_attention.py` (free; reads JSON only).

`run_maintenance_pipeline.py` computes `MAINTENANCE = [s for s in PIPELINE if s not in PAID_STEPS]`. `PAID_STEPS` (in `run_full_mochi_pipeline.py`) lists 6 engines:
- Tavily: `japanese_chinese_discovery_engine`, `grant_discovery_engine`, `rumor_mill_engine`, `rumor_mill_expansion_runner`
- Claude: `ibm_email_writer`, `why_it_fits_engine`

### The gap I verified — PAID_STEPS is INCOMPLETE

I grepped every engine for `anthropic` / `claude` / `tavily` / `messages.create`. 13 engines touch a paid API. Six are correctly in `PAID_STEPS`. **Three more are in the `PIPELINE` (and therefore in `MAINTENANCE`) but are NOT in `PAID_STEPS`:**

- `content_translation_engine.py` (PIPELINE line 113) — `claude-sonnet-4-6`, `client.messages.create`
- `saffron_translation_engine.py` (PIPELINE line 114) — `claude-sonnet-4-6`
- `contact_translation_engine.py` (PIPELINE line 115) — `claude-sonnet-4-6`

So the maintenance pipeline's docstring claim ("Zero Tavily searches, zero Claude calls") is **not strictly true**. These three run on every weekly maintenance pass.

### Why net spend is still ~$0 in practice (the saving grace)

All three are **incremental / cache-gated**:
- `content_translation_engine.needs_translation()` skips any opp that already has all 8 `_zh`/`_ja` fields; if all are translated it prints "All entries already translated" and makes **zero** API calls.
- `saffron_translation_engine` only translates strings not already in `memory/translation_cache.json`.
- `contact_translation_engine` skips contact fields that already have both `_zh` and `_ja`.

And critically, the **maintenance pipeline adds no new opportunities** — discovery (the Tavily engines) is in `PAID_STEPS` and excluded. So on a steady state where the live data is fully translated, the weekly task does re-score / re-bucket / re-verify-URLs (all free HTTP) and the translation engines no-op. That matches the design intent.

**The exposure:** any change to source prose between runs — Scott edits a contact note, Saffron copy changes, a re-bucket/re-score rewrites a `why_it_fits` string, or a field gets cleared — makes the next Thursday run translate the changed strings via Claude Sonnet, silently and unattended. It is bounded (only the *delta*, batched) and cheap, but it is unsupervised recurring spend, which is exactly the category to eliminate before launch.

Also note: the 2026-06-23 run wrote `last_run.json` with **`"status": "failed"`** even though the `.bat` returned 0. The maintenance pipeline itself exited nonzero that run. Worth a look (a failing weekly job is also a data-freshness risk), but it does not change the money picture — failed or not, no `PAID_STEPS` engine runs in maintenance.

### The scary-sounding pieces are NOT wired to the schedule

- **`scripts/scheduler.py`** (the one that calls Claude-using `deep_verification_agent` and the Tavily discovery engines in its `WEEKLY_PIPELINE`) is an **orphan**. Nothing invokes it: no `.bat`, no scheduled task, no cron, no `.sh`. The Windows task runs `run_weekly_pipeline.bat`, not the scheduler. `deep_verification_agent.py` (uses `claude-haiku-4-5`) is referenced **only** as a string inside `scheduler.py`'s list — so it is effectively dead until someone runs the scheduler by hand.
- **Server-side cron:** `deploy/setup_server_pipeline.sh` would register a *server* cron (`0 0 * * 2`) running `deploy/mochi-pipeline.sh`, which **defaults to `run_maintenance_pipeline.py`** and only runs the paid `--full` pipeline when explicitly passed `--full` (the cron line passes no args). So even the server path defaults to money-safe. Whether that one-time setup script was ever run on the Lightsail box is **unknown from the repo** (verify via SSH: `sudo -u ubuntu crontab -l`). Even if it was, it runs the safe default.
- **The side-channel verification engines spend nothing on a schedule** — none are in `PIPELINE`/`MAINTENANCE`, and their only callers are the orphan `scripts/runners/*` and the orphan `scheduler.py` (see inventory).

### Money-risk bottom line / actions

1. **Add the three translation engines to `PAID_STEPS`** (or gate them behind an explicit `--translate` flag). This makes the maintenance pipeline's "zero Claude" promise literally true and closes the only unattended spend channel. One-line change; do it before launch.
2. **Decide the weekly task's fate consciously.** If unattended weekly refresh is wanted, keep it (after fix #1). If not, disable `MochiWeeklyPipeline`. Right now it is enabled by default and most observers (including the prior audit) believe nothing is scheduled — that mismatch is the real hazard.
3. **Investigate the 2026-06-23 `status: failed`** maintenance run (data-freshness, not money).
4. **Confirm/retire the server cron** via SSH (`crontab -l`); confirm it has no `--full`.

---

## Canonical data flow (the real path)

**Discovery → verification → `compact_opportunities.json` → api → React.** One write path, one read path.

1. **Write path (full):** `run_full_mochi_pipeline.py` runs `PIPELINE` (≈116 steps) via `smart_pipeline_runner.run_pipeline`, which resolves each script name across root → `engines/` → `ui/` → `scripts/runners` → `scripts/patches`. Flow: ingestion (`web_ingestion_engine` → `scraped_candidate_extractor` → `candidate_quality_gate` → `approved_candidate_importer`) → discovery expansion (the Tavily engines) → `url_verification_engine` → enrichment/scoring tail → verification tail (`fee_text_extractor`, `deadline_normaliser`, `submission_page_harvester`, `verification_report_engine`, `targeted_verification_agent`, `dead_url_pruner`) → bucketing (`exclusive_strategy_bucket_engine`) → translation tail (`content_/saffron_/contact_translation_engine`) → `daily_digest_report`. Engines mutate `deploy_data/compact_opportunities.json` and various `memory/*.json` in place.
2. **Write path (maintenance):** `run_maintenance_pipeline.py` = `PIPELINE` minus `PAID_STEPS`. Re-verifies URLs/deadlines via plain HTTP, re-scores, re-buckets, regenerates reports. This is what the weekly task runs. (Caveat: the three translation engines run here too — see money section.)
3. **Read path:** `api.py` (FastAPI on :8001) serves **opportunities exclusively from `deploy_data/compact_opportunities.json`** (lines 716, 753, 876, 928, 1305, 2251). It additionally reads app-state/source files under `memory/` for the other views: `contact_memory.json`, `submission_log.json`, `peppercorn_profile.json`, `artist_master_profile.json`, `peer_artists.json`, `career_events.json`, `translation_cache.json`, `learned_preferences.json`, `feedback.json`, `suppressed_opportunities.json`, `exhibition_log.json`. **It never reads either `verified_opportunities.json`** — confirming the side-channel outputs are dead to the app. The earlier shorthand "api.py reads only compact_opportunities.json" is true *for opportunity data* but understates the app-state reads.
4. **Frontend:** React `frontend/` (Vite, base `/mochi/`) proxies `/api` → :8001 in dev; in prod nginx serves the built `www/` and proxies `/api` to the uvicorn service (`deploy/mochi-api.service`).
5. **Publish:** `run_weekly_pipeline.bat` scp's the refreshed `compact_opportunities.json` (+ `career_strategy_report.json`, `peer_artists.json`) to the server; the API reloads by file mtime, no restart. **Note an IP mismatch:** the `.bat` scp targets `18.206.62.200`, while `CURRENT_STATE.md` says production is `35.164.133.170`. One of them is stale — the weekly publish may be silently failing to reach the live box (consistent with the failed-status run). Verify before relying on auto-publish.

---

## Dead / duplicate code inventory

### Safe to archive (no live caller — moved into `archive/dead_code/`, do NOT delete)

These are not in `PIPELINE`/`MAINTENANCE` and `api.py` does not read their outputs. Their only references are documentation or orphan runners that are themselves dead.

- `web_verification_engine.py` (root) — writes the dead `memory/verified_opportunities.json`.
- `engines/opportunity_verification_engine.py` — writes the dead `deploy_data/verified_opportunities.json`; its consumer (`submission_link_hunter`) was explicitly removed from the pipeline (`run_full_mochi_pipeline.py:17-18`).
- `submission_link_hunter.py`, `application_link_repair.py`, `verified_opportunity_importer.py` — all read the dead `memory/verified_opportunities.json`; none in the pipeline.
- `scripts/scheduler.py` — orphaned second scheduler (no caller). **Archive or clearly mark as inert**; it is the single most dangerous-looking file in the repo because it references the Claude/Tavily engines and *looks* like it runs. (If you'd rather keep it as the intended future automation, at minimum add a banner comment that it is not wired and must not be scheduled without the cost-gating fix.)
- `engines/deep_verification_agent.py` — reachable only via `scheduler.py`; archive with the scheduler or keep paired with it.
- The legacy `scripts/runners/*` family — ~95 thin one-line wrappers, many migration-era (`*.before_path_migration`, `*.py.py`). Bulk-archivable; `targeted_verification_weekly.py` is the only one referenced by the (orphan) scheduler.

### Trace caller first (referenced — verify before touching)

- The three translation engines — **in the live PIPELINE**; do not archive. (Money-gate them instead.)
- `council_pipeline_agent.py` — documented "legacy but still functional." Keep; mark clearly legacy.
- `scripts/patches/*` — one-shot migrations, "likely already run." Low risk to archive, but confirm none are referenced by `smart_pipeline_runner` resolution for a name still in `PIPELINE`.

### Retired-but-on-disk (UI)

- **Streamlit `app.py` + `ui/` + `styles/generated_visual_upgrade.css`** — retired product. `launch_mochi.bat` still opens it (a trap). Keep for reference, but rename/neutralize `launch_mochi.bat` so no one launches the wrong product.
- **`frontend2/`** — see next section.

### Sprawl scale (measured)

150 root `.py`, 105 `engines/*.py`, 114 `README*.md`, 62 files already in `archive/dead_code/`. The README proliferation directly violates the project's own "reports multiply faster than insight" lesson.

---

## The two-frontend situation

- **`frontend/` is canonical** (Vite base `/mochi/`, port 5177, launched by `start_mochi.bat`). Most recent app commits land here (`229417db` move-to-/mochi).
- **`frontend2/` is the retired v2 sandbox** whose UX improvements were already ported back (`40ab9737`, 2026-06-18). It is still on disk and still has its own `package-lock.json`, dev server (`start_mochi_v2.bat`, port 5178), and recent-ish commits (`8a3fb4e6 "Restore text labels in compact companion nav"`).
- **Deploy is safe:** `deploy.sh` defaults to `FRONTEND_DIR=frontend` (the earlier launch-trap where it shipped `frontend2/` was fixed). Shipping the wrong app now requires an explicit `MOCHI_FRONTEND=frontend2` override.
- **Residual risk = editing the wrong app, not shipping it.** `frontend2/` is a fully working second app with its own launcher; an agent or person can easily open it, "fix" something, and watch it never reach production. `frontend2/` still receiving commits is the warning sign. **Recommendation:** archive `frontend2/` (move to `archive/`) or at minimum delete `start_mochi_v2.bat` and drop a `frontend2/RETIRED.md`. Until it's gone, this stays a recurring confusion source — it's the exact thing CURRENT_STATE flags as "the thing that has caused confusion."

---

## Consolidation recommendations (ranked)

1. **Close the money channel (do first, pre-launch).** Add `content_translation_engine.py`, `saffron_translation_engine.py`, `contact_translation_engine.py` to `PAID_STEPS` (or gate behind `--translate`). Then consciously keep-or-disable the `MochiWeeklyPipeline` Windows task. Net effect: the weekly automation becomes provably $0, and the "is something spending money?" question has a permanent answer.
2. **Neutralize the orphan scheduler.** Archive `scripts/scheduler.py` + `engines/deep_verification_agent.py` together, OR add a loud "NOT WIRED — do not schedule without cost-gating" banner. It is the highest-confusion / highest-latent-cost artifact in the tree.
3. **Archive the side-channel verification cluster** (`web_verification_engine.py`, `engines/opportunity_verification_engine.py`, `submission_link_hunter.py`, `application_link_repair.py`, `verified_opportunity_importer.py`) and delete/quarantine the two stale `verified_opportunities.json` files. Confirmed dead to both pipeline and API.
4. **Retire `frontend2/` from the working tree** (move to `archive/`, kill `start_mochi_v2.bat`). Remove the only remaining "wrong app" footgun.
5. **Bulk-archive the `scripts/runners/*` legacy wrappers and migration `scripts/patches/*`**, keeping only what an active path resolves. ~95 files of mostly migration-era cruft.
6. **Neutralize `launch_mochi.bat`** (retired Streamlit launcher) and **prune the 114 README files** down to the canonical few (CURRENT_STATE / CLAUDE / AGENTS already supersede them). Reduce the doc surface that lets agents re-derive stale truth.
7. **Refresh stale audits.** `reports/ux_pass_2026-06/04_LOGIC_EFFECTIVENESS.md` asserts the scheduler has never run and no scheduled task exists — both now false. Stale audits are a trust hazard; correct or date-stamp them.
8. **Fix the publish IP mismatch** (`18.206.62.200` in the `.bat` vs `35.164.133.170` in CURRENT_STATE) and investigate the 2026-06-23 `status: failed` maintenance run.

Every item above is consolidation, not expansion — fully aligned with the stated posture. None require new features, scoring layers, or reports.

---

## Launch verdict

**GO for launch, conditional on one pre-launch fix.** The serving architecture is clean and single-pathed: `api.py` reads `compact_opportunities.json` (+ app-state), the canonical pipeline writes it, and the frontend deploys the right app by default. The blocking condition is the **unattended weekly money channel**: before launch, money-gate the three translation engines (or disable `MochiWeeklyPipeline`) so the enabled weekly task is provably $0. The sprawl (orphan scheduler, side-channel engines, `frontend2/`, 114 READMEs) is a confusion/maintenance risk, not a launch blocker — but item #1 and #2 should ship before the task fires again on 2026-06-30.
