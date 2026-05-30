
import subprocess
import sys

PIPELINE = [
    "run_real_verification.py",
    "application_link_repair.py",
    "application_page_crawler.py",
    "opportunity_type_classifier.py",
    "application_action_report.py",
]

for script in PIPELINE:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("REPAIRED APPLICATION PIPELINE COMPLETE")
