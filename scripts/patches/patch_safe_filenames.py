
from pathlib import Path

def add_import(text, import_line):
    if import_line.strip() in text:
        return text
    lines = text.splitlines()
    last = -1
    for i, line in enumerate(lines):
        if line.startswith("import ") or line.startswith("from "):
            last = i
    if last >= 0:
        lines.insert(last + 1, import_line.strip())
        return "\n".join(lines) + "\n"
    return import_line + text

def patch_analysis_cache():
    p = Path("analysis_cache_builder.py")
    if not p.exists():
        print("missing analysis_cache_builder.py")
        return
    text = p.read_text(encoding="utf-8")
    old = text
    text = add_import(text, "from utils_filename import safe_slug\n")
    text = text.replace(
        'path = CACHE_DIR / f"{idx:03d}_{slug(title)[:80]}.md"',
        'path = CACHE_DIR / f"{idx:03d}_{safe_slug(title, max_len=80)}.md"'
    )
    if text != old:
        p.with_suffix(".py.before_filename_fix").write_text(old, encoding="utf-8")
        p.write_text(text, encoding="utf-8")
        print("patched analysis_cache_builder.py")

def patch_opportunity_report():
    p = Path("opportunity_report_engine.py")
    if not p.exists():
        print("missing opportunity_report_engine.py")
        return
    text = p.read_text(encoding="utf-8")
    old = text
    text = add_import(text, "from utils_filename import safe_filename\n")
    text = text.replace(
        'title = (opp.get("title") or opp.get("name") or f"opportunity_{idx}").replace("/", "-").replace("\\\\", "-")',
        'title = safe_filename(opp.get("title") or opp.get("name") or f"opportunity_{idx}", max_len=70)'
    )
    if text != old:
        p.with_suffix(".py.before_filename_fix").write_text(old, encoding="utf-8")
        p.write_text(text, encoding="utf-8")
        print("patched opportunity_report_engine.py")

def patch_inquiry():
    p = Path("inquiry_draft_generator.py")
    if not p.exists():
        print("missing inquiry_draft_generator.py")
        return
    text = p.read_text(encoding="utf-8")
    old = text
    text = add_import(text, "from utils_filename import safe_filename\n")
    text = text.replace(
        'safe_title = title_of(opp).replace("/", "-").replace("\\\\", "-")[:60]',
        'safe_title = safe_filename(title_of(opp), max_len=60)'
    )
    if text != old:
        p.with_suffix(".py.before_filename_fix").write_text(old, encoding="utf-8")
        p.write_text(text, encoding="utf-8")
        print("patched inquiry_draft_generator.py")

def main():
    patch_analysis_cache()
    patch_opportunity_report()
    patch_inquiry()

if __name__ == "__main__":
    main()
