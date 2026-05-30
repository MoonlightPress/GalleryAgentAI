
import json
from pathlib import Path

SRC = "memory/application_page_results.json"
OUT = "memory/typed_opportunities.json"
REPORT = "reports/opportunity_buckets.md"

TYPE_RULES = {
    "book_fair": ["art book fair", "book fair", "printed matter", "offprint", "tokyo art book fair"],
    "zine_fair": ["zine", "mount zine"],
    "gallery_submission": ["gallery", "opa", "hb gallery", "pinpoint", "utrecht", "book and sons", "post"],
    "open_exhibition": ["open exhibition", "open calls", "open call", "mall galleries", "royal institute", "pastel society", "society of women artists"],
    "competition": ["prize", "competition", "award", "jackson"],
    "residency": ["residency", "air", "tokas", "youkobo", "bankart"],
    "publication": ["publication", "magazine", "journal", "self publish", "printed matter"],
    "contact_only": ["contact", "info@", "mail@"],
}

PRIORITY = [
    "gallery_submission",
    "open_exhibition",
    "competition",
    "book_fair",
    "zine_fair",
    "publication",
    "residency",
    "contact_only",
    "unknown",
]

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def blob(item):
    parts = []
    for k in ["title", "url", "contact", "submission_open", "deadline"]:
        if item.get(k):
            parts.append(str(item[k]))

    for k in ["ranked_submission_links", "application_page_results", "submission_links", "relevant_links"]:
        for x in item.get(k, []) or []:
            if isinstance(x, dict):
                parts.append(str(x.get("label", "")))
                parts.append(str(x.get("url", "")))
                parts.append(str(x.get("final_url", "")))

    return " ".join(parts).lower()

def classify(item):
    text = blob(item)
    hits_by_type = {}

    for typ, terms in TYPE_RULES.items():
        hits = [t for t in terms if t in text]
        if hits:
            hits_by_type[typ] = hits

    if not hits_by_type:
        return "unknown", {}

    for typ in PRIORITY:
        if typ in hits_by_type:
            return typ, hits_by_type

    return "unknown", hits_by_type

def action_hint(typ):
    return {
        "gallery_submission": "Prepare a short gallery inquiry and 8-12 image PDF.",
        "open_exhibition": "Verify current call, deadline, fee, size rules, and submit only if current.",
        "competition": "Check deadline, fee, eligibility, and whether prize/reputation is worth it.",
        "book_fair": "Check exhibitor application requirements; useful only if she has a zine/book object.",
        "zine_fair": "Make a small watercolor zine first; do not treat as gallery representation.",
        "publication": "Use only if the work is converted into a sequence, book, or printed edition.",
        "residency": "Lower priority unless it supports a specific project and has a clear deadline.",
        "contact_only": "Use for soft inquiry only; do not assume there is an open submission.",
        "unknown": "Manual review required.",
    }.get(typ, "Manual review required.")

def main():
    data = load(SRC, [])

    if not data:
        raise SystemExit("memory/application_page_results.json is empty or missing. Run run_fixed_application_pipeline.py.")

    buckets = {k: [] for k in PRIORITY}

    typed = []
    for original in data:
        # Preserve every field. Add only classification fields.
        item = dict(original)

        typ, hits = classify(item)
        item["opportunity_type"] = typ
        item["opportunity_type_hits"] = hits
        item["next_action_hint"] = action_hint(typ)

        typed.append(item)
        buckets.setdefault(typ, []).append(item)

    Path("memory").mkdir(exist_ok=True)
    json.dump(typed, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = ["# Opportunity Buckets", "", "Opportunities grouped by practical action type.", ""]

    for typ in PRIORITY:
        items = buckets.get(typ, [])
        title = typ.replace("_", " ").title()
        lines.append(f"## {title}")
        lines.append("")
        if not items:
            lines.append("_No items._")
            lines.append("")
            continue

        for item in items[:20]:
            lines.append(f"- **{item.get('title')}**")
            lines.append(f"  - Contact: {item.get('contact', 'unknown')}")
            lines.append(f"  - Submission: {item.get('submission_open', 'unknown')}")
            lines.append(f"  - Deadline: {item.get('deadline', 'unknown')}")
            lines.append(f"  - Action: {item.get('next_action_hint')}")

            links = item.get("ranked_submission_links", []) or item.get("submission_links", [])
            if links:
                best = links[0]
                lines.append(f"  - Best link: {best.get('label') or '[no label]'} — {best.get('url')}")

        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT)
    print("Wrote", REPORT)

if __name__ == "__main__":
    main()
