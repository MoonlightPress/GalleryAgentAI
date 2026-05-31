
import json
from pathlib import Path

SRC = "memory/research_completeness.json"
OUT = "reports/research_task_queue.md"

def main():
    rows = json.load(open(SRC, encoding="utf-8"))

    lines = [
        "# Research Task Queue",
        "",
        "Use this as the next manual or automated research list.",
        "",
    ]

    task_number = 1
    for r in rows:
        if r["status"] == "ready_for_review":
            continue

        lines.append(f"## {r['title']}")
        lines.append(f"- Current completeness: {r['score']}%")
        lines.append(f"- Link: {r['best_link']}")
        lines.append("")
        lines.append("### Tasks")

        for field in r["missing"]:
            label = {
                "contact": "Find official contact email or inquiry form.",
                "deadline": "Find current deadline or confirm none is listed.",
                "application_link": "Find application/submission/open-call page.",
                "application_page_crawled": "Crawl the application page and extract requirements.",
                "website": "Find official website.",
                "opportunity_type": "Classify opportunity type.",
                "fit_reasoning": "Generate DNA fit reasoning.",
            }.get(field, f"Fill missing field: {field}")
            lines.append(f"{task_number}. {label}")
            task_number += 1

        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT).write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
