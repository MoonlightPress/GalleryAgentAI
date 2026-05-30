
import subprocess
import sys

steps = [
    "repair_config_paths.py",
    "run_path_migration_check.py",
]

for step in steps:
    print("=" * 70)
    print("RUNNING:", step)
    print("=" * 70)

    result = subprocess.run([sys.executable, step])

    if result.returncode != 0:
        raise SystemExit(f"FAILED: {step}")

print("Config repair test complete.")
