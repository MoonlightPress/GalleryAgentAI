
from pathlib import Path
import json
import shutil

MANIFEST_PATH = Path("reports/project_organization_manifest.json")

def main():
    if not MANIFEST_PATH.exists():
        raise SystemExit("No manifest found. Cannot restore.")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    for item in reversed(manifest):
        src = Path(item["to"])
        dest = Path(item["from"])

        if not src.exists():
            print(f"SKIP missing moved file: {src}")
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)

        if dest.exists():
            print(f"SKIP destination already exists: {dest}")
            continue

        shutil.move(str(src), str(dest))
        print(f"RESTORED {src} -> {dest}")

    print("Restore complete.")

if __name__ == "__main__":
    main()
