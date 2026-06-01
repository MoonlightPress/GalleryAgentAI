
import json
from pathlib import Path

SRC = "memory/actionable_target_shortlist.json"
REPORT = "reports/do_not_waste_time.md"

BAD_SIGNALS = [
    "archive",
    "past",
    "2019",
    "2020",
    "2021",
    "2022",
    "2023",
    "catalog",
    "product",
]

def badness(p):
    url = (p.get("submission_page_url") or "").lower()
    title = (p.get("source_title") or "").lower()
    text = f"{url} {title}"

    score = 0
    hits = []
    for b in BAD_SIGNALS:
        if b in text:
            score += 1
            hits.append(b)

    if p.get("actionability_score", 0) <= 1:
        score += 2
        hits.append("low actionability")

    return score, hits

def main():
    if not Path(SRC).exists():
        raise SystemExit("Missing memory/actionable_target_shortlist.json.")

    targets = json.loads(Path(SRC).read_text(encoding="utf-8"))

    flagged = []
    for p in targets:
        score, hits = badness(p)
        if score:
            flagged.append((score, hits, p))

    flagged.sort(key=lambda x: x[0], reverse=True)

    lines = [
        "# Do Not Waste Time",
        "",
        "These targets should be deprioritized until better evidence appears.",
        "",
    ]

    for score, hits, p in flagged:
        lines.append(f"## {p.get('source_title')}")
        lines.append(f"- Reason: {', '.join(hits)}")
        lines.append(f"- Page: {p.get('submission_page_url')}")
        lines.append(f"- Actionability score: {p.get('actionability_score')}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {REPORT}")

if __name__ == "__main__":
    main()
