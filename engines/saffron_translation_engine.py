"""
saffron_translation_engine.py

Auto-translates the Saffron / career-strategy payload's authored + generated
strings into Simplified Chinese, written to memory/translation_cache.json.

Opportunity card strings (name, one_sentence, why) are already translated into
compact_opportunities.json (_zh) by content_translation_engine and are skipped
here. This engine covers everything else Saffron renders: analysis prose,
scenario steps, generated next-actions, templated summaries, dates, etc.

Incremental + cached: only translates strings not already in the cache. Safe to
re-run. Run it after the weekly pipeline (or after editing Saffron copy) so the
Chinese stays current with zero hand-maintained map.

Usage:  python engines/saffron_translation_engine.py [--api https://twilightdreamworks.com]
"""

import sys
import json
import os
import re
import time
import argparse
import urllib.request
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from json_repair import repair_json

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

CACHE   = ROOT / "memory" / "translation_cache.json"
COMPACT = ROOT / "deploy_data" / "compact_opportunities.json"
MODEL   = "claude-sonnet-4-6"
BATCH   = 12

SYSTEM = (
    "You are a professional translator for an art-career app used by a Chinese "
    "watercolor painter. Translate each English UI / career-analysis string into "
    "natural, concise Simplified Chinese (简体中文).\n"
    "Rules:\n"
    "- Address the artist as 你 (second person). Never 她/他.\n"
    "- Preserve proper nouns (gallery / venue / organisation / prize names, "
    "@handles, URLs) exactly as written — do not translate or transliterate them.\n"
    "- Keep dates and numbers intact; translate only the words around them.\n"
    "- Match the original length and tone. No added commentary.\n"
    "- Return ONLY a JSON object mapping each exact input string to its translation."
)


def load_cache() -> dict:
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    return {}


def save_cache(c: dict) -> None:
    CACHE.write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch(base: str, path: str):
    try:
        with urllib.request.urlopen(base + path, timeout=30) as r:
            return json.load(r)
    except Exception as e:
        print(f"  fetch {path} failed: {e}")
        return {}


def translatable(s) -> bool:
    if not isinstance(s, str):
        return False
    s = s.strip()
    if len(s) < 2 or s.startswith("http"):
        return False
    if not re.search(r"[A-Za-z]", s):       # no latin letters => nothing to translate
        return False
    return True


def collect_strings(obj, out: set):
    if isinstance(obj, str):
        if translatable(obj):
            out.add(obj.strip())
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k == "_i18n":               # the translation map itself
                continue
            collect_strings(v, out)
    elif isinstance(obj, list):
        for v in obj:
            collect_strings(v, out)


def opp_covered() -> set:
    """English strings already translated in compact_opportunities (skip them)."""
    covered = set()
    if not COMPACT.exists():
        return covered
    opps = json.loads(COMPACT.read_text(encoding="utf-8"))
    pairs = [("name", "name_zh"), ("one_sentence", "one_sentence_zh"),
             ("why_this_fits_short", "why_it_fits_zh")]
    for o in opps:
        for en_k, zh_k in pairs:
            en = (o.get(en_k) or "").strip()
            if en and o.get(zh_k):
                covered.add(en)
    return covered


def translate_batch(client, strings: list) -> dict:
    prompt = (
        "Translate every string below into Simplified Chinese. Return a JSON object "
        "whose keys are the EXACT input strings and whose values are the translations.\n\n"
        + json.dumps(strings, ensure_ascii=False, indent=2)
    )
    resp = client.messages.create(
        model=MODEL, max_tokens=8000, system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = resp.content[0].text.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
    a, b = raw.find("{"), raw.rfind("}")
    if a != -1 and b != -1:
        raw = raw[a:b + 1]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return json.loads(repair_json(raw))


def run(base: str):
    cache = load_cache()
    zh = cache.setdefault("zh", {})

    strings: set = set()
    for path in ("/api/saffron", "/api/career_strategy"):
        collect_strings(fetch(base, path), strings)

    skip = opp_covered()
    todo = sorted(s for s in strings if s not in zh and s not in skip)
    print(f"strings seen: {len(strings)} | already cached: {len(zh)} | "
          f"opp-covered: {len(skip)} | to translate: {len(todo)}")
    if not todo:
        print("Nothing to translate.")
        return

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    done = errors = 0
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        n = i // BATCH + 1
        total = (len(todo) + BATCH - 1) // BATCH
        print(f"  batch {n}/{total} ({len(batch)})...", end=" ", flush=True)
        try:
            result = translate_batch(client, batch)
            for en in batch:
                v = result.get(en)
                if isinstance(v, str) and v.strip():
                    zh[en] = v.strip()
            done += len(batch)
            print(f"ok ({done}/{len(todo)})")
        except anthropic.RateLimitError:
            print("rate limited — 30s"); time.sleep(30)
            errors += 1
        except Exception as e:
            print(f"ERROR: {e}"); errors += 1; time.sleep(2)
        save_cache(cache)   # save after every batch

    print(f"\nDone. {done} translated, {errors} batch errors. Cache: {CACHE}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--api", default="https://twilightdreamworks.com",
                    help="Base URL of the running API to pull payload strings from")
    run(ap.parse_args().api)
