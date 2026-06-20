import json, urllib.request, re, sys
sys.stdout.reconfigure(encoding='utf-8')

def fetch(path):
    try:
        return json.load(urllib.request.urlopen('https://twilightdreamworks.com'+path, timeout=20))
    except Exception as e:
        return {'_err': str(e)}

saf = fetch('/api/saffron'); car = fetch('/api/career_strategy')

strings = set()
def walk(o):
    if isinstance(o, str):
        if re.search(r'[A-Za-z]', o) and len(o.strip()) > 2:
            strings.add(o.strip())
    elif isinstance(o, dict):
        for k, v in o.items():
            if k == '_i18n': continue   # the translation map itself, not content
            walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(saf); walk(car)

# Extract SF_ZH english keys (left-hand side) by simple line parsing
src = open('frontend/src/components/SaffronPage.jsx', encoding='utf-8').read()
block = src.split('const SF_ZH = {', 1)[1].split('\n}', 1)[0]
keys = set()
for line in block.splitlines():
    s = line.strip()
    if s.startswith('"') and '": "' in s:
        k = s[1:].split('": "', 1)[0]
        keys.add(k)

# Plus the live _i18n map the payload now ships (opportunity translations)
keys |= set((saf.get('_i18n', {}).get('zh', {}) or {}).keys())

unmapped = sorted(s for s in strings if s not in keys)
def proseish(s):
    if s.startswith('http'): return False
    if re.match(r'^[\d\W]+$', s): return False
    return len(s.split()) >= 4
prose = [s for s in unmapped if proseish(s)]
print(f"served english strings: {len(strings)} | mapped: {len(strings)-len(unmapped)} | unmapped: {len(unmapped)} | unmapped multi-word: {len(prose)}")
print("\n=== UNMAPPED multi-word (the real leaks) ===")
for s in prose[:70]:
    print(" -", s[:150])
