
import subprocess
import sys

for script in [
    "opportunity_dna_matcher.py",
    "top_10_because_report.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("OPPORTUNITY DNA MATCHER COMPLETE")
