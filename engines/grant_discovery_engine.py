"""
grant_discovery_engine.py

Discovers arts grants relevant to GEGYjiji: Tokyo-based Chinese watercolor
painter. Searches Japanese, Chinese, and English sources for:
- Government arts grants (文化庁, Tokyo Metro, Japan Foundation)
- International fellowship grants (Asian Cultural Council, etc.)
- Private foundation arts grants

Adds discovered grants to deploy_data/compact_opportunities.json.
Category: "grant" | Opportunity type: "grant"
"""

import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

import json
import os
import re
import time
import argparse
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

import anthropic
from tavily import TavilyClient

ROOT        = Path(__file__).parent.parent
MEM         = ROOT / "memory"
OPP_PATH    = ROOT / "deploy_data" / "compact_opportunities.json"
LOG_PATH    = MEM / "grant_discovery_log.json"
REPORT_PATH = ROOT / "reports" / "grant_discovery_report.md"

CACHE_DAYS    = 7
QUERY_PAUSE   = 3.5
SNIPPET_CHARS = 600
MAX_SNIPPETS  = 6

tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
claude = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

TODAY = datetime.now().strftime("%Y-%m-%d")


# ── Query catalogue ────────────────────────────────────────────────────────────

GRANT_QUERIES = [
    {
        "id": "grant_jp_joseikin_artist",
        "group": "GRANT",
        "lang": "ja",
        "q": "助成金 アーティスト 公募 2026 2027 絵画 水彩",
        "domains": [],
    },
    {
        "id": "grant_jp_bunkasho",
        "group": "GRANT",
        "lang": "ja",
        "q": "文化庁 助成金 芸術家 2026 応募",
        "domains": [],
    },
    {
        "id": "grant_jp_bunka_shinko",
        "group": "GRANT",
        "lang": "ja",
        "q": "日本芸術文化振興会 助成 2026",
        "domains": [],
    },
    {
        "id": "grant_jp_tokyo_metro",
        "group": "GRANT",
        "lang": "ja",
        "q": "東京都 文化助成 アーティスト 2026",
        "domains": [],
    },
    {
        "id": "grant_en_japan_foundation",
        "group": "GRANT",
        "lang": "en",
        "q": "Japan Foundation artist grant fellowship 2026 2027",
        "domains": [],
    },
    {
        "id": "grant_en_acc",
        "group": "GRANT",
        "lang": "en",
        "q": "Asian Cultural Council fellowship grant 2026 2027 Asia artist",
        "domains": [],
    },
    {
        "id": "grant_en_tokyo_arts",
        "group": "GRANT",
        "lang": "en",
        "q": "Tokyo arts grant individual artist 2026 2027",
        "domains": [],
    },
    {
        "id": "grant_jp_shinjin_overseas",
        "group": "GRANT",
        "lang": "ja",
        "q": "新進芸術家海外研修制度 2026 応募",
        "domains": [],
    },
    {
        "id": "grant_zh_chinese_overseas",
        "group": "GRANT",
        "lang": "zh",
        "q": "中国 文化 助成金 海外 華人 艺术家 2026",
        "domains": [],
    },
    {
        "id": "grant_jp_asia_creative",
        "group": "GRANT",
        "lang": "ja",
        "q": "アジア文化創造支援 助成 2026",
        "domains": [],
    },
]


# ── Grant scoring ──────────────────────────────────────────────────────────────

GRANT_BASE_SCORE = 8.0  # Grants are high value by default — low competition, high impact
GRANT_BOOSTS = {
    "asian_cultural_council": 1.5,  # Perfect eligibility (Chinese national)
    "japan_foundation": 1.0,
    "bunka_cho": 1.0,
    "tokyo_metro": 0.8,
    "chinese_government": 0.7,
    "private_foundation": 0.5,
}


def grant_score(opp: dict) -> float:
    """Score grants with grant-specific logic."""
    name = (opp.get("name") or opp.get("organization") or "").lower()
    score = GRANT_BASE_SCORE

    if "asian cultural council" in name or "acc" in name:
        score += GRANT_BOOSTS["asian_cultural_council"]
    elif "japan foundation" in name or "国際交流基金" in name:
        score += GRANT_BOOSTS["japan_foundation"]
    elif "文化庁" in name or "bunka" in name or "bunkasho" in name:
        score += GRANT_BOOSTS["bunka_cho"]
    elif "東京都" in name or "tokyo metro" in name or "tokas" in name:
        score += GRANT_BOOSTS["tokyo_metro"]
    elif "chinese" in name or "中国" in name:
        score += GRANT_BOOSTS["chinese_government"]
    else:
        score += GRANT_BOOSTS["private_foundation"]

    conf = opp.get("confidence", "medium")
    if conf == "high":
        score += 0.3
    elif conf == "low":
        score -= 0.5

    if opp.get("deadline"):
        score += 0.1

    return round(min(10.0, max(5.0, score)), 2)


# ── Tavily search ──────────────────────────────────────────────────────────────

_QUOTA_ERROR = object()


def run_query(q: str, domains: list) -> str | object:
    """Return snippets string, empty string (no results), or _QUOTA_ERROR."""
    kwargs: dict = {"search_depth": "basic", "max_results": MAX_SNIPPETS}
    if domains:
        kwargs["include_domains"] = domains

    for attempt in range(3):
        try:
            res = tavily.search(q, **kwargs)
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
                print("    Tavily quota exhausted — stopping.")
                return _QUOTA_ERROR
            if "rate" in msg.lower() or "excessive" in msg.lower():
                wait = 20 * (attempt + 1)
                print(f"    rate-limited — waiting {wait}s")
                time.sleep(wait)
            else:
                print(f"    Tavily error: {exc}")
                return ""
    return ""


# ── Claude extraction ──────────────────────────────────────────────────────────

_SYSTEM = """\
You are a research assistant extracting arts grant listings from web search snippets.
The artist is GEGYjiji — a watercolor and illustration artist based in Tokyo. She is a Chinese
national, age 26. She works with urban observation, architecture, memory, and quiet spaces.

Extract ONLY real, concrete grant opportunities that are explicitly described in the text.
Focus on: government arts grants, foundation grants, fellowship programs, residency grants
with stipend. Do NOT extract exhibitions, open calls for art submission, or galleries.
Do NOT invent, infer, or hallucinate grant details. If a snippet only mentions a past
event or a grant with no relevance to visual arts, skip it.
Return null for any field not found in the source text.
"""

_EXTRACT_PROMPT = """\
Source group: {group}
Language context: {lang}
Search query used: {query}

Web search snippets:
---
{text}
---

Extract all distinct arts grant opportunities visible in these snippets. For each one, return:
  "name"           — full name of the grant / fellowship / funding program
  "organization"   — government body, foundation, or institution offering the grant
  "city"           — city (use "Tokyo" if Japan-based, "New York" for ACC, etc.)
  "country"        — country name (e.g. "Japan", "USA", "International")
  "deadline"       — deadline text or date if given, null otherwise
  "amount"         — grant amount or stipend if mentioned, null otherwise
  "submission_url" — direct URL to application page, null if not found
  "contact"        — contact email or URL, null if not found
  "source_url"     — URL of the page where this grant was found
  "why_fits"       — one sentence: why this grant fits a Tokyo-based Chinese watercolor artist
  "source_lang"    — "ja", "zh", or "en"
  "confidence"     — "high" (explicit listing), "medium" (likely current), or "low" (uncertain)

Return a JSON object with key "opportunities" containing an array.
If no real grant opportunities are found, return {{"opportunities": []}}.
Return only valid JSON, no code fences, no commentary.\
"""


def extract_grants(group: str, lang: str, query: str, text: str) -> list[dict]:
    if not text.strip():
        return []

    prompt = _EXTRACT_PROMPT.format(
        group=group, lang=lang, query=query,
        text=text[:5000],
    )
    try:
        resp = claude.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2000,
            system=[{
                "type": "text", "text": _SYSTEM,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": prompt}],
        )
        raw = resp.content[0].text.strip()
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        data = json.loads(raw)
        return data.get("opportunities", [])
    except Exception as exc:
        print(f"    Claude error: {exc}")
        return []


# ── Opportunity normaliser ─────────────────────────────────────────────────────

def normalise_grant(raw: dict, query_meta: dict) -> dict | None:
    name = (raw.get("name") or "").strip()
    if not name or len(name) < 4:
        return None

    raw["_group"] = query_meta["group"]
    score = grant_score(raw)

    org = (raw.get("organization") or name).strip()
    why = (raw.get("why_fits") or f"{org} is a grant opportunity for artists.").strip()
    amount = raw.get("amount") or ""
    one_sentence = why
    if amount:
        one_sentence = f"{why} Amount: {amount}."

    return {
        "name":                      name,
        "title":                     name,
        "organization":              org,
        "category":                  "grant",
        "opportunity_type":          "grant",
        "action_type":               "apply",
        "native_medium":             "all",
        "city":                      (raw.get("city") or "Unknown").strip(),
        "country":                   (raw.get("country") or "Unknown").strip(),
        "source_url":                raw.get("source_url") or raw.get("submission_url") or "",
        "submission_page":           raw.get("submission_url") or "",
        "official_website":          raw.get("source_url") or "",
        "deadline":                  raw.get("deadline") or None,
        "fees":                      "Free to apply",
        "contact":                   raw.get("contact") or None,
        "grant_amount":              amount or None,
        "overall_score":             score,
        "differentiated_score":      score,
        "watercolor_adjusted_score": score,
        "source_purity_score":       score,
        "one_sentence":              one_sentence,
        "why_this_fits_short":       why,
        "quick_action":              "Verify eligibility and current cycle at the official website before applying.",
        "verification_status":       "partial",
        "verification_bucket":       "research_needed",
        "recommendation_visibility": "show",
        "manual_review_needed":      True,
        "deadline_verified":         bool(raw.get("deadline")),
        "fees_verified":             True,
        "submission_process_known":  bool(raw.get("submission_url")),
        "contact_verified":          bool(raw.get("contact")),
        "source_lang":               raw.get("source_lang", "en"),
        "discovery_group":           "GRANT",
        "source_type":               "grant_discovery",
        "added_by":                  "grant_discovery_engine",
        "added_at":                  TODAY,
        "research_priority":         "high" if raw.get("deadline") else "medium",
        "confidence_level":          raw.get("confidence", "medium").capitalize(),
        "tags":                      _make_grant_tags(raw),
    }


def _make_grant_tags(raw: dict) -> list[str]:
    tags = ["grant", "funding"]
    lang = raw.get("source_lang", "")
    if lang == "ja":
        tags.append("japanese_source")
    elif lang == "zh":
        tags.append("chinese_source")
    if raw.get("deadline"):
        tags.append("has_deadline")
    if raw.get("submission_url"):
        tags.append("has_submission_url")
    org  = (raw.get("organization") or "").lower()
    name = (raw.get("name") or "").lower()
    combined = org + " " + name
    if "asian cultural council" in combined:
        tags.append("acc")
        tags.append("chinese_national_eligible")
    if "japan foundation" in combined or "国際交流基金" in combined:
        tags.append("japan_foundation")
    if "文化庁" in combined or "bunka" in combined:
        tags.append("bunka_cho")
    if "東京都" in combined or "tokyo metro" in combined:
        tags.append("tokyo_metro")
    return tags


# ── Deduplication ──────────────────────────────────────────────────────────────

def name_key(item: dict) -> str:
    n = (item.get("title") or item.get("name") or "").lower().strip()
    return re.sub(r"\s+", " ", n)


# ── I/O helpers ────────────────────────────────────────────────────────────────

def load_json(path: Path, fallback):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return fallback


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def query_cache_fresh(qid: str, log: dict) -> bool:
    entry = log.get("queries", {}).get(qid, {})
    ts = entry.get("last_run")
    if not ts:
        return False
    try:
        age = (datetime.now() - datetime.fromisoformat(ts)).days
        return age < CACHE_DAYS
    except Exception:
        return False


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Grant Discovery Engine")
    parser.add_argument("--force", action="store_true", help="Ignore 7-day query cache")
    parser.add_argument("--max",   type=int, default=0,  help="Max queries to run (0=all)")
    args = parser.parse_args()

    print("=== Grant Discovery Engine ===")
    print(f"Started: {datetime.now().isoformat()}\n")

    existing_opps = load_json(OPP_PATH, [])
    existing_keys = {name_key(o) for o in existing_opps}
    log           = load_json(LOG_PATH, {"queries": {}, "runs": []})

    queries = GRANT_QUERIES
    print(f"Queries planned: {len(queries)} | Existing opportunities: {len(existing_opps)}\n")

    all_found: list[dict] = []
    added:     list[dict] = []
    run_count: int        = 0
    quota_hit: bool       = False

    for qmeta in queries:
        qid = qmeta["id"]

        if not args.force and query_cache_fresh(qid, log):
            cached = log["queries"][qid].get("last_run", "?")[:10]
            print(f"  [GRANT] {qid} — cached {cached}")
            continue

        if args.max and run_count >= args.max:
            print(f"\nLimit of {args.max} queries reached — stopping.")
            break

        run_count += 1
        print(f"  [GRANT] {qid}")
        print(f"    query: {qmeta['q'][:70]}")

        text = run_query(qmeta["q"], qmeta.get("domains", []))
        if text is _QUOTA_ERROR:
            quota_hit = True
            print("  Stopping — Tavily quota exhausted.\n")
            break

        if not text:
            log["queries"][qid] = {"last_run": datetime.now().isoformat(), "found": 0}
            print(f"    no results\n")
            continue

        grants = extract_grants(qmeta["group"], qmeta["lang"], qmeta["q"], text)
        print(f"    Claude extracted: {len(grants)} items")

        new_this_query = 0
        for raw in grants:
            norm = normalise_grant(raw, qmeta)
            if not norm:
                continue
            all_found.append(norm)
            key = name_key(norm)
            if key not in existing_keys:
                existing_keys.add(key)
                added.append(norm)
                new_this_query += 1
                print(f"    + {norm['name'][:60]} [{norm['country']}] score={norm['overall_score']}")

        log["queries"][qid] = {
            "last_run": datetime.now().isoformat(),
            "found":    len(grants),
            "added":    new_this_query,
        }
        print()

    # ── Write results ──────────────────────────────────────────────────────────
    if added:
        existing_opps.extend(added)
        existing_opps.sort(
            key=lambda x: float(x.get("overall_score", 0) or 0),
            reverse=True,
        )
        save_json(OPP_PATH, existing_opps)
        print(f"Wrote {OPP_PATH}")

    log["runs"].append({
        "run_at":      datetime.now().isoformat(),
        "queries_run": run_count,
        "new_grants":  len(added),
        "quota_hit":   quota_hit,
    })
    save_json(LOG_PATH, log)

    # ── Report ─────────────────────────────────────────────────────────────────
    lines = [
        "# Grant Discovery Report",
        f"",
        f"Run: {TODAY}  |  Queries run: {run_count}  |  New grants: {len(added)}",
        f"",
    ]
    if quota_hit:
        lines += ["**Note:** Tavily quota exhausted — run was cut short.", ""]

    for o in added:
        dl     = f" · {o['deadline']}" if o.get("deadline") else ""
        amount = f" · {o['grant_amount']}" if o.get("grant_amount") else ""
        lines.append(f"- **{o['name']}** [{o['city']}, {o['country']}]{dl}{amount}")
        lines.append(f"  {o['why_this_fits_short']}")
        if o.get("source_url"):
            lines.append(f"  → {o['source_url']}")
        lines.append("")

    if not added:
        lines += ["No new grant opportunities found in this run.", ""]

    lines += [
        "## Stats",
        f"- New grants discovered: {len(added)}",
        f"- Total in pipeline: {len(existing_opps)}",
        "",
    ]

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

    print(f"\n=== Summary ===")
    print(f"Queries run:    {run_count}")
    print(f"New grants:     {len(added)}")
    print(f"Pipeline total: {len(existing_opps)}")
    print(f"Wrote {REPORT_PATH}")
    print(f"Wrote {LOG_PATH}")
    print("\nDone.")


if __name__ == "__main__":
    main()
