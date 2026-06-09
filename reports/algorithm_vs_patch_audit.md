# Algorithm vs. Data-Patch Audit — Last 20 Commits

**Date:** 2026-06-10
**Question for every change:** does it survive a fresh pipeline run?

- **A — Engine rule:** code (api.py, `engines/`, `frontend/`, config) or a fix to a hand-curated *source* file. Survives a from-scratch pipeline run, or is the canonical input the pipeline reads.
- **B — Data patch:** a manual edit to a file the pipeline *regenerates* (notably `deploy_data/compact_opportunities.json` and the generated `Memory/*.json` + `reports/*.md`). Overwritten on a fresh run unless an engine rule reproduces it.

## The core architectural finding

`deploy_data/compact_opportunities.json` is a **curated hybrid artifact**, not pure engine output:

1. `enriched_to_compact_opportunities.py` is **preserving** — it keeps existing entries (dropping only `import_source == "opportunity_intelligence_sprint_v1"`) and appends new enriched ones. It does **not** recompute `exclusive_primary_bucket`, `category`, `priority`, or `why_relevant`.
2. `engines/exclusive_strategy_bucket_engine.py` writes buckets to a **separate** file (`memory/exclusive_strategy_buckets.json`) using **different bucket names** (`publication_editorial`, `competitions_awards`, …) than the `exclusive_primary_bucket` values served from compact (`publication_targets`, `japan_book_ecosystem`, `relationship_builders`, …). The two are **decoupled** — nothing syncs the engine's verdict back onto the served field.
3. Most per-entry fields in compact are written by **one-shot seed/patch scripts** (`add_cafe_zine_entries.py`, `scripts/patches/*`) that hardcode values.

**Consequence:** "delete all JSON and run the pipeline from scratch" would **not** reproduce today's served dataset. The bucket/category/priority fields on compact are effectively curated data with no single deterministic engine owner. This is the root cause behind most B's below, and the highest-leverage thing to fix structurally (see Exceptions doc).

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

## What could not be converted (see `reports/patch_exceptions.md`)

- `#10`, `#20` compact bucket/category edits — the served `exclusive_primary_bucket`/`category` fields have **no deterministic engine owner** (bucket engine is decoupled, different names). Converting requires a new pipeline step that maps the bucket engine's verdict onto compact and reconciles the naming — a real refactor, too broad to land safely unsupervised.
- `#20` deadline correction (`"1 July 2025" → "Rolling consignment — contact directly"`) — per-opportunity real-world truth that no engine can derive without re-scraping the source.
- `#15` `why_relevant` text — curated per-venue justification; an engine could generate generic copy but not this specific reasoning.
- `#19` peppercorn seed goals — `peppercorn_profile.json` is app-state, not pipeline output; the **schema** (id+done) is produced by the app on save, the seed goals are example data.

## Recommendation

The single highest-leverage structural fix is to **make `exclusive_primary_bucket` engine-owned**: add a normalization step late in the pipeline that writes the bucket engine's verdict onto each compact entry (reconciling the `publication_editorial` vs `publication_targets` naming), so bucket assignment stops being curated data. Until then, bucket edits to compact remain unavoidable data patches and must be logged per the Data Patch Rule.
