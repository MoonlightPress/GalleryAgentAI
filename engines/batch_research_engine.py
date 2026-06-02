"""
Batch research pass: fetches missing deadline/contact/fee data for
high-priority research queue items using Tavily.
Uses regex heuristics to extract dates, emails, and fees from search results.
Reads: memory/research_priority_queue.json, memory/research_queue.json,
       memory/opportunities.json
Writes: memory/research_results.json (full run log),
        memory/opportunities.json (patched in place)
"""
import sys, json, os, re, time
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from tavily import TavilyClient

ROOT   = Path(__file__).parent.parent
MEM    = ROOT / "memory"
tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

# Regex patterns for extraction
_DATE_PATTERNS = [
    r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+202[5-9]\b',
    r'\b\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+202[5-9]\b',
    r'\b202[5-9][-/]\d{2}[-/]\d{2}\b',
    r'\b\d{1,2}/\d{1,2}/202[5-9]\b',
]
_EMAIL_RE   = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')
_FEE_RE     = re.compile(r'(?:¥|USD|\$|€|£|JPY|submission fee)[^\n.]{0,60}', re.IGNORECASE)
_SUBMIT_RE  = re.compile(r'https?://[^\s"\'<>]+(?:submit|apply|entry|entries|application|form)[^\s"\'<>]*', re.IGNORECASE)
_CLOSED_RE  = re.compile(r'\b(closed|no longer accepting|submissions? closed|deadline passed|ended)\b', re.IGNORECASE)


def extract_from_text(text: str, source_url: str) -> dict:
    """Regex-heuristic extraction — no LLM required."""
    found: dict = {}

    # Deadline
    for pat in _DATE_PATTERNS:
        m = re.search(pat, text)
        if m:
            found["deadline"] = m.group(0)
            break

    # Contact email — skip generic domains
    for m in _EMAIL_RE.finditer(text):
        email = m.group(0)
        if not any(skip in email for skip in ["@example", "@your", "@email", "@sentry", "@pixel"]):
            found["contact_email"] = email
            break

    # Fee
    m = _FEE_RE.search(text)
    if m:
        found["fees"] = m.group(0).strip()

    # Submission page (prefer a URL different from source)
    for m in _SUBMIT_RE.finditer(text):
        url = m.group(0)
        if url != source_url:
            found["submission_page"] = url
            break

    # Active status
    if _CLOSED_RE.search(text):
        found["is_active"] = False

    return found


def search_venue(name: str, source_url: str, missing: list[str]) -> dict:
    """Run Tavily search and extract structured data with regex heuristics."""
    all_text = ""

    queries = []
    if source_url:
        queries.append(source_url)
    if "deadline" in missing or "fees" in missing:
        queries.append(f'"{name}" open call deadline submission 2026')

    # One query per item to stay within Tavily dev plan rate limits
    for q in queries[:1]:
        for attempt in range(3):
            try:
                res = tavily.search(q, search_depth="basic", max_results=3)
                for r in res.get("results", []):
                    all_text += f"\n{r.get('url','')}\n{r.get('content','')[:800]}\n"
                time.sleep(3.0)
                break
            except Exception as e:
                msg = str(e)
                if "excessive" in msg or "rate" in msg.lower() or "blocked" in msg.lower():
                    wait = 20 * (attempt + 1)
                    print(f"  Rate limited — waiting {wait}s …")
                    time.sleep(wait)
                else:
                    print(f"  Tavily error for {name}: {e}")
                    break

    if not all_text.strip():
        return {}

    return extract_from_text(all_text, source_url)


def load_json(path: Path) -> list | dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    print("=== Batch Research Engine ===")
    print(f"Started: {datetime.now().isoformat()}\n")

    # Load queues
    priority_q = load_json(MEM / "research_priority_queue.json")
    research_q = load_json(MEM / "research_queue.json")
    opps       = load_json(MEM / "opportunities.json")
    if isinstance(opps, dict):
        opps = opps.get("opportunities", opps.get("items", []))

    # Build lookup: name → opp record
    opp_by_name = {o.get("name", "").lower(): o for o in opps}
    opp_by_id   = {o.get("id", ""): o for o in opps}

    # Build combined target list: priority_q first, then high-priority from research_q
    seen_slugs: set[str] = set()
    targets: list[dict] = []

    for item in priority_q:
        slug = item.get("title", "").lower().replace(" ", "_")
        if slug not in seen_slugs:
            seen_slugs.add(slug)
            targets.append({
                "name":    item["title"],
                "slug":    slug,
                "missing": item.get("missing_fields", []),
                "source":  "",
                "score":   item.get("score", 0),
            })

    for item in research_q:
        if item.get("priority") != "high":
            continue
        slug = item.get("venue_slug", "")
        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)
        targets.append({
            "name":    item["venue_name"],
            "slug":    slug,
            "missing": item.get("missing", []),
            "source":  item.get("source", ""),
            "score":   0,
        })
        if len(targets) >= 70:
            break

    print(f"Targets: {len(targets)} items to research\n")

    results   = []
    updated   = 0
    not_found = 0

    for i, t in enumerate(targets):
        name    = t["name"]
        missing = t["missing"]
        source  = t["source"]

        print(f"[{i+1}/{len(targets)}] {name}")
        print(f"  Missing: {missing}")
        print(f"  Source:  {source or '(none)'}")

        extracted = search_venue(name, source, missing)

        result_entry = {
            "name":      name,
            "slug":      t["slug"],
            "missing":   missing,
            "source":    source,
            "extracted": extracted,
            "timestamp": datetime.now().isoformat(),
        }

        if extracted:
            print(f"  Found:   {list(extracted.keys())}")
            # Patch the opportunity record if it exists
            opp = opp_by_name.get(name.lower())
            if opp:
                patched = []
                if extracted.get("deadline") and not opp.get("deadline"):
                    opp["deadline"] = extracted["deadline"]
                    patched.append("deadline")
                if extracted.get("contact_email") and not opp.get("contact_email"):
                    opp["contact_email"] = extracted["contact_email"]
                    patched.append("contact_email")
                if extracted.get("fees") and not opp.get("fees"):
                    opp["fees"] = extracted["fees"]
                    patched.append("fees")
                if extracted.get("submission_page") and not opp.get("submission_page"):
                    opp["submission_page"] = extracted["submission_page"]
                    patched.append("submission_page")
                if extracted.get("is_active") is False:
                    opp["status"] = "permanently_closed"
                    patched.append("status→closed")
                if patched:
                    result_entry["patched"] = patched
                    updated += 1
                    print(f"  Patched: {patched}")
            else:
                result_entry["note"] = "No matching opportunity record found"
                not_found += 1
        else:
            print(f"  Found:   nothing")
            not_found += 1

        results.append(result_entry)
        print()

        # Rate limit courtesy pause
        time.sleep(0.3)

    # Save results
    save_json(MEM / "research_results.json", {
        "run_at": datetime.now().isoformat(),
        "total":  len(targets),
        "updated": updated,
        "not_found": not_found,
        "results": results,
    })
    print(f"Saved research_results.json")

    # Save patched opportunities
    save_json(MEM / "opportunities.json", opps)
    print(f"Saved opportunities.json ({updated} records patched)")

    print(f"\n=== Done ===")
    print(f"Researched: {len(targets)}")
    print(f"Patched:    {updated}")
    print(f"No match:   {not_found}")


if __name__ == "__main__":
    main()
