
import subprocess
import sys

for script in [
    "tabf_real_entity_validator.py",
    "tabf_contact_harvester_queue.py",
    "tabf_validated_overlap_report.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("TABF REAL ENTITY VALIDATOR COMPLETE")
