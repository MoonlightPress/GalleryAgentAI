import subprocess
import sys

commands = [
    ["python", "run_intelligence_pipeline.py"],
    ["python", "-m", "streamlit", "run", "app.py"],
]

for cmd in commands:
    print("=" * 70)
    print("RUNNING:", " ".join(cmd))
    print("=" * 70)
    subprocess.run(cmd)
