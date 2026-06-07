"""
Rumor Mill Expansion Runner

Runs rumor-mill research on ALL opportunities that:
  - are not yet verified
  - have not been touched by the rumor mill yet
  - have a live URL (url_verification_status == "ok")

Uses Tavily search + Claude Haiku to extract deadline, fee, contact,
and submission_url from search result snippets.

Reads/Writes: deploy_data/compact_opportunities.json
Cost control: top 80 by overall_score only
"""
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

import anthropic

COMPACT_PATH = ROOT / "deploy_data" / "compact_opportunities.json"

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
TAVILY_ENDPOINT = "https://api.tavily.com/search"

TOP_N = 80
PAUSE = 0.5
MODEL = "claude-haiku-4-5-20251001"
SNIPPET_CHARS = 3000


def needs_expansion(opp: dict) -> bool:
    if opp.get("verification_status") == "verified":
        return False
    if opp.get("rumor_mill_sentiment") not in (None, "", "pending"):
        return False
    if opp.get("url_verification_status") != "ok":
        return False
    return True


def tavily_search(query: str) -> list[dict]:
    if not TAVILY_API_KEY:
        print("[warn] TAVILY_API_KEY not set")
        return []
    try:
        resp = requests.post(
            TAVILY_ENDPOINT,
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "search_depth": "basic",
                "max_results": 3,
            },
            timeout=15,
        )
        if resp.status_code != 200:
            return []
        data = resp.json()
        return data.get("results", [])
    except Exception as e:
        print(f"  [tavily error] {e}")
        return []


def build_snippet(results: list[dict]) -> str:
    parts = []
    for r in results:
        title = r.get("title", "")
        url = r.get("url", "")
        content = r.get("content", "")
        parts.append(f"Title: {title}\nURL: {url}\nSnippet: {content[:800]}")
    combined = "\n\n---\n\n".join(parts)
    return combined[:SNIPPET_CHARS]


def extract_with_claude(client: anthropic.Anthropic, title: str, org: str, snippet: str) -> dict | None:
    if not snippet.strip():
        return None

    prompt = (
        f"From these search results about \"{title}\" by \"{org}\", extract the following:\n"
        f"- deadline date (when submissions close)\n"
        f"- entry fee (cost to apply or 'Free' if no fee)\n"
        f"- contact email\n"
        f"- submission URL (where to apply)\n\n"
        f"Search results:\n{snippet}\n\n"
        f"Return ONLY valid JSON with these keys: deadline, fee, contact, submission_url. "
        f"Use null for any field not found. No explanation, just JSON."
    )

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except Exception as e:
        print(f"  [claude error] {e}")
        return None


def apply_extracted(opp: dict, extracted) -> list[str]:
    if not isinstance(extracted, dict):
        return []
    changes = []

    deadline = extracted.get("deadline")
    if deadline and not opp.get("deadline_verified"):
        opp["deadline"] = deadline
        opp["deadline_verified"] = True
        opp["deadline_source"] = "rumor_mill_expansion"
        changes.append(f"deadline={deadline}")

    fee = extracted.get("fee")
    if fee and not opp.get("fees_verified"):
        opp["fees"] = fee
        opp["fees_verified"] = True
        opp["fees_source"] = "rumor_mill_expansion"
        changes.append(f"fee={fee}")

    contact = extracted.get("contact")
    if contact and not opp.get("contact_verified"):
        opp["contact"] = contact
        opp["contact_verified"] = True
        opp["contact_source"] = "rumor_mill_expansion"
        changes.append(f"contact={contact}")

    sub_url = extracted.get("submission_url")
    if sub_url and not opp.get("submission_page"):
        opp["submission_page"] = sub_url
        changes.append(f"submission_url={sub_url[:60]}")

    return changes


def main():
    if not COMPACT_PATH.exists():
        print(f"[error] compact_opportunities.json not found at {COMPACT_PATH}")
        return

    if not TAVILY_API_KEY:
        print("[error] TAVILY_API_KEY not set in environment")
        return

    if not ANTHROPIC_API_KEY:
        print("[error] ANTHROPIC_API_KEY not set in environment")
        return

    with open(COMPACT_PATH, "r", encoding="utf-8") as f:
        opps = json.load(f)

    candidates = [o for o in opps if needs_expansion(o)]
    candidates.sort(key=lambda o: float(o.get("overall_score", 0) or 0), reverse=True)
    batch = candidates[:TOP_N]

    print(f"[rumor_mill_expansion_runner] {len(opps)} total | {len(candidates)} eligible | processing {len(batch)}")

    claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    processed = 0
    data_found = 0

    for opp in batch:
        title = opp.get("title", "")
        org = opp.get("organization", "")
        query = f"{title} {org} submission deadline fee"

        results = tavily_search(query)
        snippet = build_snippet(results)

        if not snippet.strip():
            opp["rumor_mill_sentiment"] = "no_data"
            print(f"  [no results] {title[:50]}")
            processed += 1
            time.sleep(PAUSE)
            continue

        extracted = extract_with_claude(claude_client, title, org, snippet)

        if extracted is None:
            opp["rumor_mill_sentiment"] = "no_data"
            print(f"  [parse error] {title[:50]}")
        else:
            changes = apply_extracted(opp, extracted)
            if changes:
                opp["rumor_mill_sentiment"] = "positive"
                data_found += 1
                print(f"  [found] {title[:50]} — {', '.join(changes)}")
            else:
                opp["rumor_mill_sentiment"] = "no_data"
                print(f"  [searched, no new data] {title[:50]}")

        processed += 1
        time.sleep(PAUSE)

    with open(COMPACT_PATH, "w", encoding="utf-8") as f:
        json.dump(opps, f, ensure_ascii=False, indent=2)

    print()
    print(f"[done] processed={processed}  data_found={data_found}")
    print(f"[saved] {COMPACT_PATH}")


if __name__ == "__main__":
    main()
