
import subprocess
import sys

for script in [
    "category_metrics_v1.py",
    "zine_battle_plan_metrics.py",
    "zine_website_metrics_merge.py",
    "category_metrics_dashboard_export.py",
]:
    print("=" * 70)
    print("RUNNING:", script)
    print("=" * 70)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {script}")

print("CATEGORY METRICS V1 COMPLETE")
