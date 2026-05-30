
import subprocess, sys

PIPELINE = [
    "venue_intelligence_builder.py",
    "venue_memory_engine.py",
    "opportunity_report_engine.py",
    "analysis_cache_builder.py",
    "research_queue_report.py",
    "global_research_queue_builder.py",
    "candidate_quality_gate.py",
    "strategy_explainer_generator.py",
    "portfolio_pitch_generator.py",
    "smart_cover_letter_engine.py",
    "submission_timeline_engine.py",
    "pipeline_debug_summary.py",
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
print("REPORT PIPELINE COMPLETE")
