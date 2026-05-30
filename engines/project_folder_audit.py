
from pathlib import Path
from collections import defaultdict

OUT_PATH = Path("reports/project_folder_audit.md")

GROUPS = {
    "patch_*.py": "Patch scripts",
    "run_*.py": "Runner scripts",
    "*_engine.py": "Engine scripts",
    "*_components.py": "UI component scripts",
    "README*.md": "README files",
    "*.zip": "Zip files",
    "*.json": "Top-level JSON files",
}

KEEP_ROOT = {
    "app.py",
    "requirements.txt",
    "run_full_mochi_pipeline.py",
    "safe_pipeline_runner.py",
    "utils_filename.py",
}

def main():
    root = Path(".")
    lines = [
        "# Project Folder Audit",
        "",
        "This is a cleanup planning report. It does not move files.",
        "",
        "## Files that should probably remain in root",
        "",
    ]

    for name in sorted(KEEP_ROOT):
        status = "exists" if Path(name).exists() else "missing"
        lines.append(f"- {name} — {status}")

    lines += ["", "## Suggested future folders", ""]
    lines += [
        "- `scripts/patches/` for patch scripts",
        "- `scripts/runners/` for run scripts",
        "- `engines/` for scoring/research/intelligence engines",
        "- `ui/` for Streamlit component modules",
        "- `docs/` for README files",
        "- `archive/zips/` for old generated zip packages",
        "- `data/` or keep existing `memory/`, `deploy_data/`, `reports/`, `ingestion/`",
        "",
        "## Current root clutter by pattern",
        "",
    ]

    for pattern, label in GROUPS.items():
        files = sorted(str(p) for p in root.glob(pattern) if p.is_file())
        lines.append(f"### {label} — {len(files)}")
        lines.append("")
        for f in files[:80]:
            lines.append(f"- {f}")
        if len(files) > 80:
            lines.append(f"- ... and {len(files) - 80} more")
        lines.append("")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_PATH}")

if __name__ == "__main__":
    main()
