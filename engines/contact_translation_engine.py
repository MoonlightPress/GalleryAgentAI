"""
contact_translation_engine.py

Translates CRM contact prose into Simplified Chinese AND Japanese, writing
`<field>_zh` / `<field>_ja` siblings back onto memory/contact_memory.json.

These are the strings the React "people to reach out to" section
(RelationshipTargets) renders: why_relevant, notes, and the crm_analysis
prose (contact_summary, next_action, follow_up_timing, risk_notes). Without
this step those fields render English in 中文 / 日本語 mode.

Mirrors content_translation_engine: claude-sonnet-4-6, batched, incremental
(skips fields that already have both _zh and _ja), saves after every batch so
it is safe to re-run. Run it in the translation phase of the pipeline, after
any engine that (re)writes contact prose.

The translations are derived data — this engine is the rule that regenerates
them. Deleting the _zh/_ja fields and re-running reproduces them, so a
from-scratch pipeline run yields fully-translated contacts.

Usage:  python engines/contact_translation_engine.py
"""

import sys
import json
import os
import time
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from json_repair import repair_json

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

CONTACTS = ROOT / "memory" / "contact_memory.json"
MODEL = "claude-sonnet-4-6"
BATCH = 16   # unique strings per request

# Top-level contact prose fields, and the nested crm_analysis prose fields.
TOP_FIELDS = ["why_relevant", "notes", "personal_note"]
CA_FIELDS = ["contact_summary", "next_action", "follow_up_timing", "risk_notes"]

SYSTEM = (
    "You are a professional translator for an art-career app used by a Chinese "
    "watercolor painter. Translate each English CRM note about a gallery / venue / "
    "contact into BOTH natural, concise Simplified Chinese (简体中文) AND Japanese "
    "(日本語).\n"
    "Rules:\n"
    "- Address the artist as 你 (Chinese) / second person; never 她/他.\n"
    "- Preserve proper nouns (gallery / venue / organisation / prize names, person "
    "names, @handles, URLs) exactly as written — do not translate or transliterate.\n"
    "- Keep dates, numbers and prices intact; translate only the words around them.\n"
    "- Match the original length and tone. No added commentary.\n"
    "- Return ONLY a JSON object mapping each EXACT input string to an object "
    '{"zh": "…", "ja": "…"}.'
)


def load_contacts():
    data = json.loads(CONTACTS.read_text(encoding="utf-8"))
    contacts = data.get("contacts", []) if isinstance(data, dict) else data
    return data, contacts


def save(data, contacts):
    out = contacts if isinstance(data, list) else {**data, "contacts": contacts}
    CONTACTS.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")


import re as _re
_WORD = _re.compile(r"[A-Za-z]{2,}")


def is_english(s) -> bool:
    """True when the string contains an English *phrase* worth translating.

    Counts a run of >=3 Latin words so mixed strings — English prose around a
    CJK proper noun, e.g. "Research ZINEフェス東京's booth costs" — are caught,
    while a bare two-word proper noun ("LOCAL Gallery") is left alone. The
    translator is instructed to preserve the embedded proper nouns verbatim.
    """
    if not isinstance(s, str):
        return False
    s = s.strip()
    if len(s) < 2 or s.startswith("http"):
        return False
    return len(_WORD.findall(s)) >= 3


def iter_targets(contacts):
    """Yield (holder_dict, field) for every translatable prose field."""
    for c in contacts:
        for f in TOP_FIELDS:
            yield c, f
        ca = c.get("crm_analysis")
        if isinstance(ca, dict):
            for f in CA_FIELDS:
                yield ca, f


def collect_pending(contacts) -> list[str]:
    pending: set[str] = set()
    for holder, field in iter_targets(contacts):
        en = (holder.get(field) or "").strip() if isinstance(holder.get(field), str) else ""
        if not is_english(en):
            continue
        if holder.get(field + "_zh") and holder.get(field + "_ja"):
            continue   # already translated
        pending.add(en)
    return sorted(pending)


def translate_batch(client, strings: list[str]) -> dict:
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


def apply_translations(contacts, table: dict):
    """Write _zh/_ja siblings wherever the English source matches a translated key."""
    for holder, field in iter_targets(contacts):
        en = (holder.get(field) or "").strip() if isinstance(holder.get(field), str) else ""
        tr = table.get(en)
        if not isinstance(tr, dict):
            continue
        if tr.get("zh"):
            holder[field + "_zh"] = tr["zh"].strip()
        if tr.get("ja"):
            holder[field + "_ja"] = tr["ja"].strip()


def run():
    data, contacts = load_contacts()
    pending = collect_pending(contacts)
    print(f"Contacts: {len(contacts)} | unique strings to translate: {len(pending)}")
    if not pending:
        print("All contact prose already translated.")
        return

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    table: dict = {}
    done = errors = 0
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
        # Apply + save after every batch so an interruption keeps progress.
        apply_translations(contacts, table)
        save(data, contacts)

    print(f"\nDone. {done} strings translated, {errors} batch errors. -> {CONTACTS}")


if __name__ == "__main__":
    run()
