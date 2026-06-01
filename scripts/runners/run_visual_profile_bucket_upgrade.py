import runpy
from pathlib import Path

target = Path(r"scripts/runners/run_visual_profile_bucket_upgrade.py")
runpy.run_path(str(target), run_name="__main__")
