"""One-time: seed memory/translation_cache.json from the hand-reviewed SF_ZH map
in SaffronPage.jsx, so the auto-translator doesn't re-spend Claude on them."""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
jsx = (ROOT / "frontend/src/components/SaffronPage.jsx").read_text(encoding="utf-8")
block = jsx.split("const SF_ZH = {", 1)[1].split("\n}", 1)[0]

zh = {}
for line in block.splitlines():
    s = line.strip()
    if s.startswith('"') and '": "' in s:
        body = s[1:]
        k = body.split('": "', 1)[0]
        v = body.split('": "', 1)[1].rsplit('",', 1)[0]
        if k and v:
            zh[k] = v

cache_path = ROOT / "memory" / "translation_cache.json"
cache = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}
cache.setdefault("zh", {}).update(zh)
cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"seeded {len(zh)} reviewed strings into {cache_path}")
