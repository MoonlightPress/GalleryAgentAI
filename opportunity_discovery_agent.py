import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from anthropic import Anthropic
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json
import os
import re
from tavily import TavilyClient

load_dotenv(dotenv_path=".env")

MODEL = "claude-sonnet-4-5"

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

HEADERS = {"User-Agent": "Mozilla/5.0"}

SEARCH_QUERIES = [
    "Tokyo contemporary art open call emerging artists",
    "Tokyo gallery artist submission contemporary painting",
    "Tokyo artist-run space open call painting",
    "Japan art competition contemporary painting open call",
    "Tokyo illustration fair artist application",
    "Asian contemporary painting open call artist",
    "art book fair Tokyo artist application",
    "Tokyo zine fair artist table application",
    "artist residency Japan visual artist open call",
    "contemporary realism gallery Tokyo artist submission"
]


def load_text(path, fallback=""):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)



def search_web(query, max_results=5):

    try:
        response = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=max_results
        )

    except Exception as e:
        print(f"Search failed: {query}")
        print(e)
        return []

    results = []

    for r in response.get("results", []):

        results.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "query": query
        })

    return results



def fetch_page_text(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except Exception:
        return ""

    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text("\n", strip=True)
    return text[:8000]


def extract_emails(text):
    emails = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )
    return sorted(list(set(emails)))


def classify_candidates_with_claude(candidates, artist_dossier, artist_preferences):
    prompt = f"""
You are Agent Q: Opportunity Discovery and Filtering Agent.

Your job:
Evaluate raw web search candidates and turn only the useful ones into structured artist opportunity cards.

The artist:
{artist_dossier}

Artist preferences:
{json.dumps(artist_preferences, indent=2, ensure_ascii=False)}

Raw candidates:
{json.dumps(candidates, indent=2, ensure_ascii=False)}

Return ONLY valid JSON.

Return a JSON array.

Each item must follow this schema:

{{
  "name": "",
  "type": "",
  "city": "",
  "country": "",
  "official_website": "",
  "contact_page": "",
  "submission_page": "",
  "contact_email": "",
  "status": "research_needed",
  "priority": "A/B/C",
  "fit_score": 1,
  "urgency_score": 1,
  "effort_score": 1,
  "strategic_score": 1,
  "emotional_resistance": 1,
  "confidence_score": 0.0,
  "why_fit": "",
  "next_action": "",
  "risk_notes": "",
  "source_url": "",
  "source_query": "",
  "human_verification_needed": []
}}

Rules:
- Include only candidates that are plausibly useful.
- Reject generic search results, directories, articles, and irrelevant pages.
- Prefer realistic opportunities over prestigious fantasy targets.
- Do not invent emails or submission pages.
- If something is uncertain, say so in risk_notes.
- Scores must be conservative.
- Status should usually be research_needed unless the candidate clearly has contact/submission info.
- Keep results practical for an emerging artist.
- The artist-facing purpose is to reduce overwhelm, not create a giant homework pile.
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=5000,
        messages=[{"role": "user", "content": prompt}]
    )

    output = response.content[0].text
    cleaned = output.replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)


def merge_opportunities(existing, discovered):
    for new_opp in discovered:
        new_opp["discovered_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_opp["source"] = "opportunity_discovery_agent"

        existing_index = None

        for i, old in enumerate(existing):
            old_name = old.get("name", "").lower().strip()
            new_name = new_opp.get("name", "").lower().strip()

            if old_name and new_name and old_name == new_name:
                existing_index = i
                break

        if existing_index is not None:
            existing[existing_index].update(new_opp)
        else:
            existing.append(new_opp)

    return existing


def main():
    artist_dossier = load_text("artist_dossier.md")
    artist_preferences = load_json("memory/artist_preferences.json", {})
    opportunities = load_json("memory/opportunities.json", [])

    raw_candidates = []

    print("Searching for opportunities...")

    for query in SEARCH_QUERIES:
        print(f"Search: {query}")
        results = search_web(query, max_results=4)

        for result in results:
            page_text = fetch_page_text(result["url"])
            emails = extract_emails(page_text)

            raw_candidates.append({
                "title": result["title"],
                "url": result["url"],
                "query": result["query"],
                "page_excerpt": page_text[:1500],
                "emails_found": emails
            })

    print(f"Raw candidates gathered: {len(raw_candidates)}")

    if not raw_candidates:
        print("No candidates found.")
        return

    discovered = classify_candidates_with_claude(
        raw_candidates,
        artist_dossier,
        artist_preferences
    )

    print(f"Useful opportunities discovered: {len(discovered)}")

    merged = merge_opportunities(opportunities, discovered)

    save_json("memory/opportunities.json", merged)

    with open("opportunity_discovery_report.json", "w", encoding="utf-8") as f:
        json.dump(discovered, f, indent=2, ensure_ascii=False)

    print("Saved memory/opportunities.json")
    print("Saved opportunity_discovery_report.json")


if __name__ == "__main__":
    main()