import subprocess
import os


pipeline = [
    "artist_intelligence_agent.py",
    "artist_preference_questions_agent.py",
    "pathway_progress_agent.py"
]

print()
print("RUNNING ARTIST INTELLIGENCE PIPELINE")
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

print("ARTIST INTELLIGENCE PIPELINE FINISHED")