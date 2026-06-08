import json
import os
import sys
from pathlib import Path
from datetime import date
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils_filename import safe_slug

from opportunity_report_engine import (
    load_json,
    opportunity_report_markdown,
)

OPP_PATH = "deploy_data/compact_opportunities.json"
PROFILE_PATH = "memory/artist_master_profile.json"

CACHE_DIR = Path("memory/generated_analysis")


def save_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)





def main():
    opps = load_json(OPP_PATH, [])
    profile = load_json(PROFILE_PATH, {})

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped = 0

    for idx, opp in enumerate(opps):
        title = opp.get("title") or opp.get("name") or f"opp_{idx}"
        path  = CACHE_DIR / f"{idx:03d}_{safe_slug(title, max_len=80)}.md"

        # Skip entries whose cache is fresh enough (written today).
        # This avoids regenerating 200+ files on every pipeline run.
        if path.exists():
            try:
                first_line = path.read_text(encoding="utf-8").splitlines()[1] if path.stat().st_size > 0 else ""
                if date.today().isoformat() in first_line:
                    skipped += 1
                    continue
            except Exception:
                pass

        report = opportunity_report_markdown(opp, profile)
        enriched = f"\nREPORT GENERATED: {date.today().isoformat()}\n\n{report}\n"
        save_text(path, enriched)
        written += 1

    print(f"Cached {written} reports ({skipped} up-to-date, skipped).")


if __name__ == "__main__":
    main()
