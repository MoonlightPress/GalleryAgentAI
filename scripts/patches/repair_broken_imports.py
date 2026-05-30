
from pathlib import Path

TARGETS = [
    "analysis_cache_builder.py",
    "opportunity_report_engine.py",
    "inquiry_draft_generator.py",
    "portfolio_pitch_generator.py",
    "smart_cover_letter_engine.py",
]

def repair_analysis_cache(path):
    p = Path(path)
    if not p.exists():
        return

    text = p.read_text(encoding="utf-8")

    bad = """from opportunity_report_engine import (
from utils_filename import safe_slug
    load_json,
    opportunity_report_markdown,
)
"""

    good = """from utils_filename import safe_slug

from opportunity_report_engine import (
    load_json,
    opportunity_report_markdown,
)
"""

    text = text.replace(bad, good)

    # remove old slug helper if present
    start = text.find("def slug(text):")
    if start != -1:
        end = text.find("\ndef main():", start)
        if end != -1:
            text = text[:start] + "\n\n" + text[end:]

    p.write_text(text, encoding="utf-8")
    print("Fixed analysis_cache_builder.py")

def main():
    repair_analysis_cache("analysis_cache_builder.py")
    print("Import repair complete.")

if __name__ == "__main__":
    main()
