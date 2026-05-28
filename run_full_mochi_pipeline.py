
import subprocess
import sys


PIPELINE = [
    "opportunity_enrichment_pipeline.py",
    "venue_intelligence_builder.py",
    "venue_memory_engine.py",
    "opportunity_report_engine.py",
    "analysis_cache_builder.py",
    "research_queue_report.py",
    "inquiry_draft_generator.py",
    "career_strategy_engine.py",
    "opportunity_status_engine.py",
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
print("FULL MOCHI PIPELINE COMPLETE")
