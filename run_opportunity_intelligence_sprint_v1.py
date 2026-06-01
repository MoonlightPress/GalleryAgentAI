
import subprocess
import sys

for script in [
    "opportunity_canonicalizer_v1.py",
    "gallery_discovery_v1.py",
    "opportunity_enrichment_v1.py",
    "enriched_to_compact_opportunities.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("OPPORTUNITY INTELLIGENCE SPRINT V1 COMPLETE")
