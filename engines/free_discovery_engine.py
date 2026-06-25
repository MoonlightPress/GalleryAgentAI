"""
free_discovery_engine.py — the FREE alternative to broad Tavily discovery.

Instead of paying for open-web search, this fetches the curated set of source
URLs in `discovery_sources.py` directly (plain HTTP, $0), pulls candidate
open-call / exhibition links out of each page, dedupes them against the
opportunities we already have, and writes the NEW ones to a staging file for
review. It never touches the live `compact_opportunities.json` — discovery is
additive and safe; promotion to the live set is a separate, deliberate step.

Design (each piece is independently testable; only `fetch_source` hits network):
  fetch_source(source)        -> html | None          (urllib, best-effort)
  extract_candidates(html, s) -> list[candidate]       (pure HTML parse)
  to_compact_record(cand)     -> dict                   (compact schema, unverified)
  dedupe(records, existing)   -> list[dict]             (pure)
  run()                        -> fetch all, dedupe, write staging + summary

Tavily stays reserved for occasional NEW-venue hunting, not routine refresh.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

try:
    from engines.discovery_sources import SOURCES
except ImportError:  # when run as a script from the engines/ dir
    from discovery_sources import SOURCES

ROOT       = Path(__file__).resolve().parent.parent
OPP_PATH   = ROOT / "deploy_data" / "compact_opportunities.json"
STAGING    = ROOT / "memory" / "free_discovery_candidates.json"

_UA = ("Mozilla/5.0 (compatible; MochiDiscovery/1.0; +https://twilightdreamworks.com/mochi) "
       "art-opportunity-finder")
_TIMEOUT = 20

# Keywords that mark a link as a plausible open call / exhibition / submission.
# Per language, matched case-insensitively against the link's visible text.
_KEYWORDS = {
    "ja": ["公募", "募集", "コンペ", "コンクール", "公募展", "締切", "作品募集",
           "アワード", "賞", "水彩", "イラスト", "レジデンス", "展覧会", "祭典"],
    "zh": ["征集", "大赛", "展览", "征稿", "奖", "驻地", "水彩", "插画",
           "截稿", "报名", "公开征集", "双年展", "美展"],
    "en": ["open call", "call for", "submission", "submit", "exhibition",
           "competition", "award", "prize", "deadline", "residency", "apply",
           "entry", "juried", "watercolor", "watercolour", "fellowship", "grant"],
}
# Generic English terms always worth matching regardless of source language
# (many JP/CN sites label calls in English too).
_EN_ALWAYS = _KEYWORDS["en"]

# Navigation / chrome link text to ignore even if it matches a keyword.
_NAV_NOISE = {
    "home", "about", "contact", "login", "sign in", "menu", "search",
    "privacy", "terms", "back", "next", "more", "オープン", "一覧", "もっと見る",
    "首页", "登录", "更多", "open calls", "opportunities", "submissions",
    "browse opportunities", "all opportunities",
}


class _LinkHarvester(HTMLParser):
    """Collects (href, visible_text) pairs from anchors."""
    def __init__(self):
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._buf: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self._href = href
                self._buf = []

    def handle_data(self, data):
        if self._href is not None:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._href is not None:
            text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
            if text:
                self.links.append((self._href, text))
            self._href = None
            self._buf = []


def _matches_keyword(text: str, lang: str) -> bool:
    low = text.lower()
    terms = _KEYWORDS.get(lang, [])
    if any(k in low for k in _EN_ALWAYS):
        return True
    # Non-English keywords are matched against the original (not lowered) text.
    return any(k in text for k in terms)


def fetch_source(source: dict, *, timeout: int = _TIMEOUT) -> str | None:
    """Best-effort GET of a source's index page. Returns decoded HTML or None.
    Never raises — a dead/blocked source is skipped, not fatal."""
    url = source.get("url")
    if not url:
        return None
    try:
        req = Request(url, headers={"User-Agent": _UA, "Accept-Language": "ja,zh,en"})
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            charset = resp.headers.get_content_charset() or "utf-8"
        return raw.decode(charset, errors="replace")
    except Exception:
        return None


def extract_candidates(html: str, source: dict) -> list[dict]:
    """Pull candidate opportunity links out of a page. Pure — no network."""
    if not html:
        return []
    lang = source.get("lang", "en")
    base = source.get("url", "")
    harvester = _LinkHarvester()
    try:
        harvester.feed(html)
    except Exception:
        return []

    out: list[dict] = []
    seen: set[str] = set()
    for href, text in harvester.links:
        if len(text) < 4 or len(text) > 140:
            continue
        if text.strip().lower() in _NAV_NOISE:
            continue
        if not _matches_keyword(text, lang):
            continue
        try:
            full = urljoin(base, href)
        except Exception:
            continue
        if not full.startswith("http"):
            continue
        key = full.split("#")[0]
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "name":     text,
            "url":      full,
            "region":   source.get("region", ""),
            "locality": source.get("locality", ""),
            "lang":     lang,
            "source_name": source.get("name", ""),
        })
    return out


def to_compact_record(cand: dict) -> dict:
    """Map a raw candidate into the compact_opportunities schema, flagged
    unverified and parked in research_needed so it can never leak into an
    actionable surface before a human/pipeline promotes it."""
    return {
        "name":            cand["name"],
        "title":           cand["name"],
        "category":        "research_needed",
        "official_website": cand["url"],
        "source_url":      cand["url"],
        "deadline":        "",
        "city":            "",
        "country":         cand.get("region", ""),
        "native_medium":   "unknown",
        "one_sentence":    f"Found via free discovery on {cand.get('source_name', '')}. "
                           f"Needs verification before action.",
        "overall_score":   0,
        "exclusive_primary_bucket": "research_needed",
        "verification_status": "unverified",
        "recommendation_visibility": "hidden",
        "discovery_source": "free_scraper",
        "discovery_locality": cand.get("locality", ""),
        "discovered_at":   datetime.now(timezone.utc).isoformat(),
    }


def _norm_name(name) -> str:
    if not isinstance(name, str):
        return ""
    return re.sub(r"[\s「」『』()（）+＋・/\-:：]", "", name.lower())[:40]


def _norm_url(url) -> str:
    # Live data is messy — a url field can be a list, None, etc. Coerce safely.
    if not isinstance(url, str):
        return ""
    try:
        p = urlparse(url)
        return (p.netloc + p.path).rstrip("/").lower()
    except Exception:
        return url.lower()


def dedupe(records: list[dict], existing: list[dict]) -> list[dict]:
    """Drop records that match something we already have (by normalized name or
    URL) or that collide with each other. Pure."""
    name_seen: set[str] = set()
    url_seen: set[str] = set()
    for o in existing:
        nm = _norm_name(o.get("name") or o.get("title") or "")
        if nm:
            name_seen.add(nm)
        for k in ("official_website", "source_url", "submission_page"):
            u = _norm_url(o.get(k, ""))
            if u:
                url_seen.add(u)

    out: list[dict] = []
    for r in records:
        nm = _norm_name(r.get("name") or r.get("title") or "")
        u = _norm_url(r.get("official_website") or r.get("source_url") or "")
        if (nm and nm in name_seen) or (u and u in url_seen):
            continue
        if nm:
            name_seen.add(nm)
        if u:
            url_seen.add(u)
        out.append(r)
    return out


def _load_json(path: Path, fallback):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return fallback


def run(sources: list[dict] | None = None, *, write: bool = True) -> dict:
    """Fetch every source, extract candidates, dedupe against the live set, and
    stage the new ones. Returns a summary dict. Never raises on a bad source."""
    sources = SOURCES if sources is None else sources
    existing = _load_json(OPP_PATH, [])
    if isinstance(existing, dict):
        existing = existing.get("items", [])

    raw: list[dict] = []
    per_source: dict[str, int] = {}
    reached = 0
    for s in sources:
        html = fetch_source(s)
        if html is None:
            per_source[s.get("name", "?")] = -1   # unreachable
            continue
        reached += 1
        cands = extract_candidates(html, s)
        per_source[s.get("name", "?")] = len(cands)
        raw.extend(cands)

    records = [to_compact_record(c) for c in raw]
    new_records = dedupe(records, existing)

    summary = {
        "sources_total":   len(sources),
        "sources_reached": reached,
        "candidates_raw":  len(raw),
        "candidates_new":  len(new_records),
        "per_source":      per_source,
        "generated_at":    datetime.now(timezone.utc).isoformat(),
    }

    if write:
        STAGING.parent.mkdir(parents=True, exist_ok=True)
        STAGING.write_text(
            json.dumps({"_summary": summary, "candidates": new_records},
                       indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return summary


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    s = run()
    print("Free discovery pass:")
    print(f"  sources reached : {s['sources_reached']}/{s['sources_total']}")
    print(f"  raw candidates  : {s['candidates_raw']}")
    print(f"  new (deduped)   : {s['candidates_new']}")
    print(f"  staged to       : {STAGING}")
    if s["candidates_new"]:
        print("  (review the staging file; promotion to the live set is a separate step)")
