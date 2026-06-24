"""
opp_strategy_translation_engine.py

Translates the opportunity *strategy prose* that content_translation_engine does
not cover — relationship_note, submission_strategy, recommended_body_of_work and
quick_action — into Simplified Chinese AND Japanese, writing `<field>_zh` /
`<field>_ja` siblings onto deploy_data/compact_opportunities.json.

These are the strings the React press cards (OpportunitiesSection) and the
opportunity detail panel render. Without this step they show English in 中文 /
日本語 mode.

Per-field incremental: only translates a field that has English text and is
missing its _zh/_ja sibling, so it never re-translates the core card fields
(name/one_sentence/why_it_fits/three_bullets — those are content_translation_
engine's job). Batched, saves after every batch, safe to re-run.

The translations are derived data — this engine is the rule that regenerates
them. Run it in the translation phase of the pipeline, after
content_translation_engine.

Usage:  python engines/opp_strategy_translation_engine.py
"""

import sys
import json
import os
import re
import time
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from json_repair import repair_json

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

COMPACT = ROOT / "deploy_data" / "compact_opportunities.json"
MODEL = "claude-sonnet-4-6"
BATCH = 16   # unique strings per request

FIELDS = ["relationship_note", "submission_strategy", "recommended_body_of_work", "quick_action"]

SYSTEM = (
    "You are a professional translator for an art-career app used by a Chinese "
    "watercolor painter. Translate each English strategy note about a gallery / "
    "venue / publication / opportunity into BOTH natural, concise Simplified "
    "Chinese (简体中文) AND Japanese (日本語).\n"
    "Rules:\n"
    "- Address the artist as 你 (Chinese) / second person; never 她/他.\n"
    "- Preserve proper nouns (gallery / venue / organisation / prize names, person "
    "names, @handles, URLs, emails, phone numbers, hashtags) exactly as written — "
    "do not translate or transliterate them.\n"
    "- Keep dates, numbers and prices intact; translate only the words around them.\n"
    "- Match the original length and tone. No added commentary.\n"
    "- Return ONLY a JSON object mapping each EXACT input string to an object "
    '{"zh": "…", "ja": "…"}.'
)

_WORD = re.compile(r"[A-Za-z]{2,}")


def is_english(s) -> bool:
    if not isinstance(s, str):
        return False
    s = s.strip()
    if len(s) < 2 or s.startswith("http"):
        return False
    return len(_WORD.findall(s)) >= 3


def load_opps():
    data = json.loads(COMPACT.read_text(encoding="utf-8"))
    opps = data if isinstance(data, list) else data.get("items", data.get("opportunities", []))
    return data, opps


def save(data, opps):
    if isinstance(data, list):
        COMPACT.write_text(json.dumps(opps, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        COMPACT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def collect_pending(opps) -> list:
    pending = set()
    for o in opps:
        for f in FIELDS:
            v = o.get(f)
            if is_english(v) and not (o.get(f + "_zh") and o.get(f + "_ja")):
                pending.add(v.strip())
    return sorted(pending)


def translate_batch(client, strings):
    prompt = (
        "Translate every string below into Simplified Chinese and Japanese. Return a "
        'JSON object whose keys are the EXACT input strings and whose values are '
        '{"zh": "…", "ja": "…"} objects.\n\n'
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


def apply_translations(opps, table):
    for o in opps:
        for f in FIELDS:
            v = o.get(f)
            if not is_english(v):
                continue
            tr = table.get(v.strip())
            if not isinstance(tr, dict):
                continue
            if tr.get("zh"):
                o[f + "_zh"] = tr["zh"].strip()
            if tr.get("ja"):
                o[f + "_ja"] = tr["ja"].strip()


def run():
    data, opps = load_opps()
    pending = collect_pending(opps)
    print(f"Opportunities: {len(opps)} | unique strategy strings to translate: {len(pending)}")
    if not pending:
        print("All opportunity strategy prose already translated.")
        return

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    table, done, errors = {}, 0, 0
    total_batches = (len(pending) + BATCH - 1) // BATCH
    for i in range(0, len(pending), BATCH):
        batch = pending[i:i + BATCH]
        n = i // BATCH + 1
        print(f"  batch {n}/{total_batches} ({len(batch)})...", end=" ", flush=True)
        try:
            result = translate_batch(client, batch)
            for en in batch:
                v = result.get(en)
                if isinstance(v, dict):
                    table[en] = v
            done += len(batch)
            print(f"ok ({done}/{len(pending)})")
        except anthropic.RateLimitError:
            print("rate limited — 30s"); time.sleep(30); errors += 1; continue
        except Exception as e:
            print(f"ERROR: {e}"); errors += 1; time.sleep(2); continue
        apply_translations(opps, table)
        save(data, opps)

    print(f"\nDone. {done} strings translated, {errors} batch errors. -> {COMPACT}")


if __name__ == "__main__":
    run()
