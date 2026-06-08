#!/usr/bin/env python3
"""
Merge saffron_insights_i18n.json translations back into saffron_insights.js in-place.
The result is a self-contained JS file with _zh/_ja fields baked into every entry.
No separate JSON file needed at runtime — translations are committed in the JS itself.
"""
import sys, os, json, re, subprocess, tempfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

JS_PATH   = Path('C:/ScottStuff/GalleryAgentAI/frontend/src/data/saffron_insights.js')
I18N_PATH = Path('C:/ScottStuff/GalleryAgentAI/frontend/src/data/saffron_insights_i18n.json')

if not I18N_PATH.exists():
    print("ERROR: saffron_insights_i18n.json not found. Run translate_saffron_insights.py first.")
    sys.exit(1)

translated = json.loads(I18N_PATH.read_text(encoding='utf-8'))

# ── Build a flat map: (structure_name, path_key) → {_zh, _ja} ────────────────
# We'll use node.js to reconstruct the JS with translations injected

def extract_translations_flat(data: dict) -> dict:
    """Walk translated data and build a lookup: value_en → {zh, ja}"""
    lookup = {}

    def walk(obj):
        if isinstance(obj, dict):
            keys = list(obj.keys())
            for k in keys:
                if k.endswith('_zh') or k.endswith('_ja'):
                    continue
                v = obj[k]
                v_zh = obj.get(k + '_zh')
                v_ja = obj.get(k + '_ja')
                if isinstance(v, str) and v_zh and v_ja:
                    lookup[v] = {'zh': v_zh, 'ja': v_ja}
                elif isinstance(v, list) and v_zh and v_ja:
                    # Array of strings (unlocks)
                    for i, item in enumerate(v):
                        if isinstance(item, str) and i < len(v_zh) and i < len(v_ja):
                            lookup[item] = {'zh': v_zh[i], 'ja': v_ja[i]}
                walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(data)
    return lookup

lookup = extract_translations_flat(translated)
print(f"Translation lookup entries: {len(lookup)}")

# ── Read and rewrite saffron_insights.js ─────────────────────────────────────
# Strategy: use node.js to parse the JS, inject translations, and regenerate it.
# This preserves the exact JS structure and avoids regex hacks on JS syntax.

inject_script = """
const fs = require('fs');
const vm = require('vm');
const lookup = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));

const jsText = fs.readFileSync(process.argv[3], 'utf8');
const modified = jsText
  .replace(/export const /g, 'let ')
  .replace(/export default /g, 'let _default_ = ');

const ctx = {};
const fn = new Function('module', 'exports', modified +
  '\\nmodule.LL=LICENSING_LANDSCAPE;module.PM=PRESS_PITCH_MAP;module.GL=GRANT_LANDSCAPE;module.RS=REVENUE_STREAMS;module.CDM=CAREER_DEPENDENCY_MAP;'
);
fn(ctx, {});

function injectTranslations(obj) {
  if (!obj || typeof obj !== 'object') return;
  if (Array.isArray(obj)) { obj.forEach(injectTranslations); return; }

  const keys = Object.keys(obj);
  keys.forEach(k => {
    if (k.endsWith('_zh') || k.endsWith('_ja')) return;
    const v = obj[k];
    if (typeof v === 'string' && lookup[v] && !obj[k + '_zh']) {
      obj[k + '_zh'] = lookup[v].zh;
      obj[k + '_ja'] = lookup[v].ja;
    } else if (Array.isArray(v) && lookup[v[0]] && !obj[k + '_zh']) {
      // string array (unlocks)
      obj[k + '_zh'] = v.map(s => (lookup[s] || {zh: s}).zh);
      obj[k + '_ja'] = v.map(s => (lookup[s] || {ja: s}).ja);
    }
    injectTranslations(v);
  });
}

injectTranslations(ctx.LL);
injectTranslations(ctx.PM);
injectTranslations(ctx.GL);
injectTranslations(ctx.RS);
injectTranslations(ctx.CDM);

// Write back to JS using JSON.stringify for each const
const out = [
  '// Structured insight content for Saffron\\'s five new sections.',
  '// Translations (_zh, _ja) are baked in — do not edit manually, run scripts/translate_saffron_insights.py',
  '',
  'export const LICENSING_LANDSCAPE = ' + JSON.stringify(ctx.LL, null, 2) + ';',
  '',
  'export const PRESS_PITCH_MAP = ' + JSON.stringify(ctx.PM, null, 2) + ';',
  '',
  'export const GRANT_LANDSCAPE = ' + JSON.stringify(ctx.GL, null, 2) + ';',
  '',
  'export const REVENUE_STREAMS = ' + JSON.stringify(ctx.RS, null, 2) + ';',
  '',
  'export const CAREER_DEPENDENCY_MAP = ' + JSON.stringify(ctx.CDM, null, 2) + ';',
].join('\\n');

process.stdout.write(out);
"""

# Write the inject script
with tempfile.NamedTemporaryFile(suffix='.cjs', mode='w', delete=False, encoding='utf-8') as f:
    f.write(inject_script)
    tmp = f.name

with tempfile.NamedTemporaryFile(suffix='.json', mode='w', delete=False, encoding='utf-8') as lf:
    json.dump(lookup, lf, ensure_ascii=False)
    lookup_path = lf.name

result = subprocess.run(
    ['node', tmp, lookup_path, str(JS_PATH)],
    capture_output=True,
    timeout=30,
    cwd='C:/ScottStuff/GalleryAgentAI'
)
os.unlink(lookup_path)
os.unlink(tmp)

if result.returncode != 0:
    print("Node error:", result.stderr.decode('utf-8', errors='replace')[:500])
    sys.exit(1)

new_js = result.stdout.decode('utf-8')
JS_PATH.write_text(new_js, encoding='utf-8')

# Count how many _zh fields are present
zh_count = new_js.count('_zh')
print(f"Wrote {JS_PATH.name} with {zh_count} _zh fields")

# Clean up the separate i18n JSON (no longer needed)
# I18N_PATH.unlink()
# print("Cleaned up saffron_insights_i18n.json")
print("Done. saffron_insights.js now contains baked-in translations.")
