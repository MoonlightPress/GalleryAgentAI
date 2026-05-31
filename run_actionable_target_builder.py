
import subprocess
import sys

for script in [
    "actionable_target_builder.py",
    "dashboard_actionable_export.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("ACTIONABLE TARGET BUILDER COMPLETE")
