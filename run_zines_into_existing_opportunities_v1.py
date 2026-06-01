
import subprocess
import sys

for script in [
    "zine_targets_to_opportunities.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("ZINES INTO EXISTING OPPORTUNITIES COMPLETE")
