
import json
from pathlib import Path

VERIFIED = "memory/verified_opportunities.json"
SUBMISSION_TARGETS = "memory/submission_targets.json"
RANKED = "memory/ranked_submission_links.json"
APP_RESULTS = "memory/application_page_results.json"
REPORT = "reports/application_link_repair_report.md"

KEYWORDS = [
    "application", "apply", "open call", "open-calls", "open_calls",
    "submission", "submit", "entry", "entries", "competition",
    "応募", "公募", "募集", "申込", "エントリー"
]

BAD = [
    "google.com/maps", "facebook.com", "instagram.com", "x.com",
    "twitter.com", "youtube.com", "tiktok.com", "pinterest.com",
    "/exhibition/", "/exhibitions/", "/schedule/", "/artist/", "/artists/",
    "/archive/", "/blog/", "/news/", "#main-content"
]

MANUAL_KNOWN_LINKS = {
    "TOKYO ART BOOK FAIR": [
        {"label": "Application", "url": "https://tokyoartbookfair.com/application/", "same_domain": True}
    ],
    "Royal Institute of Painters in Water Colours": [
        {"label": "Mall Galleries Open Calls", "url": "https://www.mallgalleries.org.uk/open-calls", "same_domain": True}
    ],
    "Mall Galleries Open Exhibitions": [
        {"label": "Mall Galleries Open Calls", "url": "https://www.mallgalleries.org.uk/open-calls", "same_domain": True}
    ],
    "Pastel Society Open Exhibition": [
        {"label": "Mall Galleries Open Calls", "url": "https://www.mallgalleries.org.uk/open-calls", "same_domain": True}
    ],
    "Pinpoint Gallery": [
        {"label": "Competition / Application", "url": "https://pinpointgallery.com/competition/", "same_domain": True}
    ],
    "Jackson's Art Prize": [
        {"label": "Jackson's Art Prize", "url": "https://www.jacksonsart.com/paintingprize/", "same_domain": True}
    ],
}

def load(path):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return []

def save(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    json.dump(data, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

def good_link(link):
    blob = (str(link.get("label", "")) + " " + str(link.get("url", ""))).lower()
    if any(bad in blob for bad in BAD):
        return False
    return any(k.lower() in blob for k in KEYWORDS)

def score_link(link):
    blob = (str(link.get("label", "")) + " " + str(link.get("url", ""))).lower()
    score = 0
    for k in KEYWORDS:
        if k.lower() in blob:
            score += 4
    if "application" in blob:
        score += 5
    if "open-calls" in blob or "open_calls" in blob or "open call" in blob:
        score += 5
    if "competition" in blob:
        score += 3
    if link.get("same_domain"):
        score += 1
    return score

def unique_links(links):
    out = []
    seen = set()
    for link in links:
        url = link.get("url")
        if not url or url in seen:
            continue
        seen.add(url)
        out.append(link)
    return out

def repair_item(item):
    title = item.get("title") or ""
    candidates = []

    for link in item.get("relevant_links", []) or []:
        if good_link(link):
            candidates.append(dict(link))

    for manual in MANUAL_KNOWN_LINKS.get(title, []):
        candidates.append(dict(manual))

    candidates = unique_links(candidates)
    for link in candidates:
        link["submission_link_score"] = score_link(link)
        link["application_link_score"] = score_link(link)

    candidates.sort(key=lambda x: x.get("application_link_score", 0), reverse=True)

    item["submission_links"] = candidates[:10]
    item["ranked_submission_links"] = candidates[:10]
    return item

def main():
    data = load(VERIFIED)

    if not data:
        raise SystemExit("memory/verified_opportunities.json is missing or empty. Run python run_real_verification.py first.")

    repaired = []
    counts = []

    for item in data:
        item = repair_item(dict(item))
        repaired.append(item)
        counts.append((item.get("title"), len(item.get("ranked_submission_links", []))))

    # Preserve same repaired data through the files downstream tools expect.
    save(SUBMISSION_TARGETS, repaired)
    save(RANKED, repaired)

    # Do not overwrite application_page_results if it has crawled pages, but if it is stale/empty, seed it.
    existing_app = load(APP_RESULTS)
    if not existing_app or all(len(x.get("ranked_submission_links", [])) == 0 for x in existing_app):
        save(APP_RESULTS, repaired)

    lines = ["# Application Link Repair Report", ""]
    for title, count in counts:
        lines.append(f"- {title}: {count}")

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Application link repair complete.")
    print("Nonzero link records:", sum(1 for _, c in counts if c > 0))
    print("Wrote", REPORT)

if __name__ == "__main__":
    main()
