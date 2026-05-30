
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "reports/global_research_queue.md"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def missing_fields(opp):
    fields = []
    if not opp.get("submission_page"):
        fields.append("submission process")
    if not opp.get("deadline"):
        fields.append("deadline")
    if not opp.get("fees"):
        fields.append("fees")
    if not (opp.get("contact") or opp.get("email") or opp.get("contact_url")):
        fields.append("contact")
    return fields


def main():
    opps = load_json(OPP_PATH, [])
    global_opps = [
        o for o in opps
        if o.get("source_type") == "global_seed"
        or str(o.get("country", "")).lower() not in {"", "japan"}
        or "global" in [str(t).lower() for t in o.get("tags", [])]
    ]

    lines = [
        "# Global Research Queue",
        "",
        "These are global or international opportunities that need verification before being presented as fully actionable.",
        ""
    ]

    for opp in sorted(global_opps, key=lambda x: float(x.get("overall_score", 0) or 0), reverse=True):
        lines.append(f"## {opp.get('title')}")
        lines.append(f"- Score: {opp.get('overall_score')}/10")
        lines.append(f"- Country: {opp.get('country', '')}")
        lines.append(f"- Category: {opp.get('category', '')}")
        lines.append(f"- Source: {opp.get('source_url') or opp.get('source_link') or opp.get('official_website') or ''}")
        lines.append(f"- Missing: {', '.join(missing_fields(opp)) or 'none'}")
        lines.append(f"- Next: {opp.get('quick_action', 'Research submission process and current eligibility.')}")
        lines.append("")

    Path(OUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_PATH}")
    print(f"Global opportunities: {len(global_opps)}")


if __name__ == "__main__":
    main()
