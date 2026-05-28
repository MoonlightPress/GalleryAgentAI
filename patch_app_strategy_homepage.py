
from pathlib import Path
import re

APP_PATH = Path("app.py")
BACKUP_PATH = Path("app_before_strategy_homepage_patch.py")

if not APP_PATH.exists():
    raise SystemExit("app.py not found. Run from C:\\ScottStuff\\GalleryAgentAI")

text = APP_PATH.read_text(encoding="utf-8")
BACKUP_PATH.write_text(text, encoding="utf-8")

if "from strategy_homepage_components import render_strategy_homepage" not in text:
    text = text.replace(
        "import streamlit as st\n",
        "import streamlit as st\n\nfrom strategy_homepage_components import render_strategy_homepage\n",
        1
    )

pattern = r"(with tabs\[0\]:\n)([\s\S]*?)(\nwith tabs\[1\]:)"
match = re.search(pattern, text)

if not match:
    raise SystemExit("Could not find with tabs[0] block. Backup created.")

new_block = '''with tabs[0]:
    render_strategy_homepage()

    selected_title = st.session_state.get("selected_title")
    if selected_title:
        selected = next((o for o in opps if get_title(o) == selected_title), None)
        if selected:
            render_detail(selected)
'''

text = text[:match.start()] + new_block + match.group(3) + text[match.end():]
APP_PATH.write_text(text, encoding="utf-8")
print("Patched app.py with strategy homepage.")
print("Backup saved as app_before_strategy_homepage_patch.py")
