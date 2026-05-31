
import subprocess
import sys

PIPELINE = [
    "publication_readiness_patch.py",
    "opportunity_context_enricher.py",
    "artist_fit_scorer.py",
]

for script in PIPELINE:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("PERSONALIZED FIT CONTEXT PATCH COMPLETE")
