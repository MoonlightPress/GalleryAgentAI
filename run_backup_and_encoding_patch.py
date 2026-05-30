
import subprocess
import sys

PIPELINE = [
    "encoding_request_patch.py",
    "deployment_readiness_audit.py",
]

for script in PIPELINE:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("BACKUP AND ENCODING PATCH COMPLETE")
print("Next recommended command:")
print("python project_backup_git_helper.py")
print("git push")
