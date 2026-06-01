
import subprocess
import sys

for script in [
    "opportunity_normalizer_v1.py",
    "opportunity_summary.py",
    "normalized_opportunity_review_template.py",
    "normalized_opportunity_dashboard_export.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("OPPORTUNITY NORMALIZER V1 COMPLETE")
