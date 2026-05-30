
import subprocess, sys

PIPELINE = [
    "web_ingestion_engine.py",
    "scraped_candidate_extractor.py",
    "candidate_quality_gate.py",
    "approved_candidate_importer.py",
    "url_verification_engine.py",
    "score_sanity_engine.py",
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
print("INGESTION PIPELINE COMPLETE")
