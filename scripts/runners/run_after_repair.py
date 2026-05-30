
import subprocess
import sys

steps = [
    "repair_broken_imports.py",
    "analysis_cache_builder.py",
    "pipeline_debug_summary.py",
]

for step in steps:
    print("=" * 60)
    print("RUNNING:", step)
    print("=" * 60)

    result = subprocess.run([sys.executable, step])

    if result.returncode != 0:
        raise SystemExit(f"FAILED: {step}")

print("SUCCESS")
