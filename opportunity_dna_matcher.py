
import json
from pathlib import Path

OPPS = "memory/contextualized_opportunities.json"
CONTEXT = "memory/personalized_artist_context.json"
DNA = "memory/artist_dna.json"
OUT = "memory/dna_matches.json"
REPORT = "reports/dna_match_report.md"

DNA_THEMES = [
    "watercolor",
    "works on paper",
    "zine",
    "artist book",
    "publication",
    "urban",
    "architecture",
    "memory",
    "quiet",
    "domestic",
    "small press",
    "bookstore",
    "gallery",
    "illustration",
]

TYPE_MATCH_REASON = {
    "gallery_submission": [
        "direct venue relationship possible",
        "fits works-on-paper or small exhibition pathway",
        "useful for building local visibility"
    ],
    "book_fair": [
        "artist already has zines",
        "publication practice makes book-fair context plausible",
        "audience overlaps with small-press and artist-book culture"
    ],
    "zine_fair": [
        "artist already has zines",
        "low-pressure publication ecosystem",
        "good fit for small watercolor sequences"
    ],
    "publication": [
        "could fit if works are sequenced as a project",
        "supports small-press visibility",
        "useful only with a coherent series"
    ],
    "open_exhibition": [
        "formal exhibition path",
        "works-on-paper may be eligible",
        "good if deadline, fee, and rules are verified"
    ],
    "competition": [
        "can provide external validation",
        "useful only if medium and fee fit",
        "less personal than gallery/bookstore paths"
    ],
    "unknown": [
        "fit cannot be trusted until opportunity type is verified"
    ]
}

TYPE_BASE = {
    "gallery_submission": 7.7,
    "book_fair": 7.8,
    "zine_fair": 8.0,
    "publication": 6.8,
    "open_exhibition": 7.0,
    "competition": 6.2,
    "unknown": 3.5,
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def blob(item):
    parts = []
    for k in ["title", "opportunity_type", "best_link", "url"]:
        if item.get(k):
            parts.append(str(item[k]))
    ctx = item.get("context_summary", {})
    for k in ["best_link", "actionability"]:
        if ctx.get(k):
            parts.append(str(ctx[k]))
    for k in ["ranked_submission_links", "submission_links", "application_page_results"]:
        for x in item.get(k, []) or []:
            if isinstance(x, dict):
                parts.append(str(x.get("label", "")))
                parts.append(str(x.get("url", "")))
                parts.append(str(x.get("text_preview", ""))[:500])
    return " ".join(parts).lower()

def score_match(item, context):
    typ = item.get("opportunity_type") or "unknown"
    text = blob(item)
    ctx = item.get("context_summary", {})

    score = TYPE_BASE.get(typ, 4.0)
    reasons = list(TYPE_MATCH_REASON.get(typ, []))
    risks = []

    hits = [t for t in DNA_THEMES if t in text]
    if hits:
        score += min(1.2, len(hits) * 0.2)
        reasons.append("keyword/audience overlap: " + ", ".join(hits[:6]))

    title = str(item.get("title") or "")

    if title in {"TOKYO ART BOOK FAIR", "MOUNT ZINE", "UTRECHT", "Book and Sons", "POST"}:
        score += 0.8
        reasons.append("existing zines make this more relevant than a painting-only profile")

    if title in {"HB Gallery", "OPA Gallery", "Pinpoint Gallery"}:
        score += 0.7
        reasons.append("small gallery / illustration-adjacent path looks compatible with watercolor")

    if ctx.get("actionability") == "actionable_research_target":
        score += 0.7
        reasons.append("application or open-call page found")
    elif ctx.get("actionability") == "needs_manual_verification":
        score -= 0.4
        risks.append("submission/contact path still needs manual verification")
    elif ctx.get("actionability") == "reject_or_archive":
        score -= 4.5
        risks.append("likely false positive or archive/catalog page")

    missing = ctx.get("missing", [])
    if "contact" in missing:
        risks.append("contact not yet confirmed")
    if "deadline" in missing:
        risks.append("deadline not yet confirmed")
    if "application/submission link" in missing:
        risks.append("application/submission link not yet confirmed")

    if typ in {"book_fair", "zine_fair"}:
        risks.append("requires selecting or preparing a concrete zine/book object")

    if typ == "competition":
        risks.append("may be competitive or fee-dependent")

    score = round(max(0, min(10, score)), 2)

    if score >= 8:
        verdict = "strong_match"
    elif score >= 6.5:
        verdict = "promising_match"
    elif score >= 5:
        verdict = "research_only"
    else:
        verdict = "low_priority"

    return {
        "title": item.get("title"),
        "opportunity_type": typ,
        "dna_match_score": score,
        "verdict": verdict,
        "reasons": reasons,
        "risks": list(dict.fromkeys(risks)),
        "best_link": ctx.get("best_link") or item.get("url"),
        "actionability": ctx.get("actionability"),
    }

def main():
    opps = load(OPPS, [])
    context = load(CONTEXT, {})
    dna = load(DNA, {})

    matches = [score_match(item, context) for item in opps]
    matches.sort(key=lambda x: x["dna_match_score"], reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(matches, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Opportunity DNA Match Report",
        "",
        "This explains why each opportunity fits or does not fit the artist profile.",
        "",
    ]

    for m in matches:
        lines.append(f"## {m['title']}")
        lines.append(f"- DNA Match Score: {m['dna_match_score']}/10")
        lines.append(f"- Verdict: {m['verdict']}")
        lines.append(f"- Type: {m['opportunity_type']}")
        lines.append(f"- Link: {m.get('best_link')}")
        lines.append("")
        lines.append("### Why it fits")
        for r in m["reasons"]:
            lines.append(f"- {r}")
        if m["risks"]:
            lines.append("")
            lines.append("### Risks / missing pieces")
            for r in m["risks"]:
                lines.append(f"- {r}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT)
    print("Wrote", REPORT)

if __name__ == "__main__":
    main()
