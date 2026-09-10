"""Read-only source inventory for the Saffron editorial review."""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

def literal(node):
    if isinstance(node, ast.Constant):
        return str(node.value)
    if isinstance(node, ast.JoinedStr):
        return ''.join(str(n.value) if isinstance(n, ast.Constant) else ast.unparse(n) for n in node.values)
    return ast.unparse(node)

rows = []
for name in ['futures_engine.py', 'book_economics_engine.py', 'recurring_calendar_engine.py', 'outreach_kit_engine.py']:
    file = ROOT / 'engines' / name
    tree = ast.parse(file.read_text(encoding='utf-8-sig'))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == '_t' and len(node.args) >= 2:
            rows.append({'file': 'engines/' + name, 'line': node.lineno, 'en': literal(node.args[0]), 'zh': literal(node.args[1])})
rows.sort(key=lambda r: (r['file'], r['line']))
(OUT / 'python_copy_inventory.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
for name in sorted(set(r['file'] for r in rows)):
    group = [r for r in rows if r['file'] == name]
    print(name, len(group), 'units;', sum(len(r['zh']) for r in group), 'Chinese characters')
