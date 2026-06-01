
import subprocess
import sys

PIPELINE = [
    "web_verification_engine.py",
    "link_audit_report.py",
    "submission_link_hunter.py",
    "opportunity_action_builder.py",
]

for script in PIPELINE:
    print("=" * 60)
    print("RUNNING:", script)
    print("=" * 60)

    result = subprocess.run([sys.executable, script])

    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("VERIFIER V2 LINK SAVER COMPLETE")
