
import json
import re
from pathlib import Path

from deadline_priority_extractor import best_deadline

PROMOTED = "memory/actionable_targets_with_links.json"
EXTRACTIONS = "memory/official_page_extractions.json"
OUT_JSON = "memory/submission_checklists.json"
OUT_REPORT = "reports/submission_checklists.md"

FEE_PATTERNS = [
    r"(?:entry fee|application fee|submission fee|fee|応募料|参加費|出展料|料金)[^\n。.:：]{0,100}[.:：]?\s*([$£€¥]\s?[0-9,]+|[0-9,]+\s?(?:yen|円|jpy|usd|gbp|eur|pounds?))",
    r"([$£€¥]\s?[0-9,]+|[0-9,]+\s?(?:yen|円|jpy|usd|gbp|eur|pounds?))[^\n。]{0,100}(?:entry fee|application fee|submission fee|応募料|参加費|出展料|fee)",
]

REQUIREMENT_MAP = [
    ("portfolio", ["portfolio", "ポートフォリオ"], "Portfolio or portfolio link"),
    ("artist_statement", ["artist statement", "statement", "ステートメント"], "Artist statement"),
    ("bio", ["bio", "biography", "profile", "プロフィール", "略歴"], "Short artist bio / profile"),
    ("cv", ["cv", "resume", "résumé", "履歴"], "CV / artist resume"),
    ("images", ["images", "jpg", "jpeg", "png", "作品画像", "画像"], "Images of work"),
    ("work_details", ["title", "medium", "dimensions", "size", "year", "作品名", "サイズ", "技法", "制作年"], "Work details: title, medium, size, year"),
    ("pdf", ["pdf", "PDF"], "PDF document"),
    ("book_zine", ["zine", "book", "publication", "artist book", "ZINE", "冊子"], "Zine/book/publication details"),
    ("price_edition", ["price", "edition", "copies", "価格", "部数", "エディション"], "Edition size and price"),
]

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def by_title(rows):
    return {r.get("title"): r for r in rows if r.get("title")}

def collect_text(extraction):
    if not extraction:
        return ""
    parts = []
    for page in extraction.get("pages", []):
        parts.append(page.get("text_preview", ""))
        parts.extend(page.get("deadline_clues", []) or [])
        parts.extend(page.get("eligibility_clues", []) or [])
        parts.extend(page.get("requirements", []) or [])
    parts.extend(extraction.get("deadline_clues", []) or [])
    parts.extend(extraction.get("eligibility_clues", []) or [])
    return "\n".join([str(p) for p in parts if p])

def extract_fee(text):
    for pat in FEE_PATTERNS:
        m = re.search(pat, text or "", flags=re.I)
        if m:
            g = m.group(1)
            if g:
                return g
    return "unknown"

def requirement_checklist(text, target):
    low = (text or "").lower()
    checklist = []
    found_keys = set()

    for key, terms, label in REQUIREMENT_MAP:
        if any(t.lower() in low for t in terms):
            checklist.append({"item": label, "source": "page_text", "confirmed": True})
            found_keys.add(key)

    typ = target.get("opportunity_type", "")
    # Add sensible defaults, but mark as unconfirmed.
    defaults = []
    if typ == "book_fair":
        defaults = [
            "Zine/book/publication details",
            "Sample images or spreads",
            "Edition size and price",
            "Artist bio / profile",
        ]
    elif typ == "zine_fair":
        defaults = [
            "Zine images or sample pages",
            "Edition size and price",
            "Short artist bio / profile",
        ]
    elif typ == "gallery_submission":
        defaults = [
            "8-12 images of work",
            "Artist statement",
            "Short artist bio / profile",
            "Work details: title, medium, size, year",
        ]
    elif typ == "competition":
        defaults = [
            "Images of work",
            "Work details: title, medium, size, year",
            "Artist bio / profile",
            "Entry fee confirmation",
        ]
    elif typ == "open_exhibition":
        defaults = [
            "Images of work",
            "Work details: title, medium, size, year",
            "Eligibility check",
            "Entry fee confirmation",
        ]

    existing_labels = {x["item"] for x in checklist}
    for d in defaults:
        if d not in existing_labels:
            checklist.append({"item": d, "source": "type_default", "confirmed": False})

    return checklist or [{"item": "Manual requirement review needed", "source": "fallback", "confirmed": False}]

def submission_method(target):
    if target.get("application_form_url") and target["application_form_url"] != "unknown":
        if "google.com/forms" in target["application_form_url"]:
            return "Google Form"
        return "Application form"
    if target.get("submission_guidelines_url") and target["submission_guidelines_url"] != "unknown":
        return "Read guidelines first"
    if target.get("open_call_url") and target["open_call_url"] != "unknown":
        return "Open call page"
    if target.get("contact_page_url") and target["contact_page_url"] != "unknown":
        return "Contact page / inquiry"
    return "Manual research needed"

def build_checklist(target, extraction):
    text = collect_text(extraction)
    deadline, deadline_sentence, deadline_candidates = best_deadline(text)
    fee = extract_fee(text)

    # Keep previously known values if extractor has nothing better.
    if deadline == "unknown" and target.get("deadline") and target.get("deadline") != "unknown":
        deadline = target.get("deadline")
        deadline_sentence = "Existing target deadline field; verify manually."

    if fee == "unknown" and target.get("fee") and target.get("fee") != "unknown":
        fee = target.get("fee")

    contact = target.get("official_contact_email") or "unknown"

    checklist = {
        "title": target.get("title"),
        "status": target.get("status"),
        "confidence": target.get("confidence"),
        "submission_method": submission_method(target),
        "recommended_url": target.get("recommended_next_url") or target.get("official_submission_url"),
        "application_form_url": target.get("application_form_url"),
        "submission_guidelines_url": target.get("submission_guidelines_url"),
        "open_call_url": target.get("open_call_url"),
        "contact_page_url": target.get("contact_page_url"),
        "contact_email": contact,
        "deadline": deadline,
        "deadline_context": deadline_sentence,
        "fee": fee,
        "required_materials": requirement_checklist(text, target),
        "eligibility_clues": (extraction or {}).get("eligibility_clues", [])[:5],
        "deadline_candidates": deadline_candidates[:5],
    }
    return checklist

def main():
    targets = load(PROMOTED, [])
    extractions = by_title(load(EXTRACTIONS, []))

    # Focus on currently actionable / near-actionable items.
    selected = targets[:8]
    checklists = [build_checklist(t, extractions.get(t.get("title"))) for t in selected]

    Path("memory").mkdir(exist_ok=True)
    json.dump(checklists, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = ["# Submission Checklists", "", "Artist-facing preparation checklists generated from promoted links and official page extraction.", ""]

    for c in checklists:
        lines.append(f"## {c['title']}")
        lines.append(f"- Submission method: {c['submission_method']}")
        lines.append(f"- Recommended URL: {c['recommended_url']}")
        lines.append(f"- Contact email: {c['contact_email']}")
        lines.append(f"- Contact page: {c['contact_page_url']}")
        lines.append(f"- Deadline: {c['deadline']}")
        if c["deadline_context"]:
            lines.append(f"- Deadline context: {c['deadline_context']}")
        lines.append(f"- Fee: {c['fee']}")
        lines.append("")
        lines.append("### Prepare")
        for item in c["required_materials"]:
            box = "[x]" if item["confirmed"] else "[ ]"
            note = "confirmed" if item["confirmed"] else "likely needed"
            lines.append(f"- {box} {item['item']} ({note})")
        if c["eligibility_clues"]:
            lines.append("")
            lines.append("### Eligibility clues")
            for e in c["eligibility_clues"]:
                lines.append(f"- {e}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
