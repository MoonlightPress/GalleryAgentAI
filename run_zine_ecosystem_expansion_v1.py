
import subprocess
import sys

for script in [
    "zine_ecosystem_seed.py",
    "zine_ecosystem_report.py",
    "zine_battle_plan.py",
    "zine_dashboard_export.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("ZINE ECOSYSTEM EXPANSION V1 COMPLETE")
