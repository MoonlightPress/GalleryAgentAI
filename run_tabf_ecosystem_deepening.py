
import subprocess
import sys

for script in [
    "tabf_exhibitor_crawler.py",
    "merge_tabf_ecosystem.py",
    "ecosystem_coverage_gap_report.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("TABF ECOSYSTEM DEEPENING COMPLETE")
