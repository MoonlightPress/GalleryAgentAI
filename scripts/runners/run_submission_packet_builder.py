
import subprocess
import sys

PIPELINE = [
    "submission_packet_builder.py",
    "artist_packet_templates.py",
    "do_not_submit_yet_report.py",
]

for script in PIPELINE:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("SUBMISSION PACKET BUILDER COMPLETE")
