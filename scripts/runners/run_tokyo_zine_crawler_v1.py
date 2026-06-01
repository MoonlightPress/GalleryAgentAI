
import subprocess
import sys

for script in [
    "tokyo_zine_ecosystem_crawler.py",
    "zine_section_summary.py",
    "zine_site_export.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("TOKYO ZINE CRAWLER V1 COMPLETE")
