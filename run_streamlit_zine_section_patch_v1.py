
import shutil
from pathlib import Path
import subprocess
import sys

Path("ui").mkdir(exist_ok=True)
shutil.copyfile("zine_opportunity_section.py", "ui/zine_opportunity_section.py")

result = subprocess.run([sys.executable, "patch_app_add_zine_section.py"])
if result.returncode != 0:
    raise SystemExit("Patch failed.")

print("STREAMLIT ZINE SECTION PATCH COMPLETE")
print("Run the app with:")
print("python -m streamlit run app.py")
