
import subprocess
import sys

for script in [
    "tokyo_zine_business_collector.py",
    "zine_business_section_summary.py",
    "zine_business_dashboard_export.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("TOKYO ZINE BUSINESS COLLECTOR V1 COMPLETE")
