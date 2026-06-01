
import subprocess
import sys

PIPELINE = [
    "target_shortlist_builder.py",
    "outreach_email_builder.py",
    "portfolio_prep_checklist_builder.py",
    "waste_filter_report.py",
]

for script in PIPELINE:
    print("=" * 60)
    print("RUNNING:", script)
    print("=" * 60)

    result = subprocess.run([sys.executable, script])

    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("OUTREACH PACK COMPLETE")
