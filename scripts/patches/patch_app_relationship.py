
from pathlib import Path

path = Path("app.py")

text = path.read_text(encoding="utf-8")

if (
    "from relationship_ui_components import *"
    not in text
):
    text = text.replace(
        "import streamlit as st",
        "import streamlit as st\nfrom relationship_ui_components import *",
    )

if (
    'relationship_memory = load_json('
    not in text
):
    text = text.replace(
        'strategy_feed = load_json(',
        'relationship_memory = load_json("memory/relationship_memory.json", {})\nstrategy_feed = load_json('
    )

target = "render_detail(selected)"

replacement = """
memory = relationship_memory.get(
    get_title(selected),
    {}
)

render_relationship_bar(memory)

render_detail(selected)
"""

text = text.replace(target, replacement)

path.write_text(text, encoding="utf-8")

print("Patched app.py")
