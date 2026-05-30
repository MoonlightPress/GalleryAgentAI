
from pathlib import Path
import re

TARGET_FILES = [
    "opportunity_report_engine.py",
    "analysis_cache_builder.py",
    "inquiry_draft_generator.py",
    "portfolio_pitch_generator.py",
    "smart_cover_letter_engine.py",
    "source_dossier_generator.py",
    "curator_dossier_engine.py",
    "institution_profile_engine.py",
]


def add_import(text, import_line):
    if import_line.strip() in text:
        return text

    lines = text.splitlines()
    last_import_idx = -1

    for i, line in enumerate(lines):
        if line.startswith("import ") or line.startswith("from "):
            last_import_idx = i

    if last_import_idx >= 0:
        lines.insert(last_import_idx + 1, import_line.strip())
        return "\n".join(lines) + "\n"

    return import_line + text


def remove_local_safe_filename(text):
    """
    Remove simple local safe_filename/safe_slug functions that conflict
    with utils_filename.py.

    This intentionally only removes top-level functions named safe_filename
    or safe_slug and stops at the next top-level def/class/import/constant.
    """

    pattern = re.compile(
        r'\ndef (safe_filename|safe_slug)\([^\n]*\):\n'
        r'(?:    .*\n|    \n)+',
        re.MULTILINE,
    )

    return pattern.sub("\n", text)


def patch_calls(text):
    # Normalize common old function argument names.
    text = text.replace("max_length=", "max_len=")

    # Fix accidental calls where old local function accepted only one arg
    # but new utility can handle it. No further change needed.

    return text


def patch_file(path):
    p = Path(path)

    if not p.exists():
        print(f"SKIP missing: {path}")
        return

    original = p.read_text(encoding="utf-8")
    text = original

    text = remove_local_safe_filename(text)

    if "safe_slug(" in text and "from utils_filename import safe_slug" not in text:
        text = add_import(text, "from utils_filename import safe_slug\n")

    if "safe_filename(" in text and "from utils_filename import safe_filename" not in text:
        text = add_import(text, "from utils_filename import safe_filename\n")

    text = patch_calls(text)

    if text != original:
        backup = p.with_suffix(p.suffix + ".before_filename_collision_fix")
        backup.write_text(original, encoding="utf-8")
        p.write_text(text, encoding="utf-8")
        print(f"PATCHED {path}")
    else:
        print(f"NO CHANGE {path}")


def main():
    for path in TARGET_FILES:
        patch_file(path)

    print("")
    print("Filename collision patch complete.")


if __name__ == "__main__":
    main()
