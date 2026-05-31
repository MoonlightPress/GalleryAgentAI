
import subprocess
import sys

for script in [
    "relevance_engine_v1.py",
    "opportunity_evidence_cards.py",
    "dashboard_evidence_cards_export.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("RELEVANCE ENGINE V1 COMPLETE")
