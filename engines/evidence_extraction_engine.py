
import json
import os
import re
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
SCRAPED_PATH = "ingestion/scraped_pages.json"
OUT_PATH = "memory/evidence_records.json"

EVIDENCE_PATTERNS = {
    "submission": [
        "submit",
        "submission",
        "apply",
        "application",
        "open call",
        "call for",
        "portfolio review",
    ],
    "fees": [
        "fee",
        "application fee",
        "entry fee",
        "participation fee",
        "free to apply",
    ],
    "deadline": [
        "deadline",
        "due",
        "apply by",
        "closes",
        "until",
    ],
    "photobook_fit": [
        "photobook",
        "photo book",
        "artist book",
        "printed matter",
        "zine",
        "publication",
    ],
    "artist_fit": [
        "photography",
        "contemporary photography",
        "visual artist",
        "emerging artist",
        "artist-run",
        "independent",
    ],
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

def title_of(opp):
    return opp.get("title") or opp.get("name") or "Unknown"

def snippets_for(text, terms, max_snippets=4):
    text = re.sub(r"\s+", " ", text or "")
    lower = text.lower()
    snippets = []

    for term in terms:
        idx = lower.find(term.lower())
        if idx == -1:
            continue

        start = max(0, idx - 180)
        end = min(len(text), idx + 260)
        snippet = text[start:end].strip()

        if snippet and snippet not in snippets:
            snippets.append(snippet)

        if len(snippets) >= max_snippets:
            break

    return snippets

def page_for_opp(opp, pages):
    url = (
        opp.get("source_url")
        or opp.get("source_link")
        or opp.get("official_website")
        or opp.get("submission_page")
        or ""
    )

    org = str(opp.get("organization") or "").lower()
    title = str(title_of(opp)).lower()

    for page in pages:
        page_url = page.get("final_url") or page.get("source_url") or ""
        source_name = str(page.get("source_name") or "").lower()

        if url and (url in page_url or page_url in url):
            return page

        if org and org in source_name:
            return page

        if title and title in source_name:
            return page

    return None

def build_evidence_for_opp(opp, pages):
    page = page_for_opp(opp, pages)
    record = {
        "title": title_of(opp),
        "source_url": opp.get("source_url") or opp.get("source_link") or opp.get("official_website") or "",
        "evidence": {},
        "evidence_count": 0,
        "evidence_quality": "none",
    }

    if not page:
        return record

    text = page.get("text", "")

    for kind, terms in EVIDENCE_PATTERNS.items():
        snippets = snippets_for(text, terms)
        if snippets:
            record["evidence"][kind] = {
                "terms": [t for t in terms if t.lower() in text.lower()],
                "snippets": snippets,
                "source_name": page.get("source_name"),
                "source_url": page.get("final_url") or page.get("source_url"),
                "status_code": page.get("status_code"),
            }

    record["evidence_count"] = sum(len(v.get("snippets", [])) for v in record["evidence"].values())

    if record["evidence_count"] >= 6:
        record["evidence_quality"] = "strong"
    elif record["evidence_count"] >= 3:
        record["evidence_quality"] = "moderate"
    elif record["evidence_count"] >= 1:
        record["evidence_quality"] = "weak"

    return record

def main():
    opps = load_json(OPP_PATH, [])
    pages = load_json(SCRAPED_PATH, [])

    records = {}

    for opp in opps:
        records[title_of(opp)] = build_evidence_for_opp(opp, pages)

    save_json(OUT_PATH, records)

    print(f"Wrote {OUT_PATH}")
    print(f"Built evidence records for {len(records)} opportunities.")

if __name__ == "__main__":
    main()
