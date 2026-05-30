
import subprocess
import sys

for script in [
    "opportunity_type_classifier.py",
    "application_action_report.py",
]:
    print("=" * 60)
    print("RUNNING:", script)
    print("=" * 60)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("OPPORTUNITY TYPE PATCH COMPLETE")
