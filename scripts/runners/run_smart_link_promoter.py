
import subprocess
import sys

for script in ["smart_link_promoter.py", "actionable_target_link_refiner.py"]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("SMART LINK PROMOTER COMPLETE")
