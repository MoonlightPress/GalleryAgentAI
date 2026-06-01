
import subprocess
import sys

for script in [
    "submission_requirements_extractor.py",
    "dashboard_checklist_export.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("SUBMISSION REQUIREMENTS EXTRACTOR COMPLETE")
