
from pathlib import Path
import re

path = Path("app.py")

if not path.exists():
    raise SystemExit("app.py not found.")

text = path.read_text(encoding="utf-8")

if "from feedback_ui_components import render_feedback_learning_panel" not in text:
    text = text.replace(
        "import streamlit as st",
        "import streamlit as st\nfrom feedback_ui_components import render_feedback_learning_panel"
    )

# Add Feedback tab if tabs are still the four-tab version.
if 'st.tabs(["Mochi Atelier", "Mousehole", "Observatory", "Archive"])' in text:
    text = text.replace(
        'st.tabs(["Mochi Atelier", "Mousehole", "Observatory", "Archive"])',
        'st.tabs(["Mochi Atelier", "Feedback", "Mousehole", "Observatory", "Archive"])'
    )

    text = text.replace(
        'with tabs[1]:\n    st.header("Mousehole")',
        'with tabs[1]:\n    render_feedback_learning_panel()\n\nwith tabs[2]:\n    st.header("Mousehole")'
    )

    text = text.replace(
        'with tabs[2]:\n    st.header("Observatory")',
        'with tabs[3]:\n    st.header("Observatory")'
    )

    text = text.replace(
        'with tabs[3]:\n    st.header("Archive")',
        'with tabs[4]:\n    st.header("Archive")'
    )

else:
    # If user has a newer tab layout, append a simple feedback panel after strategy homepage if possible.
    if "render_feedback_learning_panel()" not in text:
        text += '\n\nst.markdown("---")\nrender_feedback_learning_panel()\n'

path.write_text(text, encoding="utf-8")
print("Patched app with feedback learning panel.")
