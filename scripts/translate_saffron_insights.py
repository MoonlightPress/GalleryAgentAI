#!/usr/bin/env python3
"""
Translate saffron_insights.js content fields.
Produces saffron_insights_i18n.json with _zh/_ja fields added to every text entry.
"""
import sys, os, json, re, subprocess, tempfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = "claude-sonnet-4-6"

JS_PATH  = Path('C:/ScottStuff/GalleryAgentAI/frontend/src/data/saffron_insights.js')
OUT_PATH = Path('C:/ScottStuff/GalleryAgentAI/frontend/src/data/saffron_insights_i18n.json')

# ── Extract data from ES module JS file ───────────────────────────────────────

def extract_data():
    code = JS_PATH.read_text(encoding='utf-8')
    modified = code.replace('export const ', 'let ').replace('export default ', 'let _default_ = ')
    mjs = f"""
import {{ readFileSync }} from 'fs';
const _code = {json.dumps(modified)};
const _fn = new Function('module', 'exports', _code + '\\nmodule.LICENSING_LANDSCAPE=LICENSING_LANDSCAPE;module.PRESS_PITCH_MAP=PRESS_PITCH_MAP;module.GRANT_LANDSCAPE=GRANT_LANDSCAPE;module.REVENUE_STREAMS=REVENUE_STREAMS;module.CAREER_DEPENDENCY_MAP=CAREER_DEPENDENCY_MAP;');
const _ctx = {{}};
_fn(_ctx, {{}});
console.log(JSON.stringify(_ctx));
"""
    with tempfile.NamedTemporaryFile(suffix='.mjs', mode='w', delete=False, encoding='utf-8') as f:
        f.write(mjs)
        tmp = f.name
    try:
        result = subprocess.run(['node', tmp], capture_output=True, timeout=15)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.decode('utf-8', errors='replace')[:400])
        return json.loads(result.stdout.decode('utf-8'))
    finally:
        os.unlink(tmp)

# ── Translation helpers ───────────────────────────────────────────────────────

def translate_batch(texts: list[str]) -> tuple[list[str], list[str]]:
    if not texts:
        return [], []
    numbered = "\n".join(f"{i+1}. {t}" for i, t in enumerate(texts))
    prompt = f"""You are translating UI text for an artist career system about a Chinese watercolor artist in Tokyo.

Translate each numbered English string to Simplified Chinese (zh) and Japanese (ja).
- Keep proper nouns (gallery/brand/magazine names, city names) as-is
- Keep Instagram handles, URLs, currency amounts (¥xxx) as-is
- Be natural and professional in both target languages
- For Japanese, prefer hiragana/kanji over katakana for common words

Respond ONLY with JSON:
{{"translations": [{{"zh": "...", "ja": "..."}}, ...]}}

Strings:
{numbered}"""

    msg = client.messages.create(model=MODEL, max_tokens=4096,
                                  messages=[{"role": "user", "content": prompt}])
    raw = msg.content[0].text.strip()
    m = re.search(r'\{[\s\S]*\}', raw)
    if not m:
        raise ValueError(f"No JSON: {raw[:200]}")
    try:
        result = json.loads(m.group())
    except json.JSONDecodeError:
        try:
            from json_repair import repair_json
            result = json.loads(repair_json(m.group()))
        except Exception as e:
            raise ValueError(f"JSON parse failed: {e}\n{raw[:400]}")

    translations = result['translations']
    return [t['zh'] for t in translations], [t['ja'] for t in translations]

def add_i18n_to_objects(objects: list, fields: list, label: str = ''):
    total = 0
    all_texts, field_map = [], []
    for i, obj in enumerate(objects):
        for f in fields:
            v = obj.get(f)
            if v and isinstance(v, str) and not obj.get(f + '_zh'):
                all_texts.append(v)
                field_map.append((i, f))
    if not all_texts:
        return 0
    BATCH = 20
    for s in range(0, len(all_texts), BATCH):
        bt = all_texts[s:s+BATCH]
        bm = field_map[s:s+BATCH]
        zh, ja = translate_batch(bt)
        for k, (oi, f) in enumerate(bm):
            objects[oi][f + '_zh'] = zh[k]
            objects[oi][f + '_ja'] = ja[k]
            total += 1
        print(f"  {label}: {s+len(bt)}/{len(all_texts)}", flush=True)
    return total

def add_i18n_to_unlocks(objects: list):
    total = 0
    for obj in objects:
        ul = obj.get('unlocks', [])
        if ul and not obj.get('unlocks_zh'):
            zh, ja = translate_batch(ul)
            obj['unlocks_zh'] = zh
            obj['unlocks_ja'] = ja
            total += len(ul)
    return total

# ── Main ─────────────────────────────────────────────────────────────────────

print("Extracting data from saffron_insights.js...", flush=True)
data = extract_data()
print(f"Extracted {len(data)} structures: {list(data.keys())}", flush=True)

# Load existing translations if any
if OUT_PATH.exists():
    existing = json.loads(OUT_PATH.read_text(encoding='utf-8'))
    # Merge existing translations back so we don't retranslate
    # (Simple approach: just overwrite — retranslation is fast enough)

total = 0

print("\nLICENSING_LANDSCAPE...")
ll = data.get('LICENSING_LANDSCAPE', {})
for group in ll.get('items', []):
    total += add_i18n_to_objects([group], ['category'], 'group')
    total += add_i18n_to_objects(group.get('entries', []), ['note'], 'entry')

print("\nPRESS_PITCH_MAP...")
total += add_i18n_to_objects(
    data.get('PRESS_PITCH_MAP', {}).get('items', []),
    ['type', 'why_fits', 'how_to_pitch', 'timeline', 'category_note', 'how_discovered'],
    'press'
)

print("\nGRANT_LANDSCAPE...")
total += add_i18n_to_objects(
    data.get('GRANT_LANDSCAPE', {}).get('items', []),
    ['why_apply', 'eligibility', 'competition', 'tip', 'category_note', 'note'],
    'grant'
)

print("\nREVENUE_STREAMS...")
total += add_i18n_to_objects(
    data.get('REVENUE_STREAMS', {}).get('items', []),
    ['stream', 'description', 'pricing', 'why_now', 'action'],
    'revenue'
)

print("\nCAREER_DEPENDENCY_MAP...")
cdm = data.get('CAREER_DEPENDENCY_MAP', {})
for ms in cdm.get('milestones', []):
    total += add_i18n_to_objects([ms], ['label'], 'milestone')
    items = ms.get('items', [])
    total += add_i18n_to_objects(items, ['complete'], 'milestone_item')
    total += add_i18n_to_unlocks(items)

OUT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"\nDone. {total} fields translated → {OUT_PATH}")
