
import subprocess
import sys

for script in [
    "career_channel_engine.py",
    "career_battle_plan_generator.py",
    "career_overview_generator.py",
    "dashboard_career_channel_export.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("CAREER CHANNEL ENGINE COMPLETE")
