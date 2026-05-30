import runpy
from pathlib import Path

target = Path(r"scripts/runners/run_artist_intelligence_v2.py")
runpy.run_path(str(target), run_name="__main__")
