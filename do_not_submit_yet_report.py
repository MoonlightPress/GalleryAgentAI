
import json
from pathlib import Path

SRC = "memory/submission_packets.json"
OUT = "reports/do_not_submit_yet.md"

def main():
    packets = json.load(open(SRC, encoding="utf-8"))
    lines = [
        "# Do Not Submit Yet",
        "",
        "These are not necessarily bad. They need more preparation or verification before asking the artist to spend energy.",
        "",
    ]

    for p in packets:
        reasons = []
        if p.get("contact") == "unknown":
            reasons.append("contact unknown")
        if p.get("deadline") == "unknown":
            reasons.append("deadline unknown")
        if not p.get("best_link"):
            reasons.append("no actionable link")
        if p.get("opportunity_type") in {"book_fair", "zine_fair", "publication"}:
            reasons.append("requires a book/zine/sequence object first")
        if p.get("opportunity_type") == "unknown":
            reasons.append("opportunity type unknown")

        if reasons:
            lines.append(f"## {p.get('title')}")
            lines.append(f"- Type: {p.get('opportunity_type')}")
            lines.append(f"- Reasons: {', '.join(reasons)}")
            lines.append(f"- Next: {p.get('next_action')}")
            lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT).write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
