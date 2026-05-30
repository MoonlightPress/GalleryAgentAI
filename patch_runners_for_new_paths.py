
from pathlib import Path

TARGETS = [
    Path("run_full_mochi_pipeline.py"),
    *Path("scripts/runners").glob("run_*.py"),
    *Path(".").glob("run_*.py"),
]

def patch_file(path):
    if not path.exists():
        return False

    text = path.read_text(encoding="utf-8")
    old = text

    text = text.replace(
        "from safe_pipeline_runner import run_pipeline",
        "from smart_pipeline_runner import run_pipeline",
    )

    text = text.replace(
        "from safe_pipeline_runner import run_script",
        "from smart_pipeline_runner import run_script",
    )

    # If a runner hardcodes subprocess directly, leave it alone for now.
    if text != old:
        backup = path.with_suffix(path.suffix + ".before_path_migration")
        backup.write_text(old, encoding="utf-8")
        path.write_text(text, encoding="utf-8")
        print(f"PATCHED {path}")
        return True

    print(f"NO CHANGE {path}")
    return False

def main():
    seen = set()
    count = 0

    for path in TARGETS:
        real = str(path)
        if real in seen:
            continue
        seen.add(real)

        if patch_file(path):
            count += 1

    print(f"Patched runners: {count}")

if __name__ == "__main__":
    main()
