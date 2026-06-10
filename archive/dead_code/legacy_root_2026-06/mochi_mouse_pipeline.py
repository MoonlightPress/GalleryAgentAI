import subprocess
import os


pipeline = [
    "pathway_progress_agent.py",
    "mousehole_task_progress_agent.py",
    "daily_suggestions_agent.py",
    "fast_local_pipeline.py"
]

print()
print("RUNNING MOCHI + MOUSE LOCAL PIPELINE")
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

print("MOCHI + MOUSE PIPELINE FINISHED")