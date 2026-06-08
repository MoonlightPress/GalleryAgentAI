"""
content_translation_engine.py

Translates opportunity card content into Simplified Chinese AND Japanese.
Adds name_zh, one_sentence_zh, why_it_fits_zh, three_bullets_zh (Chinese)
and  name_ja, one_sentence_ja, why_it_fits_ja, three_bullets_ja (Japanese)
to every entry in deploy_data/compact_opportunities.json.

Uses claude-sonnet-4-6 in batches of 8 for quality.
Saves progress after every batch — safe to re-run if interrupted.
Skips entries that already have all eight _zh/_ja fields populated.
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


def needs_translation(opp: dict) -> bool:
    return not all(opp.get(f) for f in ALL_FIELDS)


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
            raw = resp.content[0].text.strip()
            # Strip markdown fences if present
            if raw.startswith("```"):
                lines = raw.split("\n")
                raw = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
            # Extract array portion and repair any JSON formatting issues
            start_idx = raw.find("[")
            end_idx = raw.rfind("]")
            if start_idx != -1 and end_idx != -1:
                raw = raw[start_idx:end_idx + 1]
            try:
                results = json.loads(raw)
            except json.JSONDecodeError:
                results = json.loads(repair_json(raw))
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
                raw = resp.content[0].text.strip()
                if raw.startswith("```"):
                    lines = raw.split("\n")
                    raw = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
                results = json.loads(raw)
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
    run()
