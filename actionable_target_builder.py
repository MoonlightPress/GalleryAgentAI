
import json
import re
from pathlib import Path

COMPLETENESS = "memory/research_completeness.json"
CONTEXTUAL = "memory/contextualized_opportunities.json"
DNA = "memory/dna_matches.json"
OUT_JSON = "memory/actionable_targets.json"
OUT_REPORT = "reports/actionable_now.md"

EMAIL_RE = r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"

FEE_PATTERNS = [
    r"(?:entry fee|application fee|fee|応募料|参加費)[^\n。.:：]{0,30}[.:：]?\s*([$£€¥]\s?[0-9,]+|[0-9,]+\s?(?:yen|円|jpy|usd|gbp|eur|pounds?))",
    r"([$£€¥]\s?[0-9,]+|[0-9,]+\s?(?:yen|円|jpy|usd|gbp|eur|pounds?))[^\n。]{0,30}(?:entry fee|application fee|応募料|参加費|fee)",
]

DATE_PATTERNS = [
    r"\b20[2-9][0-9][-/\.][0-9]{1,2}[-/\.][0-9]{1,2}\b",
    r"\b[0-9]{1,2}[-/\.][0-9]{1,2}[-/\.]20[2-9][0-9]\b",
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+[0-9]{1,2},?\s+20[2-9][0-9]\b",
    r"\b20[2-9][0-9]年\s*[0-9]{1,2}月\s*[0-9]{1,2}日\b",
]

ELIGIBILITY_TERMS = [
    "eligibility", "eligible", "open to", "artists", "international", "residents",
    "応募資格", "対象", "参加資格", "eligible artists"
]

REQUIREMENT_TERMS = [
    "portfolio", "artist statement", "cv", "bio", "images", "jpg", "jpeg", "pdf",
    "作品", "ポートフォリオ", "ステートメント", "略歴", "画像", "プロフィール"
]

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def has_value(v):
    if v is None:
        return False
    s = str(v).strip().lower()
    return bool(s and s not in {"unknown", "none", "null", "n/a", "not publicly listed"})

def by_title(rows):
    return {r.get("title"): r for r in rows if r.get("title")}

def collect_text(item):
    chunks = []
    for page in item.get("application_page_results", []) or []:
        chunks.append(str(page.get("text_preview", "")))
        chunks.extend(page.get("requirement_hits", []) or [])
        chunks.extend(page.get("date_candidates", []) or [])
        chunks.extend(page.get("emails", []) or [])
    for link in item.get("ranked_submission_links", []) or item.get("submission_links", []) or []:
        chunks.append(str(link.get("label", "")))
        chunks.append(str(link.get("url", "")))
    return "\n".join(chunks)

def first_email(item, text):
    if has_value(item.get("contact")):
        return item.get("contact"), "existing_contact_field"
    for page in item.get("application_page_results", []) or []:
        emails = page.get("emails", []) or []
        if emails:
            return emails[0], page.get("final_url") or page.get("url") or "application_page"
    found = re.findall(EMAIL_RE, text)
    if found:
        return found[0], "page_text"
    return "unknown", ""

def first_deadline(item, text):
    if has_value(item.get("deadline")):
        return item.get("deadline"), "existing_deadline_field"
    for page in item.get("application_page_results", []) or []:
        dates = page.get("date_candidates", []) or []
        if dates:
            return dates[0], page.get("final_url") or page.get("url") or "application_page"
    for pat in DATE_PATTERNS:
        m = re.search(pat, text, re.I)
        if m:
            return m.group(0), "page_text"
    return "unknown", ""

def first_fee(text):
    for pat in FEE_PATTERNS:
        m = re.search(pat, text, re.I)
        if m:
            return m.group(1), "page_text"
    return "unknown", ""

def extract_requirements(text):
    low = text.lower()
    hits = []
    for term in REQUIREMENT_TERMS:
        if term.lower() in low and term not in hits:
            hits.append(term)
    # Normalize into artist-facing checklist.
    normalized = []
    mapping = [
        ("portfolio", "portfolio PDF or portfolio link"),
        ("artist statement", "artist statement"),
        ("cv", "CV / artist resume"),
        ("bio", "short artist bio"),
        ("images", "images of work"),
        ("jpg", "JPG image files"),
        ("jpeg", "JPEG image files"),
        ("pdf", "PDF document"),
        ("作品", "work details"),
        ("ポートフォリオ", "portfolio"),
        ("ステートメント", "artist statement"),
        ("略歴", "artist bio/CV"),
        ("画像", "images of work"),
        ("プロフィール", "profile/bio"),
    ]
    for raw, label in mapping:
        if raw.lower() in low and label not in normalized:
            normalized.append(label)
    return normalized or ["manual requirement check needed"]

def extract_eligibility(text):
    sentences = re.split(r"(?<=[.!?。])\s+", text)
    found = []
    for s in sentences:
        low = s.lower()
        if any(term.lower() in low for term in ELIGIBILITY_TERMS):
            clean = " ".join(s.split())
            if 20 <= len(clean) <= 280:
                found.append(clean)
    return found[:3]

def best_application_url(item):
    links = item.get("ranked_submission_links", []) or item.get("submission_links", [])
    if links:
        return links[0].get("url", "")
    ctx = item.get("context_summary", {})
    return ctx.get("best_link") or item.get("url") or ""

def source_urls(item):
    urls = []
    if item.get("url"):
        urls.append(item.get("url"))
    ctx = item.get("context_summary", {})
    if ctx.get("best_link"):
        urls.append(ctx.get("best_link"))
    for link in item.get("ranked_submission_links", []) or item.get("submission_links", []):
        if link.get("url"):
            urls.append(link["url"])
    for page in item.get("application_page_results", []):
        if page.get("final_url"):
            urls.append(page["final_url"])
    out = []
    seen = set()
    for u in urls:
        if u and u not in seen:
            seen.add(u)
            out.append(u)
    return out

def confidence(contact, deadline, fee, eligibility, reqs, app_url, completeness_score):
    score = 0.0
    if has_value(app_url): score += 0.20
    if has_value(contact): score += 0.15
    if has_value(deadline): score += 0.20
    if has_value(fee): score += 0.10
    if eligibility: score += 0.15
    if reqs and reqs != ["manual requirement check needed"]: score += 0.10
    score += min(0.10, float(completeness_score or 0) / 1000)
    return round(min(0.99, score), 2)

def main():
    completeness = load(COMPLETENESS, [])
    contextual = load(CONTEXTUAL, [])
    dna = load(DNA, [])

    c_by = by_title(completeness)
    d_by = by_title(dna)

    targets = []
    for item in contextual:
        title = item.get("title")
        comp = c_by.get(title, {})
        # Focus on the current actionable/research-near set.
        if comp.get("score", 0) < 55:
            continue
        if comp.get("status") == "not_actionable_yet":
            continue

        text = collect_text(item)
        contact, contact_source = first_email(item, text)
        deadline, deadline_source = first_deadline(item, text)
        fee, fee_source = first_fee(text)
        requirements = extract_requirements(text)
        eligibility = extract_eligibility(text)
        app_url = best_application_url(item)

        conf = confidence(contact, deadline, fee, eligibility, requirements, app_url, comp.get("score", 0))

        status = "actionable" if conf >= 0.65 else "needs_final_verification"

        target = {
            "title": title,
            "status": status,
            "opportunity_type": item.get("opportunity_type", "unknown"),
            "completeness_score": comp.get("score", 0),
            "dna_match_score": d_by.get(title, {}).get("dna_match_score"),
            "official_submission_url": app_url or "unknown",
            "official_contact_email": contact,
            "contact_source": contact_source,
            "deadline": deadline,
            "deadline_source": deadline_source,
            "fee": fee,
            "fee_source": fee_source,
            "eligibility": eligibility,
            "required_materials": requirements,
            "confidence": conf,
            "source_urls": source_urls(item),
            "missing": comp.get("missing", []),
        }
        targets.append(target)

    targets.sort(key=lambda x: (x["status"] == "actionable", x["confidence"], x.get("completeness_score", 0)), reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(targets, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Actionable Now",
        "",
        "This report only includes opportunities that are at least partially researched. Unknown fields remain unknown rather than guessed.",
        "",
    ]

    ready = [x for x in targets if x["status"] == "actionable"]
    verify = [x for x in targets if x["status"] != "actionable"]

    def section(title, rows):
        lines.append(f"## {title}")
        lines.append("")
        if not rows:
            lines.append("_No items._")
            lines.append("")
            return
        for t in rows:
            lines.append(f"### {t['title']}")
            lines.append(f"- Status: {t['status']}")
            lines.append(f"- Type: {t['opportunity_type']}")
            lines.append(f"- Confidence: {int(t['confidence'] * 100)}%")
            lines.append(f"- Completeness: {t['completeness_score']}%")
            if t.get("dna_match_score") is not None:
                lines.append(f"- DNA match: {t['dna_match_score']}/10")
            lines.append(f"- Submission URL: {t['official_submission_url']}")
            lines.append(f"- Contact: {t['official_contact_email']}")
            lines.append(f"- Deadline: {t['deadline']}")
            lines.append(f"- Fee: {t['fee']}")
            lines.append("")
            lines.append("#### Required materials")
            for m in t["required_materials"]:
                lines.append(f"- {m}")
            if t["eligibility"]:
                lines.append("")
                lines.append("#### Eligibility clues")
                for e in t["eligibility"]:
                    lines.append(f"- {e}")
            lines.append("")
            lines.append("#### Source URLs")
            for u in t["source_urls"]:
                lines.append(f"- {u}")
            lines.append("")

    section("Ready / Near Ready", ready)
    section("Needs Final Verification", verify)

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Actionable:", len(ready), "Needs verification:", len(verify))

if __name__ == "__main__":
    main()
