import runpy
from pathlib import Path

target = Path(r"scripts/runners/run_discovery_expansion.py")
runpy.run_path(str(target), run_name="__main__")
