
import json
import os
from pathlib import Path

EVIDENCE_PATH = "memory/evidence_records.json"
OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_DIR = "reports/source_dossiers"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def safe_filename(text):
    return (
        str(text)
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "")
        .replace("?", "")
        [:90]
    )

def title_of(opp):
    return opp.get("title") or opp.get("name") or "Unknown"

def dossier(title, opp, ev):
    lines = [
        f"# Source Dossier — {title}",
        "",
        f"Score: {opp.get('overall_score')}/10",
        f"Evidence quality: {ev.get('evidence_quality', 'none')}",
        f"Evidence count: {ev.get('evidence_count', 0)}",
        f"Source: {ev.get('source_url') or opp.get('source_url') or opp.get('official_website') or ''}",
        "",
        "## Summary",
        "",
        opp.get("one_sentence", ""),
        "",
        "## Fit Claim",
        "",
        opp.get("why_this_fits_short", ""),
        "",
        "## Evidence",
        "",
    ]

    evidence = ev.get("evidence", {})

    if not evidence:
        lines.append("No extracted evidence yet. This opportunity should remain unverified or capped.")
    else:
        for kind, data in evidence.items():
            lines.append(f"### {kind.title()}")
            lines.append("")
            lines.append(f"Source: {data.get('source_name')} — {data.get('source_url')}")
            lines.append("")
            for snippet in data.get("snippets", []):
                lines.append(f"> {snippet}")
                lines.append("")

    return "\n".join(lines)

def main():
    evidence = load_json(EVIDENCE_PATH, {})
    opps = load_json(OPP_PATH, [])
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

    count = 0

    for opp in opps:
        title = title_of(opp)
        ev = evidence.get(title, {})
        path = Path(OUT_DIR) / f"{safe_filename(title)}.md"
        path.write_text(dossier(title, opp, ev), encoding="utf-8")
        count += 1

    print(f"Wrote {count} source dossiers to {OUT_DIR}")

if __name__ == "__main__":
    main()
