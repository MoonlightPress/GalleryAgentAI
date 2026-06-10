import json
import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote_plus, urljoin, urlparse, parse_qs, unquote


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


BAD_DOMAINS = [
    "facebook.com",
    "instagram.com",
    "artsy.net",
    "artfacts.net",
    "wikipedia.org",
    "google.com",
    "duckduckgo.com"
]


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def clean_duckduckgo_url(url):
    if url.startswith("//"):
        url = "https:" + url

    parsed = urlparse(url)

    if "duckduckgo.com" in parsed.netloc and parsed.path.startswith("/l/"):
        qs = parse_qs(parsed.query)
        if "uddg" in qs:
            return unquote(qs["uddg"][0])

    return url


def search_duckduckgo(query, max_results=5):
    url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    results = []

    for a in soup.select("a.result__a")[:max_results]:
        href = clean_duckduckgo_url(a.get("href", ""))
        title = a.get_text(" ", strip=True)

        if href:
            results.append({
                "title": title,
                "url": href,
                "query": query
            })

    return results


def fetch_page(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        return r.text
    except Exception:
        return ""


def extract_emails(text):
    emails = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )
    return sorted(list(set(emails)))


def find_relevant_links(base_url, html):
    soup = BeautifulSoup(html, "html.parser")

    contact_links = []
    submission_links = []
    instagram_links = []

    for a in soup.find_all("a"):
        text = a.get_text(" ", strip=True).lower()
        href = a.get("href")

        if not href:
            continue

        full_url = urljoin(base_url, href)

        if "instagram.com" in full_url:
            instagram_links.append(full_url)

        if any(word in text for word in [
            "contact",
            "inquiry",
            "about",
            "お問い合わせ",
            "連絡"
        ]):
            contact_links.append(full_url)

        if any(word in text for word in [
            "submission",
            "submit",
            "portfolio",
            "artist",
            "open call",
            "応募",
            "公募",
            "募集"
        ]):
            submission_links.append(full_url)

    return {
        "contact_links": sorted(list(set(contact_links))),
        "submission_links": sorted(list(set(submission_links))),
        "instagram_links": sorted(list(set(instagram_links)))
    }


def domain_score(url):
    netloc = urlparse(url).netloc.lower()
    score = 0

    if any(bad in netloc for bad in BAD_DOMAINS):
        score -= 5

    if netloc.endswith(".com") or netloc.endswith(".jp") or netloc.endswith(".org"):
        score += 1

    return score


def looks_like_official_site(contact_name, result):
    raw_name = contact_name.lower()
    compact_name = raw_name.replace(" ", "").replace("&", "").replace("-", "")

    url = result["url"].lower()
    title = result["title"].lower()
    compact_url = url.replace("-", "").replace("_", "").replace("/", "").replace(".", "")
    compact_title = title.replace(" ", "").replace("&", "").replace("-", "")

    score = domain_score(url)

    if compact_name in compact_title:
        score += 5

    if compact_name in compact_url:
        score += 5

    if "official" in title or "official" in url:
        score += 2

    if "gallery" in title or "gallery" in url:
        score += 2

    if "contact" in title or "contact" in url:
        score += 1

    return score


def build_queries(contact):
    name = contact.get("name", "")
    city = contact.get("city", "")
    country = contact.get("country", "")

    return [
        f"{name} {city} gallery official website",
        f"{name} official",
        f"{name} contemporary art gallery",
        f"{name} contact",
        f"{name} submission",
        f"{name} {country} art gallery"
    ]


def verify_contact(contact):
    name = contact.get("name", "")

    print(f"\nVerifying: {name}")

    all_results = []

    for query in build_queries(contact):
        print(f"Search: {query}")
        try:
            all_results.extend(search_duckduckgo(query))
        except Exception as e:
            print(f"Search failed: {e}")

    seen = set()
    deduped = []

    for result in all_results:
        url = result["url"]
        if url not in seen:
            seen.add(url)
            deduped.append(result)

    if not deduped:
        return {
            "verification_status": "not_found",
            "official_website": "",
            "contact_page": "",
            "submission_page": "",
            "instagram": "",
            "emails": [],
            "last_verified": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "verification_notes": "No search results found."
        }

    ranked = sorted(
        deduped,
        key=lambda r: looks_like_official_site(name, r),
        reverse=True
    )

    best = ranked[0]
    official_url = best["url"]

    html = fetch_page(official_url)
    emails = extract_emails(html)
    links = find_relevant_links(official_url, html)

    contact_page = links["contact_links"][0] if links["contact_links"] else ""
    submission_page = links["submission_links"][0] if links["submission_links"] else ""
    instagram = links["instagram_links"][0] if links["instagram_links"] else ""

    status = "needs_manual_review"

    if official_url:
        status = "official_site_candidate"

    if contact_page or emails:
        status = "contact_info_found"

    return {
        "verification_status": status,
        "official_website": official_url,
        "contact_page": contact_page,
        "submission_page": submission_page,
        "instagram": instagram,
        "emails": emails,
        "search_results": ranked[:10],
        "last_verified": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "verification_notes": "Auto-verification candidate. Human should confirm before outreach."
    }


contact_memory = load_json(
    "memory/contact_memory.json",
    {"contacts": []}
)

contacts = contact_memory.get("contacts", [])

if not contacts:
    raise Exception("No contacts found in memory/contact_memory.json")

for i, contact in enumerate(contacts):
    verification = verify_contact(contact)

    contacts[i]["web_verification"] = verification

    if verification.get("official_website"):
        contacts[i]["official_website"] = verification["official_website"]

    if verification.get("contact_page"):
        contacts[i]["contact_page"] = verification["contact_page"]

    if verification.get("submission_page"):
        contacts[i]["submission_page"] = verification["submission_page"]

    if verification.get("emails"):
        contacts[i]["contact_email"] = verification["emails"][0]

    contacts[i]["status"] = "research_needed"

    if verification["verification_status"] == "contact_info_found":
        contacts[i]["status"] = "ready_to_review"


contact_memory["contacts"] = contacts

save_json(
    "memory/contact_memory.json",
    contact_memory
)

print("\nUpdated memory/contact_memory.json")