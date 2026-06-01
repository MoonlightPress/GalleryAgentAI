
import subprocess
import sys

for script in [
    "opportunity_pitch_generator.py",
    "shiny_cards_export.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("OPPORTUNITY PITCH GENERATOR COMPLETE")
