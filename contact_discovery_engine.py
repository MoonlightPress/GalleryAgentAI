
import json, re
from pathlib import Path

SRC = "memory/personalized_fit_scores.json"
OUT = "memory/contact_targets.json"
REPORT = "reports/contact_discovery_report.md"

def load():
    return json.load(open(SRC, encoding="utf-8"))

def infer_contacts(item):
    url = (item.get("context_summary", {}) or {}).get("best_link") or item.get("url","")
    domain = url.replace("https://","").replace("http://","").split("/")[0].replace("www.","")
    guesses = [
        f"info@{domain}",
        f"contact@{domain}",
        f"gallery@{domain}",
    ]
    return guesses

def main():
    data = load()
    targets = [x for x in data if x.get("personalized_priority")=="high"]

    out = []
    lines = ["# Contact Discovery Report",""]

    for t in targets:
        entry = {
            "title": t.get("title"),
            "score": t.get("personalized_fit_score"),
            "best_link": (t.get("context_summary",{}) or {}).get("best_link"),
            "contact_guesses": infer_contacts(t),
            "needs_manual_verification": True
        }
        out.append(entry)

        lines.append(f"## {entry['title']}")
        lines.append(f"- Score: {entry['score']}")
        lines.append(f"- Link: {entry['best_link']}")
        lines.append("- Candidate Contacts:")
        for c in entry["contact_guesses"]:
            lines.append(f"  - {c}")
        lines.append("")

    Path("memory").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)

    json.dump(out, open(OUT,"w",encoding="utf-8"), indent=2, ensure_ascii=False)
    Path(REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT)
    print("Wrote", REPORT)

if __name__ == "__main__":
    main()
