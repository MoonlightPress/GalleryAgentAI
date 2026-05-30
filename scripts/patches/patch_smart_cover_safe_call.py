
from pathlib import Path

path = Path("smart_cover_letter_engine.py")

if not path.exists():
    raise SystemExit("smart_cover_letter_engine.py not found.")

text = path.read_text(encoding="utf-8")
old = text

if "from utils_filename import safe_filename" not in text:
    lines = text.splitlines()
    last_import = -1
    for i, line in enumerate(lines):
        if line.startswith("import ") or line.startswith("from "):
            last_import = i
    if last_import >= 0:
        lines.insert(last_import + 1, "from utils_filename import safe_filename")
        text = "\n".join(lines) + "\n"
    else:
        text = "from utils_filename import safe_filename\n" + text

# Replace all remaining old helper calls.
text = text.replace('f"{safe(title)}.md"', 'f"{safe_filename(title, max_len=90)}.md"')
text = text.replace("f'{safe(title)}.md'", "f'{safe_filename(title, max_len=90)}.md'")
text = text.replace("safe(title)", "safe_filename(title, max_len=90)")

# Remove any old local safe() function if it still exists.
start = text.find("def safe(text):")
if start != -1:
    next_def = text.find("\ndef ", start + 1)
    if next_def != -1:
        text = text[:start] + "\n" + text[next_def + 1:]
    else:
        text = text[:start]

if text != old:
    path.with_suffix(".py.before_smart_cover_safe_fix").write_text(old, encoding="utf-8")
    path.write_text(text, encoding="utf-8")
    print("PATCHED smart_cover_letter_engine.py")
else:
    print("NO CHANGE smart_cover_letter_engine.py")

print("Done.")
