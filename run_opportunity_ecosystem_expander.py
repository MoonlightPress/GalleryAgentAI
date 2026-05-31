
import subprocess
import sys

for script in [
    "opportunity_ecosystem_expander.py",
    "ecosystem_density_score.py",
    "opportunity_career_path_report.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("OPPORTUNITY ECOSYSTEM EXPANDER COMPLETE")
