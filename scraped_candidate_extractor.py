
import json
import os
from pathlib import Path
from urllib.parse import urlparse


SCRAPED_PATH = "ingestion/scraped_pages.json"
SOURCE_PATH = "source_targets.json"
OUT_PATH = "ingestion/opportunity_candidates.json"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def keyword_score(text, keywords):
    text = (text or "").lower()
    hits = [k for k in keywords if k.lower() in text]
    return len(hits), hits


def reject_score(text, reject_keywords):
    text = (text or "").lower()
    hits = [k for k in reject_keywords if k.lower() in text]
    return len(hits), hits


def infer_category(text, source_type):
    t = (text + " " + source_type).lower()

    if "photobook" in t or "photo book" in t:
        return "global_photobook"
    if "zine" in t or "printed matter" in t or "artist book" in t:
        return "zine_print"
    if "residency" in t:
        return "residency"
    if "open call" in t or "award" in t:
        return "photo_open_call"
    if "book fair" in t or "fair" in t:
        return "art_book_fair"
    if "gallery" in t or "exhibition" in t:
        return "gallery_event"

    return source_type or "research_candidate"


def candidate_from_page(page, fit_keywords, reject_keywords):
    text = page.get("text", "")
    title = page.get("title") or page.get("source_name")
    fit_count, fit_hits = keyword_score(text, fit_keywords)
    bad_count, bad_hits = reject_score(text, reject_keywords)

    score = min(8.5, 4.5 + fit_count * 0.45 - bad_count * 1.2)

    return {
        "title": title,
        "organization": page.get("source_name"),
        "category": infer_category(text, page.get("source_type", "")),
        "city": "Online" if page.get("region") == "Global" else "",
        "country": page.get("region", ""),
        "overall_score": round(max(0, score), 2),
        "prestige_score": 0,
        "difficulty_score": 0,
        "confidence_level": "low" if page.get("status_code") != 200 else "medium",
        "verification_status": "partial",
        "source_type": "scraped_candidate",
        "source_url": page.get("final_url") or page.get("source_url"),
        "official_website": page.get("final_url") or page.get("source_url"),
        "submission_page": "",
        "deadline": "",
        "fees": "",
        "one_sentence": f"Candidate discovered from {page.get('source_name')}. Needs manual verification before recommendation.",
        "why_this_fits_short": "Potential fit based on source context and keyword overlap: " + ", ".join(fit_hits[:8]),
        "quick_action": "Open source, verify current opportunities, submission process, fees, deadline, and contact.",
        "three_bullets": [
            "Automatically discovered candidate.",
            "Needs verification before being treated as actionable.",
            "Keyword hits: " + ", ".join(fit_hits[:10])
        ],
        "fit_keyword_hits": fit_hits,
        "reject_keyword_hits": bad_hits,
        "manual_review_needed": True,
        "missing_fields": ["submission process", "deadline", "fees", "contact"]
    }


def candidates_from_links(page, fit_keywords, reject_keywords):
    out = []

    for link in page.get("links", []):
        label = link.get("label", "")
        url = link.get("url", "")
        text = (label + " " + url).lower()

        fit_count, fit_hits = keyword_score(text, fit_keywords)
        bad_count, bad_hits = reject_score(text, reject_keywords)

        if fit_count == 0 or bad_count > 0:
            continue

        host = urlparse(url).netloc

        out.append({
            "title": label[:90] or host,
            "organization": page.get("source_name"),
            "category": infer_category(text, page.get("source_type", "")),
            "city": "Online" if page.get("region") == "Global" else "",
            "country": page.get("region", ""),
            "overall_score": round(min(8.2, 4.0 + fit_count * 0.7), 2),
            "prestige_score": 0,
            "difficulty_score": 0,
            "confidence_level": "low",
            "verification_status": "weak",
            "source_type": "scraped_link_candidate",
            "source_url": url,
            "official_website": url,
            "submission_page": url if any(w in text for w in ["submit", "submission", "open-call", "open call", "apply"]) else "",
            "deadline": "",
            "fees": "",
            "one_sentence": f"Candidate link discovered from {page.get('source_name')}.",
            "why_this_fits_short": "Possible fit based on link text: " + ", ".join(fit_hits[:8]),
            "quick_action": "Open and verify whether this is current and relevant.",
            "three_bullets": [
                "Discovered from source link list.",
                "Needs manual verification.",
                "Keyword hits: " + ", ".join(fit_hits[:10])
            ],
            "fit_keyword_hits": fit_hits,
            "reject_keyword_hits": bad_hits,
            "manual_review_needed": True,
            "missing_fields": ["deadline", "fees", "contact"]
        })

    return out


def main():
    pages = load_json(SCRAPED_PATH, [])
    config = load_json(SOURCE_PATH, {})
    fit_keywords = config.get("fit_keywords", [])
    reject_keywords = config.get("reject_keywords", [])

    candidates = []

    for page in pages:
        if page.get("status_code") == 200:
            candidates.append(candidate_from_page(page, fit_keywords, reject_keywords))
            candidates.extend(candidates_from_links(page, fit_keywords, reject_keywords))

    # Deduplicate by source URL/title pair.
    seen = set()
    unique = []

    for c in candidates:
        key = (c.get("title", "").lower(), c.get("source_url", "").lower())
        if key in seen:
            continue
        seen.add(key)
        unique.append(c)

    unique.sort(key=lambda x: float(x.get("overall_score", 0) or 0), reverse=True)

    save_json(OUT_PATH, unique)

    print(f"Wrote {OUT_PATH}")
    print(f"Candidates: {len(unique)}")


if __name__ == "__main__":
    main()
