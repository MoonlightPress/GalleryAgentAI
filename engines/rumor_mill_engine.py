"""
Rumor Mill Engine — Needs Research processor.

For each opportunity in the needs_research bucket:
  - Searches English, Japanese, and Chinese sources for missing factual data:
    deadline, entry fee, contact email, submission URL
  - Japanese sources: x.com/twitter.com (締切/公募/展示), note.com (公募/締切/展覧会)
  - Chinese sources: weibo.com, lofter.com, zcool.com.cn (截止日期/申请/展览)
  - If any data found: populates fields, moves opportunity to the appropriate bucket
  - If nothing found: logs "searched YYYY-MM-DD, no data found", leaves in place

Reads/Writes: memory/opportunity_buckets.json
Log/cache:    memory/rumor_mill.json
Schedule:     weekly
"""
import sys
import json
import os
import re
import time
import argparse
from pathlib import Path
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

import anthropic
from tavily import TavilyClient

ROOT         = Path(__file__).parent.parent
MEM          = ROOT / "memory"
BUCKET_PATH  = MEM / "opportunity_buckets.json"
LOG_PATH     = MEM / "rumor_mill.json"

CACHE_DAYS   = 7
QUERY_PAUSE  = 3.5
SNIPPET_CHARS = 500
MAX_TEXT_CHARS = 4000

tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
claude = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


# ── bucket assignment ──────────────────────────────────────────────────────────

_BOOK_CATS = {
    "book_publishing", "zine_print", "global_photobook", "global_book_arts",
    "global_artist_book_platform", "zine_fair_booth", "global_art_book_fair",
    "bookstore_gallery", "bookstore_event",
}
_PUB_CATS = {"group_publication_open_call"}
_RESIDENCY_CATS = {"residency", "residency_beijing", "global_residency", "global_grant_fellowship"}
_EASY_CATS = {"cafe_gallery", "market_event", "gallery_small", "fair_popup", "cafe"}


def choose_target_bucket(item: dict) -> str:
    cat     = item.get("category", "")
    score   = float(item.get("score", 0) or 0)
    country = str(item.get("country", "Japan")).lower()

    if cat in _BOOK_CATS:
        return "book_zine_targets"
    if cat in _PUB_CATS:
        return "publication_targets"
    if cat in _RESIDENCY_CATS:
        return "global_reach" if country not in ("", "japan") else "high_confidence"
    if score >= 8.5:
        return "career_changing"
    if score >= 8.0:
        return "high_confidence"
    if cat in _EASY_CATS:
        return "easy_wins"
    if score >= 7.0:
        return "relationship_builders"
    return "low_priority"


# ── search ────────────────────────────────────────────────────────────────────

_JAPAN_COUNTRIES  = {"", "japan", "jp"}
_CHINA_COUNTRIES  = {"china", "cn", "china (beijing)", "china (shanghai)"}


def build_queries(item: dict) -> list[tuple[str, list[str]]]:
    title   = item.get("title", "").strip()
    source  = item.get("source", "")
    country = str(item.get("country", "")).lower().strip()
    t = f'"{title}"'

    queries = [
        # English — factual data
        (f"{t} deadline submission 2025 2026",       []),
        (f"{t} apply entry fee cost",                []),
        (f"{t} contact email submissions open call", []),
    ]

    # Japanese queries only for Japan-country or unknown-country items
    if country in _JAPAN_COUNTRIES:
        queries.append((f"{t} 締切 公募 展示 申し込み", ["x.com", "twitter.com"]))
        queries.append((f"{t} 公募 締切 展覧会",         ["note.com"]))

    # Chinese queries only for China-country items
    if country in _CHINA_COUNTRIES:
        queries.append((f"{t} 截止日期 申请 展览", ["weibo.com", "lofter.com", "zcool.com.cn"]))

    if source:
        try:
            from urllib.parse import urlparse
            domain = urlparse(source).netloc
            if domain:
                queries.append((f"{title} deadline open call submit", [domain]))
        except Exception:
            pass

    return queries


# Sentinel returned when Tavily quota is exhausted — caller must not cache result
_QUOTA_ERROR = None


def run_query(query: str, include_domains: list[str] | None = None) -> str | None:
    """Return text snippets, empty string (no results), or None (quota exhausted)."""
    kwargs: dict = {"search_depth": "basic", "max_results": 5}
    if include_domains:
        kwargs["include_domains"] = include_domains

    for attempt in range(3):
        try:
            res = tavily.search(query, **kwargs)
            parts = [
                f"[{r.get('url', '')}]\n{r.get('content', '')[:SNIPPET_CHARS]}"
                for r in res.get("results", [])
                if r.get("content", "").strip()
            ]
            time.sleep(QUERY_PAUSE)
            return "\n\n".join(parts)
        except Exception as exc:
            msg = str(exc)
            if "usage limit" in msg.lower() or "plan" in msg.lower():
                print(f"    Tavily quota exhausted — stopping searches.")
                return _QUOTA_ERROR
            if "rate" in msg.lower() or "excessive" in msg.lower():
                wait = 20 * (attempt + 1)
                print(f"    rate-limited — waiting {wait}s")
                time.sleep(wait)
            else:
                print(f"    Tavily error: {exc}")
                return ""
    return ""


# ── Claude fact extraction ─────────────────────────────────────────────────────

_SYSTEM = (
    "You are a research assistant extracting factual data from web search results "
    "about art opportunities. Extract only what is explicitly stated in the text — "
    "never infer or fabricate. Return null for any field not found."
)

_EXTRACT_PROMPT = """\
Opportunity: {title}

Search results:
---
{text}
---

Extract factual data about this opportunity. Return a single JSON object with these keys:
  "deadline"       — exact date (YYYY-MM-DD) or descriptive text (e.g. "Rolling", "June 2026"), null if not found
  "fee"            — entry fee as text (e.g. "Free", "$25", "3,000 yen per piece"), null if not found
  "contact_email"  — contact email address, null if not found
  "submission_url" — direct URL to the application/submission page (not homepage), null if not found
  "data_found"     — true if ANY of the above fields has a value, false if all are null

Return only valid JSON, no code fences, no commentary.\
"""


def extract_facts(title: str, raw_text: str) -> dict:
    empty = {"deadline": None, "fee": None, "contact_email": None,
             "submission_url": None, "data_found": False}
    if not raw_text.strip():
        return empty

    prompt = _EXTRACT_PROMPT.format(title=title, text=raw_text[:MAX_TEXT_CHARS])
    try:
        resp = claude.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            system=[{"type": "text", "text": _SYSTEM,
                     "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": prompt}],
        )
        text = resp.content[0].text.strip()
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        return json.loads(text)
    except Exception as exc:
        print(f"    Claude error: {exc}")
        return empty


# ── helpers ───────────────────────────────────────────────────────────────────

def load_json(path: Path, fallback):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return fallback


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def is_fresh(title: str, log: dict) -> bool:
    entry = log.get(title, {})
    ts = entry.get("searched_at")
    if not ts:
        return False
    try:
        age = (datetime.now() - datetime.fromisoformat(ts)).days
        return age < CACHE_DAYS
    except Exception:
        return False


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Rumor Mill Engine — Needs Research processor")
    parser.add_argument("--force", action="store_true",
                        help="Re-search all items, ignoring the 7-day cache")
    parser.add_argument("--max", type=int, default=0,
                        help="Maximum items to process this run (0 = unlimited)")
    args = parser.parse_args()

    print("=== Rumor Mill Engine ===")
    print(f"Started: {datetime.now().isoformat()}\n")

    all_buckets   = load_json(BUCKET_PATH, {})
    needs_research = list(all_buckets.get("needs_research", []))
    log            = load_json(LOG_PATH, {}).get("entries", {}) if LOG_PATH.exists() else {}

    total = len(needs_research)
    print(f"needs_research: {total} items")
    if args.force:
        print("Mode: --force (ignoring cache)\n")
    if args.max:
        print(f"Limit: {args.max} items this run\n")

    moved:    list[tuple[dict, str]] = []
    searched: int = 0

    for i, item in enumerate(needs_research):
        title = item.get("title", f"item_{i}")

        if not args.force and is_fresh(title, log):
            cached_date = log[title].get("searched_at", "?")[:10]
            print(f"[{i+1:03d}/{total}] {title[:65]} — cached {cached_date}")
            continue

        if args.max and searched >= args.max:
            print(f"\nLimit of {args.max} reached — stopping.")
            break

        searched += 1
        print(f"[{i+1:03d}/{total}] {title[:65]}")

        queries   = build_queries(item)
        all_text  = ""
        quota_hit = False
        for q, domains in queries:
            snippet = run_query(q, domains or None)
            if snippet is _QUOTA_ERROR:
                quota_hit = True
                break
            if snippet:
                all_text += snippet + "\n\n"

        if quota_hit:
            print(f"  → skipped (Tavily quota exhausted — not cached)\n")
            searched -= 1  # don't count against --max; abort remaining items
            break

        facts = extract_facts(title, all_text)

        today = datetime.now().strftime("%Y-%m-%d")
        log[title] = {
            "title":       title,
            "searched_at": datetime.now().isoformat(),
            "data_found":  facts.get("data_found", False),
            "found":       {k: v for k, v in facts.items()
                            if k not in ("data_found",) and v is not None},
        }

        if facts.get("data_found"):
            for field in ("deadline", "fee", "contact_email", "submission_url"):
                if facts.get(field) is not None:
                    item[field] = facts[field]

            target = choose_target_bucket(item)
            moved.append((item, target))
            found_summary = ", ".join(
                f"{k}={v!r}" for k, v in facts.items()
                if k not in ("data_found",) and v is not None
            )
            print(f"  found: {found_summary}")
            print(f"  → moving to {target}")
        else:
            item["search_log"] = f"searched {today}, no data found"
            print(f"  → no data found")

        print()

    # Apply moves: remove from needs_research, add to target buckets
    moved_titles = {item["title"] for item, _ in moved}
    all_buckets["needs_research"] = [
        item for item in needs_research
        if item.get("title") not in moved_titles
    ]
    for item, target in moved:
        all_buckets.setdefault(target, []).append(item)

    save_json(BUCKET_PATH, all_buckets)
    save_json(LOG_PATH, {
        "updated_at": datetime.now().isoformat(),
        "entries":    log,
    })

    remaining = len(all_buckets["needs_research"])
    print(f"=== Summary ===")
    print(f"Searched: {searched}  Moved out: {len(moved)}  Remaining in needs_research: {remaining}")
    print(f"Saved {BUCKET_PATH}")
    print(f"Saved {LOG_PATH}")
    print("\nDone.")


if __name__ == "__main__":
    main()
