
import subprocess
import sys

for script in [
    "zine_category_curator.py",
    "zine_website_top_section.py",
    "zine_website_export.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("ZINE WEBSITE TOP SECTION V1 COMPLETE")
