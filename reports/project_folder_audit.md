# Project Folder Audit

This is a cleanup planning report. It does not move files.

## Files that should probably remain in root

- app.py — exists
- requirements.txt — exists
- run_full_mochi_pipeline.py — exists
- safe_pipeline_runner.py — exists
- utils_filename.py — exists

## Suggested future folders

- `scripts/patches/` for patch scripts
- `scripts/runners/` for run scripts
- `engines/` for scoring/research/intelligence engines
- `ui/` for Streamlit component modules
- `docs/` for README files
- `archive/zips/` for old generated zip packages
- `data/` or keep existing `memory/`, `deploy_data/`, `reports/`, `ingestion/`

## Current root clutter by pattern

### Patch scripts — 57

- patch_app_after_compact.py
- patch_app_artist_image_review.py
- patch_app_compact.py
- patch_app_compact_detail.py
- patch_app_feedback_learning.py
- patch_app_fit_audit.py
- patch_app_portfolio_matching.py
- patch_app_relationship.py
- patch_app_strategy_homepage.py
- patch_artist_intelligence_v2_pipeline.py
- patch_atelier_text_colors.py
- patch_compact_dense_ui.py
- patch_console_encoding.py
- patch_filename_collision.py
- patch_final_guard_pipeline.py
- patch_full_pipeline_global.py
- patch_full_pipeline_strategy.py
- patch_mochi_atelier_big.py
- patch_opportunity_atelier_ui.py
- patch_opportunity_detail_position.py
- patch_opportunity_grid_ui.py
- patch_opportunity_horizontal_rows.py
- patch_opportunity_polish_ui.py
- patch_opportunity_rows_safe.py
- patch_opportunity_rows_ui.py
- patch_pipeline_aesthetic.py
- patch_pipeline_artist_dataset.py
- patch_pipeline_artist_intelligence.py
- patch_pipeline_artist_review.py
- patch_pipeline_autonomous.py
- patch_pipeline_candidate_quality.py
- patch_pipeline_cleanup_stabilizer.py
- patch_pipeline_compatibility.py
- patch_pipeline_curator_brain.py
- patch_pipeline_curator_intelligence.py
- patch_pipeline_evidence.py
- patch_pipeline_feedback_learning.py
- patch_pipeline_fit_audit.py
- patch_pipeline_ingestion.py
- patch_pipeline_institution_research.py
- patch_pipeline_live_refresh.py
- patch_pipeline_local_image_processing.py
- patch_pipeline_network.py
- patch_pipeline_portfolio_matching.py
- patch_pipeline_publication_deadline.py
- patch_pipeline_relationship.py
- patch_pipeline_reputation.py
- patch_pipeline_source_expansion.py
- patch_pipeline_submission_strategy.py
- patch_pretty_no_vector_ui.py
- patch_real_header_assets.py
- patch_report_writer_filenames.py
- patch_safe_filenames.py
- patch_smart_cover_safe_call.py
- patch_strategy_homepage_global_sections.py
- patch_visual_profile_bucket_pipeline.py
- patch_visual_system.py

### Runner scripts — 14

- run_after_repair.py
- run_artist_intelligence_v2.py
- run_full_mochi_pipeline.py
- run_ingestion_only.py
- run_intelligence_pipeline.py
- run_intelligence_pipeline.py.py
- run_remaining_reports.py
- run_remaining_reports_again.py
- run_report_core_after_filename_fix.py
- run_reports_only.py
- run_required_core_only.py
- run_scoring_only.py
- run_verification_upgrade.py
- run_visual_profile_bucket_upgrade.py

### Engine scripts — 48

- artist_dataset_score_engine.py
- artist_profile_scoring_engine.py
- career_path_engine.py
- career_pathway_engine.py
- career_strategy_engine.py
- claim_validation_engine.py
- curator_dossier_engine.py
- curator_intelligence_engine.py
- curator_personality_engine.py
- deadline_extraction_engine.py
- detail_confidence_engine.py
- discovery_engine.py
- ecosystem_expansion_engine.py
- ecosystem_map_engine.py
- evidence_extraction_engine.py
- feedback_learning_engine.py
- fit_audit_engine.py
- institution_fit_engine.py
- institution_network_engine.py
- institution_profile_engine.py
- lineage_scoring_engine.py
- momentum_scoring_engine.py
- momentum_wave_engine.py
- opportunity_decay_engine.py
- opportunity_differentiation_engine.py
- opportunity_report_engine.py
- opportunity_status_engine.py
- opportunity_verification_engine.py
- peer_artist_engine.py
- portfolio_match_engine.py
- preference_rescoring_engine.py
- publication_frequency_engine.py
- publisher_match_engine.py
- recommendation_engine.py
- relationship_memory_engine.py
- reputation_engine.py
- research_priority_engine.py
- score_sanity_engine.py
- serendipity_engine.py
- smart_cover_letter_engine.py
- social_proof_engine.py
- source_type_weight_engine.py
- submission_strategy_engine.py
- submission_timeline_engine.py
- url_verification_engine.py
- venue_memory_engine.py
- visual_similarity_engine.py
- web_ingestion_engine.py

### UI component scripts — 10

- artist_image_review_components.py
- compact_detail_components.py
- feedback_ui_components.py
- fit_audit_ui_components.py
- mochi_action_components.py
- mochi_dashboard_components.py
- portfolio_match_ui_components.py
- relationship_ui_components.py
- report_ui_components.py
- strategy_homepage_components.py

### README files — 38

- README.md
- README_ACTION_SYSTEM.md
- README_ARTIST_DATASET_BUILDER.md
- README_ARTIST_IMAGE_REVIEW.md
- README_ARTIST_INTELLIGENCE.md
- README_ARTIST_INTELLIGENCE_V2.md
- README_AUTONOMOUS_RESEARCH.md
- README_CLEANUP_INGESTION_STABILIZER.md
- README_COMPACT_DETAIL_UX_PATCH.md
- README_CURATOR_BRAIN.md
- README_CURATOR_INTELLIGENCE.md
- README_EVIDENCE_UPGRADE.md
- README_FEEDBACK_LEARNING_UPGRADE.md
- README_FINAL_GUARDRAILS_FIX.md
- README_FIT_AUDIT_UPGRADE.md
- README_GLOBAL_OPPORTUNITY_UPGRADE.md
- README_INGESTION_UPGRADE.md
- README_LINEAGE_INTELLIGENCE.md
- README_LIVE_REFRESH_AND_VISUAL_SIMILARITY.md
- README_LOCAL_IMAGE_PROCESSING.md
- README_MAINTENANCE.md
- README_MOST_IMPACTFUL_NEXT_STEP.md
- README_NETWORK_INTELLIGENCE.md
- README_NEXT_STEPS.md
- README_PIPELINE.md
- README_PIPELINE_COMPATIBILITY_FIX.md
- README_PORTFOLIO_MATCHING.md
- README_PRESENTATION_UPGRADE.md
- README_PUBLICATION_DEADLINE_INTELLIGENCE.md
- README_RELATIONSHIP_UPGRADE.md
- README_REPORT_WRITER_FILENAME_FIX.md
- README_REPUTATION_SYSTEM.md
- README_SAFE_FILENAME_COLLISION_FIX.md
- README_SOURCE_EXPANSION.md
- README_STRATEGY_HOMEPAGE.md
- README_SUBMISSION_STRATEGY.md
- README_VERIFIED_CANDIDATE_IMPORTER.md
- README_VISUAL_PROFILE_AND_BUCKETS.md

### Zip files — 2

- .zip
- A.zip

### Top-level JSON files — 25

- artist_graph_report.json
- artist_intelligence_seed_data.json
- artist_lineage_profiles.json
- artist_memory_entry.json
- artist_research_seed.json
- artist_visual_profile_template.json
- artists_preferences.json
- career_reconstruction_seed.json
- contact_entry.json
- energy_profile.json
- executive_plan.json
- expanded_source_registry.json
- global_opportunity_seeds.json
- mousehole_task_seed.json
- multilingual_outreach_preview.json
- opportunity_discovery_report.json
- opportunity_entry.json
- pathway_model_seed.json
- portfolio_bodies.json
- portfolio_cluster_template.json
- portfolio_profiles.json
- project_manifest.json
- relationship_entry.json
- relationship_memory.json
- source_targets.json
