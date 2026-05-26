import subprocess
import os


pipeline = [
    "career_reconstruction_agent.py",
    "artist_graph_builder.py",
    "trajectory_scoring_agent.py",
    "ecosystem_bridge_agent.py",
    "career_compound_scoring_agent.py",
    "fast_local_pipeline.py"
]

print()
print("RUNNING CAREER INTELLIGENCE PIPELINE")
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

print("CAREER INTELLIGENCE PIPELINE COMPLETE")