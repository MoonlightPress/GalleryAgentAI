
from pathlib import Path

path = Path("app.py")

if not path.exists():
    raise SystemExit("app.py not found.")

text = path.read_text(encoding="utf-8")
old = text

if "from compact_detail_components import render_compact_detail" not in text:
    # Add near streamlit import if possible.
    if "import streamlit as st" in text:
        text = text.replace(
            "import streamlit as st",
            "import streamlit as st\nfrom compact_detail_components import render_compact_detail"
        )
    else:
        text = "from compact_detail_components import render_compact_detail\n" + text

css_loader = 