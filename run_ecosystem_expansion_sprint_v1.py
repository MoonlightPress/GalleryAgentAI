
import subprocess
import sys

for script in [
    "gallery_ecosystem_mapper_v1.py",
    "fair_ecosystem_mapper_v1.py",
    "open_call_verifier_v2.py",
    "opportunity_heatmap_v1.py",
    "ecosystem_battle_plans_v1.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("ECOSYSTEM EXPANSION SPRINT V1 COMPLETE")
