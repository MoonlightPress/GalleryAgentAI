
import subprocess
import sys

for script in [
    "submission_link_hunter.py",
    "requirement_extractor.py",
    "opportunity_action_builder.py",
]:
    print("=" * 60)
    print("RUNNING:", script)
    print("=" * 60)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("SUBMISSION LINK PRECISION PATCH COMPLETE")
