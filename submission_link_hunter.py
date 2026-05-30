
import json
from urllib.parse import urlparse

SRC = "memory/verified_opportunities.json"
OUT = "memory/submission_targets.json"

KEYWORDS = [
    "submit", "submission", "apply", "application", "entry", "open call",
    "artist call", "opportunity", "contest", "award", "exhibition",
    "応募", "公募", "募集", "申込", "エントリー"
]

BAD_DOMAINS = [
    "google.com", "maps.google", "facebook.com", "instagram.com",
    "x.com", "twitter.com", "youtube.com", "youtu.be", "tiktok.com",
    "linkedin.com", "pinterest.com"
]

BAD_LABELS = [
    "map", "maps", "google map", "the mall, london", "directions",
    "facebook", "instagram", "youtube", "twitter", "x", "tiktok"
]

def bad_link(link):
    url = str(link.get("url", "")).lower()
    label = str(link.get("label", "")).lower().strip()
    domain = urlparse(url).netloc.lower()

    if any(bad in domain or bad in url for bad in BAD_DOMAINS):
        return True
    if any(bad in label for bad in BAD_LABELS):
        return True
    if url.startswith("mailto:") or url.startswith("tel:"):
        return True
    return False

def score_link(link):
    blob = (str(link.get("label", "")) + " " + str(link.get("url", ""))).lower()
    score = 0
    for k in KEYWORDS:
        if k in blob:
            score += 2
    if link.get("same_domain"):
        score += 1
    if "open-call" in blob or "open_calls" in blob or "open-calls" in blob:
        score += 4
    if "contact" in blob:
        score -= 1
    return score

def main():
    data = json.load(open(SRC, encoding="utf-8"))
    results = []

    for item in data:
        found = []
        for link in item.get("relevant_links", []):
            if bad_link(link):
                continue
            blob = (str(link.get("label", "")) + " " + str(link.get("url", ""))).lower()
            if any(k in blob for k in KEYWORDS):
                link = dict(link)
                link["submission_link_score"] = score_link(link)
                found.append(link)

        found.sort(key=lambda x: x.get("submission_link_score", 0), reverse=True)
        item["submission_links"] = found[:10]
        results.append(item)

    json.dump(results, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
