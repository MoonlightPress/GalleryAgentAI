
import subprocess
import sys

for script in [
    "gallery_quality_refiner_v1.py",
    "art_fair_expansion_v1.py",
    "verification_field_extractor_v1.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("INGRESS REFINEMENT SPRINT V1 COMPLETE")
