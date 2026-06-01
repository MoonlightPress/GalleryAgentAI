
from pathlib import Path

APP = Path("app.py")

IMPORT_LINE = "from ui.zine_opportunity_section import render_zine_section\n"

OLD_BLOCK = """with tabs[0]:
    render_strategy_homepage()
"""

NEW_BLOCK = """with tabs[0]:
    render_zine_section()
    st.markdown("---")
    render_strategy_homepage()
"""

def main():
    text = APP.read_text(encoding="utf-8")

    if IMPORT_LINE not in text:
        marker = "from ui.strategy_homepage_components import render_strategy_homepage\n"
        if marker in text:
            text = text.replace(marker, marker + IMPORT_LINE)
        else:
            text = IMPORT_LINE + text

    if NEW_BLOCK in text:
        APP.write_text(text, encoding="utf-8")
        print("app.py already patched.")
    elif OLD_BLOCK in text:
        text = text.replace(OLD_BLOCK, NEW_BLOCK)
        APP.write_text(text, encoding="utf-8")
        print("Patched app.py: zine section now renders above strategy homepage.")
    else:
        APP.write_text(text, encoding="utf-8")
        print("Import added, but could not find the expected tabs[0] block.")
        print("Manually replace:")
        print(OLD_BLOCK)
        print("with:")
        print(NEW_BLOCK)

if __name__ == "__main__":
    main()
