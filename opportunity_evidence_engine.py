
import json
import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

PITCHES = "memory/opportunity_pitches.json"
PROMOTED = "memory/promoted_opportunity_links.json"
EXTRACTIONS = "memory/official_page_extractions.json"

OUT_JSON = "memory/opportunity_evidence.json"
OUT_REPORT = "reports/opportunity_evidence.md"

HEADERS = {"User-Agent": "Mozilla/5.0 (MochiEvidenceEngine/1.0)"}

EVIDENCE_TERMS = {
    "past_exhibitor": [
        "exhibitor", "exhibitors", "出展者", "参加者", "past exhibitors",
        "participants", "参加アーティスト"
    ],
    "artist": [
        "artist", "artists", "アーティスト", "作家", "illustrator", "illustrators",
        "painter", "watercolor", "水彩", "イラスト"
    ],
    "publisher": [
        "publisher", "publishers", "press", "independent press", "出版", "出版社"
    ],
    "bookstore_gallery": [
        "bookstore", "book shop", "gallery", "books", "zine", "art book",
        "書店", "ギャラリー", "本", "zine", "ZINE"
    ],
}

BAD_LINK_TERMS = [
    "privacy", "terms", "cookie", "cart", "account", "login", "policy",
    "facebook", "instagram", "x.com", "twitter", "youtube"
]

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def by_title(rows):
    return {r.get("title"): r for r in rows if r.get("title")}

def fetch(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=18, allow_redirects=True)
        r.encoding = r.apparent_encoding or r.encoding
        return r.url, r.text, r.status_code, None
    except Exception as e:
        return url, "", None, str(e)

def visible_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    return "\n".join([line.strip() for line in soup.get_text("\n").splitlines() if line.strip()])

def extract_evidence_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        label = " ".join(a.get_text(" ", strip=True).split())
        url = urljoin(base_url, a["href"])
        blob = (label + " " + url).lower()
        if any(b in blob for b in BAD_LINK_TERMS):
            continue
        if any(term.lower() in blob for terms in EVIDENCE_TERMS.values() for term in terms):
            links.append({"label": label or "[no label]", "url": url})
    out, seen = [], set()
    for l in links:
        if l["url"] not in seen:
            seen.add(l["url"])
            out.append(l)
    return out[:20]

def score_sentence(sentence):
    low = sentence.lower()
    score = 0
    types = []
    for typ, terms in EVIDENCE_TERMS.items():
        if any(t.lower() in low for t in terms):
            score += 2
            types.append(typ)
    if any(t in low for t in ["past", "previous", "archive", "2024", "2025", "2026", "history", "過去"]):
        score += 2
    if 40 <= len(sentence) <= 260:
        score += 1
    return score, types

def evidence_sentences(text):
    chunks = re.split(r"(?<=[.!?。])\s+|\n", text or "")
    scored = []
    for c in chunks:
        clean = " ".join(c.split())
        if len(clean) < 30 or len(clean) > 320:
            continue
        score, types = score_sentence(clean)
        if score >= 3:
            scored.append({
                "text": clean,
                "score": score,
                "types": types,
            })
    scored.sort(key=lambda x: x["score"], reverse=True)
    # de-dupe similar exact text
    out, seen = [], set()
    for s in scored:
        key = s["text"][:120]
        if key not in seen:
            seen.add(key)
            out.append(s)
    return out[:10]

def extract_names_from_text(text):
    # Simple conservative extraction: capitalized multi-word names and Japanese quoted/entity-like chunks.
    names = []
    for m in re.findall(r"\b[A-Z][A-Za-z'&.-]+(?:\s+[A-Z][A-Za-z'&.-]+){1,4}\b", text or ""):
        if len(m) < 4:
            continue
        if m.lower() in {"Tokyo Art Book Fair", "Mall Galleries Open Exhibitions"}:
            continue
        names.append(m)
    # preserve order
    out, seen = [], set()
    for n in names:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out[:15]

def source_urls_for(title, promoted, extraction, pitch):
    urls = []
    if pitch.get("recommended_url"):
        urls.append(pitch["recommended_url"])
    if extraction:
        urls.extend(extraction.get("source_urls_checked", []) or [])
        for link in extraction.get("relevant_links", []) or []:
            if link.get("url"):
                urls.append(link["url"])
    if promoted:
        for bucket in ["submission_guidelines", "open_calls", "application_forms", "contact_pages"]:
            for link in promoted.get(bucket, []) or []:
                if link.get("url"):
                    urls.append(link["url"])
    out, seen = [], set()
    for u in urls:
        if u and u != "unknown" and u not in seen:
            seen.add(u)
            out.append(u)
    return out[:5]

def build_evidence_for(pitch, promoted, extraction):
    title = pitch.get("title")
    urls = source_urls_for(title, promoted, extraction, pitch)
    page_results = []
    all_text = []

    for url in urls:
        final_url, html, status, error = fetch(url)
        text = visible_text(html) if html else ""
        links = extract_evidence_links(html, final_url) if html else []
        page_results.append({
            "url": url,
            "final_url": final_url,
            "http_status": status,
            "error": error,
            "text_length": len(text),
            "evidence_links": links,
            "evidence_sentences": evidence_sentences(text),
            "possible_names": extract_names_from_text(text),
        })
        all_text.append(text)

    combined = "\n".join(all_text)
    sentences = []
    links = []
    names = []

    for p in page_results:
        sentences.extend(p["evidence_sentences"])
        links.extend(p["evidence_links"])
        names.extend(p["possible_names"])

    sentences.sort(key=lambda x: x["score"], reverse=True)
    links = list({l["url"]: l for l in links}.values())[:12]
    names = list(dict.fromkeys(names))[:20]

    # Evidence strength is deliberately conservative.
    strength = 0
    if sentences: strength += 30
    if links: strength += 30
    if names: strength += 20
    if len(combined) > 3000: strength += 10
    if urls: strength += 10

    if strength >= 70:
        status = "evidence_found"
    elif strength >= 35:
        status = "partial_evidence"
    else:
        status = "weak_evidence"

    return {
        "title": title,
        "evidence_status": status,
        "evidence_strength": min(100, strength),
        "urls_checked": urls,
        "possible_names": names,
        "evidence_links": links,
        "evidence_sentences": sentences[:8],
        "page_results": page_results,
    }

def main():
    pitches = load(PITCHES, [])
    promoted_by = by_title(load(PROMOTED, []))
    extraction_by = by_title(load(EXTRACTIONS, []))

    # Focus first on top artist-facing opportunities.
    pitches = pitches[:8]

    evidence = []
    for pitch in pitches:
        title = pitch.get("title")
        print("Evidence:", title)
        evidence.append(build_evidence_for(
            pitch,
            promoted_by.get(title),
            extraction_by.get(title),
        ))

    Path("memory").mkdir(exist_ok=True)
    json.dump(evidence, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Opportunity Evidence Report",
        "",
        "This report looks for concrete evidence that an opportunity is real, relevant, and worth attention.",
        "",
    ]

    for e in evidence:
        lines.append(f"## {e['title']}")
        lines.append(f"- Evidence status: {e['evidence_status']}")
        lines.append(f"- Evidence strength: {e['evidence_strength']}%")
        lines.append(f"- URLs checked: {len(e['urls_checked'])}")
        lines.append("")
        if e["possible_names"]:
            lines.append("### Possible names / organizations found")
            for n in e["possible_names"][:10]:
                lines.append(f"- {n}")
            lines.append("")
        if e["evidence_links"]:
            lines.append("### Evidence links")
            for l in e["evidence_links"][:8]:
                lines.append(f"- {l['label']} — {l['url']}")
            lines.append("")
        if e["evidence_sentences"]:
            lines.append("### Evidence text")
            for s in e["evidence_sentences"][:5]:
                lines.append(f"- {s['text']}")
            lines.append("")
        if not e["evidence_sentences"] and not e["evidence_links"]:
            lines.append("_No strong evidence extracted yet._")
            lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
