from pathlib import Path

p = Path("opportunity_report_engine.py")
text = p.read_text(encoding="utf-8")

text = text.replace(
    'f"reports/opportunities/{idx:03d}_{title[:60]}.md"',
    'f"reports/opportunities/{idx:03d}_{safe_filename(title)}.md"'
)

if "def safe_filename" not in text:
    text = text.replace(
        "import os\n",
        """import os
import re

def safe_filename(name):
    name = str(name)
    name = re.sub(r'[<>:"/\\\\|?*]', '_', name)
    name = re.sub(r'\\s+', ' ', name).strip()
    return name[:80]
"""
    )

p.write_text(text, encoding="utf-8")
print("Patched.")