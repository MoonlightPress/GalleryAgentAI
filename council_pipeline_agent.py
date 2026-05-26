import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import subprocess

pipeline = [
    "opportunity_discovery_agent.py",
    "opportunity_validator.py",
    "opportunity_resolution_agent.py",
    "artist_profile_agent.py",
    "opportunity_ranking_agent.py",
    "opportunity_filter_agent.py",
    "submission_packet_agent.py",
    "incremental_council_agent.py",
    "compact_view_agent.py",
    "materials_memory_agent.py",
    "pipeline_status_agent.py"
]

print()
print("RUNNING FULL COUNCIL PIPELINE")
print()

for script in pipeline:

    print(f"RUNNING: {script}")

    result = subprocess.run(
        ["python", script],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        print()
        print("FAILED:")
        print(script)
        print()
        print(result.stderr)

        break

    else:

        print("OK")
        print()

print("PIPELINE FINISHED")