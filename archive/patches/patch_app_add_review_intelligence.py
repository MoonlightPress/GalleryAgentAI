from pathlib import Path

APP = Path("app.py")
IMPORT_LINE = "from ui.opportunity_review_sections import render_opportunity_review_sections\n"

def main():
    text = APP.read_text(encoding="utf-8")

    if IMPORT_LINE not in text:
        # Put the import near other ui imports when possible.
        markers = [
            "from ui.category_context_streamlit_section import render_category_context_section\n",
            "from ui.zine_opportunity_section import render_zine_section\n",
            "from ui.strategy_homepage_components import render_strategy_homepage\n",
        ]
        for marker in markers:
            if marker in text:
                text = text.replace(marker, marker + IMPORT_LINE)
                break
        else:
            text = IMPORT_LINE + text

    if "render_opportunity_review_sections()" not in text:
        # Prefer to put it after category context if present.
        anchors = [
            '    render_category_context_section()\n    st.markdown("---")\n',
            '    render_publishing_section(render_compact_card)\n    st.markdown("---")\n',
            '    render_zine_section(render_compact_card)\n    st.markdown("---")\n',
        ]
        for anchor in anchors:
            if anchor in text:
                text = text.replace(
                    anchor,
                    anchor + '    render_opportunity_review_sections()\n    st.markdown("---")\n'
                )
                break
        else:
            old = "with tabs[0]:\n    render_strategy_homepage()\n"
            new = "with tabs[0]:\n    render_opportunity_review_sections()\n    st.markdown(\"---\")\n    render_strategy_homepage()\n"
            if old in text:
                text = text.replace(old, new)
            else:
                print("Could not find a safe insert point. Import was added, but render call was not inserted.")

    APP.write_text(text, encoding="utf-8")
    print("Patched app.py with Review Intelligence section.")

if __name__ == "__main__":
    main()
