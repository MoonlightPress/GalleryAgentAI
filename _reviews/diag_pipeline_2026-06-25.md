# Pipeline + Engine Architecture Diagnostic — 2026-06-25

**Scope:** read-only. No edits, no paid steps, no Tavily/Claude calls. Ran the two offline unit
test modules only (`tests/test_deadline_normaliser.py`, `tests/test_targeted_verification_agent.py`).

**Method:** read `run_full_mochi_pipeline.py` (PIPELINE + PAID_STEPS), `run_maintenance_pipeline.py`,
`smart_pipeline_runner.py`, `scripts/scheduler.py`, `api.py` (serve path), the two verification
engines, the side-channel writers, and the decay engine. Confirmed in-PIPELINE membership
programmatically.

---

## Data flow (confirmed)

```
discovery (Tavily, PAID) → ingestion/quality-gate → enrichment → scoring tail →
url_verification_engine (step 9, URL-reachable only) → opportunity_truth_checker →
fee/deadline/submission harvesters → verification_report_engine →
targeted_verification_agent (HTTP HEAD/GET + closed-call phrases, free) →
dead_url_pruner → exclusive_strategy_bucket_engine → translation engines (PAID, last) →
**deploy_data/compact_opportunities.json**
```

- **The API serves exactly ONE file:** `deploy_data/compact_opportunities.json`
  (`api.py:874, 911, 1034, 1086, 1472, 2457, 2951`). It never reads any `verified_opportunities.json`.
- Pipeline engines mutate `deploy_data/compact_opportunities.json` in place (e.g.
  `opportunity_status_engine.py:8`, `opportunity_decay_engine.py:7`).
- **Side-channel writers that the app never reads (DEAD to the app):**
  - `web_verification_engine.py:11` → `memory/verified_opportunities.json`
  - `engines/opportunity_verification_engine.py:6` → `deploy_data/verified_opportunities.json`
  - `enriched_to_compact_opportunities.py` → writes compact, but is **not in PIPELINE**.
  None of these three appear in `run_full_mochi_pipeline.PIPELINE` (verified).

---

## Prioritized findings

### P0 — CRITICAL

**P0-1 — `scripts/scheduler.py` is an ungated money-spending orphan.**
Its `WEEKLY_PIPELINE` calls `deep_verification_agent.py` (Claude) and `rumor_mill_engine.py`
(Tavily); its `monthly` tier shells out to the full paid pipeline. None of this passes through
`PAID_STEPS` — `run_pipeline()` (`smart_pipeline_runner.py:36`) has no money awareness; gating
lives only in the *maintenance* wrapper, which the scheduler bypasses. If anything (cron/Task
Scheduler/manual) fires `scheduler.py`, it spends with nobody watching.
*Evidence:* `scripts/scheduler.py:52-53` (deep_verification_agent + rumor_mill in WEEKLY),
`:67-68,102-104` (monthly→full pipeline), `smart_pipeline_runner.py:36-54` (no PAID_STEPS check).
*Fix:* Archive `scheduler.py` to `archive/dead_code/` (it predates the monthly/PAID_STEPS model —
CURRENT_STATE says cadence is now MONTHLY-by-hand), OR make it import and skip `PAID_STEPS`.
Confirm nothing schedules it before relying on "it isn't running."

**P0-2 — `deep_verification_agent.py` (Claude) is reachable ONLY via the orphaned scheduler.**
It is not in PIPELINE and not in PAID_STEPS (PAID_STEPS can't gate it because it's never a
full-pipeline step). It is pure latent Claude spend gated behind P0-1.
*Evidence:* `scripts/scheduler.py:53`; absent from `run_full_mochi_pipeline.py`.
*Fix:* Archive alongside scheduler, or fold its capability into the in-pipeline
`targeted_verification_agent` (free HTTP) if its extraction is still wanted.

### P1 — HIGH

**P1-1 — 3 failing tests = real verification-logic gap (NOT stale tests): venue exemption
unimplemented in the pipeline engines.**
`tests/test_deadline_normaliser.py` (VenueExemptionTests) and
`tests/test_targeted_verification_agent.py` (test_venue_past_deadline_is_still_real) expect that an
evergreen venue (`category="bookstore_gallery"`) with a stale date is NOT flagged passed / IS still
"real". The engines don't support it:
- `classify_deadline(blob, deadline_field, today=None)` has **no `category` parameter** → `TypeError`
  (2 errors). `engines/deadline_normaliser.py:128`.
- `_deadline_is_real(opp, today)` ignores `opp["category"]` → returns `False` for a past-dated
  bookstore_gallery (1 failure). `engines/targeted_verification_agent.py:81-93`.
This is a genuine drift: the serve layer ALREADY exempts evergreen venues
(`api.py:_deadline_passed` returns False for `RELATIONSHIP_CATEGORIES`, `api.py:806`), but the
pipeline engines do not — so a relationship/consignment venue with an old event date gets
`deadline_verified=False` / demoted at pipeline time even though it's evergreen. The behavior is
inconsistent between engine and serve layers; the tests encode the correct (serve-layer) intent.
*Evidence:* test run output — 2 ERROR (`unexpected keyword argument 'category'`), 1 FAIL
(`False is not true`); `engines/deadline_normaliser.py:128`, `engines/targeted_verification_agent.py:81`.
*Fix:* Add an optional `category=None` param to `classify_deadline` and `deadline_is_past`/the
venue check, exempting `RELATIONSHIP_CATEGORIES` (bookstore_gallery, consignment, etc.) from
`passed`/`deadline_past` — mirroring `api.py:806`. Have `_deadline_is_real` read `opp["category"]`.

**P1-2 — No freshness/prune step in the full pipeline writes closed/past opps out of the served
file; `opportunity_decay_engine.py` is scheduler-only.**
Past-deadline opps persist in `deploy_data/compact_opportunities.json` indefinitely. The full
pipeline's only prune is `dead_url_pruner.py` (URL-reachability, not deadline). `opportunity_decay_engine.py`
is NOT in PIPELINE — it runs only from `scheduler.py` DAILY (which per P0-1 / `last_run.json=failed
6/23` isn't running). Past opps are *hidden* from actionable sections at serve time
(`api.py:_deadline_passed` applied at `:943` IBM and `:963` category sections — robust, multi-date,
per-request), and fall into the Watch List by design. So the user-facing surface is correct, but the
**stored data never decays**, the file grows monotonically, and any consumer that reads the raw file
(or a future browse-all view) sees stale closed calls.
*Evidence:* `opportunity_decay_engine.py` absent from PIPELINE (verified); `scripts/scheduler.py:44`
(decay only in DAILY tier); `api.py:943,963` (serve-time hide, not data prune).
*Fix:* Add `opportunity_decay_engine.py` (and/or a deadline-archiver that sets
`status=closed_this_cycle` for non-venue past deadlines) to the full PIPELINE tail, so the served
file is pruned at pipeline time rather than relying solely on the serve-time filter.

### P2 — MEDIUM

**P2-1 — Side-channel verification engines duplicate work and write dead files.**
`web_verification_engine.py` (→`memory/verified_opportunities.json`) and
`engines/opportunity_verification_engine.py` (→`deploy_data/verified_opportunities.json`) re-do
verification but write files the API never reads. They are not in PIPELINE, so they don't run in a
normal pass — but they remain live, importable, and a maintenance/confusion hazard (and at least one
duplicates Tavily/HTTP work). The 2026-06-19 audit already flagged this; still present.
*Evidence:* `web_verification_engine.py:11`, `engines/opportunity_verification_engine.py:6`; neither
in PIPELINE; `api.py` reads only `compact_opportunities.json`.
*Fix:* Move both to `archive/dead_code/` after confirming `scripts/runners/*` don't depend on them.
Keep exactly one canonical verification path on `compact_opportunities.json`.

**P2-2 — `submission_link_hunter.py` is referenced by the orphaned scheduler but deliberately
removed from the live pipeline** (it read the dead `verified_opportunities.json`).
The live PIPELINE comment (`run_full_mochi_pipeline.py:17-18`) documents its removal; the scheduler
WEEKLY still calls it (`scripts/scheduler.py:54`). Another reason P0-1's scheduler is stale.
*Fix:* Resolved by archiving the scheduler (P0-1).

### P3 — LOW / HOUSEKEEPING

**P3-1 — `smart_pipeline_runner.run_pipeline` has no money guardrail of its own.**
Gating is enforced only by which list is passed in (full vs maintenance). Any caller assembling its
own list (scheduler, ad-hoc) can run paid steps. Consider having `run_pipeline` accept/consult
`PAID_STEPS` and refuse paid steps unless an explicit `allow_paid=True` is passed.
*Evidence:* `smart_pipeline_runner.py:36-54`.

**P3-2 — Maintenance pipeline correctness: PAID_STEPS now correctly includes the 4 translation
engines** (the 2026-06-24 money-gate fix is present), so `run_maintenance_pipeline.py`
(`= [s for s in PIPELINE if s not in PAID_STEPS]`) is safe for unattended runs. No action — noting
it as verified.
*Evidence:* `run_full_mochi_pipeline.py:123-142` (PAID_STEPS: 4 Tavily + ibm_email_writer +
why_it_fits + 4 translation engines), `run_maintenance_pipeline.py:11`.

---

## PAID-step gating audit (every Claude/Tavily caller reachable in the full pipeline)

| Engine | API | In PIPELINE | In PAID_STEPS | Verdict |
|---|---|---|---|---|
| japanese_chinese_discovery_engine | Tavily | yes | yes | gated ✓ |
| grant_discovery_engine | Tavily | yes | yes | gated ✓ |
| rumor_mill_engine | Tavily | yes | yes | gated ✓ |
| rumor_mill_expansion_runner | Tavily | yes | yes | gated ✓ |
| ibm_email_writer | Claude | yes | yes | gated ✓ |
| why_it_fits_engine | Claude | yes | yes | gated ✓ |
| content_translation_engine | Claude | yes | yes | gated ✓ |
| opp_strategy_translation_engine | Claude | yes | yes | gated ✓ |
| saffron_translation_engine | Claude | yes | yes | gated ✓ |
| contact_translation_engine | Claude | yes | yes | gated ✓ |
| **deep_verification_agent** | **Claude** | **no (scheduler-only)** | **n/a** | **UNGATED — P0-2** |
| targeted_verification_agent | none (HTTP) | yes | n/a | free ✓ |

The full/maintenance split is sound. The only money-leak vector is the **orphaned scheduler path**
(P0-1/P0-2), which lives entirely outside the PAID_STEPS model.

---

## One-line summary

The PAID_STEPS gating on the canonical full/maintenance pipelines is correct and complete; the only
money risk is the stale `scripts/scheduler.py` (+ `deep_verification_agent.py`) which sidesteps it —
archive both. The 3 failing tests are a **real** engine bug (venue-exemption implemented at serve
time but missing in `deadline_normaliser`/`targeted_verification_agent`), not stale tests. The app
serves exactly one file (`deploy_data/compact_opportunities.json`); the two `verified_opportunities.json`
side channels are dead and should be archived. Past-deadline opps are correctly hidden at serve time
but never pruned from the stored file because `opportunity_decay_engine.py` isn't in the live pipeline.
