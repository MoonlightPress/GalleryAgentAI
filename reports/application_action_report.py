
import json
from pathlib import Path

SRC = "memory/typed_opportunities.json"
FALLBACK = "memory/application_page_results.json"
OUT = "reports/application_action_report.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def best_deadline(item):
    for page in item.get("application_page_results", []):
        if page.get("date_candidates"):
            return page["date_candidates"][0]
    return item.get("deadline") or "unknown"

def best_contact(item):
    if item.get("contact") and item.get("contact") != "unknown":
        return item["contact"]
    for page in item.get("application_page_results", []):
        if page.get("emails"):
            return page["emails"][0]
    return "unknown"

def main():
    data = load(SRC, None)
    if data is None:
        data = load(FALLBACK, [])

    lines = [
        "# Application Action Report",
        "",
        "This report follows likely application/open-call links and extracts useful next-action data.",
        "",
    ]

    for item in data[:20]:
        links = item.get("ranked_submission_links", [])
        pages = item.get("application_page_results", [])

        lines.append(f"## {item.get('title')}")
        if item.get("opportunity_type"):
            lines.append(f"- Type: {item.get('opportunity_type')}")
        if item.get("next_action_hint"):
            lines.append(f"- Next action: {item.get('next_action_hint')}")
        lines.append(f"- Contact: {best_contact(item)}")
        lines.append(f"- Best deadline/date candidate: {best_deadline(item)}")
        lines.append(f"- Ranked submission links: {len(links)}")
        lines.append(f"- Crawled application pages: {len(pages)}")

        if links:
            lines.append("")
            lines.append("### Best Application Links")
            for link in links[:5]:
                lines.append(f"- {link.get('label') or '[no label]'} — {link.get('url')} — score {link.get('application_link_score')}")

        if pages:
            lines.append("")
            lines.append("### Page Findings")
            for page in pages[:3]:
                lines.append(f"- {page.get('final_url')}")
                lines.append(f"  - HTTP: {page.get('http_status')}")
                lines.append(f"  - Emails: {', '.join(page.get('emails', [])[:3]) or 'none'}")
                lines.append(f"  - Dates: {', '.join(page.get('date_candidates', [])[:5]) or 'none'}")
                lines.append(f"  - Requirement hits: {', '.join(page.get('requirement_hits', [])[:8]) or 'none'}")

        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT).write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
