
import json, os
from pathlib import Path

OPP_PATH="deploy_data/compact_opportunities.json"
OUT="reports/native_painting_action_report.md"

def load(path,fallback):
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    return fallback

def main():
    opps=load(OPP_PATH,[])
    painting=[o for o in opps if o.get("native_medium")=="painting" or o.get("painting_gate_status")=="promoted"]
    painting.sort(key=lambda x: float(x.get("painting_priority_score", x.get("source_purity_score",0)) or 0), reverse=True)

    lines=[
        "# Native Painting Action Report",
        "",
        "This is the corrected action report for Nin as a watercolor painter / works-on-paper artist.",
        "",
        "## Top Native Painting / Works on Paper Targets",
        ""
    ]

    for o in painting[:25]:
        title=o.get("title") or o.get("name") or "Unknown"
        score=o.get("painting_priority_score", o.get("source_purity_score"))
        why=o.get("why_this_fits_short") or o.get("one_sentence") or ""
        url=o.get("official_website") or o.get("source_url") or ""
        lines.append(f"- **{title}** — {score}. {why}")
        if url:
            lines.append(f"  - URL: {url}")
        if o.get("manual_review_needed"):
            lines.append("  - Next: verify current submission/contact details.")

    lines += ["", "## First Practical Plan", "", "1. Build one 10–12 work watercolor PDF.", "2. Verify the top 5 gallery/open-call sources.", "3. Send 3 short inquiries, not a full emotional portfolio pitch.", "4. Keep artist-book/zine targets separate from native painting targets."]

    Path("reports").mkdir(exist_ok=True)
    Path(OUT).write_text("\n".join(lines),encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__=="__main__":
    main()
