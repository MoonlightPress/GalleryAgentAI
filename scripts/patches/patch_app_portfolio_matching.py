
from pathlib import Path

path = Path("app.py")

if not path.exists():
    raise SystemExit("app.py not found.")

text = path.read_text(encoding="utf-8")

if "from portfolio_match_ui_components import render_portfolio_match_panel" not in text:
    text = text.replace(
        "import streamlit as st",
        "import streamlit as st\nfrom portfolio_match_ui_components import render_portfolio_match_panel"
    )

if 'st.tabs(["Mochi Atelier", "Mousehole", "Observatory", "Archive"])' in text:
    text = text.replace(
        'st.tabs(["Mochi Atelier", "Mousehole", "Observatory", "Archive"])',
        'st.tabs(["Mochi Atelier", "Portfolio Match", "Mousehole", "Observatory", "Archive"])'
    )

    text = text.replace(
        'with tabs[1]:\n    st.header("Mousehole")',
        'with tabs[1]:\n    render_portfolio_match_panel()\n\nwith tabs[2]:\n    st.header("Mousehole")'
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
    if "render_portfolio_match_panel()" not in text:
        text += '\n\nst.markdown("---")\nrender_portfolio_match_panel()\n'

path.write_text(text, encoding="utf-8")

print("Patched app with portfolio matching panel.")
