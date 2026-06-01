import shutil
from pathlib import Path
import subprocess
import sys

for script in ["best_moves_engine_v1.py"]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

Path("ui").mkdir(exist_ok=True)
shutil.copyfile("best_moves_streamlit_section.py", "ui/best_moves_streamlit_section.py")

result = subprocess.run([sys.executable, "patch_app_add_best_moves.py"])
if result.returncode != 0:
    raise SystemExit("app.py patch failed.")

print("BEST MOVES SPRINT V1 COMPLETE")
print("Launch:")
print("python -m streamlit run app.py")
