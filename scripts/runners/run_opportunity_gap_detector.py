
import subprocess
import sys

for script in [
    "opportunity_gap_detector.py",
    "targeted_research_queue.py",
    "dashboard_gap_export.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("OPPORTUNITY GAP DETECTOR COMPLETE")
