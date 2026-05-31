
import subprocess
import sys

for script in [
    "tabf_entity_cleanup_v1.py",
    "tabf_publisher_ranker.py",
    "tabf_nin_overlap_report.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("TABF ENTITY CLEANUP COMPLETE")
