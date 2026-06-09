"""
batch_translate_names.py

Batch-translates Japanese/Chinese opportunity names to short English names
and saves them as `name_en` on entries in deploy_data/compact_opportunities.json.

Source:  memory/needs_translation.json
Target:  deploy_data/compact_opportunities.json
Model:   claude-haiku-4-5-20251001
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import json
import re
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Resolve paths — works whether run from project root or worktree
# ---------------------------------------------------------------------------
def _find_root() -> Path:
    """Return the directory that contains both memory/ and deploy_data/."""
    candidates = [
        Path(__file__).resolve().parents[2],        # worktree root (scripts/patches -> root)
        Path.cwd(),                                  # wherever we were invoked from
        Path("C:/ScottStuff/GalleryAgentAI"),        # hard fallback
    ]
    for p in candidates:
        if (p / "deploy_data" / "compact_opportunities.json").exists():
            return p
    raise FileNotFoundError("Cannot locate project root with deploy_data/compact_opportunities.json")

def _find_needs_translation() -> Path:
    """
    needs_translation.json may live in the project root memory/ OR the worktree memory/.
    Search common locations.
    """
    candidates = [
        Path(__file__).resolve().parents[2] / "memory" / "needs_translation.json",
        Path.cwd() / "memory" / "needs_translation.json",
        Path("C:/ScottStuff/GalleryAgentAI") / "memory" / "needs_translation.json",
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError("Cannot locate memory/needs_translation.json")

PROJECT_ROOT = _find_root()
NEEDS_TRANSLATION_PATH = _find_needs_translation()
COMPACT_PATH = PROJECT_ROOT / "deploy_data" / "compact_opportunities.json"
BATCH_SIZE = 20
MODEL = "claude-haiku-4-5-20251001"

print(f"Project root:         {PROJECT_ROOT}", flush=True)
print(f"needs_translation at: {NEEDS_TRANSLATION_PATH}", flush=True)
print(f"compact at:           {COMPACT_PATH}", flush=True)

# ---------------------------------------------------------------------------
# Load .env (try project root first, then worktree root)
# ---------------------------------------------------------------------------
try:
    from dotenv import load_dotenv
    for env_path in [
        PROJECT_ROOT / ".env",
        Path("C:/ScottStuff/GalleryAgentAI") / ".env",
    ]:
        if env_path.exists():
            load_dotenv(env_path)
            break
except ImportError:
    pass

api_key = os.environ.get("ANTHROPIC_API_KEY", "")
if not api_key:
    print("ERROR: ANTHROPIC_API_KEY not set.", flush=True)
    sys.exit(1)

import anthropic
client = anthropic.Anthropic(api_key=api_key)

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
with open(NEEDS_TRANSLATION_PATH, encoding="utf-8") as f:
    needs = json.load(f)

with open(COMPACT_PATH, encoding="utf-8") as f:
    compact = json.load(f)

print(f"Needs translation: {len(needs)} entries", flush=True)
print(f"Compact opportunities: {len(compact)} entries", flush=True)

# ---------------------------------------------------------------------------
# Build lookup structures for compact_opportunities
# ---------------------------------------------------------------------------
title_index: dict[str, int] = {}  # title_lower -> list index
name_index: dict[str, int] = {}   # name_lower -> list index

for i, o in enumerate(compact):
    t = (o.get("title") or "").strip()
    n = (o.get("name") or "").strip()
    if t:
        title_index[t.lower()] = i
    if n and n.lower() != t.lower():
        name_index[n.lower()] = i

# ---------------------------------------------------------------------------
# Call Claude in batches
# ---------------------------------------------------------------------------
def translate_batch(batch: list[dict]) -> dict[int, str]:
    """
    Returns mapping: local index (0-based within batch) -> name_en string.
    """
    items_text = "\n".join(
        f"{i+1}. name: {entry['name']}"
        + (f" | context: {entry['one_sentence'][:120]}" if entry.get('one_sentence') else "")
        for i, entry in enumerate(batch)
    )

    prompt = (
        f"You are translating Japanese and Chinese opportunity/exhibition names into short, natural English names.\n\n"
        f"Rules:\n"
        f"- 2–6 words each\n"
        f"- Natural English, not literal translation — capture the spirit and type of opportunity\n"
        f"- Use common sense abbreviations (e.g. \"Japan Watercolor Exhibition\" not "
        f"\"The 113th Annual Exhibition of the Japan Watercolor Painting Society\")\n"
        f"- For grant programs, use \"<Org> Grant\" or \"<Org> Fellowship\"\n"
        f"- For open calls/exhibitions, use \"<Theme> Open Call\" or \"<Venue> Exhibition\"\n"
        f"- For art fairs/zine fests, use \"<Name> Art Fair\" or \"<Name> Zine Fair\"\n"
        f"- For residencies, use \"<Org> Residency\"\n"
        f"- If the name already contains a clear English title, extract/abbreviate it\n"
        f"- Return ONLY a JSON array of {len(batch)} strings, one per item, in the same order\n\n"
        f"Items:\n{items_text}\n\n"
        f"Return ONLY the JSON array, no extra text."
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()

    # Strip markdown code fences if present
    raw = re.sub(r'^```json\s*', '', raw)
    raw = re.sub(r'^```\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)
    raw = raw.strip()

    try:
        arr = json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r'\[.*\]', raw, re.DOTALL)
        if m:
            try:
                arr = json.loads(m.group())
            except json.JSONDecodeError:
                arr = []
        else:
            arr = []

    if not arr:
        print(f"\n  WARNING: Could not parse JSON from response: {raw[:200]}", flush=True)
        arr = [""] * len(batch)

    if len(arr) != len(batch):
        print(f"\n  WARNING: Got {len(arr)} translations for {len(batch)} items", flush=True)
        # Pad or truncate
        arr = arr[:len(batch)] + [""] * max(0, len(batch) - len(arr))

    return {i: str(name_en) for i, name_en in enumerate(arr)}


# ---------------------------------------------------------------------------
# Process all batches and build name->name_en map
# All ids are empty, so we key by the `name` field
# ---------------------------------------------------------------------------
name_to_en: dict[str, str] = {}  # entry['name'] -> name_en

total_batches = (len(needs) + BATCH_SIZE - 1) // BATCH_SIZE
print(f"\nProcessing {len(needs)} entries in {total_batches} batches of {BATCH_SIZE}...\n", flush=True)

for batch_num in range(total_batches):
    start = batch_num * BATCH_SIZE
    end = min(start + BATCH_SIZE, len(needs))
    batch = needs[start:end]

    print(f"Batch {batch_num + 1}/{total_batches} (items {start+1}–{end})...", end=" ", flush=True)

    translations = translate_batch(batch)

    for i, entry in enumerate(batch):
        en = translations.get(i, "").strip()
        if en:
            name_to_en[entry["name"]] = en

    got = sum(1 for v in translations.values() if str(v).strip())
    print(f"got {got} translations", flush=True)

    # Small delay to avoid rate limits
    if batch_num < total_batches - 1:
        time.sleep(0.5)

print(f"\nTotal translations obtained: {len(name_to_en)}", flush=True)

# ---------------------------------------------------------------------------
# Apply name_en to compact_opportunities.json
# ---------------------------------------------------------------------------
applied = 0
skipped_existing = 0
no_match = 0
unmatched_names = []

for needs_entry in needs:
    src_name = needs_entry["name"]
    name_en = name_to_en.get(src_name, "").strip()
    if not name_en:
        continue

    matched_idx = None

    # 1. Exact match on title (case-insensitive)
    idx = title_index.get(src_name.lower())
    if idx is not None:
        matched_idx = idx

    # 2. Exact match on name (case-insensitive)
    if matched_idx is None:
        idx = name_index.get(src_name.lower())
        if idx is not None:
            matched_idx = idx

    # 3. Substring match: src contained in title/name or title/name contained in src
    if matched_idx is None:
        src_lower = src_name.lower()
        for i, o in enumerate(compact):
            t = (o.get("title") or "").strip().lower()
            n = (o.get("name") or "").strip().lower()
            # Require at least 10 chars to avoid false positives on short strings
            if t and len(t) >= 10 and (t in src_lower or src_lower in t):
                matched_idx = i
                break
            if n and len(n) >= 10 and (n in src_lower or src_lower in n):
                matched_idx = i
                break

    if matched_idx is None:
        no_match += 1
        unmatched_names.append(src_name)
        continue

    # Skip if name_en already set (don't overwrite existing values)
    existing = compact[matched_idx].get("name_en", "").strip()
    if existing:
        skipped_existing += 1
        continue

    compact[matched_idx]["name_en"] = name_en
    applied += 1

# ---------------------------------------------------------------------------
# Write back
# ---------------------------------------------------------------------------
with open(COMPACT_PATH, "w", encoding="utf-8") as f:
    json.dump(compact, f, ensure_ascii=False, indent=2)

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
print(f"\n--- Results ---", flush=True)
print(f"  name_en set:           {applied}", flush=True)
print(f"  skipped (had name_en): {skipped_existing}", flush=True)
print(f"  no match in compact:   {no_match}", flush=True)
if unmatched_names:
    print(f"\n  Unmatched needs_translation entries:", flush=True)
    for n in unmatched_names[:20]:
        print(f"    - {n[:80]}", flush=True)
    if len(unmatched_names) > 20:
        print(f"    ... and {len(unmatched_names) - 20} more", flush=True)

# Verification read
with open(COMPACT_PATH, encoding="utf-8") as f:
    verify = json.load(f)
has_name_en = sum(1 for o in verify if o.get("name_en", "").strip())
print(f"\n  Compact entries with name_en now: {has_name_en} / {len(verify)}", flush=True)
print("Done.", flush=True)
