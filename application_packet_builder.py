
import json
from pathlib import Path
from datetime import datetime

CHECKLISTS = "memory/submission_checklists.json"
CONTEXT = "memory/personalized_artist_context.json"
DNA = "memory/artist_dna.json"

OUT_JSON = "memory/application_packets.json"
OUT_REPORT = "reports/application_packets.md"

TYPE_DEFAULTS = {
    "book_fair": {
        "image_count": "6-10 images or sample spreads",
        "statement_length": "80-120 words",
        "bio_length": "60-90 words",
        "estimated_time": "2-4 hours if zine materials already exist",
        "first_step": "Choose the specific zine/book/publication to submit.",
        "packet_items": [
            "zine/book title",
            "short description",
            "sample spreads or cover image",
            "edition size",
            "price",
            "artist bio",
            "links / Instagram / website"
        ],
    },
    "zine_fair": {
        "image_count": "8-16 zine pages or mockup pages",
        "statement_length": "50-100 words",
        "bio_length": "50-80 words",
        "estimated_time": "2-5 hours depending on mockup readiness",
        "first_step": "Choose one zine and prepare a simple mockup/preview.",
        "packet_items": [
            "zine title",
            "cover image",
            "sample pages",
            "edition size",
            "price",
            "short artist note",
            "artist bio"
        ],
    },
    "gallery_submission": {
        "image_count": "8-12 artwork images",
        "statement_length": "120-180 words",
        "bio_length": "60-100 words",
        "estimated_time": "2-3 hours if images are already selected",
        "first_step": "Select 8-12 coherent works that look like one body of work.",
        "packet_items": [
            "8-12 images",
            "artist statement",
            "short bio",
            "work list: title, medium, size, year",
            "portfolio PDF or link",
            "Instagram / website"
        ],
    },
    "open_exhibition": {
        "image_count": "1-5 images depending on call rules",
        "statement_length": "80-150 words",
        "bio_length": "60-100 words",
        "estimated_time": "1-3 hours after rules are verified",
        "first_step": "Confirm deadline, fee, eligibility, medium, and image formatting rules.",
        "packet_items": [
            "images formatted to rules",
            "work details",
            "artist statement if requested",
            "short bio",
            "entry fee confirmation",
            "eligibility confirmation"
        ],
    },
    "competition": {
        "image_count": "1-5 strongest works",
        "statement_length": "80-150 words if requested",
        "bio_length": "60-100 words",
        "estimated_time": "1-3 hours after rules are verified",
        "first_step": "Confirm fee, deadline, eligibility, and whether rights terms are acceptable.",
        "packet_items": [
            "strongest images",
            "work details",
            "artist bio",
            "artist statement if requested",
            "fee confirmation",
            "rights/usage terms check"
        ],
    },
    "unknown": {
        "image_count": "unknown",
        "statement_length": "unknown",
        "bio_length": "unknown",
        "estimated_time": "unknown until opportunity is verified",
        "first_step": "Verify the opportunity type and submission process.",
        "packet_items": [
            "manual research needed"
        ],
    },
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def infer_type(title, method, url):
    blob = f"{title} {method} {url}".lower()
    if "book" in blob or "art book fair" in blob or "printed matter" in blob:
        return "book_fair"
    if "zine" in blob:
        return "zine_fair"
    if "gallery" in blob or "pinpoint" in blob or "opa" in blob or "hb" in blob:
        return "gallery_submission"
    if "open call" in blob or "mallgalleries" in blob or "water colours" in blob or "pastel" in blob:
        return "open_exhibition"
    if "prize" in blob or "competition" in blob:
        return "competition"
    return "unknown"

def clean_materials(items):
    out = []
    seen = set()
    for x in items:
        if isinstance(x, dict):
            label = x.get("item")
            confirmed = x.get("confirmed", False)
            source = x.get("source", "")
        else:
            label = str(x)
            confirmed = False
            source = "unknown"
        if not label or label in seen:
            continue
        seen.add(label)
        out.append({
            "item": label,
            "confirmed": bool(confirmed),
            "source": source,
        })
    return out

def build_packet(checklist):
    title = checklist.get("title")
    method = checklist.get("submission_method", "")
    url = checklist.get("recommended_url", "")

    typ = infer_type(title, method, url)
    defaults = TYPE_DEFAULTS.get(typ, TYPE_DEFAULTS["unknown"])

    extracted = clean_materials(checklist.get("required_materials", []))
    extracted_labels = {x["item"] for x in extracted}

    packet_items = []
    for item in extracted:
        packet_items.append(item)

    for item in defaults["packet_items"]:
        if item not in extracted_labels:
            packet_items.append({
                "item": item,
                "confirmed": False,
                "source": "type_template",
            })

    must_do_first = []
    if checklist.get("deadline") == "unknown":
        must_do_first.append("Confirm deadline.")
    if checklist.get("fee") == "unknown":
        must_do_first.append("Confirm fee or whether there is no fee.")
    if checklist.get("contact_email") == "unknown" and checklist.get("contact_page_url") in {"unknown", None, ""}:
        must_do_first.append("Find contact route.")
    if not must_do_first:
        must_do_first.append(defaults["first_step"])

    return {
        "title": title,
        "opportunity_type": typ,
        "submission_method": method,
        "recommended_url": url,
        "contact_page": checklist.get("contact_page_url"),
        "contact_email": checklist.get("contact_email"),
        "deadline": checklist.get("deadline"),
        "deadline_context": checklist.get("deadline_context"),
        "fee": checklist.get("fee"),
        "image_count": defaults["image_count"],
        "statement_length": defaults["statement_length"],
        "bio_length": defaults["bio_length"],
        "estimated_time": defaults["estimated_time"],
        "first_step": defaults["first_step"],
        "must_do_first": must_do_first,
        "packet_items": packet_items,
        "eligibility_clues": checklist.get("eligibility_clues", []),
    }

def main():
    checklists = load(CHECKLISTS, [])
    packets = [build_packet(c) for c in checklists]

    Path("memory").mkdir(exist_ok=True)
    json.dump(packets, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Application Packets",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "These packets convert opportunity research into concrete preparation work.",
        "",
    ]

    for p in packets:
        lines.append(f"## {p['title']}")
        lines.append(f"- Type: {p['opportunity_type']}")
        lines.append(f"- Submission method: {p['submission_method']}")
        lines.append(f"- Recommended URL: {p['recommended_url']}")
        lines.append(f"- Contact page: {p['contact_page']}")
        lines.append(f"- Contact email: {p['contact_email']}")
        lines.append(f"- Deadline: {p['deadline']}")
        lines.append(f"- Fee: {p['fee']}")
        lines.append(f"- Estimated prep time: {p['estimated_time']}")
        lines.append(f"- Image requirement estimate: {p['image_count']}")
        lines.append(f"- Statement length estimate: {p['statement_length']}")
        lines.append(f"- Bio length estimate: {p['bio_length']}")
        lines.append("")
        lines.append("### Do first")
        for x in p["must_do_first"]:
            lines.append(f"- {x}")
        lines.append("")
        lines.append("### Packet checklist")
        for item in p["packet_items"]:
            box = "[x]" if item["confirmed"] else "[ ]"
            status = "confirmed" if item["confirmed"] else "template / likely"
            lines.append(f"- {box} {item['item']} ({status})")
        if p["eligibility_clues"]:
            lines.append("")
            lines.append("### Eligibility clues")
            for e in p["eligibility_clues"][:5]:
                lines.append(f"- {e}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
