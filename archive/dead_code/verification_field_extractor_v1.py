
import json
import re
from pathlib import Path
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

ENRICHED = Path("memory/enriched_opportunities.json")
OUT_JSON = Path("memory/verified_opportunity_fields.json")
OUT_DEPLOY = Path("deploy_data/verified_opportunity_fields.json")
OUT_REPORT = Path("reports/verified_opportunity_fields.md")

HEADERS = {"User-Agent": "Mozilla/5.0 (MochiVerificationExtractor/1.0)"}

DEADLINE_PATTERNS = [
    r"(deadline|締切|応募締切|application deadline|申込締切)[^\n。:：]{0,40}[:：]?\s*([^\n。]{0,80})",
    r"((20\d{2})[./年-]\s?\d{1,2}[./月-]\s?\d{1,2}日?)",
    r"([A-Z][a-z]+ \d{1,2}, 20\d{2})",
]
FEE_PATTERNS = [
    r"(fee|entry fee|application fee|booth fee|出展料|参加費|応募料)[^\n。:：]{0,40}[:：]?\s*([^\n。]{0,80})",
    r"(¥\s?\d[\d,]*)",
    r"(\d[\d,]*\s?円)",
]
EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

def load(path, fallback):
    if path.exists():
        return json.load(open(path, encoding="utf-8"))
    return fallback

def fetch_text(url):
    if not url or url.startswith("//"):
        return ""
    if url.lower().endswith(".pdf"):
        return ""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.encoding = r.apparent_encoding or r.encoding
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        return " ".join(soup.get_text("\n", strip=True).split())
    except Exception:
        return ""

def extract_first(patterns, text):
    for pat in patterns:
        m = re.search(pat, text, flags=re.I)
        if m:
            return " ".join([g for g in m.groups() if g])[:180]
    return ""

def extract_emails(text):
    return sorted(set(re.findall(EMAIL_PATTERN, text)))[:5]

def classify_application_route(url, text):
    blob = f"{url} {text[:2000]}".lower()
    if any(x in blob for x in ["submittable", "jotform", "google forms", "application form", "応募フォーム", "申込フォーム"]):
        return "form"
    if "@" in text:
        return "email_possible"
    if any(x in blob for x in ["application", "apply", "応募", "申込"]):
        return "application_page"
    return "check_source"

def main():
    enriched = load(ENRICHED, {"opportunities": []}).get("opportunities", [])
    # Verify top 8 per category to keep runtime sane.
    selected = []
    for cat in ["zines", "contests", "residencies", "galleries", "publishing"]:
        rows = [o for o in enriched if o.get("career_category") == cat]
        selected.extend(rows[:8])

    records = []
    for o in selected:
        name = o.get("canonical_name", "")
        url = o.get("best_url", "")
        print("VERIFY:", name, url)
        text = fetch_text(url)
        deadline = extract_first(DEADLINE_PATTERNS, text)
        fee = extract_first(FEE_PATTERNS, text)
        emails = extract_emails(text)
        route = classify_application_route(url, text)

        records.append({
            "canonical_name": name,
            "career_category": o.get("career_category"),
            "url": url,
            "deadline_extracted": deadline,
            "fee_extracted": fee,
            "emails": emails,
            "application_route": route,
            "has_page_text": bool(text),
            "text_sample": text[:400] if text else "",
            "verification_status": "field_extraction_attempted",
        })

    OUT_JSON.parent.mkdir(exist_ok=True)
    OUT_DEPLOY.parent.mkdir(exist_ok=True)
    OUT_REPORT.parent.mkdir(exist_ok=True)

    data = {"verified_count": len(records), "records": records}
    OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_DEPLOY.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Verified Opportunity Fields", "", f"- Records: {len(records)}", ""]
    for r in records:
        lines.append(f"### {r['canonical_name']}")
        lines.append(f"- Category: {r['career_category']}")
        lines.append(f"- URL: {r['url']}")
        lines.append(f"- Deadline: {r['deadline_extracted'] or 'Not extracted'}")
        lines.append(f"- Fee: {r['fee_extracted'] or 'Not extracted'}")
        lines.append(f"- Emails: {', '.join(r['emails']) if r['emails'] else 'Not extracted'}")
        lines.append(f"- Application route: {r['application_route']}")
        lines.append("")
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_DEPLOY)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
