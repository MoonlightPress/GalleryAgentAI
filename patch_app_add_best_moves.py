from pathlib import Path

APP = Path("app.py")
IMPORT_LINE = "from ui.best_moves_streamlit_section import render_best_moves_section\n"

def main():
    text = APP.read_text(encoding="utf-8")

    if IMPORT_LINE not in text:
        markers = [
            "from ui.zine_opportunity_section import render_zine_section\n",
            "from ui.strategy_homepage_components import render_strategy_homepage\n",
        ]
        for marker in markers:
            if marker in text:
                text = text.replace(marker, marker + IMPORT_LINE)
                break
        else:
            text = IMPORT_LINE + text

    if "render_best_moves_section()" not in text:
        # Put it at top of first tab if possible.
        old = "with tabs[0]:\n"
        if old in text:
            text = text.replace(old, "with tabs[0]:\n    render_best_moves_section()\n    st.markdown(\"---\")\n", 1)
        else:
            print("Could not find tabs[0]. Import was added but render call was not inserted.")

    APP.write_text(text, encoding="utf-8")
    print("Patched app.py with Best Next Moves section.")

if __name__ == "__main__":
    main()
