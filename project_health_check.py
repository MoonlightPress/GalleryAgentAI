
import json
import os
from pathlib import Path

MANIFEST = "project_manifest.json"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def file_status(path):
    p = Path(path)
    if not p.exists():
        return "MISSING", ""
    if p.is_file():
        return "OK", f"{p.stat().st_size} bytes"
    return "NOT FILE", ""

def folder_status(path):
    p = Path(path)
    if not p.exists():
        return "MISSING", "0 files"
    count = len([x for x in p.rglob("*") if x.is_file()])
    return "OK", f"{count} files"

def main():
    manifest = load_json(MANIFEST, {})
    if not manifest:
        print("Missing project_manifest.json")
        raise SystemExit(1)

    print("\\nMOCHI PROJECT HEALTH CHECK")
    print("=" * 70)

    file_groups = [
        ("CORE APP FILES", manifest.get("core_app_files", [])),
        ("CORE DATA FILES", manifest.get("core_data_files", [])),
        ("CORE ENGINE FILES", manifest.get("core_engine_files", [])),
        ("CORE UI FILES", manifest.get("core_ui_files", [])),
    ]

    missing = []

    for label, paths in file_groups:
        print(f"\\n{label}")
        print("-" * 70)
        for path in paths:
            status, info = file_status(path)
            print(f"{status:10} {path} {info}")
            if status == "MISSING":
                missing.append(path)

    print("\\nASSET FOLDERS")
    print("-" * 70)
    for path in manifest.get("asset_folders", []):
        status, info = folder_status(path)
        print(f"{status:10} {path} {info}")

    print("\\nGENERATED FOLDERS")
    print("-" * 70)
    for path in manifest.get("generated_folders", []):
        status, info = folder_status(path)
        print(f"{status:10} {path} {info}")

    print("\\nSUMMARY")
    print("-" * 70)
    if missing:
        print("Missing required files:")
        for path in missing:
            print(f"- {path}")
    else:
        print("Core files present.")

if __name__ == "__main__":
    main()
