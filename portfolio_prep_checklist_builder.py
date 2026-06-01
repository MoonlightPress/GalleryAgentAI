
import json
from pathlib import Path
from collections import Counter

SRC = "memory/actionable_target_shortlist.json"
REPORT = "reports/portfolio_prep_checklist.md"

DEFAULTS = [
    "10–12 images of finished watercolor work",
    "1-page portfolio PDF",
    "80–120 word artist statement",
    "short bio",
    "dimensions / medium / year for each work",
    "artist website or Instagram link",
    "contact email",
]

def main():
    if not Path(SRC).exists():
        raise SystemExit("Missing memory/actionable_target_shortlist.json.")

    targets = json.loads(Path(SRC).read_text(encoding="utf-8"))

    reqs = Counter()
    for t in targets:
        for r in t.get("requirements_detected", []):
            reqs[r] += 1

    lines = [
        "# Portfolio Prep Checklist",
        "",
        "Prepare this once, then reuse it for the top targets.",
        "",
        "## Core Materials",
        "",
    ]

    for item in DEFAULTS:
        lines.append(f"- {item}")

    lines += [
        "",
        "## Requirements Detected Across Crawled Pages",
        "",
    ]

    if not reqs:
        lines.append("_No specific requirements detected yet._")
    else:
        for req, count in reqs.most_common():
            lines.append(f"- {req}: seen on {count} page(s)")

    lines += [
        "",
        "## Practical First Portfolio PDF Structure",
        "",
        "1. Cover: artist name + project/series title",
        "2. 10–12 watercolor images",
        "3. For each work: title, year, medium, dimensions",
        "4. 80–120 word statement",
        "5. Short bio",
        "6. Contact / links",
    ]

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {REPORT}")

if __name__ == "__main__":
    main()
