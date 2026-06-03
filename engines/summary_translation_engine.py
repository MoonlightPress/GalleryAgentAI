"""
Generates summary_zh and summary_ja for opportunities missing them.
Reads/writes deploy_data/compact_opportunities.json.
Run once; re-run is safe (skips already-translated entries).
"""
import json
import os
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
load_dotenv()

import anthropic

OPP_PATH = Path("deploy_data/compact_opportunities.json")
REPORT_PATH = Path("reports/summary_translation_report.md")
MODEL = "claude-haiku-4-5-20251001"
BATCH_SIZE = 20  # entries per API call


def load_opps():
    return json.loads(OPP_PATH.read_text(encoding="utf-8"))


def save_opps(opps):
    OPP_PATH.write_text(json.dumps(opps, indent=2, ensure_ascii=False), encoding="utf-8")


def needs_translation(opp):
    summary = (opp.get("one_sentence") or "").strip()
    if not summary:
        return False
    missing_zh = not (opp.get("summary_zh") or "").strip()
    missing_ja = not (opp.get("summary_ja") or "").strip()
    return missing_zh or missing_ja


def translate_batch(client, batch):
    """Translate a batch of (index, summary, name) tuples. Returns list of (index, zh, ja)."""
    items_text = "\n".join(
        f'{i}. [{item["name"]}] {item["summary"]}'
        for i, item in enumerate(batch)
    )

    prompt = f"""Translate each numbered opportunity summary below into Chinese (Simplified) and Japanese.

Rules:
- Keep translations concise — match the length of the English original
- Use natural, fluent language appropriate for an art/exhibition context
- Proper nouns (venue names, city names) can remain in English or use established kanji/hanzi
- Return ONLY a JSON array, no other text

Format:
[
  {{"zh": "Chinese translation", "ja": "Japanese translation"}},
  ...
]
(one object per numbered item, in the same order)

Items:
{items_text}"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```", 2)[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.rsplit("```", 1)[0].strip()

    translations = json.loads(raw)
    return translations


def main():
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    opps = load_opps()

    to_translate = [(i, o) for i, o in enumerate(opps) if needs_translation(o)]
    print(f"Opportunities needing translation: {len(to_translate)}")

    if not to_translate:
        print("Nothing to do.")
        return

    total_translated = 0
    lines = ["# Summary Translation Report", ""]

    for batch_start in range(0, len(to_translate), BATCH_SIZE):
        batch_indices = to_translate[batch_start : batch_start + BATCH_SIZE]
        batch = [
            {
                "idx": idx,
                "name": (opps[idx].get("name") or opps[idx].get("title") or "")[:60],
                "summary": (opps[idx].get("one_sentence") or "")[:200],
            }
            for idx, _ in batch_indices
        ]

        try:
            translations = translate_batch(client, batch)
        except Exception as e:
            print(f"  Batch {batch_start//BATCH_SIZE + 1} failed: {e}")
            continue

        for item, trans in zip(batch, translations):
            opp = opps[item["idx"]]
            zh = (trans.get("zh") or "").strip()
            ja = (trans.get("ja") or "").strip()
            if not opp.get("summary_zh"):
                opp["summary_zh"] = zh
            if not opp.get("summary_ja"):
                opp["summary_ja"] = ja
            total_translated += 1
            lines.append(f"- [{item['name']}]")
            lines.append(f"  EN: {item['summary'][:100]}")
            lines.append(f"  ZH: {zh[:100]}")
            lines.append(f"  JA: {ja[:100]}")
            lines.append("")

        save_opps(opps)
        print(f"  Batch {batch_start//BATCH_SIZE + 1}: translated {len(batch)} entries")

        if batch_start + BATCH_SIZE < len(to_translate):
            time.sleep(0.5)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nTranslated {total_translated} opportunities.")
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
