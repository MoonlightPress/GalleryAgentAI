
from pathlib import Path

APP = Path("app.py")
IMPORT_LINE = "from ui.zine_opportunity_section import render_zine_section\n"

def main():
    text = APP.read_text(encoding="utf-8")

    if IMPORT_LINE not in text:
        marker = "from ui.strategy_homepage_components import render_strategy_homepage\n"
        if marker in text:
            text = text.replace(marker, marker + IMPORT_LINE)
        else:
            text = IMPORT_LINE + text

    # Replace v1 call if present.
    text = text.replace("    render_zine_section()\n", "    render_zine_section(render_compact_card)\n")

    # If zine section is not yet inserted, insert it above strategy homepage.
    old = """with tabs[0]:
    render_strategy_homepage()
"""
    new = """with tabs[0]:
    render_zine_section(render_compact_card)
    st.markdown("---")
    render_strategy_homepage()
"""
    if "render_zine_section(render_compact_card)" not in text and old in text:
        text = text.replace(old, new)

    APP.write_text(text, encoding="utf-8")
    print("Patched app.py for zine section v2.")

if __name__ == "__main__":
    main()
