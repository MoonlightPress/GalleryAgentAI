
import subprocess
import sys

for script in [
    "google_maps_candidate_extractor.py",
    "extracted_business_decisions_template.py",
    "ingest_extracted_business_decisions.py",
    "extracted_business_site_export.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("GOOGLE MAPS CANDIDATE EXTRACTOR V1 COMPLETE")
