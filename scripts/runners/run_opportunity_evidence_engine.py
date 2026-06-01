
import subprocess
import sys

for script in [
    "opportunity_evidence_engine.py",
    "opportunity_quality_board.py",
    "dashboard_evidence_export.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("OPPORTUNITY EVIDENCE ENGINE COMPLETE")
