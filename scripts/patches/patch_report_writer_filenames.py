
from pathlib import Path
import re

def ensure_import(text):
    if "from utils_filename import safe_filename" in text:
        return text

    lines = text.splitlines()
    last_import = -1

    for i, line in enumerate(lines):
        if line.startswith("import ") or line.startswith("from "):
            last_import = i

    if last_import >= 0:
        lines.insert(last_import + 1, "from utils_filename import safe_filename")
        return "\n".join(lines) + "\n"

    return "from utils_filename import safe_filename\n" + text


def remove_local_safe_function(text):
    pattern = re.compile(
        r'\ndef (safe|safe_filename)\([^\n]*\):\n'
        r'(?:    .*\n|    \n)+',
        re.MULTILINE,
    )
    return pattern.sub("\n", text)


def patch_portfolio_pitch():
    p = Path("portfolio_pitch_generator.py")
    if not p.exists():
        print("SKIP missing portfolio_pitch_generator.py")
        return

    text = p.read_text(encoding="utf-8")
    old = text

    text = ensure_import(text)
    text = remove_local_safe_function(text)

    text = text.replace(
        'path = Path(OUT_DIR) / f"{safe_filename(title)}.md"',
        'path = Path(OUT_DIR) / f"{safe_filename(title, max_len=80)}.md"'
    )

    text = text.replace(
        'path = Path(OUT_DIR) / f"{safe(title)}.md"',
        'path = Path(OUT_DIR) / f"{safe_filename(title, max_len=80)}.md"'
    )

    # Emergency direct replacement for current observed failure.
    text = text.replace(
        'f"{title}.md"',
        'f"{safe_filename(title, max_len=80)}.md"'
    )

    if text != old:
        p.with_suffix(".py.before_report_writer_filename_fix").write_text(old, encoding="utf-8")
        p.write_text(text, encoding="utf-8")
        print("PATCHED portfolio_pitch_generator.py")
    else:
        print("NO CHANGE portfolio_pitch_generator.py")


def patch_smart_cover():
    p = Path("smart_cover_letter_engine.py")
    if not p.exists():
        print("SKIP missing smart_cover_letter_engine.py")
        return

    text = p.read_text(encoding="utf-8")
    old = text

    text = ensure_import(text)
    text = remove_local_safe_function(text)

    text = text.replace(
        'Path(OUT_DIR) / f"{safe(title)}.md"',
        'Path(OUT_DIR) / f"{safe_filename(title, max_len=90)}.md"'
    )

    text = text.replace(
        'Path(OUT_DIR) / f"{title}.md"',
        'Path(OUT_DIR) / f"{safe_filename(title, max_len=90)}.md"'
    )

    if text != old:
        p.with_suffix(".py.before_report_writer_filename_fix").write_text(old, encoding="utf-8")
        p.write_text(text, encoding="utf-8")
        print("PATCHED smart_cover_letter_engine.py")
    else:
        print("NO CHANGE smart_cover_letter_engine.py")


def main():
    patch_portfolio_pitch()
    patch_smart_cover()
    print("Report writer filename patch complete.")


if __name__ == "__main__":
    main()
