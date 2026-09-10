"""Read-only source checks; writes validation evidence only into this review folder."""
from pathlib import Path
import importlib.util
import json
import math
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


copy = load_module(HERE / 'copy_decisions.py', 'review_copy')
inventory = json.loads((HERE / 'python_copy_inventory.json').read_text(encoding='utf-8'))
unused = []
for file, line, match in copy.EDITS:
    if not any(r['file'] == file and r['line'] == line and (match is None or r['zh'] == match)
               for r in inventory):
        unused.append([file, line, match])


def chinese_paths(obj, path=''):
    if isinstance(obj, dict):
        if 'zh' in obj and 'en' in obj:
            yield path
        else:
            for key, value in obj.items():
                yield from chinese_paths(value, f'{path}.{key}' if path else key)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            yield from chinese_paths(value, f'{path}.{index}')


ladder_paths = set(chinese_paths(json.loads((HERE / 'ladders_snapshot.json').read_text(encoding='utf-8'))))
unused_ladders = sorted(set(copy.LADDER_EDITS) - ladder_paths)

# Importing this module defines constants/functions only. Do not call any pipeline.
book = load_module(ROOT / 'engines/book_economics_engine.py', 'review_book')
math_rows = []
for price, route, run in [(4950, 'china', 300), (4950, 'japan_digital', 100), (11000, 'japan_digital', 100)]:
    item = next(o for o in book._options(price) if o['route'] == route and o['run'] == run)
    math_rows.append({
        'price_jpy': price, 'route': route, 'run': run,
        'unit_jpy': item['unit_jpy'], 'prepaid_print_jpy': item['outlay_jpy'],
        'existing_model_copies': item['breakeven_direct'],
        'simplified_cash_recovery_copies_excluding_all_selling_costs': math.ceil(item['outlay_jpy'] / price),
    })

broken_links = []
encoding_errors = []
docs = sorted(HERE.glob('*.md'))
for doc in docs:
    content = doc.read_text(encoding='utf-8')
    if '\ufffd' in content:
        encoding_errors.append(doc.name)
    for target in re.findall(r'\]\((C:/[^)]+)\)', content):
        actual = re.sub(r':\d+$', '', target)
        if not Path(actual).is_file():
            broken_links.append({'document': doc.name, 'target': target})

result = {
    'unused_engine_edit_selectors': unused,
    'unused_ladder_edit_selectors': unused_ladders,
    'broken_local_document_links': broken_links,
    'unicode_replacement_character_files': encoding_errors,
    'arithmetic_diagnostics': math_rows,
    'arithmetic_scope': 'Comparison of the existing pure calculation against simplified prepaid-cash recovery. Excludes all selling costs; not a production quote, forecast or recommended target.',
    'markdown_files_checked': [d.name for d in docs],
}
(HERE / 'validation_results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
assert not unused and not unused_ladders and not broken_links and not encoding_errors
assert [r['existing_model_copies'] for r in math_rows] == [109, 184, 41]
assert [r['simplified_cash_recovery_copies_excluding_all_selling_costs'] for r in math_rows] == [80, 65, 30]
