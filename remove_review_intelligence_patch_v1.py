from pathlib import Path
import re

APP = Path("app.py")

IMPORT_LINE = "from ui.opportunity_review_sections import render_opportunity_review_sections\n"

def main():
    text = APP.read_text(encoding="utf-8")

    # Remove import.
    text = text.replace(IMPORT_LINE, "")

    # Remove render call plus following separator if present.
    text = text.replace('    render_opportunity_review_sections()\n    st.markdown("---")\n', "")
    text = text.replace('    render_opportunity_review_sections()\n', "")

    APP.write_text(text, encoding="utf-8")
    print("Removed Review Intelligence section from app.py.")
    print("The report files remain available in /reports, but they will no longer flood the website.")

if __name__ == "__main__":
    main()
