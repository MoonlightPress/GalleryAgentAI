
import subprocess
import sys
from pathlib import Path

SEARCH_DIRS = [
    Path("."),
    Path("engines"),
    Path("ui"),
    Path("scripts/runners"),
    Path("scripts/patches"),
    Path("reports"),
]

OPTIONAL_SCRIPTS = {
    "strategy_explainer_generator.py",
    "deep_match_scoring_engine.py",
    "rumor_mill_engine.py",
}


def find_script(script):
    script_path = Path(script)

    if script_path.exists():
        return script_path

    for folder in SEARCH_DIRS:
        candidate = folder / script
        if candidate.exists():
            return candidate

    return None


def run_pipeline(pipeline):
    for script in pipeline:
        print()
        print("=" * 70)
        print("RUNNING:", script)
        print("=" * 70)

        resolved = find_script(script)

        if resolved is None:
            if script in OPTIONAL_SCRIPTS:
                print(f"SKIP optional missing script: {script}")
                continue
            raise SystemExit(f"FAILED required missing script: {script}")

        result = subprocess.run([sys.executable, str(resolved)])

        if result.returncode != 0:
            raise SystemExit(f"FAILED: {script}")

    print()
    print("PIPELINE COMPLETE")
