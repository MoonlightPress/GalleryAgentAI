
import json
from pathlib import Path

SRC = "memory/official_page_extractions.json"
OUT = "memory/promoted_opportunity_links.json"
REPORT = "reports/promoted_links_report.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def norm(s):
    return str(s or "").lower()

def promote_link(link):
    label = norm(link.get("label"))
    url = norm(link.get("url"))
    blob = label + " " + url
    categories = []

    if any(x in blob for x in ["application-form", "application_form", "form", "google.com/forms", "apply", "申込", "申し込み", "応募フォーム"]):
        categories.append("application_form")
    if any(x in blob for x in ["application", "応募", "応募要項", "guideline", "requirements", "competition", "entry", "submit", "submission"]):
        categories.append("submission_guidelines")
    if any(x in blob for x in ["contact", "contact-us", "inquiry", "お問い合わせ", "問合せ"]):
        categories.append("contact_page")
    if any(x in blob for x in ["open-call", "open_calls", "open-calls", "open call", "公募", "募集"]):
        categories.append("open_call")
    if "instagram.com" in blob:
        categories.append("instagram")
    if not categories:
        categories.append("other")

    weights = {
        "application_form": 10,
        "submission_guidelines": 8,
        "open_call": 8,
        "contact_page": 6,
        "instagram": 2,
        "other": 0,
    }
    score = sum(weights.get(c, 0) for c in categories)

    return {
        "label": link.get("label") or "[no label]",
        "url": link.get("url"),
        "categories": categories,
        "score": score,
    }

def main():
    data = load(SRC, [])
    promoted = []
    lines = ["# Promoted Links Report", "", "Classifies extracted links by practical use.", ""]

    for item in data:
        title = item.get("title")
        all_links = []
        all_links.extend(item.get("relevant_links", []) or [])
        for page in item.get("pages", []) or []:
            all_links.extend(page.get("relevant_links", []) or [])

        seen = set()
        promoted_links = []
        for link in all_links:
            url = link.get("url")
            if not url or url in seen:
                continue
            seen.add(url)
            promoted_links.append(promote_link(link))

        promoted_links.sort(key=lambda x: x["score"], reverse=True)

        buckets = {
            "application_forms": [x for x in promoted_links if "application_form" in x["categories"]],
            "submission_guidelines": [x for x in promoted_links if "submission_guidelines" in x["categories"]],
            "contact_pages": [x for x in promoted_links if "contact_page" in x["categories"]],
            "open_calls": [x for x in promoted_links if "open_call" in x["categories"]],
            "instagram": [x for x in promoted_links if "instagram" in x["categories"]],
            "other": [x for x in promoted_links if x["categories"] == ["other"]],
        }

        promoted.append({"title": title, "promoted_links": promoted_links, **buckets})

        lines.append(f"## {title}")
        for bucket_name in ["application_forms", "submission_guidelines", "open_calls", "contact_pages", "instagram"]:
            links = buckets[bucket_name]
            lines.append(f"- {bucket_name}: {len(links)}")
            for link in links[:4]:
                lines.append(f"  - {link['label']} — {link['url']} — score {link['score']}")
        lines.append("")

    Path("memory").mkdir(exist_ok=True)
    json.dump(promoted, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    Path("reports").mkdir(exist_ok=True)
    Path(REPORT).write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT)
    print("Wrote", REPORT)

if __name__ == "__main__":
    main()
