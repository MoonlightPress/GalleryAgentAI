
import shutil
from pathlib import Path
import subprocess
import sys

# Build the context data.
result = subprocess.run([sys.executable, "category_context_engine_v1.py"])
if result.returncode != 0:
    raise SystemExit("Category context build failed.")

# Install optional Streamlit section.
Path("ui").mkdir(exist_ok=True)
shutil.copyfile("category_context_streamlit_section.py", "ui/category_context_streamlit_section.py")

# Patch app.py.
result = subprocess.run([sys.executable, "patch_app_add_category_context.py"])
if result.returncode != 0:
    raise SystemExit("app.py patch failed.")

print("CATEGORY CONTEXT V1 COMPLETE")
print("Launch:")
print("python -m streamlit run app.py")
