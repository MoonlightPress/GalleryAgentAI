
from pathlib import Path

path = Path("app.py")

if not path.exists():
    raise SystemExit("app.py not found.")

text = path.read_text(encoding="utf-8")

if "from artist_image_review_components import render_artist_image_review_panel" not in text:
    text = text.replace(
        "import streamlit as st",
        "import streamlit as st\nfrom artist_image_review_components import render_artist_image_review_panel"
    )

if 'st.tabs(["Mochi Atelier", "Mousehole", "Observatory", "Archive"])' in text:
    text = text.replace(
        'st.tabs(["Mochi Atelier", "Mousehole", "Observatory", "Archive"])',
        'st.tabs(["Mochi Atelier", "Artist Images", "Mousehole", "Observatory", "Archive"])'
    )

    text = text.replace(
        'with tabs[1]:\n    st.header("Mousehole")',
        'with tabs[1]:\n    render_artist_image_review_panel()\n\nwith tabs[2]:\n    st.header("Mousehole")'
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
    if "render_artist_image_review_panel()" not in text:
        text += '\n\nst.markdown("---")\nrender_artist_image_review_panel()\n'

path.write_text(text, encoding="utf-8")

print("Patched app with Artist Images review panel.")
