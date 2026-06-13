# API Logic Audit — api.py (2026-06-13, agent-verified)

## ✅ SYSTEMIC FIXES ROUND 2 (2026-06-13 morning — "no interference" pass)
1. **Tier-4 hard guard in the bucket engine** (`engines/exclusive_strategy_bucket_engine.py`):
   `career_tier == 4` now returns stretch_targets BEFORE any rule that can emit
   immediate_best_moves (the old check was a name list evaluated too late).
   Engine re-run regenerated the data: NWWS rerouted to stretch_targets, IBM 13→12,
   verified live through /api/opportunities. Survives any fresh pipeline run.
2. **Follow-up loop exists now** (`api.py` /api/today): pending submissions 14–90
   days old with no follow-up become the Quick Win ("You applied to X N days ago…",
   localized zh/ja), computed fresh per request. Priority: overdue application →
   stale CRM contact → regular quick win. New `PATCH /api/submissions/{id}` records
   outcome / `followed_up` (which auto-clears the nudge). Unit-tested with synthetic
   log: 20-day pending fires; 5-day and already-followed entries skipped.
   v2 FocusCard shows a localized "Follow-up" label for these cards.
3. **Verification wired into the pipeline** (`run_full_mochi_pipeline.py`):
   `targeted_verification_agent.py` (pure HTTP — no Tavily/Claude despite the name)
   inserted after final_score_guard. Every future pipeline run now re-verifies
   URLs/deadlines. (A manual one-off run was blocked by the permission classifier
   on a mistaken Tavily assumption — harmless; next pipeline run covers it.)
4. **IBM draft coverage rule** (`engines/ibm_email_writer.py`): targets now include
   everything in immediate_best_moves regardless of tier (was Tier 1-2 only — why
   portal competitions never got artifacts). ⚠ Generation BLOCKED: the Anthropic
   API key has no credits ("credit balance too low"). After top-up:
   `python engines/ibm_email_writer.py --limit 15`.
5. **Weekly scheduler prepared, not registered**: `run_weekly_pipeline.bat` (logs to
   logs/pipeline_runs/, writes memory/last_run.json). Registering a persistent
   Windows task requires explicit user action:
   `schtasks /Create /TN "MochiWeeklyPipeline" /TR "C:\ScottStuff\GalleryAgentAI\run_weekly_pipeline.bat" /SC WEEKLY /D TUE /ST 09:00 /F`
   Note: pipeline runs consume Tavily quota + Claude API credits.

## ✅ FIXES APPLIED THIS SESSION (2026-06-13, backend)
1. **/api/today staleness gate** (api.py): quick_win fallback now requires
   `not _deadline_past(x)`; all four stretch_goal candidate paths now require
   `not _deadline_past(x)`. Evergreen relationship venues with stale deadline
   *fields* now serve `deadline:""` in today-cards (residue, not an action date).
   NOTE: API server restart still required for these to take effect (running PID
   predates the edit). Restart: kill the python on :8001, `python api.py`.
2. **False follower claim fixed (engine rule + data patch together, per Data
   Patch Rule):** `engines/ibm_email_writer.py` (2×) and
   `engines/why_it_fits_engine.py` (2×) said ~90k Instagram followers — that's
   the Twitter number; Instagram is ~26k (see CLAUDE.md Artist Social Media).
   Patched generated data containing the claim: deploy_data/compact_opportunities.json
   (4 strings), memory/exclusive_strategy_buckets.json (2). Historical md reports
   left as-is (pipeline regenerates them; engines now produce correct number).

## Root cause of stale Today's Focus (confirmed)
`/api/today` (api.py:2317) applies `_ibm_eligible()` ONLY to the high_impact slot
(api.py:2321-2327). Two slots are ungated:
- **quick_win fallback** (api.py:2340-2346): selects from raw `load_opportunities()`
  with only a contact-"@" check — no `_deadline_past()` check.
- **stretch_goal** (api.py:2370-2400): selects from stretch_targets/watch_list/
  research_needed buckets — no deadline check at all.

12 opportunities with July/Nov 2025 deadlines exist in current data, including the
two observed live ("UTRECHT 1 July 2025" IBM; "2026 Global Grant Cycle" 2025-11-19).

**Fix (engine rule):** apply `_ibm_eligible(x)` (or at minimum `not _deadline_past(x)`)
to quick_win fallback and stretch_goal candidate lists. For relationship-category
quick wins (evergreen venues), the existing carve-out in `_ibm_eligible` already
handles contact-verified entries.

Also ungated: category sections + watch_list inside `bucket()` (api.py:631-644) serve
past-deadline items mixed with live ones (v2 UI guards this client-side).

## today_role generation
No engine computes Today's Focus; slots are picked at request time inside /api/today
(`_card()` api.py:2428-2435). No daily rotation, no completed-item avoidance beyond
submission-log suppression inherited from IBM list.

## Email draft coverage (deploy_data/compact_opportunities.json, n=379)
- email_en: **27 (7.1%)** · email_ja: **30 (7.9%)** · email_zh: **0** (writer engine
  `engines/ibm_email_writer.py` explicitly sets zh empty, line ~285; targets Tier 1-2
  lacking drafts, line ~255; uses Claude API)
- why_this_fits_short: 379/379 · three_bullets: 379/379
- deadline_verified: 275 (72.6%) · contact: 137 (36.1%) · submission_page: 200 (52.8%)
→ 93% of "Copy email" actions would fall back to the generic api.py templates.

## Endpoint inventory
GET /api/opportunities (649, gated IBM + sections) · POST /api/feedback (673) ·
GET /api/feedback/insights (747) · POST /api/feedback/suppress-category (791) ·
GET/POST /api/submissions (820/827) · GET/POST /api/contacts (881/897) ·
PATCH /api/contacts/update + /api/contacts/{name} · GET /api/contacts/lookup (1000) ·
GET /api/saffron (1019-2165) · GET/POST /api/peppercorn (2210/2256) ·
GET/POST /api/career_events (2265/2273) · GET/POST/DELETE /api/exhibition_log
(2286-2306) · GET /api/today (2317) · GET /api/health (2472) ·
POST /webhook/deploy (2486) · GET /api/career_strategy (2500 — serves
memory/career_strategy_report.json, generated by engines/career_strategy_engine.py).
