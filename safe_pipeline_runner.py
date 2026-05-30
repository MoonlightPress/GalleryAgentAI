
import subprocess
import sys
from pathlib import Path

OPTIONAL_SCRIPTS = {
    "visual_profile_ingester.py",
    "deep_match_scoring_engine.py",
    "feedback_learning_engine.py",
    "preference_rescoring_engine.py",
    "portfolio_match_engine.py",
    "submission_strategy_engine.py",
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
    "global_research_queue_builder.py",
    "portfolio_pitch_generator.py",
    "smart_cover_letter_engine.py",
    "submission_timeline_engine.py",
    "strategy_explainer_generator.py",
}

ALIASES = {
    "deep_match_scoring_engine.py": [
        "artist_profile_scoring_engine.py",
        "artist_dataset_score_engine.py",
    ],
}

def resolve_script(script):
    if Path(script).exists():
        return script

    for replacement in ALIASES.get(script, []):
        if Path(replacement).exists():
            print(f"USING {replacement} instead of missing {script}")
            return replacement

    return script

def run_script(script):
    resolved = resolve_script(script)

    if not Path(resolved).exists():
        if script in OPTIONAL_SCRIPTS:
            print(f"SKIP optional missing script: {script}")
            return True

        print(f"FAILED required missing script: {script}")
        return False

    result = subprocess.run([sys.executable, resolved])
    return result.returncode == 0

def run_pipeline(pipeline):
    for script in pipeline:
        print()
        print("=" * 70)
        print("RUNNING:", script)
        print("=" * 70)

        ok = run_script(script)

        if not ok:
            raise SystemExit(f"FAILED: {script}")

    print()
    print("PIPELINE COMPLETE")
