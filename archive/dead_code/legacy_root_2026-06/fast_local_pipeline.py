import subprocess
import os


pipeline = [
    "opportunity_database_agent.py",
    "compact_view_agent.py",
    "opportunity_stats_agent.py",
    "pipeline_status_agent.py"
]


print()
print("RUNNING FAST LOCAL PIPELINE")
print("No Claude. No web. No council regeneration.")
print()

for script in pipeline:
    if not os.path.exists(script):
        print(f"SKIP missing: {script}")
        continue

    print(f"RUNNING: {script}")

    result = subprocess.run(["python", script])

    if result.returncode != 0:
        print(f"FAILED: {script}")
        raise SystemExit(result.returncode)

    print("OK")
    print()

print("FAST LOCAL PIPELINE FINISHED")