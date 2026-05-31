
import subprocess
import sys

for script in [
    "official_page_extractor.py",
    "actionable_target_refiner.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("OFFICIAL PAGE EXTRACTOR COMPLETE")
