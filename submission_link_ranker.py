
import json
from pathlib import Path
from urllib.parse import urlparse

SRC = "memory/submission_targets.json"
OUT = "memory/ranked_submission_links.json"

GOOD_URL_BITS = [
    "apply", "application", "open-call", "open-calls", "opencall",
    "submission", "submit", "entry", "entries", "artist-call",
    "call-for-artists", "opportunities", "competition", "prize",
    "公募", "応募", "募集", "申込", "エントリー"
]

BAD_URL_BITS = [
    "/exhibition/", "/exhibitions/", "/schedule/", "/artist/",
    "/artists/", "/archive/", "/news/", "/blog/", "/event/",
    "/events/", "/programs/events/", "google.com/maps"
]

GOOD_LABEL_BITS = [
    "apply", "application", "open call", "open calls", "submit",
    "submission", "entry", "entries", "call for artists",
    "opportunities", "competition", "prize", "応募", "公募", "募集"
]

BAD_LABEL_BITS = [
    "learn more", "overview", "schedule", "exhibition", "artist",
    "archive", "news", "blog", "event", "skip to main content",
    "map", "directions"
]

def score_link(link):
    url = str(link.get("url", "")).lower()
    label = str(link.get("label", "")).lower()
    score = int(link.get("submission_link_score", 0) or 0)

    for bit in GOOD_URL_BITS:
        if bit in url:
            score += 5

    for bit in GOOD_LABEL_BITS:
        if bit in label:
            score += 4

    for bit in BAD_URL_BITS:
        if bit in url:
            score -= 6

    for bit in BAD_LABEL_BITS:
        if bit in label:
            score -= 5

    if link.get("same_domain"):
        score += 1

    domain = urlparse(url).netloc.lower()
    if "google" in domain or "facebook" in domain or "instagram" in domain:
        score -= 20

    return score

def main():
    data = json.load(open(SRC, encoding="utf-8"))

    for item in data:
        ranked = []
        for link in item.get("submission_links", []):
            link = dict(link)
            link["application_link_score"] = score_link(link)
            if link["application_link_score"] > 0:
                ranked.append(link)

        ranked.sort(key=lambda x: x.get("application_link_score", 0), reverse=True)
        item["ranked_submission_links"] = ranked[:8]

    Path("memory").mkdir(exist_ok=True)
    json.dump(data, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
