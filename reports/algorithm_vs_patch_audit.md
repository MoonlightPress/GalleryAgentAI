# Algorithm vs. Data-Patch Audit — Last 20 Commits

**Date:** 2026-06-10
**Question for every change:** does it survive a fresh pipeline run?

- **A — Engine rule:** code (api.py, `engines/`, `frontend/`, config) or a fix to a hand-curated *source* file. Survives a from-scratch pipeline run, or is the canonical input the pipeline reads.
- **B — Data patch:** a manual edit to a file the pipeline *regenerates* (notably `deploy_data/compact_opportunities.json` and the generated `Memory/*.json` + `reports/*.md`). Overwritten on a fresh run unless an engine rule reproduces it.

## The core architectural finding

**Correction (2026-06-10):** an earlier draft of this audit claimed `exclusive_primary_bucket` had "no deterministic engine owner" and that the bucket engine wrote only to a separate file. **That was wrong** — it missed `save_json(OPP_PATH, opps)` at the end of `engines/exclusive_strategy_bucket_engine.py`.

The reality:

1. `engines/exclusive_strategy_bucket_engine.py` **is** in the pipeline (`run_full_mochi_pipeline.py:97`). Its `main()` calls `choose_bucket(opp)` for every entry, writes `opp["exclusive_primary_bucket"] = bucket`, and **saves it back onto `deploy_data/compact_opportunities.json`** (it also writes a secondary analysis file, `memory/exclusive_strategy_buckets.json`). `choose_bucket` returns the same vocabulary compact serves (`publication_targets`, `japan_book_ecosystem`, `competitions_awards`, …). So the field **is** engine-owned.
2. `enriched_to_compact_opportunities.py` is **preserving** (keeps existing entries, appends new enriched), so it doesn't fight the bucket engine.
3. Measured reproducibility: running `choose_bucket` over all 379 served entries diverged from the served buckets on **only 3 entries** — i.e. the dataset was already **99.2% engine-reproducible**. The 3 were manual patches (see below). After this fix it is **100%** (0 diffs).

**Consequence:** the bucket field is reproducible. The remaining risk was the handful of manual `exclusive_primary_bucket` edits that a fresh engine run would silently overwrite. Those are now resolved (engine verdicts accepted where policy-correct; one sanctioned `bucket_override` where a curated decision was worth keeping).

## Commit-by-commit classification

| # | Commit | Summary | Files | Class |
|---|--------|---------|-------|-------|
| 1 | `01db4c86` | Instagram 26k + carousel live counts | api.py, frontend ×3, **artist_master_profile.json** | **A** — code + source profile (hand-curated input, not regenerated; `social_presence` is now read at runtime) |
| 2 | `d21db229` | Stop tracking `.pyc` | .gitignore, pyc removal | **A** — repo hygiene |
| 3 | `1e6a351f` | Contact dedup + write guards | api.py, PeppercornPage | **A** — engine/code |
| 4 | `cd931872` | Confirmed-only group-show count | engine, api.py, frontend, *career_strategy_report.json* | **A** — engine rule; the committed report is a fresh artifact regenerated **from** the fixed engine |
| 5 | `ae031687` | Wire dead preference loops | peppercorn_preference_engine.py | **A** — engine |
| 6 | `8ff6780c` | Style 4 Saffron sections + active count | api.py, SaffronPage css/jsx, translations | **A** — code |
| 7 | `e8dd75ff` | Remove Twitter; (swapped follower data) | code ×5 **+ incidental generated** (career_strategy_report, exclusive_strategy_buckets, needs_translation, reports ×3) | **A** for code; the generated files were **incidentally committed** (`git add -A`) — they are B-artifacts, harmless because overwritten, but a commit-hygiene smell |
| 8 | `c7196c8f` | Checklist typo + double-count guard | api.py, career_strategy_engine | **A** — engine |
| 9 | `e40bf794` | Score-chain zero-bypass, bucket excludes | api.py | **A** — engine |
| 10 | `97315944` | Var shadowing, TodaysFocus, **shashasha bucket** | frontend ×2, **compact_opportunities.json** | **B** — `exclusive_primary_bucket: japan_book_ecosystem → publication_targets` (see Exceptions) |
| 11 | `7c7197bc` | Twitter visibility, IBM relationship gate | api.py, SaffronPage | **A** — engine |
| 12 | `d01ec2b2` | Saffron/OppCard i18n | frontend ×3 | **A** — code |
| 13 | `b1cfd70f` | Wire `suppressed_categories` into load | api.py | **A** — engine rule (closes a dead loop) |
| 14 | `c8c37024` | closed_this_cycle badge; Twitter in drafts | api.py, frontend ×2, **drafts/**, **reports/** | **A** for code; drafts/reports are generated outputs (B-artifacts) |
| 15 | `e3044ad0` | CRM quality + verification | **contact_memory.json**, **compact_opportunities.json** | **B** — priority `A/B/C → high/medium/low`, added `why_relevant`, status changes (see Exceptions; priority now **converted**) |
| 16 | `2c4d0385` | Greeting, calendar, section links, i18n | api.py, frontend ×4 | **A** — code |
| 17 | `205a8a72` | Bucket routing/name mismatch, syntax | engines ×2, research_main.py | **A** — engine |
| 18 | `98fb0dd9` | OppDetailPanel fixes + i18n | api.py, frontend ×2 | **A** — code |
| 19 | `66c9c6c6` | peppercorn goals schema (id+done) | **peppercorn_profile.json** | **B (app-state)** — not pipeline-regenerated, but absent from-scratch; schema is app-produced (see Exceptions) |
| 20 | `9b26df47` | 4-agent quality pass | api.py, frontend ×2, **compact_opportunities.json** | **B** — added `category` to entries, deadline correction, bucket change (see Exceptions) |

**Tally:** 14 pure-A, 2 A-with-incidental-generated-files (#7, #14), 4 B (#10, #15, #19, #20).

## What was converted to an engine rule in this audit

- **CRM priority labels (#15):** added `_normalize_contact_priorities()` in `api.py`, applied in `get_contacts()` and the Saffron `venue_tracker`. Legacy `A/B/C` is coerced to `high/medium/low` **at read time**, so the served data is correct regardless of which historical seed wrote it — even if old labels reappear in the source JSON. This converts the priority half of `e3044ad0` from a one-time data patch into a permanent rule.

## Bucket edits (`#10`, `#20`) — RESOLVED (2026-06-10)

`exclusive_primary_bucket` is engine-owned (above). The 3 entries where the served data diverged from a fresh engine run were reconciled:

- **Der Greif, PhotoVogue** (`reject → research_needed`): the engine routes these photography open-calls to `research_needed` as translation candidates. The manual `reject` actually **violated** the documented "do not penalize photography opportunities" policy, so the engine verdict was accepted — this is a fix, not a loss.
- **shashasha** (`japan_book_ecosystem` vs `publication_targets`): a deliberate prior curation (it's a publisher you submit to). Preserved via the new **`bucket_override`** field, which `choose_bucket` honors deterministically. The curated decision now lives in the data as an engine-respected rule, not a silent patch.

Result: 0 diffs between served compact and a fresh `choose_bucket` run.

## What still cannot be converted (see `reports/patch_exceptions.md`)

- `#20` deadline correction (`"1 July 2025" → "Rolling consignment — contact directly"`) — per-opportunity real-world truth that no engine can derive without re-scraping. Belongs to the Verification layer.
- `#20`/`#2` `category` backfill — needs an enrichment classifier pass over legacy entries.
- `#15` `why_relevant` text — curated per-venue justification; an engine could emit generic copy but not this reasoning.
- `#19` peppercorn seed goals — app-state, not pipeline output; schema (id+done) is app-produced.

## Recommendation

The bucket-ownership gap is closed. Remaining structural work, in priority order: (1) extend Verification to refresh per-opportunity deadlines (kills the deadline-patch class); (2) an enrichment backfill that classifies category-less legacy entries. Both let more of the dataset rebuild correctly from scratch.
