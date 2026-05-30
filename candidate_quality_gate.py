
import json
import os
from pathlib import Path
from urllib.parse import urlparse

CANDIDATE_PATH = "ingestion/opportunity_candidates.json"
APPROVED_PATH = "ingestion/approved_candidates.json"
REJECTED_PATH = "ingestion/rejected_candidates.json"
REPORT_PATH = "reports/candidate_quality_gate_report.md"

BAD_TITLE_EXACT = {
    "instagram",
    "facebook",
    "pinterest",
    "tiktok",
    "x",
    "learn",
    "continue reading",
    "magazine subscribers",
    "magazine subscription",
    "see all exhibitions",
    "browse printed matter editions",
    "exhibitions",
    "submission amendment",
}

BAD_TITLE_CONTAINS = [
    "facebook",
    "instagram",
    "pinterest",
    "tiktok",
    "www.facebook.com",
    "www.instagram.com",
    "continue reading",
    "magazine subscription",
    "magazine subscribers",
    "see all exhibitions",
    "browse printed matter editions",
]

BAD_HOSTS = {
    "www.facebook.com",
    "facebook.com",
    "instagram.com",
    "www.instagram.com",
    "pinterest.com",
    "www.pinterest.com",
    "tiktok.com",
    "www.tiktok.com",
    "x.com",
    "twitter.com",
}

STRONG_TERMS = {
    "open call",
    "submission",
    "submit",
    "apply",
    "residency",
    "portfolio review",
    "award",
    "grant",
    "artist book",
    "photobook",
    "zine",
    "printed matter",
    "book fair",
    "exhibition opportunity",
    "deadline",
    "call for",
}

WEAK_TERMS = {
    "photography",
    "publication",
    "gallery",
    "exhibition",
    "artist",
    "book",
}


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def text_blob(c):
    parts = [
        c.get("title", ""),
        c.get("one_sentence", ""),
        c.get("why_this_fits_short", ""),
        c.get("category", ""),
        c.get("source_url", ""),
    ]

    parts += [str(x) for x in c.get("fit_keyword_hits", [])]

    return " ".join(str(x) for x in parts).lower()


def evaluate(c):
    title = str(c.get("title") or "").strip().lower()
    url = c.get("source_url") or c.get("official_website") or ""
    host = urlparse(url).netloc.lower()
    blob = text_blob(c)

    if not title or len(title) < 4:
        return False, ["bad/missing title"]

    if title in BAD_TITLE_EXACT:
        return False, [f"junk title: {title}"]

    for bad in BAD_TITLE_CONTAINS:
        if bad in title:
            return False, [f"junk title contains: {bad}"]

    if host in BAD_HOSTS:
        return False, [f"junk host: {host}"]

    strong = [t for t in STRONG_TERMS if t in blob]
    weak = [t for t in WEAK_TERMS if t in blob]

    score = len(strong) * 2 + len(weak)

    if c.get("submission_page"):
        score += 3

    if c.get("deadline"):
        score += 2

    if c.get("source_type") == "scraped_link_candidate":
        score -= 2

    # Generic pages are not enough unless they contain strong opportunity language.
    if not strong and not c.get("submission_page"):
        return False, ["generic page without opportunity language"]

    reasons = []

    if strong:
        reasons.append("strong: " + ", ".join(strong[:5]))

    if weak:
        reasons.append("weak: " + ", ".join(weak[:5]))

    if c.get("submission_page"):
        reasons.append("has submission link")

    if score >= 5:
        return True, reasons or ["passes quality threshold"]

    return False, reasons + [f"score too low: {score}"]


def main():
    candidates = load_json(CANDIDATE_PATH, [])

    approved = []
    rejected = []

    for c in candidates:
        ok, reasons = evaluate(c)
        c["quality_gate_status"] = "approved" if ok else "rejected"
        c["quality_gate_reasons"] = reasons

        if ok:
            approved.append(c)
        else:
            rejected.append(c)

    save_json(APPROVED_PATH, approved)
    save_json(REJECTED_PATH, rejected)

    lines = [
        "# Candidate Quality Gate Report",
        "",
        f"Approved: {len(approved)}",
        f"Rejected: {len(rejected)}",
        "",
        "## Rejected",
        "",
    ]

    for c in rejected:
        lines.append(f"- {c.get('title')} — {', '.join(c.get('quality_gate_reasons', []))}")

    lines += ["", "## Approved", ""]

    for c in approved:
        lines.append(f"- {c.get('title')} — {', '.join(c.get('quality_gate_reasons', []))}")

    Path(REPORT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Approved candidates: {len(approved)}")
    print(f"Rejected candidates: {len(rejected)}")
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
