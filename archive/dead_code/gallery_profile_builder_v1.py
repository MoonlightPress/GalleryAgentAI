import json, re
from pathlib import Path
from urllib.parse import parse_qs, urlparse, unquote
import requests
from bs4 import BeautifulSoup

SRC = Path("memory/gallery_ecosystem.json")
OUT_JSON = Path("memory/gallery_profiles.json")
OUT_REPORT = Path("reports/gallery_profiles.md")
HEADERS = {"User-Agent": "Mozilla/5.0 (MochiGalleryProfileBuilder/1.0)"}
EMAIL_RE = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

RENTAL_TERMS = ["rental gallery", "貸しギャラリー", "レンタルギャラリー", "space rental", "利用料金", "使用料"]
SUBMISSION_TERMS = ["submission", "submit", "open call", "apply", "application", "募集", "公募", "応募", "作家募集", "参加アーティスト"]
EMERGING_TERMS = ["emerging", "young artist", "若手", "新人", "登竜門", "new power", "grid next"]
CURATED_TERMS = ["represented artists", "exhibition", "current exhibition", "企画展", "展覧会", "作家"]

def load(path, fallback):
    return json.load(open(path, encoding="utf-8")) if path.exists() else fallback

def unwrap(url):
    if not url:
        return ""
    if url.startswith("//"):
        url = "https:" + url
    q = parse_qs(urlparse(url).query)
    return unquote(q["uddg"][0]) if "uddg" in q and q["uddg"] else url

def fetch(url):
    url = unwrap(url)
    if not url or url.lower().endswith(".pdf"):
        return "", ""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.encoding = r.apparent_encoding or r.encoding
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.title.get_text(" ", strip=True) if soup.title else ""
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = "\n".join(x.strip() for x in soup.get_text("\n").splitlines() if x.strip())
        return title, text[:20000]
    except Exception:
        return "", ""

def has(text, terms):
    low = str(text).lower()
    return any(t.lower() in low for t in terms)

def emails(text):
    return sorted(set(re.findall(EMAIL_RE, text)))[:5]

def gallery_type(target, text):
    blob = f"{target.get('name','')} {target.get('artist_type','')} {text}".lower()
    out = []
    if has(blob, RENTAL_TERMS): out.append("rental")
    if has(blob, CURATED_TERMS): out.append("curated/exhibition")
    if "cafe" in blob or "カフェ" in blob: out.append("gallery cafe")
    if has(blob, EMERGING_TERMS): out.append("emerging-friendly")
    return out or ["needs review"]

def exhibitions(text):
    out = []
    for line in text.splitlines():
        low = line.lower()
        if any(x in low for x in ["exhibition", "展覧会", "個展", "グループ展", "solo", "group show"]) and len(line) < 160:
            out.append(line)
    return out[:8]

def score(target, text):
    s = target.get("score", 50)
    if target.get("submission_signal") or has(text, SUBMISSION_TERMS): s += 10
    if has(text, EMERGING_TERMS): s += 8
    if has(text, RENTAL_TERMS): s -= 8
    if emails(text): s += 4
    return max(0, min(100, round(s)))

def main():
    targets = load(SRC, {"targets": []}).get("targets", [])[:80]
    profiles = []
    for t in targets:
        url = unwrap(t.get("url", ""))
        print("PROFILE:", t.get("name"))
        page_title, text = fetch(url)
        profile = {
            "name": t.get("name"),
            "url": url,
            "neighborhood": t.get("neighborhood", "Tokyo"),
            "base_score": t.get("score"),
            "profile_score": score(t, text),
            "submission_signal": bool(t.get("submission_signal") or has(text, SUBMISSION_TERMS)),
            "emails": emails(text),
            "gallery_type": gallery_type(t, text),
            "artist_type": t.get("artist_type", []),
            "fit_notes": t.get("fit_notes", []),
            "page_title": page_title,
            "exhibition_terms": exhibitions(text),
            "page_text_found": bool(text),
            "status": "profiled" if text else "needs_manual_review",
        }
        profiles.append(profile)
    profiles.sort(key=lambda x: x["profile_score"], reverse=True)
    OUT_JSON.parent.mkdir(exist_ok=True); OUT_REPORT.parent.mkdir(exist_ok=True)
    OUT_JSON.write_text(json.dumps({"profile_count": len(profiles), "profiles": profiles}, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Gallery Profiles", "", f"- Profiles: {len(profiles)}", ""]
    for p in profiles:
        lines += [f"### {p['name']}", f"- Score: {p['profile_score']}", f"- Neighborhood: {p['neighborhood']}", f"- Type: {', '.join(p['gallery_type'])}", f"- Submission signal: {p['submission_signal']}", f"- Emails: {', '.join(p['emails']) if p['emails'] else 'None extracted'}", f"- URL: {p['url']}", ""]
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT_JSON, OUT_REPORT)

if __name__ == "__main__":
    main()
