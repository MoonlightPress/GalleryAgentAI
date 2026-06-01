
import subprocess
import sys

for script in ["historical_artist_crawler_v2.py", "historical_artist_quality_audit.py"]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("HISTORICAL ARTIST CRAWLER V2 COMPLETE")
