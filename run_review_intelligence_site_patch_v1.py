import shutil
from pathlib import Path
import subprocess
import sys

Path("ui").mkdir(exist_ok=True)
shutil.copyfile("opportunity_review_sections.py", "ui/opportunity_review_sections.py")

result = subprocess.run([sys.executable, "patch_app_add_review_intelligence.py"])
if result.returncode != 0:
    raise SystemExit("app.py patch failed.")

print("REVIEW INTELLIGENCE SITE PATCH COMPLETE")
print("Launch:")
print("python -m streamlit run app.py")
