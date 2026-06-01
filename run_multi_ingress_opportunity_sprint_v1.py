
import subprocess
import sys

for script in [
    "multi_ingress_seed_queries.py",
    "multi_ingress_web_extractor.py",
    "multi_ingress_to_opportunities.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("MULTI-INGRESS OPPORTUNITY SPRINT COMPLETE")
