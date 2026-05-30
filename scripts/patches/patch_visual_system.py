
from pathlib import Path

app = Path("app.py")

text = app.read_text(encoding="utf-8")

if "from visual_card_system import *" not in text:
    text = text.replace(
        "from relationship_ui_components import *",
        "from relationship_ui_components import *\nfrom visual_card_system import *\nfrom report_layout_upgrade import *"
    )

if 'generated_visual_upgrade.css' not in text:

    inject = """
with open("styles/generated_visual_upgrade.css", "r", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True,
    )
"""

    text = text.replace(
        "st.set_page_config(",
        inject + "\n\nst.set_page_config("
    )

app.write_text(text, encoding="utf-8")

print("Patched app.py")
