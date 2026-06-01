
import shutil
from pathlib import Path
import subprocess
import sys

# 1. Add publishing opportunities to the existing opportunity feed.
result = subprocess.run([sys.executable, "publishing_targets_to_opportunities.py"])
if result.returncode != 0:
    raise SystemExit("Publishing import failed.")

# 2. Add Streamlit renderer.
Path("ui").mkdir(exist_ok=True)
shutil.copyfile("publishing_opportunity_section.py", "ui/publishing_opportunity_section.py")

# 3. Patch app.py.
result = subprocess.run([sys.executable, "patch_app_add_publishing_section.py"])
if result.returncode != 0:
    raise SystemExit("app.py patch failed.")

print("PUBLISHING INTO EXISTING OPPORTUNITIES COMPLETE")
print("Launch:")
print("python -m streamlit run app.py")
