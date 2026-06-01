
from pathlib import Path

APP = Path("app.py")
IMPORT_LINE = "from ui.publishing_opportunity_section import render_publishing_section\n"

def main():
    text = APP.read_text(encoding="utf-8")

    if IMPORT_LINE not in text:
        marker = "from ui.zine_opportunity_section import render_zine_section\n"
        if marker in text:
            text = text.replace(marker, marker + IMPORT_LINE)
        else:
            marker = "from ui.strategy_homepage_components import render_strategy_homepage\n"
            text = text.replace(marker, marker + IMPORT_LINE)

    # Put publishing directly after zines if zines are rendered.
    zine_block = """    render_zine_section(render_compact_card)
    st.markdown("---")
"""
    publishing_block = """    render_zine_section(render_compact_card)
    st.markdown("---")
    render_publishing_section(render_compact_card)
    st.markdown("---")
"""
    if "render_publishing_section(render_compact_card)" not in text and zine_block in text:
        text = text.replace(zine_block, publishing_block)

    APP.write_text(text, encoding="utf-8")
    print("Patched app.py: publishing section added after zines.")

if __name__ == "__main__":
    main()
