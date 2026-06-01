# Session 2 Status — Reorganization Progress

**Date:** 2026-06-01
**Branch:** main

## Python File Counts by Directory

| Directory | .py files | Notes |
|---|---|---|
| root | 217 | Down from 238 at session start |
| engines/ | 81 | +14 moved in this session |
| ui/ | 17 | Stable |
| scripts/runners/ | 88 | Stable |
| scripts/patches/ | 65 | Stable |
| reports/ | 45 | Stable |
| archive/dead_code/ | 59 | +7 archived in this session |

**Total tracked .py files across all dirs: ~573**

## What Was Done This Session

**Phase 1 — Archived 7 confirmed duplicates**
Root copies were byte-for-byte identical to their canonical subdirectory versions. Moved to `archive/dead_code/`:
- `best_moves_streamlit_section.py` (canonical: `ui/`)
- `category_context_streamlit_section.py` (canonical: `ui/`)
- `opportunity_review_sections.py` (canonical: `ui/`)
- `publishing_opportunity_section.py` (canonical: `ui/`)
- `zine_opportunity_section.py` (canonical: `ui/`)
- `artist_profile_purge.py` (canonical: `scripts/patches/`)
- `bucket_deduplicator.py` (canonical: `scripts/patches/`)

**Phase 2 — Moved 14 `*_engine.py` files to `engines/`**
`web_verification_engine.py` intentionally left in root (active work in progress).
All 14 are found by `smart_pipeline_runner` via its `engines/` search path — no pipeline disruption.

## Known Constraints for Future Sessions

**Files locked in root by direct imports:**

| File | Imported by |
|---|---|
| `visual_card_system.py` | `app.py` (`from visual_card_system import *`) |
| `report_layout_upgrade.py` | `app.py` (`from report_layout_upgrade import *`) |
| `smart_pipeline_runner.py` | `run_full_mochi_pipeline.py` + 14 scripts/runners files |
| `utils_filename.py` | 5 files in `engines/` |
| `opportunity_buckets.py` | `engines/career_strategy_engine.py` |
| `career_stage_profiles.py` | `engines/career_strategy_engine.py` |

**Legacy pipeline bare-name script calls (breaks if scripts move):**
`council_pipeline_agent.py` and `artist_intelligence_pipeline.py` call scripts via `subprocess.run(["python", script])` with no path prefix. Moving any of their 14 target scripts out of root breaks them:
- Council targets: `opportunity_discovery_agent.py`, `opportunity_validator.py`, `opportunity_resolution_agent.py`, `artist_profile_agent.py`, `opportunity_ranking_agent.py`, `opportunity_filter_agent.py`, `submission_packet_agent.py`, `incremental_council_agent.py`, `compact_view_agent.py`, `materials_memory_agent.py`, `pipeline_status_agent.py`
- Artist intelligence targets: `artist_intelligence_agent.py`, `artist_preference_questions_agent.py`, `pathway_progress_agent.py`

## Recommended Next Session Priorities

**1. Decide the legacy pipeline question (blocks Phase 3)**
Options:
- Upgrade `council_pipeline_agent.py` and `artist_intelligence_pipeline.py` to use `smart_pipeline_runner` (cleanest, frees 14 scripts to move)
- Keep the 14 target scripts in root permanently (simple, no risk)
- Archive the legacy pipelines as superseded (they are noted as superseded in CLAUDE.md)

**2. Phase 3 — Move ~24 pipeline processing steps to `engines/`**
Pending resolution of the legacy pipeline question. These are active pipeline steps in `run_full_mochi_pipeline.py` that belong in `engines/` by function. Safe to move: `smart_pipeline_runner` searches `engines/`.
Candidates: `scraped_candidate_extractor.py`, `candidate_quality_gate.py`, `painting_quality_gate.py`, `watercolor_opportunity_converter.py`, `opportunity_truth_checker.py`, `source_medium_classifier.py`, `translation_candidate_detector.py`, `source_purity_enforcer.py`, `native_medium_ranker.py`, `score_explanation_alignment.py`, `career_path_ranker.py`, `watercolor_project_rebuilder.py`, `dna_recommendation_booster.py`, `global_strategy_rebalance.py`, `ecosystem_opportunity_bridge.py`, `artist_project_builder.py`, `project_submission_mapper.py`, `final_score_guard.py`, `recommendation_trust_cleaner.py`, `dna_project_refiner.py`, `visual_dna_extractor.py`, `artist_visual_profile_v1.py`, `watercolor_source_expander.py`, `evidence_score_guard.py`

**3. Phase 4 — Move 6 pipeline report steps to `reports/`**
`painting_action_report.py`, `ecosystem_report.py`, `career_bucket_report.py`, `strategic_action_report.py`, `research_queue_report.py`, `pipeline_debug_summary.py`

**4. Phase 5 — Bulk-move remaining ~160 scripts to `scripts/runners/`**
Largest phase. Requires confirming no cross-imports between files being moved. After Phase 5 root should be ~30 files (entry points + locked utilities).

**5. Test after each phase**
`python run_full_mochi_pipeline.py` and `streamlit run app.py` are the two validation commands.
