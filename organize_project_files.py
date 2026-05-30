
from pathlib import Path
import shutil
import json
from datetime import datetime

ROOT = Path(".")
REPORT_PATH = ROOT / "reports" / "project_organization_report.md"
MANIFEST_PATH = ROOT / "reports" / "project_organization_manifest.json"

KEEP_IN_ROOT = {
    "app.py",
    "run_full_mochi_pipeline.py",
    "safe_pipeline_runner.py",
    "utils_filename.py",
    "requirements.txt",
    ".gitignore",
    "README.md",
    "organize_project_files.py",
    "restore_organized_files.py",
    "project_file_finder.py",
    "run_project_organizer.py",
}

RUNNER_PREFIXES = ("run_",)
PATCH_PREFIXES = ("patch_", "repair_", "fix_")

ENGINE_SUFFIXES = (
    "_engine.py",
    "_builder.py",
    "_generator.py",
    "_ingester.py",
    "_classifier.py",
    "_importer.py",
    "_expander.py",
    "_mapper.py",
    "_audit.py",
)

UI_SUFFIXES = ("_components.py", "_styles.py")

def ensure_dirs():
    for folder in [
        "scripts/runners",
        "scripts/patches",
        "engines",
        "ui",
        "docs",
        "archive/zips",
        "archive/old_backups",
        "reports",
        "data/config",
    ]:
        Path(folder).mkdir(parents=True, exist_ok=True)

def safe_move(src, dest_dir):
    src = Path(src)
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name

    if dest.exists():
        stem = src.stem
        suffix = src.suffix
        i = 2
        while True:
            candidate = dest_dir / f"{stem}_{i}{suffix}"
            if not candidate.exists():
                dest = candidate
                break
            i += 1

    shutil.move(str(src), str(dest))
    return str(dest)

def classify(path):
    name = path.name

    if name in KEEP_IN_ROOT:
        return "keep"

    if name.endswith(".zip"):
        return "archive/zips"

    if ".before_" in name or name.endswith(".bak"):
        return "archive/old_backups"

    if name.endswith(".md") and path.parent == ROOT:
        return "docs"

    if name.endswith(".json") and path.parent == ROOT:
        return "data/config"

    if name.endswith(".py"):
        if name.startswith(RUNNER_PREFIXES):
            return "scripts/runners"
        if name.startswith(PATCH_PREFIXES):
            return "scripts/patches"
        if name.endswith(UI_SUFFIXES):
            return "ui"
        if name.endswith(ENGINE_SUFFIXES):
            return "engines"

    return "keep"

def move_misplaced_python_from_reports(manifest):
    reports = ROOT / "reports"
    if not reports.exists():
        return

    for path in list(reports.glob("*.py")):
        target = classify(path)
        if target == "keep":
            target = "scripts/runners" if path.name.startswith("run_") else "scripts/patches"
        dest = safe_move(path, target)
        manifest.append({
            "from": str(path),
            "to": dest,
            "reason": "misplaced Python file in reports",
        })

def organize_root_files(manifest):
    for path in list(ROOT.iterdir()):
        if not path.is_file():
            continue
        target = classify(path)
        if target == "keep":
            continue
        dest = safe_move(path, target)
        manifest.append({
            "from": str(path),
            "to": dest,
            "reason": f"classified as {target}",
        })

def create_root_shortcuts():
    shortcuts = {
        "run_discovery_expansion.py": "scripts/runners/run_discovery_expansion.py",
        "run_artist_intelligence_v2.py": "scripts/runners/run_artist_intelligence_v2.py",
        "run_visual_profile_bucket_upgrade.py": "scripts/runners/run_visual_profile_bucket_upgrade.py",
        "run_verification_upgrade.py": "scripts/runners/run_verification_upgrade.py",
        "run_source_expansion_value_patch.py": "scripts/runners/run_source_expansion_value_patch.py",
    }

    created = []

    for root_name, target in shortcuts.items():
        target_path = Path(target)
        if not target_path.exists():
            continue

        root_path = ROOT / root_name
        if root_path.exists():
            continue

        code = (
            "import runpy\n"
            "from pathlib import Path\n\n"
            f'target = Path(r"{target}")\n'
            'runpy.run_path(str(target), run_name="__main__")\n'
        )

        root_path.write_text(code, encoding="utf-8")
        created.append(root_name)

    return created

def write_report(manifest, shortcuts):
    lines = [
        "# Project Organization Report",
        "",
        f"Run time: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Moved Files",
        "",
    ]

    if not manifest:
        lines.append("No files moved.")
    else:
        for item in manifest:
            lines.append(f"- `{item['from']}` → `{item['to']}` — {item['reason']}")

    lines += ["", "## Root Shortcuts Created", ""]

    if not shortcuts:
        lines.append("No shortcuts created.")
    else:
        for item in shortcuts:
            lines.append(f"- `{item}`")

    lines += [
        "",
        "## Rules Going Forward",
        "",
        "- `reports/` should contain reports only.",
        "- `scripts/runners/` contains runner scripts.",
        "- `scripts/patches/` contains one-time patch/fix/repair scripts.",
        "- `engines/` contains reusable engines.",
        "- `ui/` contains UI helper modules.",
        "- `archive/` contains old zips and backups.",
    ]

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

def main():
    ensure_dirs()
    manifest = []
    move_misplaced_python_from_reports(manifest)
    organize_root_files(manifest)
    shortcuts = create_root_shortcuts()
    write_report(manifest, shortcuts)

    print("Project organization complete.")
    print(f"Moved files: {len(manifest)}")
    print(f"Shortcuts created: {len(shortcuts)}")
    print(f"Report: {REPORT_PATH}")

if __name__ == "__main__":
    main()
