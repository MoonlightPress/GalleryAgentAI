from pathlib import Path


FILES = [
    "council_agent.py",
    "compact_view_agent.py"
]


REPLACEMENTS = [
    (
        "skip",
        "low strategic priority"
    ),
    (
        "avoid",
        "high caution"
    ),
    (
        "wrong fit",
        "better suited to a different strategic direction"
    ),
    (
        "undermines positioning",
        "supports a different positioning strategy"
    ),
    (
        "not recommended",
        "limited strategic value"
    ),
    (
        "poor fit",
        "requires careful evaluation"
    ),
]


for filename in FILES:
    path = Path(filename)

    if not path.exists():
        print(f"Missing: {filename}")
        continue

    text = path.read_text(encoding="utf-8")

    original = text

    for old, new in REPLACEMENTS:
        text = text.replace(old, new)

    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"PATCHED: {filename}")
    else:
        print(f"NO CHANGES: {filename}")