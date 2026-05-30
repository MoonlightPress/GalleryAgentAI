
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
EVIDENCE_PATH = "memory/evidence_records.json"
OUT_PATH = "reports/claim_validation_report.md"

CLAIMS = {
    "accepts_submissions": ["submission", "submit", "apply", "application", "open call"],
    "publication_fit": ["photobook", "artist book", "zine", "publication", "printed matter"],
    "photography_fit": ["photography", "photo", "photographer"],
    "international_fit": ["international", "global", "worldwide", "online"],
}

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def title_of(opp):
    return opp.get("title") or opp.get("name") or "Unknown"

def evidence_text(ev):
    parts = []
    for data in ev.get("evidence", {}).values():
        for snip in data.get("snippets", []):
            parts.append(snip.lower())
    return " ".join(parts)

def validate_claims(ev):
    text = evidence_text(ev)
    results = {}

    for claim, terms in CLAIMS.items():
        hits = [t for t in terms if t in text]
        results[claim] = {
            "validated": bool(hits),
            "hits": hits
        }

    return results

def main():
    opps = load_json(OPP_PATH, [])
    evidence = load_json(EVIDENCE_PATH, {})

    lines = [
        "# Claim Validation Report",
        "",
        "This report checks whether common recommendation claims have textual support.",
        "",
    ]

    for opp in opps:
        title = title_of(opp)
        ev = evidence.get(title, {})
        claims = validate_claims(ev)
        opp["claim_validation"] = claims

        weak = [k for k, v in claims.items() if not v["validated"]]

        if weak:
            lines.append(f"## {title}")
            lines.append(f"- Missing support for: {', '.join(weak)}")
            lines.append("")

    with open(OPP_PATH, "w", encoding="utf-8") as f:
        json.dump(opps, f, indent=2, ensure_ascii=False)

    Path(OUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_PATH}")

if __name__ == "__main__":
    main()
