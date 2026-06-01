
from pathlib import Path

APP = Path("app.py")
IMPORT_LINE = "from ui.category_context_streamlit_section import render_category_context_section\n"

def main():
    text = APP.read_text(encoding="utf-8")

    if IMPORT_LINE not in text:
        marker = "from ui.zine_opportunity_section import render_zine_section\n"
        if marker in text:
            text = text.replace(marker, marker + IMPORT_LINE)
        else:
            marker = "from ui.strategy_homepage_components import render_strategy_homepage\n"
            text = text.replace(marker, marker + IMPORT_LINE)

    # Put context after zines if present, otherwise before strategy homepage.
    if "render_category_context_section()" not in text:
        anchor = "    render_zine_section(render_compact_card)\n    st.markdown(\"---\")\n"
        replacement = "    render_zine_section(render_compact_card)\n    st.markdown(\"---\")\n    render_category_context_section()\n    st.markdown(\"---\")\n"
        if anchor in text:
            text = text.replace(anchor, replacement)
        else:
            anchor2 = "with tabs[0]:\n    render_strategy_homepage()\n"
            replacement2 = "with tabs[0]:\n    render_category_context_section()\n    st.markdown(\"---\")\n    render_strategy_homepage()\n"
            text = text.replace(anchor2, replacement2)

    APP.write_text(text, encoding="utf-8")
    print("Patched app.py with category context section.")

if __name__ == "__main__":
    main()
