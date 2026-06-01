
import subprocess
import sys

PIPELINE = [
    "deep_submission_page_reader.py",
    "submission_requirement_extractor.py",
    "deadline_fee_extractor.py",
    "artist_readiness_builder.py",
]

for script in PIPELINE:
    print("=" * 60)
    print("RUNNING:", script)
    print("=" * 60)

    result = subprocess.run([sys.executable, script])

    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("SUBMISSION INTELLIGENCE COMPLETE")
