
import subprocess, sys

PIPELINE = [
    "visual_profile_ingester.py",
    "opportunity_enrichment_pipeline.py",
    "deep_match_scoring_engine.py",
    "lineage_scoring_engine.py",
    "portfolio_match_engine.py",
    "submission_strategy_engine.py",
    "score_sanity_engine.py",
    "career_strategy_engine.py",
    "global_strategy_rebalance.py",
    "fit_audit_engine.py",
]

for script in PIPELINE:
    print()
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print()
print("SCORING PIPELINE COMPLETE")
