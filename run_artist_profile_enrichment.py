
import subprocess
import sys

for script in [
    "artist_profile_enrichment_engine.py",
    "artist_cluster_engine.py",
    "opportunity_artist_map.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("ARTIST PROFILE ENRICHMENT COMPLETE")
