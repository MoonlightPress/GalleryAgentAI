from smart_pipeline_runner import run_pipeline

PIPELINE = [
    # ── Discovery sources must be expanded BEFORE ingestion runs ──────────────
    "watercolor_source_expander.py",      # audit fix: was step 17, must run first
    # ── Ingestion ──────────────────────────────────────────────────────────────
    "web_ingestion_engine.py",
    "scraped_candidate_extractor.py",
    "candidate_quality_gate.py",
    "approved_candidate_importer.py",
    # ── Expanded discovery (ALL must complete before URL verification) ─────────
    "global_opportunity_expander.py",
    "japanese_chinese_discovery_engine.py",
    "grant_discovery_engine.py",
    # ── URL verification (now runs after all discovery, not in the middle) ─────
    "url_verification_engine.py",         # audit fix: moved after steps 6-8
    # ── submission_link_hunter removed: reads stale verified_opportunities.json
    #    that is not written by this pipeline; function covered by step 44 ──────
    # ── Enrichment ────────────────────────────────────────────────────────────
    "opportunity_enrichment_pipeline.py",
    "venue_intelligence_builder.py",
    "venue_memory_engine.py",
    "artist_visual_profile_v1.py",
    "visual_profile_ingester.py",
    "visual_dna_extractor.py",
    "watercolor_artist_profile_engine.py",
    "painting_discovery_engine.py",
    "painting_quality_gate.py",
    "painting_action_report.py",
    "watercolor_opportunity_converter.py",
    "opportunity_truth_checker.py",
    "source_medium_classifier.py",
    "medium_confirmation_gate.py",
    "translation_candidate_detector.py",
    "source_purity_enforcer.py",
    "native_medium_ranker.py",
    "score_explanation_alignment.py",
    "career_path_ranker.py",
    "watercolor_project_rebuilder.py",
    "dna_recommendation_booster.py",
    "deep_match_scoring_engine.py",
    "lineage_scoring_engine.py",
    "feedback_learning_engine.py",
    "submission_log_reader.py",
    "preference_rescoring_engine.py",
    "portfolio_match_engine.py",
    "submission_strategy_engine.py",
    "score_sanity_engine.py",
    "rumor_mill_engine.py",
    "rumor_mill_propagation_engine.py",
    "fee_text_extractor.py",
    "deadline_normaliser.py",
    "submission_page_harvester.py",
    "rumor_mill_expansion_runner.py",
    "verification_report_engine.py",
    "career_strategy_engine.py",
    "global_strategy_rebalance.py",
    "opportunity_differentiation_engine.py",
    "artist_ecosystem_mapper.py",
    "peer_artist_engine.py",
    "publisher_match_engine.py",
    "ecosystem_opportunity_bridge.py",
    "ecosystem_report.py",
    "artist_project_builder.py",
    "project_submission_mapper.py",
    "career_bucket_report.py",
    "fit_audit_engine.py",
    "institution_network_engine.py",
    "discovery_engine.py",
    "ecosystem_expansion_engine.py",
    "curator_personality_engine.py",
    "career_path_engine.py",
    "serendipity_engine.py",
    "reputation_engine.py",
    "momentum_wave_engine.py",
    "social_proof_engine.py",
    "research_priority_engine.py",
    "curator_intelligence_engine.py",
    "daily_quest_generator.py",
    "opportunity_report_engine.py",
    "analysis_cache_builder.py",
    "research_queue_report.py",
    "global_research_queue_builder.py",
    "inquiry_draft_generator.py",
    "ibm_email_writer.py",
    "portfolio_pitch_generator.py",
    "smart_cover_letter_engine.py",
    "submission_timeline_engine.py",
    "strategy_explainer_generator.py",
    # ── Scoring tail: tier → guard → trust → pruner → prereq → bucket ─────────
    "why_it_fits_engine.py",              # audit fix: moved before final guard
    "tier_scoring_engine.py",             # audit fix: must run before final_score_guard
    "final_score_guard.py",               # audit fix: now runs after tier adjustment
    "targeted_verification_agent.py",     # systemic fix 2026-06-13: real URL/deadline
                                          # verification was never in the pipeline —
                                          # Verification > ranking (CLAUDE.md). Pure
                                          # HTTP, no API cost.
    "recommendation_trust_cleaner.py",
    "dead_url_pruner.py",
    "prerequisite_detection_engine.py",   # audit fix: moved before bucket engine
    "exclusive_strategy_bucket_engine.py",# audit fix: now runs after prereq + why
    "peppercorn_preference_engine.py",    # apply artist preference adjustments after bucketing
    "strategic_action_report.py",
    "next_project_engine.py",
    "dna_project_refiner.py",
    "next_email_engine.py",
    "next_exhibition_engine.py",
    "pipeline_debug_summary.py",
    "project_folder_audit.py",
    "opportunity_status_engine.py",
    # Translation MUST run last, after every content field is finalized — otherwise
    # an online update ships opportunities that read English in Chinese mode.
    "content_translation_engine.py",      # name/one_sentence/why_it_fits/bullets -> zh + ja for every opp
    "opp_strategy_translation_engine.py", # relationship_note/submission_strategy/recommended_body/quick_action -> zh + ja
    "saffron_translation_engine.py",      # Saffron's analysis prose -> zh cache
    "contact_translation_engine.py",      # CRM contact prose (why_relevant/notes/analysis) -> zh + ja
    "daily_digest_report.py",
]

# Steps that spend API credits. The maintenance pipeline (run_maintenance_pipeline.py)
# excludes these; the full pipeline runs them all. Measured 2026-06-13:
# the four Tavily engines issue ~265-500 searches per full run.
PAID_STEPS = {
    # Tavily web search
    "japanese_chinese_discovery_engine.py",
    "grant_discovery_engine.py",
    "rumor_mill_engine.py",
    "rumor_mill_expansion_runner.py",
    # Claude API
    "ibm_email_writer.py",
    "why_it_fits_engine.py",
    # Claude API — translation engines. These call the model for any field that
    # isn't already cached. The maintenance pipeline must NOT run them unattended:
    # every content-GENERATING step above is already paid/excluded, so a maintenance
    # pass produces no new translatable content and these would either no-op (cache
    # hit) or, if any source prose did change, spend Claude credits with nobody
    # watching. A full (paid) run still runs them last so online updates stay translated.
    "content_translation_engine.py",
    "opp_strategy_translation_engine.py",
    "saffron_translation_engine.py",
    "contact_translation_engine.py",
}

if __name__ == "__main__":
    run_pipeline(PIPELINE)
