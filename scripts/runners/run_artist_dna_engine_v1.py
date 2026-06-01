
import subprocess
import sys

for script in [
    "artist_dna_engine.py",
    "opportunity_type_classifier.py",
    "artist_fit_scorer.py",
    "artist_fit_brief_generator.py",
    "dashboard_artist_dna_export.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("ARTIST DNA ENGINE V1 COMPLETE")
