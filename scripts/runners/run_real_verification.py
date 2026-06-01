
import subprocess
import sys

for script in [
    "web_verification_engine.py",
    "verified_opportunity_importer.py",
]:
    print("=" * 60)
    print("RUNNING:", script)
    print("=" * 60)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("REAL VERIFICATION COMPLETE")
