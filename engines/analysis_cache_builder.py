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

    for idx, opp in enumerate(opps):
        title = opp.get("title") or opp.get("name") or f"opp_{idx}"

        report = opportunity_report_markdown(
            opp,
            profile
        )

        enriched = f"""
REPORT GENERATED: {date.today().isoformat()}

{report}
"""

        path = CACHE_DIR / f"{idx:03d}_{safe_slug(title, max_len=80)}.md"

        save_text(path, enriched)

    print(f"Cached {len(opps)} reports.")


if __name__ == "__main__":
    main()
