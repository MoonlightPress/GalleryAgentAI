
import json
from pathlib import Path
from urllib.parse import urlparse

SRC = "memory/typed_opportunities.json"
FALLBACK = "memory/application_page_results.json"
OUT = "memory/contextualized_opportunities.json"
REPORT = "reports/opportunity_context_report.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def domain(url):
    try:
        return urlparse(url or "").netloc.replace("www.", "")
    except Exception:
        return ""

def best_link(item):
    links = item.get("ranked_submission_links", []) or item.get("submission_links", [])
    if links:
        return links[0].get("url", "")
    return item.get("url", "")

def contact_status(item):
    if item.get("contact") and item.get("contact") != "unknown":
        return "contact_found"
    for page in item.get("application_page_results", []):
        if page.get("emails"):
            return "contact_found_on_application_page"
    return "contact_unknown"

def application_status(item):
    links = item.get("ranked_submission_links", []) or item.get("submission_links", [])
    pages = item.get("application_page_results", [])
    if pages:
        return "application_page_crawled"
    if links:
        return "application_link_found"
    return "no_application_link_found"

def deadline_status(item):
    if item.get("deadline") and item.get("deadline") != "unknown":
        return "deadline_candidate_found"
    for page in item.get("application_page_results", []):
        if page.get("date_candidates"):
            return "deadline_candidate_found"
    return "deadline_unknown"

def likely_false_positive(item):
    title = str(item.get("title") or "").lower()
    url = best_link(item).lower()
    if "browse printed matter editions" in title:
        return True, "catalog page, not opportunity"
    if "flashpoint" in title or "protest photography" in title:
        return True, "specific exhibition page, not opportunity"
    if "/catalog/" in url:
        return True, "catalog/product page"
    return False, ""

def build_context(item):
    false_pos, false_reason = likely_false_positive(item)
    typ = item.get("opportunity_type") or "unknown"

    status_bits = [
        contact_status(item),
        application_status(item),
        deadline_status(item),
    ]

    if false_pos:
        actionability = "reject_or_archive"
    elif "application_page_crawled" in status_bits:
        actionability = "actionable_research_target"
    elif "application_link_found" in status_bits or "contact_found" in status_bits:
        actionability = "partial_action_target"
    else:
        actionability = "needs_manual_verification"

    missing = []
    if contact_status(item) == "contact_unknown":
        missing.append("contact")
    if application_status(item) == "no_application_link_found":
        missing.append("application/submission link")
    if deadline_status(item) == "deadline_unknown":
        missing.append("deadline")

    item["context_summary"] = {
        "domain": domain(best_link(item) or item.get("url", "")),
        "best_link": best_link(item),
        "contact_status": contact_status(item),
        "application_status": application_status(item),
        "deadline_status": deadline_status(item),
        "actionability": actionability,
        "missing": missing,
        "likely_false_positive": false_pos,
        "false_positive_reason": false_reason,
    }

    return item

def main():
    data = load(SRC, None)
    if data is None:
        data = load(FALLBACK, [])

    enriched = [build_context(dict(item)) for item in data]

    Path("memory").mkdir(exist_ok=True)
    json.dump(enriched, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = ["# Opportunity Context Report", "", "Adds missing-info and actionability context to each opportunity.", ""]
    for item in enriched[:30]:
        ctx = item["context_summary"]
        lines.append(f"## {item.get('title')}")
        lines.append(f"- Type: {item.get('opportunity_type', 'unknown')}")
        lines.append(f"- Actionability: {ctx['actionability']}")
        lines.append(f"- Best link: {ctx['best_link']}")
        lines.append(f"- Contact: {ctx['contact_status']}")
        lines.append(f"- Application: {ctx['application_status']}")
        lines.append(f"- Deadline: {ctx['deadline_status']}")
        if ctx["missing"]:
            lines.append(f"- Missing: {', '.join(ctx['missing'])}")
        if ctx["likely_false_positive"]:
            lines.append(f"- False positive warning: {ctx['false_positive_reason']}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT)
    print("Wrote", REPORT)

if __name__ == "__main__":
    main()
