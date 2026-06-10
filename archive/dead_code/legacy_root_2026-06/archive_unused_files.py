
import fnmatch
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

MANIFEST = "project_manifest.json"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def should_archive(path, patterns, protected):
    name = path.name
    normalized = str(path).replace("\\\\", "/")
    if name in protected or normalized in protected:
        return False
    for pattern in patterns:
        if fnmatch.fnmatch(name, pattern):
            return True
    return False

def main():
    manifest = load_json(MANIFEST, {})
    if not manifest:
        print("Missing project_manifest.json")
        raise SystemExit(1)

    patterns = manifest.get("known_junk_patterns", [])
    protected = set(manifest.get("do_not_delete", []))
    archive_root = Path(manifest.get("archive_folder", "_archive"))
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_dir = archive_root / stamp
    archive_dir.mkdir(parents=True, exist_ok=True)

    moved = []
    for path in Path(".").iterdir():
        if path.name in {".git", "_archive", "__pycache__"}:
            continue
        if should_archive(path, patterns, protected):
            dest = archive_dir / path.name
            print(f"ARCHIVE: {path} -> {dest}")
            shutil.move(str(path), str(dest))
            moved.append(str(path))

    (archive_dir / "archive_manifest.txt").write_text("\\n".join(moved), encoding="utf-8")
    print(f"Moved {len(moved)} files/folders to {archive_dir}")
    print("Nothing was deleted.")

if __name__ == "__main__":
    main()
