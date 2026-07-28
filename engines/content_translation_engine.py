"""
content_translation_engine.py

Translates opportunity card content into Simplified Chinese AND Japanese.
Adds name_zh, one_sentence_zh, why_it_fits_zh, three_bullets_zh (Chinese)
and  name_ja, one_sentence_ja, why_it_fits_ja, three_bullets_ja (Japanese)
to every entry in deploy_data/compact_opportunities.json.

Uses claude-sonnet-4-6, chunks of 8 for quality.
Skips entries that already have all eight _zh/_ja fields populated.

2026-07-28: converted to the Message Batches API (50% of standard pricing).
Translation is the dominant Claude spend of a full pipeline run and is
perfectly latency-insensitive (it runs at the end of a monthly unattended
pipeline), so the batch discount is free money. Mechanics:
  - all chunks are submitted as ONE batch, then polled until it ends;
  - the batch id is persisted to memory/pending_translation_batch.json
    BEFORE polling, so a killed or timed-out run can fetch the already-
    paid-for results on its next invocation instead of re-buying them;
  - results are applied by ITEM id (apply_batch), never chunk position,
    so fetching against a later, shifted opportunity list is safe;
  - a poll timeout is a warning, not a failure — the pipeline's remaining
    steps continue, and the pending file carries the batch forward.
Run with --sync to use the old sequential path (full price; for debugging).
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
load_dotenv(Path(__file__).parent.parent / ".env")

ROOT = Path(__file__).parent.parent
# Engines run as scripts (python engines/x.py), where sys.path[0] is engines/,
# not the repo root — required for `from engines.anthropic_batch import ...`.
sys.path.insert(0, str(ROOT))
COMPACT = ROOT / "deploy_data" / "compact_opportunities.json"

ZH_FIELDS = ["name_zh", "one_sentence_zh", "why_it_fits_zh", "three_bullets_zh"]
JA_FIELDS = ["name_ja", "one_sentence_ja", "why_it_fits_ja", "three_bullets_ja"]
ALL_FIELDS = ZH_FIELDS + JA_FIELDS

BATCH = 8
MODEL = "claude-sonnet-4-6"

SYSTEM = (
    "You are a professional translator specializing in art-world content. "
    "Translate artist career opportunity descriptions from English or Japanese "
    "into BOTH Simplified Chinese (简体中文) AND Japanese (日本語).\n"
    "Rules:\n"
    "- Preserve proper nouns (gallery names, venue names, prize names) faithfully.\n"
    "- For Japanese translations: if the opportunity name is already in Japanese, "
    "  keep it as-is for name_ja. Translate only English portions.\n"
    "- Keep translations concise — match the original length and tone.\n"
    "- three_bullets_zh and three_bullets_ja must be JSON arrays with the same "
    "  number of items as the input three_bullets.\n"
    "- Return ONLY a valid JSON array, no markdown, no explanation."
)


# Target field -> how its SOURCE value is read (mirrors build_prompt).
_SOURCE_OF = {
    "name":          lambda o: o.get("name") or o.get("title") or "",
    "one_sentence":  lambda o: o.get("one_sentence") or "",
    "why_it_fits":   lambda o: o.get("why_it_fits") or o.get("why_this_fits_short") or "",
    "three_bullets": lambda o: o.get("three_bullets") or [],
}


def needs_translation(opp: dict) -> bool:
    """A field needs translation only if its SOURCE is non-empty. Requiring
    all 8 target fields unconditionally made entries with empty source bullets
    permanently 'pending' — 402 of 801 live entries were being re-submitted
    (and re-paid) on every pipeline run with nothing left to translate."""
    for base, source in _SOURCE_OF.items():
        if not source(opp):
            continue  # nothing to translate for this field
        if not opp.get(base + "_zh") or not opp.get(base + "_ja"):
            return True
    return False


def build_prompt(batch: list[dict]) -> str:
    items = []
    for o in batch:
        items.append({
            "id":            o.get("id") or o.get("title") or o.get("name") or "",
            "name":          o.get("name") or o.get("title") or "",
            "one_sentence":  o.get("one_sentence") or "",
            "why_it_fits":   o.get("why_it_fits") or o.get("why_this_fits_short") or "",
            "three_bullets": o.get("three_bullets") or [],
        })
    return (
        "Translate all records below into both Simplified Chinese and Japanese.\n"
        "Return a JSON array. Each element must have exactly these keys:\n"
        "  id, name_zh, one_sentence_zh, why_it_fits_zh, three_bullets_zh,\n"
        "  name_ja, one_sentence_ja, why_it_fits_ja, three_bullets_ja\n"
        "If a source field is empty, return an empty string or empty array.\n\n"
        f"{json.dumps(items, ensure_ascii=False, indent=2)}"
    )


def parse_response_text(raw: str) -> list[dict]:
    """Model text -> list of translated records. Tolerates markdown fences,
    surrounding prose, and mildly broken JSON (via json_repair)."""
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
    start_idx = raw.find("[")
    end_idx = raw.rfind("]")
    if start_idx != -1 and end_idx != -1:
        raw = raw[start_idx:end_idx + 1]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return json.loads(repair_json(raw))


def build_requests(pending: list[dict], chunk_size: int = BATCH) -> list[dict]:
    """Chunk the pending list into Message Batches requests. custom_ids are
    positional labels for logging only — application is by item id."""
    requests = []
    for start in range(0, len(pending), chunk_size):
        chunk = pending[start:start + chunk_size]
        requests.append({
            "custom_id": f"translate-chunk-{start // chunk_size:04d}",
            "params": {
                "model": MODEL,
                "max_tokens": 6000,
                "system": SYSTEM,
                "messages": [{"role": "user", "content": build_prompt(chunk)}],
            },
        })
    return requests


def apply_batch(opps: list[dict], by_id: dict, results: list[dict]):
    for r in results:
        rid = r.get("id", "")
        idx = by_id.get(rid)
        if idx is None:
            continue
        opp = opps[idx]
        for field in ALL_FIELDS:
            val = r.get(field)
            if val is not None and val != "" and val != []:
                opp[field] = val


PENDING_PATH = ROOT / "memory" / "pending_translation_batch.json"


def run_batched(client=None, compact_path=COMPACT, pending_path=PENDING_PATH,
                poll_interval=60, max_wait=75 * 60):
    """Batch-API translation pass. See module docstring for the design."""
    from engines.anthropic_batch import (
        read_pending, submit_or_resume, wait_for_batch,
        iter_succeeded_texts, clear_pending)

    with open(compact_path, encoding="utf-8") as f:
        opps = json.load(f)

    by_id: dict = {}
    for idx, o in enumerate(opps):
        oid = o.get("id") or o.get("title") or o.get("name") or ""
        if oid:
            by_id[oid] = idx

    pending = [o for o in opps if needs_translation(o)]
    print(f"Entries needing translation: {len(pending)} of {len(opps)}")

    if not pending and not read_pending(pending_path):
        print("All entries already translated.")
        return

    if client is None:
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    batch_id = submit_or_resume(client, build_requests(pending), pending_path)
    if not wait_for_batch(client, batch_id, pending_path, poll_interval, max_wait):
        return  # timeout — pending file carries the batch to the next run

    applied = 0
    errored = 0
    for custom_id, text in iter_succeeded_texts(client, batch_id):
        try:
            apply_batch(opps, by_id, parse_response_text(text))
            applied += 1
        except (json.JSONDecodeError, ValueError) as exc:
            errored += 1
            print(f"  {custom_id}: unparseable response ({exc})")

    with open(compact_path, "w", encoding="utf-8") as f:
        json.dump(opps, f, ensure_ascii=False, indent=2)

    if errored == 0:
        clear_pending(pending_path)

    still = sum(1 for o in opps if needs_translation(o))
    print(f"\nDone. {applied} chunk(s) applied, {errored} errored. "
          f"{still} entries still untranslated.")
    print(f"Saved to {compact_path}")


def run():
    with open(COMPACT, encoding="utf-8") as f:
        opps = json.load(f)

    # Build id lookup (id > title > name)
    by_id: dict = {}
    for idx, o in enumerate(opps):
        oid = o.get("id") or o.get("title") or o.get("name") or ""
        if oid:
            by_id[oid] = idx

    pending = [o for o in opps if needs_translation(o)]
    total = len(pending)
    print(f"Entries needing translation: {total} of {len(opps)}")

    if total == 0:
        print("All entries already translated.")
        return

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    done = 0
    errors = 0

    for start in range(0, total, BATCH):
        batch = pending[start:start + BATCH]
        batch_num = start // BATCH + 1
        total_batches = (total + BATCH - 1) // BATCH
        print(f"  Batch {batch_num}/{total_batches} ({len(batch)} entries)...", end=" ", flush=True)

        prompt = build_prompt(batch)
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=6000,
                system=SYSTEM,
                messages=[{"role": "user", "content": prompt}],
            )
            results = parse_response_text(resp.content[0].text)
            apply_batch(opps, by_id, results)
            done += len(batch)
            print(f"ok ({done}/{total})")
        except json.JSONDecodeError as e:
            errors += 1
            print(f"JSON ERROR: {e}")
            time.sleep(2)
        except anthropic.RateLimitError:
            print("rate limited — waiting 30s")
            time.sleep(30)
            # Retry once
            try:
                resp = client.messages.create(
                    model=MODEL,
                    max_tokens=6000,
                    system=SYSTEM,
                    messages=[{"role": "user", "content": prompt}],
                )
                results = parse_response_text(resp.content[0].text)
                apply_batch(opps, by_id, results)
                done += len(batch)
                print(f"  retry ok ({done}/{total})")
            except Exception as e2:
                errors += 1
                print(f"  retry failed: {e2}")
        except Exception as e:
            errors += 1
            print(f"ERROR: {e}")
            time.sleep(2)

        # Save progress after every batch
        with open(COMPACT, "w", encoding="utf-8") as f:
            json.dump(opps, f, ensure_ascii=False, indent=2)

    print(f"\nDone. {done} translated, {errors} batch errors.")
    print(f"Saved to {COMPACT}")


if __name__ == "__main__":
    if "--sync" in sys.argv:
        run()  # old sequential path — full price; kept for debugging
    else:
        run_batched()
