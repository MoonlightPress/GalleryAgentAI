# Pipeline Audit — 2026-06-09

Audited all 97 steps of `run_full_mochi_pipeline.py`. Each script was read and traced for inputs, outputs, and field dependencies.

---

## Ordering Conflicts

### 1. watercolor_source_expander.py (step 17) modifies source_targets.json after web_ingestion_engine.py (step 1) already read it

`web_ingestion_engine.py` reads `source_targets.json` to get the list of URLs to scrape (line 113). `watercolor_source_expander.py` appends new painting-specific sources to that same file (appends to `seed_sources`, adds watercolor keywords to `fit_keywords`). The ingestion already ran — the new sources are never fetched on this pipeline pass. The expansion is wasted work every run until sources exist in the file from a prior run.

**Fix:** Move step 17 (`watercolor_source_expander.py`) to before step 1 (`web_ingestion_engine.py`), or add a check in `web_ingestion_engine.py` that runs after source expansion. The current ordering means the expanded source list only takes effect on the *next* full pipeline run.

---

### 2. score_explanation_alignment.py (step 28) reads truth_aligned_score before opportunity_truth_checker.py (step 22) has written it for some paths

`score_explanation_alignment.py` (step 28) sorts and reports on `truth_aligned_score` (line 42). `opportunity_truth_checker.py` (step 22) is what writes `truth_aligned_score` (line 149). Step 22 comes before step 28 so this is fine for opportunities already in the file — but `painting_discovery_engine.py` (step 18) adds new opportunities to `compact_opportunities.json` and initialises `truth_aligned_score` to the raw source score (line 72 of `engines/painting_discovery_engine.py`). Those newly-inserted opportunities do have the field, so there is no null error. However, `japanese_chinese_discovery_engine.py` (step 7) and `grant_discovery_engine.py` (step 8) also append new entries to `compact_opportunities.json` and do **not** set `truth_aligned_score`. This means any entry added by steps 7 or 8 will show `truth_aligned_score = 0` in the step-28 report, even though truth_checker runs at step 22 and would have computed it for them — except that `opportunity_truth_checker.py` falls back to `watercolor_adjusted_score → dna_adjusted_score → differentiated_score → overall_score` (line 104–109), so the value will be set. This is handled. No blocking bug, but the naming is misleading for report consumers.

---

### 3. career_bucket_report.py (step 57) reads memory/opportunity_buckets.json before opportunity_differentiation_engine.py (step 49) writes it

`career_bucket_report.py` reads `memory/opportunity_buckets.json` (line 6). `opportunity_differentiation_engine.py` writes `memory/opportunity_buckets.json` (line 11, `OUT_PATH`). Step 49 comes before step 57, so the ordering is correct — **but** `career_strategy_engine.py` (step 47) also imports and calls `bucket_opportunity()` from `opportunity_buckets.py` (line 8) and writes `memory/strategy_feed.json`. Then `global_strategy_rebalance.py` (step 48) reads both `compact_opportunities.json` and `memory/strategy_feed.json`. Then step 49 writes `memory/opportunity_buckets.json`. The bucket report at step 57 is reading from the correct file. Ordering here is fine.

---

### 4. strategic_action_report.py (step 88) reads exclusive_strategy_buckets.json written by exclusive_strategy_bucket_engine.py (step 86)

Step 86 writes `memory/exclusive_strategy_buckets.json`. Step 88 reads it. Steps 87 (prerequisite_detection_engine) runs between them and modifies `compact_opportunities.json` but not `exclusive_strategy_buckets.json`. The bucket data at step 88 does not reflect any prerequisite annotations that step 87 computed. This is a minor ordering issue: prerequisite flags written by step 87 to each opportunity entry will not appear in the strategic action report.

**Fix:** Move `prerequisite_detection_engine.py` to before `exclusive_strategy_bucket_engine.py` so bucket assignments can reflect prerequisite status.

---

### 5. daily_digest_report.py (step 96) reads exclusive_strategy_buckets.json (written step 86) without re-running the bucket engine after why_it_fits_engine.py (step 84) rewrites why fields

`daily_digest_report.py` uses the bucket assignments from step 86. `why_it_fits_engine.py` (step 84) rewrites `why_it_fits_short` on the entries in `compact_opportunities.json` after the bucket engine has already run. The bucket memberships are correct but the `why` text shown in the digest may be the old value. Not a blocking bug, but the digest will show stale `why` text for any entries that were rewritten at step 84.

**Fix:** Move `exclusive_strategy_bucket_engine.py` to after `why_it_fits_engine.py` (currently step 84).

---

## Duplicate Work

### 6. Five steps all write overall_score to compact_opportunities.json without coordinating

Steps that mutate `overall_score` in `compact_opportunities.json`:
- **Step 10** (`opportunity_enrichment_pipeline.py`) — runs `upgraded_score()` and writes back `overall_score`
- **Step 36** (`preference_rescoring_engine.py`) — reads `overall_score`, adds preference adjustment, writes new `overall_score`
- **Step 39** (`score_sanity_engine.py`) — caps `overall_score` based on verification strength
- **Step 81** (`final_score_guard.py`) — applies verification-weighted ceiling, writes new `overall_score`
- **Step 82** (`tier_scoring_engine.py`) — applies tier adjustment (±2.5 / ±1.0 / −0.5 / −2.0), writes new `overall_score`

The result is that `overall_score` is meaningless as a stable field between steps because it is overwritten repeatedly. `score_sanity_engine.py` (step 39) caps the field, but `tier_scoring_engine.py` (step 82) runs *after* `final_score_guard.py` (step 81) and applies a raw offset — it can push a score that `final_score_guard` just capped *back* above that cap for Tier 1 (+2.5) entries, or drive a Tier 4 entry 2 points lower than the guard's floor.

**Specific bug:** `tier_scoring_engine.py` applies `TIER_ADJUSTMENTS` directly to `overall_score` (line 102). `final_score_guard.py` computes a `quality_composite` weighted blend, multiplies by a `V_WEIGHTS` factor, and caps at a `TIER_CEILINGS` ceiling, then writes to `overall_score`. If tier scoring runs after final_score_guard (it does — step 82 vs step 81), a Tier 1 opportunity can gain +2.5 on top of a value that the guard just calibrated. The tier adjustment should feed into `final_score_guard` as an input, not run after it.

**Fix:** Move `tier_scoring_engine.py` to before `final_score_guard.py`. The intended order should be: enrich → purity → sanity → tier → final guard → trust cleaner.

---

### 7. missing_fields logic is duplicated across at least five scripts

All five of the following implement their own version of "what fields are missing from this opportunity" with slightly different field lists:
- `opportunity_enrichment_pipeline.py` (step 10) — checks source, submission_page, deadline, fees, contact
- `fit_audit_engine.py` (step 58) — checks source, submission, deadline, fees, contact
- `global_research_queue_builder.py` (step 74) — checks submission_page, deadline, fees, contact
- `inquiry_draft_generator.py` (step 75) — checks submission_page, deadline, fees, contact
- `opportunity_status_engine.py` (step 95) — checks source, submission process, deadline, fees, contact

All five produce slightly different `missing_fields` lists for the same opportunity because they check slightly different field names (e.g. step 58 checks `opp.get("contact") or opp.get("email") or opp.get("contact_url") or opp.get("contact_email")` while step 74 only checks `contact`, `email`, `contact_url`). This means the pipeline has no single authoritative "this opportunity is actionable" determination; each consumer re-derives it.

**Fix:** Centralise `missing_fields()` into `opportunity_report_engine.py` (it already has a version) and import it from there. This is not causing crashes but causes inconsistency in what gets flagged for research.

---

### 8. research_queue is built twice with different schemas

`opportunity_enrichment_pipeline.py` (step 10) writes `memory/research_queue.json` as a list of dicts with keys: `title, organization, score, priority, missing, source, recommended_action`.

`research_queue_report.py` (step 73) reads `memory/research_queue.json` and renders it.

`research_priority_engine.py` (step 68) writes `memory/research_priority_queue.json` (different file) as a separate prioritised queue.

`daily_quest_generator.py` (step 70) reads `memory/research_priority_queue.json` from step 68.

These are two parallel queues with overlapping purpose. Step 68 computes a scored priority queue; step 10 computes a simpler queue. Both feed downstream steps. Neither deduplicates against the other.

---

### 9. opportunity_differentiation_engine.py (step 49) and career_strategy_engine.py (step 47) both write opportunity_buckets

`career_strategy_engine.py` (step 47) imports `bucket_opportunity()` from `opportunity_buckets.py` and writes `memory/strategy_feed.json` containing bucketed opportunities.

`opportunity_differentiation_engine.py` (step 49) independently re-buckets all opportunities into `memory/opportunity_buckets.json` using its own logic (9 named buckets).

These are different files with different bucket schemas. The UI and downstream steps (`career_bucket_report.py` step 57) reads from `memory/opportunity_buckets.json` (step 49). The strategy feed from step 47 feeds only `global_strategy_rebalance.py` (step 48). The duplication is in the concept — both are "assign each opportunity to a strategic bucket" — but they produce different bucket taxonomies, which proliferates bucket-name confusion throughout reports.

---

## Dead Steps

### 10. submission_link_hunter.py (step 9) reads from a file not written by this pipeline

`submission_link_hunter.py` reads `memory/verified_opportunities.json` (line 17). This file has 20 entries with schema `{title, url, score, status, submission_open, ...}` — a completely different schema from `deploy_data/compact_opportunities.json`. It is written by `web_verification_engine.py`, which is not in the pipeline. The file in memory is a stale artifact from a previous one-off verification run.

**Effect:** Step 9 runs on a static 20-entry snapshot rather than the current opportunity set. Submission links it finds are written to `memory/submission_targets.json` (not read by any subsequent pipeline step) and `reports/submission_link_report.md`. The step does not modify `compact_opportunities.json`. Its output is silently disconnected from the rest of the pipeline.

**Fix:** Either retire this step (its function is covered by `submission_page_harvester.py` step 44, which correctly operates on `compact_opportunities.json`), or update it to read from `deploy_data/compact_opportunities.json` and write submission links back into the main opportunity records.

---

### 11. url_verification_engine.py (step 5) reads from deploy_data/compact_opportunities.json but the file may not have been populated yet at that point in the pipeline

Steps 1–4 operate on `ingestion/scraped_pages.json` and `ingestion/approved_candidates.json`. `approved_candidate_importer.py` (step 4) is the first step that writes to `deploy_data/compact_opportunities.json` — but only if `deploy_data/compact_opportunities.json` already exists (line 30: `opps = load_json(OPP_PATH, [])`). On a clean install with no pre-existing `compact_opportunities.json`, step 4 writes at most 25 freshly-scraped candidates. `url_verification_engine.py` (step 5) then verifies those 25. All subsequent discovery steps (6, 7, 8) append more opportunities after verification has already run. Those new entries will have no `url_verification_status` field until the next pipeline run.

**Effect:** On a cold-start run, discovery steps 6–8 add opportunities that bypass URL verification. `rumor_mill_expansion_runner.py` (step 45) has a guard: `if opp.get("url_verification_status") != "ok": return False` (line 52–55). This means freshly-discovered opportunities from steps 6–8 are excluded from rumor mill expansion on the same run they are discovered.

**Fix:** Move URL verification to after all discovery steps (after step 8, before step 9). Add a second URL-verification pass, or change step 45 to also process entries where `url_verification_status` is None/missing.

---

### 12. visual_dna_extractor.py (step 15) outputs to analysis/image_features.json and memory/artist_dna.json but only runs when images exist

`visual_dna_extractor.py` searches for images in `images/`, `artist_images/`, `data/images/`, `uploads/images/`. These directories do not exist in the repo. If no images are found, the script writes an empty or minimal `memory/artist_dna.json`. Two later steps depend on this:
- `dna_recommendation_booster.py` (step 31) — gracefully handles empty DNA with an early return (line 42: `if not dna: print(...); return`)
- `dna_project_refiner.py` (step 90) — same graceful handling (line 29)

The step does not crash but silently produces no output. The DNA boost (step 31) and project refinement (step 90) are no-ops every pipeline run on this machine.

---

### 13. visual_profile_ingester.py (step 14) reads artist_visual_profile_template.json which is a static blank template

`visual_profile_ingester.py` reads `artist_visual_profile_template.json` and guards against an empty summary (line 29: `if not visual.get("summary"): print(...); return`). The template appears to be intentionally blank — it's the placeholder for human-filled image analysis. This step is a no-op on every run until the template is manually populated.

---

## Missing Idempotency

### 14. analysis_cache_builder.py (step 72) regenerates all N opportunity report files unconditionally

`analysis_cache_builder.py` iterates over every opportunity in `compact_opportunities.json` and writes `memory/generated_analysis/NNN_<title>.md` for each one, overwriting any existing file. On a 200-opportunity dataset this creates 200 file writes every run, even when nothing changed.

**Fix:** Add a check: skip writing if the file already exists and the opportunity's `last_verified` date (or a hash of its key fields) matches what is stored in the file header. A simple check of `if path.exists(): continue` would be sufficient for most runs.

---

### 15. japanese_chinese_discovery_engine.py (step 7) and grant_discovery_engine.py (step 8) already have a 7-day query cache but it is ignored when run as pipeline steps

Both scripts have `CACHE_DAYS = 7` and skip cached queries. However, `run_full_mochi_pipeline.py` calls them as subprocess runs with no arguments, which means they use the default (cache respected). This is the correct behavior — these steps are already idempotent-by-cache. No change needed, but worth noting that the cache relies on `memory/jc_discovery_log.json` and `memory/grant_discovery_log.json` persisting between runs.

---

### 16. watercolor_source_expander.py (step 17) adds sources unconditionally, but only appends new ones

`watercolor_source_expander.py` checks `if src["url"] not in existing` before appending (line 37), so it is idempotent on the source list. However, it also appends to `fit_keywords` using `list(dict.fromkeys(...))` (line 43), which is also idempotent. No issue here.

---

### 17. inquiry_draft_generator.py (step 75) and ibm_email_writer.py (step 76) regenerate all draft files on every run

`inquiry_draft_generator.py` writes one `.txt` file per opportunity with missing fields, overwriting any existing file every run (line 59). On a 200-opportunity dataset with 150 having missing fields, this is 150 file writes per run.

`ibm_email_writer.py` reads existing `email_ja`/`email_en` fields on each opportunity and calls Claude API to generate emails. It checks whether `email_ja` is already present on the opportunity (the `--limit` flag limits how many are generated), but does not skip writing the `.txt` file to disk if it already exists. This means Claude API is called for any opportunities that lack `email_ja`, which costs API tokens on every run for newly-added opportunities.

The Claude API call in `ibm_email_writer.py` is the most expensive idempotency gap: it should skip opportunities where `email_ja` is already populated.

---

### 18. painting_quality_gate.py (step 19) and source_purity_enforcer.py (step 26) both apply score adjustments to the same fields

`painting_quality_gate.py` (step 19) promotes entries with native_medium=="painting" by +0.8 (written to `source_purity_score` proxy fields). `source_purity_enforcer.py` (step 26) reads `source_purity_score` (or falls back through other fields) and applies a further +0.7 for native=="painting". These boosts stack. A painting entry receives two separate boosts totalling +1.5 across two steps, which is the intended cumulative behavior — but it is nowhere documented and easy to break if someone changes the fallback chain in `current_score()`.

---

## Recommended Reordering

These are concrete moves that fix the bugs described above.

```
Current order → Proposed order

Step 1: web_ingestion_engine.py
...

Move step 17 (watercolor_source_expander.py) to BEFORE step 1.

Move step 5 (url_verification_engine.py) to AFTER step 8 (grant_discovery_engine.py),
so all discovery steps have run before URL verification.

Move step 82 (tier_scoring_engine.py) to BEFORE step 81 (final_score_guard.py),
so the tier adjustment feeds into the guard's composite calculation rather than
overriding it afterward.

Move step 87 (prerequisite_detection_engine.py) to BEFORE step 86
(exclusive_strategy_bucket_engine.py), so bucket assignments can use
prerequisite flags.

Move step 86 (exclusive_strategy_bucket_engine.py) to AFTER step 84
(why_it_fits_engine.py), so the bucket report reflects rewritten why text.
```

Revised sequence for the scoring tail of the pipeline (steps 79–88):

```
79: submission_timeline_engine.py      (no change)
80: strategy_explainer_generator.py    (no change, optional)
81: why_it_fits_engine.py             (was 84)
82: tier_scoring_engine.py             (was 82 — moved before final guard)
83: final_score_guard.py              (was 81)
84: recommendation_trust_cleaner.py    (was 83)
85: dead_url_pruner.py                 (was 85, no change)
86: prerequisite_detection_engine.py   (was 87 — moved before bucket engine)
87: exclusive_strategy_bucket_engine.py (was 86 — moved after prereq + why)
88: strategic_action_report.py         (was 88, no change)
```

---

## Summary of Impact by Severity

| # | Issue | Severity | Effect |
|---|-------|----------|--------|
| 1 | watercolor_source_expander after ingestion | High | New sources only scraped on next run |
| 6 | tier_scoring_engine after final_score_guard | High | Tier 1 scores can exceed guard's calibrated ceiling |
| 10 | submission_link_hunter reads stale file | High | Step is silently disconnected from current opportunity set |
| 11 | url_verification before all discovery | Medium | New opportunities from steps 6–8 skip verification |
| 4 | prerequisite_detection after bucket engine | Medium | Prerequisite flags not reflected in strategic action report |
| 5 | bucket engine before why_it_fits_engine | Medium | Daily digest shows stale why text |
| 7 | missing_fields logic duplicated | Medium | Inconsistent actionability flags across reports |
| 14 | analysis_cache_builder regenerates all files | Low | Unnecessary disk writes every run |
| 12 | visual_dna_extractor always no-op | Low | Silent no-op, no crash |
| 13 | visual_profile_ingester always no-op | Low | Silent no-op, no crash |
| 17 | ibm_email_writer calls Claude for existing emails | Low | Wasted API tokens on re-runs |
