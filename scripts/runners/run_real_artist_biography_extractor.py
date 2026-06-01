
import subprocess
import sys

for script in [
    "artist_biography_extractor.py",
    "real_artist_filter.py",
    "biography_opportunity_summary.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("REAL ARTIST BIOGRAPHY EXTRACTOR COMPLETE")
