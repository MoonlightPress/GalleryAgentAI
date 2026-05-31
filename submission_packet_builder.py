
import json
from pathlib import Path
from datetime import datetime

SRC = "memory/typed_opportunities.json"
FALLBACK = "memory/application_page_results.json"
OUT_JSON = "memory/submission_packets.json"
OUT_REPORT = "reports/submission_packet_report.md"

PACKET_RULES = {
    "gallery_submission": {
        "packet_name": "Gallery Inquiry Packet",
        "goal": "Soft inquiry or portfolio introduction.",
        "materials": [
            "8-12 image PDF portfolio",
            "short artist statement, 80-120 words",
            "1 paragraph project description",
            "artist bio, 60-90 words",
            "Instagram/website link",
            "dimensions, medium, year for each work"
        ],
        "avoid": [
            "long emotional explanation",
            "sending too many images",
            "asking for representation directly in the first email"
        ],
    },
    "open_exhibition": {
        "packet_name": "Open Exhibition Packet",
        "goal": "Submit to a formal open call only if current and eligible.",
        "materials": [
            "images formatted to required size",
            "work title, medium, dimensions, year",
            "artist statement",
            "artist CV or short bio",
            "entry fee check",
            "deadline and eligibility check"
        ],
        "avoid": [
            "submitting without checking current dates",
            "using a generic artist statement",
            "ignoring size/framing rules"
        ],
    },
    "competition": {
        "packet_name": "Competition Packet",
        "goal": "Submit only if deadline, fee, and reputation justify it.",
        "materials": [
            "strongest 3-5 images",
            "short artist statement",
            "bio",
            "entry fee confirmation",
            "rights/usage terms check",
            "deadline check"
        ],
        "avoid": [
            "low-prestige pay-to-submit traps",
            "contests that do not fit watercolor/works-on-paper",
            "submitting weak or unfocused work"
        ],
    },
    "book_fair": {
        "packet_name": "Book / Art Fair Packet",
        "goal": "Apply only if there is a concrete zine, book, print object, or edition.",
        "materials": [
            "book/zine concept",
            "mockup PDF",
            "cover image",
            "sample spreads",
            "edition/price plan",
            "short table description"
        ],
        "avoid": [
            "applying with only loose paintings",
            "treating book fairs like galleries",
            "overbuilding before testing a simple mockup"
        ],
    },
    "zine_fair": {
        "packet_name": "Zine Fair Packet",
        "goal": "Make a small, low-pressure printed object first.",
        "materials": [
            "8-16 page zine mockup",
            "simple cover",
            "short artist note",
            "print cost estimate",
            "small edition plan"
        ],
        "avoid": [
            "large expensive print runs",
            "overexplaining concept",
            "treating it as career-defining"
        ],
    },
    "publication": {
        "packet_name": "Publication Packet",
        "goal": "Approach only with a sequence or project, not loose images.",
        "materials": [
            "sequence of 10-20 works",
            "project title",
            "short project statement",
            "artist bio",
            "PDF preview"
        ],
        "avoid": [
            "sending unrelated single images",
            "pitching without a project frame"
        ],
    },
    "unknown": {
        "packet_name": "Manual Review Packet",
        "goal": "Do not submit until verified.",
        "materials": [
            "verify whether this is an opportunity",
            "confirm contact",
            "confirm deadline",
            "confirm fit"
        ],
        "avoid": [
            "spending artist energy before the opportunity is real"
        ],
    },
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def best_link(item):
    links = item.get("ranked_submission_links", []) or item.get("submission_links", [])
    if links:
        return links[0].get("url", "")
    return item.get("url", "")

def best_contact(item):
    if item.get("contact") and item.get("contact") != "unknown":
        return item.get("contact")
    for page in item.get("application_page_results", []):
        emails = page.get("emails", [])
        if emails:
            return emails[0]
    return "unknown"

def best_deadline(item):
    for page in item.get("application_page_results", []):
        dates = page.get("date_candidates", [])
        if dates:
            return dates[0]
    return item.get("deadline", "unknown")

def packet_for(item):
    typ = item.get("opportunity_type") or "unknown"
    rule = PACKET_RULES.get(typ, PACKET_RULES["unknown"])
    return {
        "title": item.get("title"),
        "opportunity_type": typ,
        "packet_name": rule["packet_name"],
        "goal": rule["goal"],
        "contact": best_contact(item),
        "best_link": best_link(item),
        "deadline": best_deadline(item),
        "materials": rule["materials"],
        "avoid": rule["avoid"],
        "next_action": item.get("next_action_hint") or rule["goal"],
    }

def main():
    data = load(SRC, None)
    if data is None:
        data = load(FALLBACK, [])
    packets = [packet_for(item) for item in data[:30]]
    Path("memory").mkdir(exist_ok=True)
    json.dump(packets, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Submission Packet Report",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "This turns opportunity data into practical artist preparation packets.",
        "",
    ]
    for packet in packets[:20]:
        lines.append(f"## {packet['title']}")
        lines.append(f"- Type: {packet['opportunity_type']}")
        lines.append(f"- Packet: {packet['packet_name']}")
        lines.append(f"- Goal: {packet['goal']}")
        lines.append(f"- Contact: {packet['contact']}")
        lines.append(f"- Deadline/date: {packet['deadline']}")
        lines.append(f"- Best link: {packet['best_link']}")
        lines.append("")
        lines.append("### Prepare")
        for m in packet["materials"]:
            lines.append(f"- {m}")
        lines.append("")
        lines.append("### Avoid")
        for a in packet["avoid"]:
            lines.append(f"- {a}")
        lines.append("")
    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
