
import json
import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

OUT_JSON = "memory/historical_artist_data_v2.json"
OUT_REPORT = "reports/historical_artist_data_v2.md"

HEADERS = {"User-Agent": "Mozilla/5.0 (MochiHistoricalArtistCrawler/2.0)"}

GOOD_TERMS = [
    "archive", "archives", "winner", "winners", "selected", "artist", "artists",
    "exhibitor", "exhibitors", "participant", "participants", "judge", "judges",
    "competition", "award", "awards", "受賞", "入賞", "作家", "アーティスト", "出展者"
]

BAD_TERMS = [
    "privacy", "policy", "contact", "access", "login", "account", "cart",
    "terms", "cookie", "facebook", "instagram", "twitter", "youtube", "#"
]

BAD_NAME_TERMS = [
    "HOME", "ABOUT", "APPLICATION", "CONTACT", "ACCESS", "ARCHIVES", "PRIVACY",
    "POLICY", "MENU", "PAGE TOP", "OPEN CALLS", "EVENTS", "BUY ART", "LOGIN",
    "NEWS", "RSS", "COPYRIGHT", "FACEBOOK", "INSTAGRAM", "SCHEDULE", "CONTACT US",
    "APPLICATION FORM", "COMMUNITY AGREEMENT", "SUBMIT", "APPLY", "SKIP"
]

JP_CONTEXT = ["作家", "アーティスト", "絵本作家", "イラストレーター", "画家", "受賞", "入賞", "審査員"]

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def by_title(rows):
    return {r.get("title"): r for r in rows if r.get("title")}

def good_url(url, label=""):
    blob = (str(label) + " " + str(url)).lower()
    if any(b in blob for b in BAD_TERMS):
        return False
    return any(g.lower() in blob for g in GOOD_TERMS)

def fetch(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=18, allow_redirects=True)
        r.encoding = r.apparent_encoding or r.encoding
        return r.url, r.text, r.status_code, None
    except Exception as e:
        return url, "", None, str(e)

def text_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    return "\n".join([line.strip() for line in soup.get_text("\n").splitlines() if line.strip()])

def candidate_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        label = " ".join(a.get_text(" ", strip=True).split())
        url = urljoin(base_url, a["href"])
        if good_url(url, label):
            links.append({"label": label or "[no label]", "url": url})
    out, seen = [], set()
    for link in links:
        if link["url"] not in seen:
            seen.add(link["url"])
            out.append(link)
    return out[:20]

def bad_name(name):
    n = " ".join(str(name).split()).strip()
    if not n or len(n) < 4 or len(n) > 80:
        return True
    upper = n.upper()
    if n.isupper():
        return True
    if any(term in upper for term in BAD_NAME_TERMS):
        return True
    if upper.count(" ") >= 5 and not any(ch in n for ch in "・ー"):
        return True
    return False

def western_names(text):
    raw = re.findall(r"\b[A-Z][A-Za-zÀ-ÖØ-öø-ÿ'’.-]+(?:\s+[A-Z][A-Za-zÀ-ÖØ-öø-ÿ'’.-]+){1,3}\b", text or "")
    return [n for n in raw if not bad_name(n)]

def jp_names(text):
    out = []
    for line in (text or "").splitlines():
        if not any(k in line for k in JP_CONTEXT):
            continue
        m = re.match(r"^([一-龥ぁ-んァ-ンー・A-Za-z\s]{2,20})[（(]", line)
        if m and not bad_name(m.group(1)):
            out.append(m.group(1).strip())
        for role in JP_CONTEXT:
            if role in line:
                before = line.split(role)[0].strip(" 。、：:　")
                m2 = re.search(r"([一-龥ァ-ンぁ-んー・]{2,12})$", before[-24:])
                if m2 and not bad_name(m2.group(1)):
                    out.append(m2.group(1))
    return out

def context_for(name, text):
    for line in (text or "").splitlines():
        if name in line:
            return " ".join(line.split())[:280]
    return ""

def entity_type(ctx):
    low = ctx.lower()
    if "judge" in low or "審査員" in ctx:
        return "judge"
    if any(x in low for x in ["winner", "award", "selected"]) or any(x in ctx for x in ["受賞", "入賞"]):
        return "winner_or_selected_artist"
    if "exhibitor" in low or "出展者" in ctx:
        return "exhibitor"
    if any(x in low for x in ["publisher", "press", "bookshop", "bookstore"]) or any(x in ctx for x in ["出版社", "書店"]):
        return "publisher_or_bookstore"
    return "artist_or_related"

def extract_entities(text, source_url, source_label):
    names = western_names(text) + jp_names(text)
    out, seen = [], set()
    for n in names:
        if n in seen:
            continue
        seen.add(n)
        ctx = context_for(n, text)
        out.append({
            "name": n,
            "entity_type": entity_type(ctx),
            "year": "unknown",
            "source_url": source_url,
            "source_label": source_label,
            "evidence": ctx or "Name extracted from archive/evidence page.",
        })
    return out[:40]

def seed_links(evidence_item, promoted_item):
    links = []
    for link in evidence_item.get("evidence_links", []) or []:
        if good_url(link.get("url"), link.get("label")):
            links.append(link)
    for page in evidence_item.get("page_results", []) or []:
        for link in page.get("evidence_links", []) or []:
            if good_url(link.get("url"), link.get("label")):
                links.append(link)
    if promoted_item:
        for bucket in ["submission_guidelines", "open_calls"]:
            for link in promoted_item.get(bucket, []) or []:
                if good_url(link.get("url"), link.get("label")):
                    links.append(link)
    out, seen = [], set()
    for l in links:
        u = l.get("url")
        if u and u not in seen:
            seen.add(u)
            out.append(l)
    return out[:10]

def process(item, promoted):
    title = item.get("title")
    links = seed_links(item, promoted)
    pages, entities = [], []

    for link in links:
        final_url, html, status, error = fetch(link.get("url"))
        text = text_from_html(html) if html else ""
        more_links = candidate_links(html, final_url) if html else []
        page_entities = extract_entities(text, final_url, link.get("label"))

        pages.append({
            "label": link.get("label"),
            "url": link.get("url"),
            "final_url": final_url,
            "http_status": status,
            "error": error,
            "entities_found": len(page_entities),
            "archive_links_found": len(more_links),
        })
        entities.extend(page_entities)

        # one shallow follow into archive/winner pages
        for l2 in more_links[:3]:
            f2, h2, s2, e2 = fetch(l2.get("url"))
            t2 = text_from_html(h2) if h2 else ""
            entities.extend(extract_entities(t2, f2, l2.get("label")))

    deduped, seen = [], set()
    for e in entities:
        if e["name"] not in seen:
            seen.add(e["name"])
            deduped.append(e)

    return {
        "title": title,
        "historical_entities": deduped,
        "historical_artists": [e for e in deduped if e["entity_type"] in {"artist_or_related", "winner_or_selected_artist", "exhibitor"}],
        "historical_publishers": [e for e in deduped if e["entity_type"] == "publisher_or_bookstore"],
        "historical_judges": [e for e in deduped if e["entity_type"] == "judge"],
        "pages_checked": pages,
        "real_entity_count": len(deduped),
    }

def main():
    evidence = load("memory/opportunity_evidence.json", [])
    promoted_by = by_title(load("memory/promoted_opportunity_links.json", []))

    results = []
    for item in evidence:
        print("Historical v2:", item.get("title"))
        results.append(process(item, promoted_by.get(item.get("title"))))

    Path("memory").mkdir(exist_ok=True)
    json.dump(results, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    total = sum(r["real_entity_count"] for r in results)
    lines = [
        "# Historical Artist Data v2",
        "",
        "This version filters out menus/navigation and only extracts entities from archive/winner/exhibitor/artist-like pages.",
        "",
        f"Total extracted entities: {total}",
        "",
    ]

    for r in results:
        lines.append(f"## {r['title']}")
        lines.append(f"- Real entity count: {r['real_entity_count']}")
        lines.append(f"- Pages checked: {len(r['pages_checked'])}")
        lines.append("")
        if r["historical_entities"]:
            lines.append("### Entities")
            for e in r["historical_entities"][:15]:
                lines.append(f"- {e['name']} — {e['entity_type']} — {e.get('source_label')}")
                if e.get("evidence"):
                    lines.append(f"  - Evidence: {e['evidence']}")
        else:
            lines.append("_No real entities found._")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Total entities:", total)

if __name__ == "__main__":
    main()
