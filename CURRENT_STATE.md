# CURRENT_STATE.md — single source of truth

**Read this first.** `CLAUDE.md` and `AGENTS.md` cover the durable *why* of the project; this file
covers the volatile *what's true right now*. When the two disagree, this file wins —
and whoever notices the drift should fix it here. Keep this file short.

_Last updated: 2026-08-20_

## IN FLIGHT (2026-08-20 evening) — the August paid pass is mid-run

**A full pipeline run is running right now, detached** (`Start-Process`, log at
`logs/pipeline_runs/full_2026-08-20_0949_resume.log`). If it is no longer running and the
log has no `PIPELINE COMPLETE`, resume it: `python run_full_mochi_pipeline.py --resume`.
It checkpoints now, so a resume does not re-buy answers it already paid for.

- **Why the run happened:** Nin used the app on 2026-08-20 06:41 JST — her first real visit
  in a while. The Aug 3 paid pass had been skipped, so discovery was ~3 weeks stale.
- **Credit spend this month:** 204 discovery + 873 lost to a killed run (see below) +
  ~1,605 rumor_mill on the resume ≈ **~2,760 of 4,000**. Tavily resets Sep 3.
- **Two ops facts learned today, both bit hard:**
  1. **Launch long runs detached.** A backgrounded shell wrapper was reaped and took the
     whole pipeline tree with it at step 39/101. `Start-Process ... -PassThru` survives.
  2. **The laptop sleeping stalls the run silently.** It advanced 8 items in 10 hours
     (3 seconds of CPU) between 09:50 and 20:03. A full run needs ~5-6 hours awake;
     hold `ES_SYSTEM_REQUIRED` for the duration.
- **Publishing is NOT part of the pipeline.** The `MochiWeeklyPipeline` scheduled task
  (next: 2026-08-25 09:00, last result 0) runs the maintenance pipeline and scp's the data
  to the server — that is what will publish this run's output. **But translation engines are
  `PAID_STEPS` and sit at steps ~97-100**, so if the full run dies before its tail, new
  opportunities publish with English showing in Chinese mode. She browses in zh.
- **Known transient:** `tests/test_dedup_key.py::test_live_data_shows_one_tabf` fails while
  the run is half-finished (discovery re-added TABF variants at step 6-8; the step that
  collapses them is ~95). It should pass once the run completes.

## Most recent work (2026-07-06 — committed on `main`, NOT yet deployed)

A weekend of tracking/analytics work, a full pipeline run, a 4-agent system audit,
and an audit-driven fix batch. All committed and pushed to `origin/main`; **the live
site is still the 2026-07-05 deploy** — a deliberate hold pending a confidence pass
before deploying the fix batch. Highlights, newest first:
- **Scoring integrity:** `truth_aligned_score` is now a cap, not a shadow (it was
  silently overriding fresher scores on 566/653 entries); dropped a false
  "artist is a photographer" exemption that let photography-only calls escape capping.
- **Deadline logic unified:** `shape_card` now serves the strict `_deadline_passed`
  value (was serving a lenient 7-day-grace flag that contradicted the actionability
  verdict); lenient fn renamed `_deadline_date_in_past` and confined to display-blanking.
- **Field accessors:** `_contact_value`/`_has_email_contact`/`_fees_value`/`_submission_url`
  — fixed 8 relationship venues invisible to Quick Win (address in `contact_email` only)
  and 54 blank fees (value under singular `fee`).
- **Today's Focus shows 3 again:** added a High Impact fallback (the
  `immediate_best_moves` bucket is structurally near-unreachable, so that slot was
  always empty → only 2 items rendered).
- **Frontend:** all 8 lint errors cleared (dead calendar-toggle + section-icon code);
  `CareerEventWidget` kept as a documented unmounted-feature TODO.
- **Ops:** `deploy.sh` prunes `memory_backups` >30d; documented why runtime logs
  aren't shipped.
- **Full audit findings + ranked backlog:** see `project_system_audit_jul2026` memory.
  Still open: pipeline resume/checkpointing, api.py monolith split, IBM-bucket rethink,
  StatusBar new-banner placement (bottom → near top), `memory/` vs `Memory/` casing.
- **The "Mochi found N new things" banner IS live and working** (99 new opps) but
  renders at the *bottom* of the page — easy to miss; relocation is queued UI work.


## The live app

- **Production (2026-06-24):** the app is at **https://twilightdreamworks.com/mochi** — root `/` now serves a
  standalone twilight landing page (`landing/index.html` → `/var/www/index.html`) for other experiments.
  nginx config lives in repo at `deploy/nginx-mochi.conf` and was applied **manually via SSH** (deploy.sh
  reloads nginx but does not install the config). `deploy.sh` still works unchanged for app updates.
- **Frontend (dev):** React (Vite) in **`frontend/`** → http://localhost:5177 (Vite `base: '/mochi/'`)
- **Backend:** **`api.py`** (FastAPI/uvicorn) → http://127.0.0.1:8001 (Vite proxies `/api` → :8001)
- **Launch both:** `start_mochi.bat`
- Streamlit **`app.py` is retired** — reference only, not the product. (`launch_mochi.bat` still
  opens it; ignore that launcher.)

## Which frontend is current — IMPORTANT

There are two React apps. This is the thing that has caused confusion:

- **`frontend/` (port 5177) is the canonical, current frontend.** Do all work here unless told otherwise.
- **`frontend2/` (port 5178) is the v2 UX-rework sandbox** (`start_mochi_v2.bat`). Its UX improvements
  were already **ported back into `frontend/`** (commit `40ab9737`, 2026-06-18). Treat it as a finished
  experiment that fed the canonical app, not a second product.

Both apps implement all three companion pages (Mochi / Peppercorn / Saffron).

## Tests

- Frontend: `cd frontend && npm test` (Node's built-in test runner over `src/**/*.test.js`).
- Python pipeline: no formal suite — validate by running the pipeline and inspecting `memory/` JSON.

## Recent completed work

- **2026-06-25 — Saffron hybrid reframe + Build B + smaller items (Claude; branch work, NOT yet deployed).**
  Six commits, full suite 150 green, frontend build + lint 0 errors, visually verified in zh.
  - **A. Saffron hybrid reframe (Scott to review the LAYOUT).** (1) *Wiring:* opportunities re-ranked
    by fit to her current level — `api._ranked_score` now multiplies a gentle level-fit term
    ([0.85,1.15]) keyed on tier-3/tier-4 readiness; tier 1-2 always in reach, tier 3/4 rise as she
    levels. Raw quality still dominates. `career_strategy_engine` emits a new `level` block
    (current/next/progress/next_unlock); cards expose `career_tier` + `fit_band`. (2) *UI:* Career
    Readiness leads with an earned Level badge + what she's built, ONE next-unlock card (gap form
    inline), remaining gaps collapsed, level-up celebration (localStorage-gated), newly-in-reach
    badges, positive advanced-state line when maxed; tier bars demoted to a disclosure.
  - **B. Free-discovery scraper** (`engines/free_discovery_engine.py`): the $0 Tavily alternative —
    fetches `discovery_sources.py` over plain HTTP, harvests candidate calls, dedupes, STAGES to
    `memory/free_discovery_candidates.json` (never touches live data). Live smoke reached AWS+NWS.
  - **Smaller items:** TABF now dedups to one card (`_dedup_key` folds year/"Exhibitor Call"/TOKIO);
    Saffron dead counts click through to Discover; the zh Press-pitch `contact` leak fixed; the
    **stranded preference loop** fixed — `peppercorn_preference_engine` refactored to idempotent
    pure functions applied at SERVE time (`api.load_opportunities`), so her server-side preference
    edits take effect on the next request (both add AND remove), on copies (cache never mutated).
  - **Persona/UX pass:** profile tab's three peer-COMPARISON sections default-collapsed to reduce the
    "everyone's ahead of me" load (reversible — Scott to sanity-check). Full report +
    remaining recommendations in `_reviews/2026-06-25_UX_persona_pass.md`.
  - **NOT deployed.** Career report regenerated locally. Next: Scott reviews A's layout; then deploy.

- **2026-06-25 — COST/CADENCE DECISION (Scott), supersedes the "MONTHLY" note below:** the full *paid*
  discovery pass runs **QUARTERLY (~every 3 months), and only when she's actually using the app** (check the
  visit telemetry / Discord feed first — if she's inactive, skip it). A full pass is ~**$26 of Tavily, all
  DISCOVERY web-search**; verification is free (HTTP `urllib`, not Tavily). $26/quarter ≈ $9/mo, under budget.
  Between passes the **free weekly maintenance pipeline** (`run_maintenance_pipeline` = PIPELINE − PAID_STEPS)
  keeps deadlines/verification/bucketing fresh at $0. Open idea: replace broad Tavily discovery with a free
  scraper over her known JP watercolor source URLs; keep Tavily only for occasional new-venue hunting.

- **2026-06-25 — Discord ops feed + her-edit durability, DEPLOYED & verified live (Claude):** Production
  (api at `/opt/mochi`, restarted; site 200, API 200) now runs three things. (1) **Her profile edits
  auto-refresh her drafts** — a Peppercorn statement edit propagates into `artist_master_profile.json` and
  fires a background draft regen (`engines/regen.py`); `ibm_email_writer.py` re-targets all eligible opps
  when `email_drafts_stale` is set and clears it on a clean run. Server now has `anthropic` + key, so regen
  *can* run server-side — **NOT yet exercised by a real edit; verify.** (2) **Discord notifications**
  (`engines/notify.py`; webhook in `/opt/mochi/.env` as `MOCHI_DISCORD_WEBHOOK`): end-of-regen result + a
  **live page-navigation feed** (`POST /api/event` + a beacon in `App.jsx`) posting every open/page-move,
  content-blind (`engines/visit_tracking.py`). (3) **Per-edit timestamped backups** of all her editable files
  into `memory/backups/` (`engines/backups.py` via `_save_her_data`), and **deploy.sh no longer clobbers
  server memory** — it snapshots `/opt/mochi/memory` → `memory_backups/<ts>/` and seeds memory only when
  absent. Fully unit-tested (profile_sync/notify/regen/visit_tracking/backups); 15 frontend tests + build green.
  **Deploy gotcha (hit & fixed):** api.py imports the `engines/` modules, so deploy.sh MUST ship them or the
  API 502s on import — `backups.py` was missed and crash-looped prod once before being added to the ship list.
  **Caveats:** server-side regen untested with a real edit; pre-handoff checklist items beyond these remain open.
- **2026-06-24 — monthly pass + serve-time quality guards (Claude):** Ran the full pipeline (the monthly
  update pass): **419 opportunities live**, fresh discovery + decay archiving. **Cadence is now MONTHLY**
  (opportunities are long-horizon) — and **before each pass, raise the Tavily pay-as-you-go LIMIT on the
  dashboard**: this pass hit the cap ~⅓ in (718 failed lookups) so verification degraded for the back
  two-thirds (absorbed gracefully into the Watch List; actionable surface stayed verified). Added serve-time
  guards in `api.py`: `_deadline_passed()` (hides passed, non-recurring, non-relationship deadlines from
  actionable sections — evaluated per request so it stays correct daily, since we only search monthly) and
  `_listing_artifact()` (drops CuratorSpace/"Browse opportunities" index captures; also rejected at ingestion
  in `candidate_quality_gate.py`). `url_verification_engine` got a 14-day `last_verified` TTL. Saffron path
  sections (Licensing/Grants/Revenue/Press) gained a "Where to start" callout; revenue corrected to her actual
  **BASE shop** (gegyjiji.base.shop, not SUZURI). Saffron zh **auto-translation wired** (engine →
  `memory/translation_cache.json` → api `_i18n`, 100% payload coverage). Hero rotating classical-Chinese poem;
  dismissible companion intros (Mochi/Saffron/Peppercorn). **Known limitation:** email drafts are write-once
  (`ibm_email_writer` only fills *missing* `email_ja`/`email_en`) AND Peppercorn saves the statement to
  `peppercorn_profile.json` while the writer reads `artist_master_profile.json` — so editing her statement does
  **not** refresh existing drafts.
- **2026-06-22 — REVERTED the Codex illustrated section headers** (the two 2026-06-21 entries just below):
  Scott didn't like them. `frontend/public/section-art/*.webp` removed, header CSS restored. **Those headers are
  not live** — the two notes below are historical only.

- **Compact illustrated watercolor section headers** (Codex, 2026-06-21; commit `1940cba3`): replaced
  Mochi's emoji-plus-title browse headings with 11 section-specific watercolor scenes. Localized live titles
  and counts nest inside each image's negative space; descriptions remain below. Headers are exactly 72px
  desktop / 56px mobile, and the optimized WebP asset set is 710KB total. No recommendation behavior, copy,
  API, generated data, `frontend2/`, or Streamlit changes. Verified with desktop/mobile screenshots, 15 passing
  frontend tests, and a successful production build; lint has 0 errors and the same unrelated pre-existing
  Peppercorn unused-disable warning. The known `StatusBar` mobile overflow remains unchanged.
- **Mochi persona-led UX observation + watercolor title accents** (Codex, 2026-06-21; commit
  `f3d72f2d`): reviewed the rendered canonical app at desktop and 390px mobile for a highly driven
  watercolor artist who is easily emotionally overwhelmed. Added quiet, irregular pigment washes to
  Today's Focus and Mochi browse-section titles only; no behavior, copy, data, `frontend2/`, or Streamlit
  changes. Main audit finding: the tone is calm, but the browse page is an endurance scroll (8,943px
  desktop / 17,735px mobile) with repeated card grids and some strongest-pick/category duplication, so
  accumulated possibility is the emotional-load risk. Also found a pre-existing 390px mobile overflow:
  `StatusBar` expands the document to 659px; quick-nav is intentionally horizontally scrollable. Verified
  15 frontend tests, production build, desktop/mobile screenshots; lint has 0 errors and one unrelated
  pre-existing Peppercorn unused-disable warning.
- **4 background-agent edge fixes** (merged + verified by Claude, 2026-06-19): (1) **CRM follow-up date bug** —
  a malformed `last_contacted` no longer surfaces a contact as overdue (which spammed the Quick Win slot);
  extracted pure `is_overdue_followup()` + 11 tests (`71b8b65a`). This was the one launch-audit finding that
  turned out *real*. (2) **Code-split** Saffron/Peppercorn pages — main bundle **520 → 362 kB** (`8f489e0a`).
  (3) **Email drafts now labelled "Draft — review and edit before sending"** (en/ja/zh) in `OppDetailPanel`
  (`7e194236`). (4) **Log rotation** — both runners prune run logs older than 30 days (`37c70eba`). Combined
  suite green: 44 Python tests, 15 frontend, lint clean, build emits split chunks. The two frontend changes
  (code-split, draft label) still want the visual smoke-test.
- **Launch-readiness fixes** (Claude, 2026-06-19): (1) **`deploy.sh` defaulted to shipping `frontend2/`**
  (the sandbox) — fixed the default to `frontend/` (canonical), so `deploy.sh` / `make_ready.bat` now ship
  the app with all current work. This was a launch trap: none of the recent frontend/ work would have reached
  the server. (2) Wired Peppercorn's orphaned `quickLog` to one-tap event logging (commit `cbf49d39`).
  (3) Verified the launch-audit's "backend error-handling" concerns are **non-issues** — `api.py` guards every
  file read (returns graceful empties, not 500s) and `TodaysFocus` already has warm loading/empty states
  (`tf.noItems` = "Nothing urgent. Come back tomorrow."). The audit over-flagged here, like the Saffron-hero
  false alarm. (4) Updated `docs/HANDOFF.md` with current state + a server-autonomy verification checklist.
- **Frontend lint cleanup** (Claude, 2026-06-19): `npm run lint` now exits clean (was 29 errors + 1 warning).
  Real fixes: moved conditionally-called `useLanguage` above early returns in `TodaysFocus` + `SaffronPage`
  (rules-of-hooks — genuine bug); removed 5 unused vars and 3 duplicate `sf.label.posts` translation keys
  (the dead shadowed copies). Justified `eslint-disable` for legitimate patterns the new rules over-flag: 4
  `setState`-in-effect (async-data → local-state sync), 1 callback-ref, 1 fast-refresh hook-beside-provider,
  1 **orphaned `quickLog` handler** (suppressed + flagged — it's a quick-log event handler with no UI wired
  to it; decide: wire it up or delete). Build + 15 frontend tests green. **Not visually smoke-tested — verify
  Peppercorn/Saffron still render after the hook-order changes.** Note: surviving zh/ja `sf.label.posts`
  labels ("条帖子"/"件の投稿") read awkwardly standalone — a content cleanup, not lint.
- **Mochi "People to reach out to" view** (Claude, 2026-06-19, tests-first; commit `687c4931`): surfaces the
  52 researched relationship contacts (previously `/api/contacts` + data only, NO UI) as a third view on
  Mochi's page (cards / calendar / **people**) — name, `why_relevant`, type/city pills, and a mailto/website
  reach-out link, sorted by priority. Pure display logic in `frontend/src/utils/relationshipTargets.js`
  (5 tests). Read-only; no outreach tracking yet. en/ja/zh strings added. Builds clean, 15 frontend tests green.
  **Caveat: not yet visually smoke-tested in a running browser** — verify the People toggle renders before launch.
- **Verification edge-case cleanup** (2 background agents, reviewed + merged by Claude, 2026-06-19, tests-first):
  (1) `engines/url_verification_engine.py` now returns `no_url` instead of `ok` when an opp has no
  `official_website`/`submission_page` — root cause was a discovery-trail `source_url` being live-checked and
  passing, so 5 URL-less opps read as verified. (2) `engines/deadline_normaliser.py` now parses 2-digit-year
  dates (`5/26/26`) and marks yearless month/day deadlines `unconfirmed_year` + unverified (16 opps, all in
  non-surfacing buckets). Full suite **33 tests green**. Merged commits `c5aa6fa9`, `87949993`. No data rewritten;
  applies on next pipeline run.
- **Verification hardening: past-deadline detection** (Claude, 2026-06-19, tests-first): added a canonical
  deadline date parser (`parse_deadline_date` / `deadline_is_past`) to `engines/deadline_normaliser.py`.
  `classify_deadline` and `targeted_verification_agent._deadline_is_real` now refuse to mark an already-passed
  deadline as `deadline_verified`, and `deadline_normaliser.main()` self-corrects previously-verified-but-expired
  entries (`deadline_verified=False`, `deadline_past=True`, which the readiness layer already demotes). 10 new
  unit tests. **Offline impact on the 380 cached opps: 103 of 279 "verified" deadlines are actually past** and
  get downgraded — including UTRECHT ("1 July 2025"), which was in `immediate_best_moves`. No data written and
  no live calls yet: the fix applies on the next pipeline run, or run `python engines/deadline_normaliser.py`
  (offline, no network) to apply in-place, then redeploy.
- **Read-only verification-layer audit** (Codex, 2026-06-19; scope commit `772700ed`; reviewed by Claude):
  Canonical in-pipeline path = `url_verification_engine` (step 9, URL-reachable only) → `opportunity_truth_checker`
  (21) → `fee_text_extractor`/`deadline_normaliser`/`submission_page_harvester` (41-43) → `verification_report_engine`
  (45) → `targeted_verification_agent` (83, live HEAD/GET + closed-call phrases) → `dead_url_pruner` (85). Core
  finding: **"URL ok" is well-proven (380/380), "actually open & actionable now" is not** (`verification_status=verified`
  only 135/380; deadline 279, fees 196, contact 139, submission 200). Non-ok URLs (57) are correctly quarantined
  (0 reach ready/strongest-picks). Sprawl: side-channel paths (`web_verification_engine`→`memory/verified_opportunities.json`,
  `opportunity_verification_engine`→`deploy_data/verified_opportunities.json`, the queue/importer/merger tools)
  duplicate verification without feeding the app. **Claude-verified:** `api.py` reads only `compact_opportunities.json`
  (the side-channel `verified_opportunities.json` files are dead to the app); the active path engines are confirmed
  wired in `run_full_mochi_pipeline.py`. **Caveat for consolidation:** those side-channel engines are still referenced
  by `scripts/runners/*` and `scripts/scheduler.py` (which calls Claude-using `deep_verification_agent`) — trace/retire
  those callers before archiving, and check whether `scheduler.py` is actively running (possible quiet Claude spend).
  Recommendation: keep one canonical path on `compact_opportunities.json`, harden `targeted_verification_agent`'s
  cached-text parsing (tests-first, free) before any deliberate live pass, then archive the side-channels (move to
  `archive/dead_code/`, don't delete). No code changes, no Tavily, no paid run.
- **Read-only readiness honesty audit** (Codex, 2026-06-19; scope commit `2b522695`): audited all
  380 cached opportunities in `deploy_data/compact_opportunities.json` with `assess_actionability`.
  No ready-status leaks and no strongest-picks leaks were found for URL error/bad/missing,
  closed/permanently closed, or non-relationship `deadline_past` conditions. Distribution:
  `ready=99`, `check_before_acting=67`, `review=130`, `closed_or_stale=84`. Native-medium unknown is
  `224/380` (`58.9%`), limiting artist-fit quality until medium tagging is improved. No generated JSON
  edits, no live web/Tavily checks, no paid pipeline run.
- **Backend readiness contract** (Codex, 2026-06-19; commit `50e0bfd7`): added tested backend
  `actionability_status`, `review_flags`, and `recommendation_reasons` shaping via
  `recommendation_readiness.py`; `api.py` now emits these fields and the current `frontend/` consumes
  them instead of treating browser heuristics as canonical. Browse strongest picks now keeps 6
  candidates for curated breadth. No generated JSON edits, no live web/Tavily checks, no `frontend2/`,
  no retired Streamlit.
- **Photography surfacing fix** (Codex, 2026-06-19): pure photography opportunities are blocked at
  the current app API boundary and rejected by the future bucket engine rule. This fixes cached
  `photo_open_call` / `native_medium: photography` rows appearing in the watch list for a watercolor
  painter. No generated JSON edits, no live web/Tavily checks, no `frontend2/`, no retired Streamlit.
- **Read-only strongest-picks audit** (Codex, 2026-06-19; scope commit `c1cb5cad`): inspected
  existing `/api/opportunities`, `deploy_data/compact_opportunities.json`, and the current frontend
  helper only. No generated JSON edits, no live web/Tavily checks, no paid pipeline run. Main finding:
  current strongest picks mostly satisfy cached readiness signals, but backend readiness fields are
  still needed because the frontend helper can treat contact-verified `needs_reverification` items as
  ready and because browse breadth must label/order uncertain items rather than delete them.
- **Mochi recommendation quality pass** (Codex, 2026-06-19): `frontend/src/utils/recommendationQuality.js`
  and `recommendationQuality.test.js` are complete. Mochi now derives internal readiness/fit signals,
  surfaces a small "strongest picks" band, sorts section cards through that quality layer, and lets
  feedback influence the current board without showing numeric scores to the artist.

## In flight (work not finished — don't assume it's done)

- **⭐ PRE-HANDOFF READINESS PASS pending (external review, 2026-06-24 night).** Scott had an outside review
  setup (not the core mochi chat) run a 5-agent code review + a live-site walk in Chinese. He is **NOT** sending
  the app to GEGYjiji yet. The prioritized action list is **`_reviews/2026-06-24_PREHANDOFF_CHECKLIST.md`** —
  read it first; the 5 facet reports are alongside it in `_reviews/`. Headline findings: (1) the all-day
  translation loop was a **render bug, not a coverage gap** — Saffron's `CareerTimeline`/`PricingIntelligence`
  render raw English fields instead of the existing `_zh` data (use `locF`, thread `lang`); only `had_zh` is
  genuinely missing. (2) Money gate: translation engines aren't in `PAID_STEPS` and the enabled
  `MochiWeeklyPipeline` task fires ≈Thu 6/30 — gate or disable. (3) Durability: server autonomy is laptop-driven
  (`last_run.json`=failed 6/23) and the Peppercorn→email-draft feedback loop is broken. **Always verify against
  the rendered page, not the engine's self-reported coverage.**
  - **Session 2 (2026-06-25) — DEPLOYED & verified live:** "Why Mochi picked it" moved off the card face into
    Details under "Mochi notes" (`5c48a496`); Saffron 日历 is now a LITERAL month-grid calendar with every list
    row linked + localized (`5c48a496`); Saffron money-tab English killed — localize the revenue/grant/licensing
    components + translate the missing grant country/amount/deadline & labels (`9f980713`, 31→11 English, all
    remaining are proper nouns). Verified on prod: calendar grid (18 deadline-days), 171/171 list links, card
    face clean, Mochi-notes in Details, money tab proper-nouns-only, 0 console errors.
  - **Overnight pass 2026-06-25 — DEPLOYED & verified live** (via `bash deploy.sh`, atomic rsync; Saffron
    confirmed not-blank, 0 console errors, 42 cards link out): every OppCard now has a click-through link
    (`b2bdec21`), the Mochi calendar view-toggle is sticky so you can get back (`7cb349f6`), `status=closed`
    excluded from Immediate Best Moves (`d9444cd1`). Money gate closed (`68c5febd`) — config-only, not part of
    the deploy package (affects the laptop pipeline, not the server). Remaining items + what was deliberately
    left for supervision are at the top of `_reviews/2026-06-24_PREHANDOFF_CHECKLIST.md`.

## Pre-launch backlog (curated from the 2026-06-19 launch-readiness audit)

The audit agent was a useful prompt but **unreliable on specifics — verify before acting** (it raised
several "blockers" that turned out to be false).

**Done:** lint clean; `quickLog` wired; **`deploy.sh` now ships `frontend/`** (was defaulting to the
`frontend2/` sandbox — a launch trap); People view; past-deadline verification; HANDOFF refreshed.

**Debunked — DO NOT re-chase:** "missing Saffron hero image" (`saffron_hero.png` exists); "api.py has
unguarded file reads" (all guarded with `.exists()`, return empties not 500s); "`/api/today` shows a
spinner not an empty state" (`TodaysFocus` already has a warm empty state — `tf.noItems` = "Nothing
urgent. Come back tomorrow.").

**Real / open before launch:**
- **Visual smoke-test Peppercorn + Saffron** after the recent hook/refactor changes (see HANDOFF "final once-over").
- **Live verification pass + email-draft generation** — paid, via `make_ready.bat`; needs Scott's go.
- **Confirm server autonomy is switched on** (cron / systemd / `.env` keys / webhook) — SSH checklist in HANDOFF.

**Minor / nice-to-have:**
- zh/ja: some server-side strategy + submission-followup strings render English-only (known gap) — still open.
- _Done 2026-06-19 (4 agents): draft-email labelling, frontend code-splitting, log rotation, CRM follow-up date bug._

## Working together (Claude + Codex)

- Both agents read their own guide (`CLAUDE.md` / `AGENTS.md`) **plus this file**. This file is the
  shared handshake — update it when something material changes (which frontend is current, how to run,
  what's mid-build) so neither agent re-derives stale state from scratch.
- Don't develop the same feature in both `frontend/` and `frontend2/`. `frontend/` is the one.
- Before making non-trivial changes, record the intended scope here if it could affect another agent's
  work. Keep notes short but concrete: active files, why the work is in-bounds, and how it will be
  verified. When the work finishes, move the note to Recent completed work with the commit hash.
- Project-boundary checks should reference this file plus `AGENTS.md` / `CLAUDE.md`: current live app,
  retired Streamlit status, the data patch rule, consolidation-over-expansion posture, and the rule
  that `frontend2/` is a sandbox, not a second product.
