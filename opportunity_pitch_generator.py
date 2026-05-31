
import json
from pathlib import Path
from datetime import datetime

PACKETS = "memory/application_packets.json"
DNA_MATCHES = "memory/dna_matches.json"
PERSONAL_CONTEXT = "memory/personalized_artist_context.json"
ACTIONABLE = "memory/actionable_targets_with_links.json"

OUT_JSON = "memory/opportunity_pitches.json"
OUT_REPORT = "reports/opportunity_pitches.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def by_title(rows):
    return {r.get("title"): r for r in rows if r.get("title")}

def effort_label(packet):
    typ = packet.get("opportunity_type", "")
    deadline = packet.get("deadline", "unknown")
    fee = packet.get("fee", "unknown")

    if typ in {"book_fair", "zine_fair"}:
        return "Medium" if deadline != "unknown" else "Medium until deadline is confirmed"
    if typ in {"gallery_submission"}:
        return "Low-Medium"
    if typ in {"open_exhibition", "competition"}:
        return "Medium after rules are verified"
    return "Unknown"

def impact_label(packet):
    typ = packet.get("opportunity_type", "")
    title = packet.get("title", "")

    if title == "TOKYO ART BOOK FAIR":
        return "High visibility in the art book / zine world"
    if "Pinpoint" in title:
        return "Focused gallery/competition visibility"
    if typ == "zine_fair":
        return "Good audience fit for existing zines"
    if typ == "gallery_submission":
        return "Good relationship-building target"
    if typ == "open_exhibition":
        return "Formal exhibition credibility if eligible"
    if typ == "competition":
        return "External validation if fee and terms are acceptable"
    return "Potential visibility, but needs more verification"

def fit_paragraph(title, typ):
    if title == "TOKYO ART BOOK FAIR":
        return (
            "This is a unusually strong fit because the artist already has zines. "
            "Her watercolor work can be presented not only as individual paintings, "
            "but as a sequence, atmosphere, or small publication. That makes an art book fair "
            "more relevant than it would be for a painter with no publication practice."
        )

    if "Pinpoint" in title:
        return (
            "This fits because it sits close to illustration, books, and gallery culture. "
            "For a watercolor artist with quiet observational work, it is a plausible bridge "
            "between fine art and publication-oriented presentation."
        )

    if title == "MOUNT ZINE":
        return (
            "This is a natural match because the artist already makes zines. "
            "It does not require pretending the work is something else; it rewards small, "
            "focused, tactile presentation."
        )

    if title in {"UTRECHT", "Book and Sons", "POST"}:
        return (
            "This is a strong bookstore/gallery crossover target. The work can be framed through "
            "small publications, paper objects, and quiet visual sequences rather than only through "
            "traditional gallery submission."
        )

    if title in {"HB Gallery", "OPA Gallery"}:
        return (
            "This is a plausible gallery inquiry target because the work is on paper, visually intimate, "
            "and suited to smaller exhibition contexts. It should be approached softly, with a concise PDF."
        )

    if typ == "open_exhibition":
        return (
            "This is useful as a formal exhibition pathway. It may not be as personally tailored as a zine "
            "or bookstore opportunity, but it can provide credibility if the rules, deadline, and fee are acceptable."
        )

    if typ == "competition":
        return (
            "This is useful only if the fee, deadline, and rights terms are acceptable. It offers external validation, "
            "but is less personal than a gallery, bookstore, or zine opportunity."
        )

    return (
        "This opportunity may fit, but the current research is incomplete. It should be treated as a research target "
        "until the submission route and requirements are clear."
    )

def why_it_matters(title, typ):
    if title == "TOKYO ART BOOK FAIR":
        return [
            "It puts the work in front of people who already care about artist books and zines.",
            "It gives her existing zines a serious context instead of treating them as side objects.",
            "It can connect paintings, sequences, and publications into one career-facing presentation.",
        ]
    if "Pinpoint" in title:
        return [
            "It is close to the book / illustration / gallery ecosystem.",
            "It gives the work a specific application path rather than a cold inquiry.",
            "It could help position her work beyond Instagram."
        ]
    if title == "MOUNT ZINE":
        return [
            "It matches her existing zine practice directly.",
            "It is lower pressure than a major gallery application.",
            "It can create a small but real audience touchpoint."
        ]
    if title in {"UTRECHT", "Book and Sons", "POST"}:
        return [
            "These are natural places for art books, paper objects, and visual sequences.",
            "They may be more emotionally compatible than aggressive gallery submission.",
            "They let the work live in a quiet, design-aware context."
        ]
    if typ == "gallery_submission":
        return [
            "A small gallery inquiry could lead to feedback, visibility, or future inclusion.",
            "It requires a clean portfolio packet but not a major new project.",
            "It can be approached softly without pressure."
        ]
    if typ == "open_exhibition":
        return [
            "Formal open exhibitions can create credibility.",
            "The rules are usually clear once the correct call is selected.",
            "It is worth considering if the fee and logistics are reasonable."
        ]
    return [
        "It may be useful, but it needs more verification before becoming a priority."
    ]

def next_steps(packet):
    title = packet.get("title", "")
    typ = packet.get("opportunity_type", "")

    steps = []
    if packet.get("recommended_url"):
        steps.append(f"Open: {packet.get('recommended_url')}")

    if title == "TOKYO ART BOOK FAIR":
        steps += [
            "Choose the strongest existing zine or publication concept.",
            "Prepare 6-10 sample images or spreads.",
            "Confirm fee and booth/application requirements.",
        ]
    elif "Pinpoint" in title:
        steps += [
            "Open the Google Form and confirm required fields.",
            "Select a coherent set of watercolor works.",
            "Prepare short bio and work details.",
        ]
    elif typ in {"zine_fair", "book_fair"}:
        steps += [
            "Choose one finished zine or publication object.",
            "Prepare sample images/spreads and price/edition details.",
            "Confirm deadline and fee.",
        ]
    elif typ == "gallery_submission":
        steps += [
            "Prepare a clean 8-12 image PDF.",
            "Write a short artist statement and bio.",
            "Find the correct contact or inquiry route.",
        ]
    elif typ in {"open_exhibition", "competition"}:
        steps += [
            "Confirm current deadline, fee, and eligibility.",
            "Check image formatting rules.",
            "Submit only if terms are acceptable.",
        ]
    else:
        steps += ["Verify the opportunity before spending more effort."]

    # de-dupe
    out = []
    for s in steps:
        if s not in out:
            out.append(s)
    return out[:6]

def caution(packet):
    title = packet.get("title", "")
    typ = packet.get("opportunity_type", "")

    if packet.get("deadline") == "unknown":
        return "Do not treat this as ready until the current deadline is confirmed."
    if packet.get("fee") == "unknown":
        return "Fee is not confirmed; check before preparing a full submission."
    if typ in {"book_fair", "zine_fair"}:
        return "Only apply with a concrete zine/book object, not loose paintings."
    if typ == "competition":
        return "Check rights terms and fee before submitting."
    return "Keep the first approach concise and practical."

def build_pitch(packet, dna_lookup):
    title = packet.get("title")
    dna = dna_lookup.get(title, {})
    typ = packet.get("opportunity_type", "unknown")

    score = dna.get("dna_match_score")
    verdict = dna.get("verdict", "research_target")

    return {
        "title": title,
        "opportunity_type": typ,
        "pitch_score": score,
        "verdict": verdict,
        "headline": f"This looks like a {typ.replace('_', ' ')} opportunity that fits her existing practice.",
        "fit_paragraph": fit_paragraph(title, typ),
        "why_it_matters": why_it_matters(title, typ),
        "effort": effort_label(packet),
        "impact": impact_label(packet),
        "deadline": packet.get("deadline"),
        "fee": packet.get("fee"),
        "recommended_url": packet.get("recommended_url"),
        "contact_page": packet.get("contact_page"),
        "next_steps": next_steps(packet),
        "caution": caution(packet),
    }

def main():
    packets = load(PACKETS, [])
    dna = by_title(load(DNA_MATCHES, []))

    pitches = [build_pitch(p, dna) for p in packets]
    pitches.sort(key=lambda x: (x.get("pitch_score") or 0), reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(pitches, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Opportunity Pitches",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "These are artist-facing opportunity explanations meant to make the best targets feel specific, relevant, and worth considering.",
        "",
    ]

    for p in pitches:
        lines.append(f"## {p['title']}")
        if p.get("pitch_score") is not None:
            lines.append(f"- Match: {p['pitch_score']}/10")
        lines.append(f"- Type: {p['opportunity_type']}")
        lines.append(f"- Effort: {p['effort']}")
        lines.append(f"- Impact: {p['impact']}")
        lines.append(f"- Deadline: {p['deadline']}")
        lines.append(f"- Fee: {p['fee']}")
        lines.append(f"- Link: {p['recommended_url']}")
        lines.append("")
        lines.append("### Why this fits")
        lines.append(p["fit_paragraph"])
        lines.append("")
        lines.append("### Why it matters")
        for item in p["why_it_matters"]:
            lines.append(f"- {item}")
        lines.append("")
        lines.append("### Next steps")
        for step in p["next_steps"]:
            lines.append(f"- {step}")
        lines.append("")
        lines.append("### Caution")
        lines.append(p["caution"])
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
