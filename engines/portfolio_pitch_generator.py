
import json
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils_filename import safe_filename

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_DIR = "reports/portfolio_pitches"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback




def pitch_for(opp):
    title = opp.get("title") or opp.get("name") or "Unknown"
    body = opp.get("recommended_body_of_work", "General Portfolio")
    why = opp.get("why_this_fits_short") or opp.get("one_sentence") or ""
    matches = opp.get("portfolio_matches", [])

    if matches:
        body_desc = matches[0].get("description", "")
        hits = ", ".join(matches[0].get("hits", [])[:8])
    else:
        body_desc = "A concise selection of her strongest current work."
        hits = ""

    return f"""# Portfolio Pitch — {title}

## Recommended Body of Work
{body}

## Why This Body Fits
{body_desc}

## Opportunity Fit
{why}

## Match Signals
{hits or "No strong keyword match stored yet."}

## Suggested Submission Framing
Present this not as a general portfolio, but as a focused body of work.

The pitch should emphasize:
- quiet atmosphere
- memory and place
- visual consistency
- publication or sequence potential
- emotional restraint
- sensitivity to everyday spaces

## Recommended Materials
- 8–12 image sequence
- short artist statement
- short project statement
- website / Instagram / PDF portfolio
- 1 paragraph explaining why this venue or publication fits the work

## Caution
Do not send too much. The first contact should feel precise, not desperate or overfull.
"""


def main():
    opps = load_json(OPP_PATH, [])
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

    count = 0

    for opp in opps[:80]:
        title = opp.get("title") or opp.get("name") or "Unknown"
        path = Path(OUT_DIR) / f"{safe_filename(title, max_len=80)}.md"
        path.write_text(pitch_for(opp), encoding="utf-8")
        count += 1

    print(f"Generated {count} portfolio pitch reports.")


if __name__ == "__main__":
    main()
