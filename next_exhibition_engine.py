
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
PROJECT_PATH = "memory/next_projects.json"
OUT_PATH = "reports/next_exhibitions.md"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def blob(opp):
    parts = []
    for key in ["title", "name", "organization", "category", "why_this_fits_short", "one_sentence", "exclusive_primary_bucket"]:
        if opp.get(key):
            parts.append(str(opp[key]))

    for key in ["visual_fit_hits", "fit_keyword_hits"]:
        for x in opp.get(key, []) or []:
            parts.append(str(x))

    return " ".join(parts).lower()


def score_for_exhibition(opp):
    text = blob(opp)
    score = float(opp.get("differentiated_score", opp.get("overall_score", 0)) or 0)

    if opp.get("recommendation_visibility") == "hidden":
        return -999

    if any(x in text for x in ["facebook", "instagram", "pinterest", "tiktok", "continue reading"]):
        return -999

    # Exhibition-adjacent but not too commercial.
    boosts = ["photobook", "artist book", "zine", "bookstore", "gallery", "artist-run", "cafe", "community"]
    penalties = ["design festa", "farmers market", "craft fair", "commercial expo"]

    for b in boosts:
        if b in text:
            score += 0.8

    for p in penalties:
        if p in text:
            score -= 2.5

    return score


def main():
    opps = load_json(OPP_PATH, [])
    projects = load_json(PROJECT_PATH, [])

    ranked = sorted(opps, key=score_for_exhibition, reverse=True)

    lines = [
        "# Next Exhibition / Visibility Targets",
        "",
        "This is not a generic top list. It asks where the next project could plausibly be shown, tested, or used for relationship-building.",
        "",
        "## Best Immediate Visibility Targets",
        "",
    ]

    count = 0
    for opp in ranked:
        if score_for_exhibition(opp) <= 0:
            continue

        title = opp.get("title") or opp.get("name") or "Unknown"
        why = opp.get("why_this_fits_short") or opp.get("one_sentence") or ""

        lines.append(f"- **{title}** — {opp.get('overall_score')} / {opp.get('differentiated_score')}. {why}")
        count += 1

        if count >= 12:
            break

    lines += [
        "",
        "## How To Use These",
        "",
        "1. Do not send a generic portfolio.",
        "2. Pick one project concept first.",
        "3. Send a short project-specific inquiry.",
        "4. Ask for the correct submission/contact path before sending a full PDF.",
    ]

    Path(OUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
