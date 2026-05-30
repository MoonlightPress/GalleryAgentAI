
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
DEADLINE_PATH = "memory/deadline_evidence.json"
FREQUENCY_PATH = "memory/publication_frequency.json"
OUT_REPORT = "reports/verified_detail_merge_report.md"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def title_of(opp):
    return opp.get("title") or opp.get("name") or "Unknown"


def match_key(opp):
    candidates = [
        opp.get("organization"),
        opp.get("title"),
        opp.get("name")
    ]
    return [str(x).lower() for x in candidates if x]


def find_match(opp, data):
    keys = match_key(opp)

    for name, item in data.items():
        lname = name.lower()
        if any(k in lname or lname in k for k in keys):
            return item

    return None


def main():
    opps = load_json(OPP_PATH, [])
    deadlines = load_json(DEADLINE_PATH, {})
    frequencies = load_json(FREQUENCY_PATH, {})

    lines = [
        "# Verified Detail Merge Report",
        "",
    ]

    changed = 0

    for opp in opps:
        d = find_match(opp, deadlines)
        f = find_match(opp, frequencies)

        if d:
            opp["deadline_evidence"] = d
            if not opp.get("deadline") and d.get("date_hits"):
                opp["deadline"] = d["date_hits"][0]
                opp["deadline_verified"] = True
                changed += 1

        if f:
            opp["publication_frequency"] = f.get("detected_frequency")
            opp["publication_frequency_confidence"] = f.get("confidence")
            opp["publication_signal_score"] = f.get("publication_signal_score")
            changed += 1

        if d or f:
            lines.append(f"## {title_of(opp)}")
            if d:
                lines.append(f"- Deadline evidence: {', '.join(d.get('date_hits', [])) or 'language only'}")
            if f:
                lines.append(f"- Publication frequency: {f.get('detected_frequency')} ({f.get('confidence')})")
            lines.append("")

    save_json(OPP_PATH, opps)

    Path(OUT_REPORT).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print(f"Merged verified details into {changed} fields.")
    print(f"Wrote {OUT_REPORT}")


if __name__ == "__main__":
    main()
