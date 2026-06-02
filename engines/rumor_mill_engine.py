"""
Rumor Mill Engine
Community intelligence pass — searches social and community sources for
reputation data on the top-30 opportunities by score.

Sources searched per venue:
  - Japanese Twitter/X:        x.com/twitter.com + venue + 展示 OR ギャラリー OR 公募
  - Japanese note.com:         note.com + venue + 展覧会 OR 公募 OR 体験
  - Chinese illustration hubs: lofter.com / zcool.com.cn / weibo.com + venue
  - Reddit art communities:    reddit.com + venue + r/ImmigrantArtists OR r/Art OR r/japanlife
  - English art community:     venue + "artist experience" OR "open call" review

Extracts: sentiment, artist-treatment notes, legitimacy flags, key quotes.

Reads:  deploy_data/compact_opportunities.json
Writes: memory/rumor_mill.json
        deploy_data/compact_opportunities.json  (adds rumor_mill_score / rumor_mill_sentiment)
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

ROOT     = Path(__file__).parent.parent
MEM      = ROOT / "memory"
OPP_PATH = ROOT / "deploy_data" / "compact_opportunities.json"
OUT_PATH = MEM / "rumor_mill.json"

TOP_N          = 30
CACHE_DAYS     = 7    # skip venues researched within this many days
QUERY_PAUSE    = 3.5  # seconds between Tavily calls
SNIPPET_CHARS  = 500  # characters to keep per result
MAX_TEXT_CHARS = 4000 # cap passed to Claude per venue


# ── clients ───────────────────────────────────────────────────────────────────

tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
claude = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


# ── search ────────────────────────────────────────────────────────────────────

def build_queries(venue: str, city: str, country: str) -> list[tuple[str, list[str]]]:
    """Returns list of (query_string, include_domains) tuples.

    Tavily does not support Google-style site: or boolean OR operators.
    Use include_domains for domain-restricted searches instead.
    """
    v = venue.strip('"')
    return [
        (f'"{v}" 展示 ギャラリー 公募',                    ["twitter.com", "x.com"]),
        (f'"{v}" 展覧会 公募 体験',                          ["note.com"]),
        (f'"{v}" artist',                                   ["lofter.com", "zcool.com.cn", "weibo.com"]),
        (f'"{v}" artist gallery open call review',          ["reddit.com"]),
        (f'"{v}" artist experience review open call exhibition residency', []),
    ]


def run_query(query: str, include_domains: list[str] | None = None) -> str:
    """Return concatenated snippets from one Tavily search, or empty string."""
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
            if "rate" in msg.lower() or "excessive" in msg.lower():
                wait = 20 * (attempt + 1)
                print(f"    rate-limited — waiting {wait}s")
                time.sleep(wait)
            else:
                print(f"    Tavily error: {exc}")
                return ""
    return ""


# ── Claude sentiment extraction ───────────────────────────────────────────────

_SYSTEM = (
    "You are an art-world intelligence analyst. You read raw search snippets "
    "from social media and community forums and extract structured reputation "
    "data about galleries, residencies, and open calls. Be concise and strictly "
    "evidence-based. Only report what is actually in the text — never invent "
    "sentiment. Content may be in Japanese, Chinese, or English."
)

_EXTRACT_PROMPT = """\
Venue: {venue}

Raw search snippets (may include unrelated content — filter by relevance):
---
{text}
---

Return a single JSON object with exactly these keys:
  "sentiment"            — "positive" | "negative" | "mixed" | "no_data"
  "sentiment_confidence" — "high" | "medium" | "low"
  "score_delta"          — float −1.0 (serious red flags) … +0.5 (strong praise); 0.0 if no_data or mixed
  "artist_treatment"     — one sentence on how artists describe being treated, or null
  "legitimacy_flags"     — list of any prestige-washing / scam concerns; [] if none
  "praise_points"        — list of specific positives mentioned; [] if none
  "concern_points"       — list of specific negatives mentioned; [] if none
  "key_quotes"           — up to 3 short direct quotes from snippets; [] if none
  "sources_hit"          — list of domain names that had relevant content; [] if none

Return only valid JSON, no code fences, no commentary.\
"""


def extract_sentiment(venue: str, raw_text: str) -> dict:
    empty = {
        "sentiment": "no_data",
        "sentiment_confidence": "low",
        "score_delta": 0.0,
        "artist_treatment": None,
        "legitimacy_flags": [],
        "praise_points": [],
        "concern_points": [],
        "key_quotes": [],
        "sources_hit": [],
    }
    if not raw_text.strip():
        return empty

    prompt = _EXTRACT_PROMPT.format(venue=venue, text=raw_text[:MAX_TEXT_CHARS])

    try:
        resp = claude.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=700,
            system=[
                {
                    "type": "text",
                    "text": _SYSTEM,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": prompt}],
        )
        text = resp.content[0].text.strip()
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        parsed = json.loads(text)
        # Clamp delta to safe range
        parsed["score_delta"] = max(-1.0, min(0.5, float(parsed.get("score_delta", 0.0) or 0.0)))
        return parsed
    except Exception as exc:
        print(f"    Claude error: {exc}")
        return empty


# ── venue name normalisation ──────────────────────────────────────────────────

_STRIP_SUFFIXES = re.compile(
    r"\s+(open call|annual exhibition|open exhibition|residency program|"
    r"international exhibition|members exhibition|juried exhibition)$",
    re.IGNORECASE,
)

def venue_name(opp: dict) -> str:
    org = (opp.get("organization") or "").strip()
    if org:
        return org
    title = (opp.get("title") or "Unknown").strip()
    return _STRIP_SUFFIXES.sub("", title).strip()


# ── helpers ───────────────────────────────────────────────────────────────────

def load_json(path: Path, fallback):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return fallback


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def cached_and_fresh(venue: str, existing: dict) -> bool:
    rec = existing.get(venue, {})
    ts = rec.get("researched_at")
    if not ts:
        return False
    try:
        age = (datetime.now() - datetime.fromisoformat(ts)).days
        return age < CACHE_DAYS
    except Exception:
        return False


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Rumor Mill Engine")
    parser.add_argument("--venue", metavar="NAME",
                        help="Research only this venue (bypasses cache, case-insensitive substring match)")
    parser.add_argument("--force", action="store_true",
                        help="Bypass cache and re-research all venues")
    args = parser.parse_args()

    print("=== Rumor Mill Engine ===")
    print(f"Started: {datetime.now().isoformat()}\n")
    if args.venue:
        print(f"Mode: single venue — '{args.venue}' (cache bypassed)\n")
    elif args.force:
        print("Mode: force re-research all venues\n")

    opps = load_json(OPP_PATH, [])
    if not opps:
        print("No opportunities found — exiting.")
        return

    top30 = sorted(
        opps,
        key=lambda x: float(x.get("overall_score", 0) or 0),
        reverse=True,
    )[:TOP_N]

    # Load previous results so we can skip fresh venues
    prior_doc  = load_json(OUT_PATH, {})
    prior_data = prior_doc.get("venues", {}) if isinstance(prior_doc, dict) else {}
    results: dict = dict(prior_data)

    # Deduplicate venues — multiple opportunities can share an org
    seen_venues: set[str] = set()

    for i, opp in enumerate(top30):
        vname = venue_name(opp)
        city    = opp.get("city", "")
        country = opp.get("country", "")
        score   = opp.get("overall_score", "?")

        if vname in seen_venues:
            print(f"[{i+1:02d}/{TOP_N}] {vname[:55]} — dedup skip")
            continue
        seen_venues.add(vname)

        # --venue filter: skip everything that doesn't match
        if args.venue and args.venue.lower() not in vname.lower():
            continue

        if not args.venue and not args.force and cached_and_fresh(vname, results):
            prior_ts = results[vname].get("researched_at", "?")[:10]
            print(f"[{i+1:02d}/{TOP_N}] {vname[:55]} — cached {prior_ts}")
            continue

        print(f"[{i+1:02d}/{TOP_N}] {vname[:55]}  (score={score})")
        queries   = build_queries(vname, city, country)
        all_text  = ""

        for q, domains in queries:
            domain_hint = f" [{','.join(domains)}]" if domains else ""
            print(f"    {q[:80]}{domain_hint}")
            snippet = run_query(q, domains or None)
            if snippet:
                all_text += snippet + "\n\n"

        chars = len(all_text)
        print(f"    Extracted {chars} chars — running sentiment analysis …")

        analysis = extract_sentiment(vname, all_text)
        analysis["venue"]         = vname
        analysis["researched_at"] = datetime.now().isoformat()
        analysis["queries_run"]   = len(queries)
        analysis["text_chars"]    = chars
        results[vname] = analysis

        delta = analysis.get("score_delta", 0.0)
        print(
            f"    → sentiment={analysis.get('sentiment')}  "
            f"confidence={analysis.get('sentiment_confidence')}  "
            f"delta={delta:+.2f}"
        )
        flags = analysis.get("legitimacy_flags", [])
        if flags:
            print(f"    ⚠ legitimacy flags: {flags}")
        print()

    # Persist rumor mill data
    out_doc = {
        "generated_at":      datetime.now().isoformat(),
        "venues_researched": len(results),
        "venues":            results,
    }
    save_json(OUT_PATH, out_doc)
    print(f"Saved {OUT_PATH}  ({len(results)} venues)\n")

    # Patch compact_opportunities.json
    patched = 0
    for opp in opps:
        vname = venue_name(opp)
        rec   = results.get(vname)
        if not rec:
            continue

        delta     = float(rec.get("score_delta", 0.0) or 0.0)
        old_score = float(opp.get("overall_score", 0.0) or 0.0)

        opp["rumor_mill_sentiment"] = rec.get("sentiment", "no_data")
        opp["rumor_mill_score"]     = delta

        if delta != 0.0 and old_score > 0:
            opp["overall_score"] = round(old_score + delta, 2)

        patched += 1

    save_json(OPP_PATH, opps)
    print(f"Patched {patched} opportunity records.\n")

    # Summary
    sentiments = [v.get("sentiment", "no_data") for v in results.values()]
    all_flags  = [
        (v["venue"], v["legitimacy_flags"])
        for v in results.values()
        if v.get("legitimacy_flags")
    ]

    print("=== Summary ===")
    print(f"Venues researched (all-time): {len(results)}")
    for label in ("positive", "negative", "mixed", "no_data"):
        n = sentiments.count(label)
        if n:
            print(f"  {label}: {n}")

    if all_flags:
        print("\n⚠ Legitimacy concerns flagged:")
        for vname, flags in all_flags:
            print(f"  {vname}: {flags}")

    print("\nDone.")


if __name__ == "__main__":
    main()
