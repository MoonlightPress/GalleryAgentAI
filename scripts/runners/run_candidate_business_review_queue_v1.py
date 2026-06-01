
import subprocess
import sys

for script in [
    "candidate_business_queue_builder.py",
    "candidate_business_decisions_template.py",
    "approved_business_ingest.py",
    "business_review_dashboard_export.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("CANDIDATE BUSINESS REVIEW QUEUE V1 COMPLETE")
