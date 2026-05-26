import subprocess
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

pipeline = [
    "compact_view_agent.py",
    "materials_memory_agent.py",
    "pipeline_status_agent.py"
]

print()
print("RUNNING FAST LOCAL PIPELINE")
print("No discovery. No Claude. No web verification.")
print()

for script in pipeline:
    if not os.path.exists(script):
        print(f"SKIP missing: {script}")
        continue

    print(f"RUNNING: {script}")

    result = subprocess.run(["python", script])

    if result.returncode != 0:
        print()
        print("FAILED:")
        print(script)
        break

    print("OK")
    print()

print("FAST LOCAL PIPELINE FINISHED")