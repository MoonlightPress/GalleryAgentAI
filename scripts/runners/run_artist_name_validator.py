
import subprocess
import sys

for script in [
    "artist_name_validator_v1.py",
    "validated_opportunity_credibility.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("ARTIST NAME VALIDATOR COMPLETE")
