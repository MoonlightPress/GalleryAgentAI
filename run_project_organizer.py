
import subprocess
import sys

result = subprocess.run([sys.executable, "organize_project_files.py"])
if result.returncode != 0:
    raise SystemExit("Organizer failed.")
print("Done.")
