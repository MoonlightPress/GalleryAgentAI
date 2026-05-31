
import subprocess
import sys

for script in [
    "research_completeness_audit.py",
    "research_task_queue_builder.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("RESEARCH COMPLETENESS AUDIT COMPLETE")
