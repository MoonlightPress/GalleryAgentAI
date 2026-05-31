
import subprocess
import sys

for script in [
    "nin_similarity_engine.py",
    "opportunity_similarity_map.py",
    "nin_opportunity_recommendations.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("NIN SIMILARITY ENGINE COMPLETE")
