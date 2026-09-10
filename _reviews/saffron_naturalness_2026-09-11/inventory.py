"""Snapshot current Chinese for a meaning-preserving fluency review. No app writes."""
import ast
import hashlib
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

rows=[]
hashes={}
for name in ['futures_engine.py','book_economics_engine.py','recurring_calendar_engine.py','outreach_kit_engine.py']:
    file='engines/'+name
    src=(ROOT/file).read_text(encoding='utf-8-sig')
    hashes[file]=hashlib.sha256(src.encode()).hexdigest()
    for n in ast.walk(ast.parse(src)):
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='_t' and len(n.args)>1:
            rows.append({'file':file,'line':n.lineno,'en':literal(n.args[0]),'zh':literal(n.args[1])})
rows.sort(key=lambda r:(r['file'],r['line']))
(OUT/'engine_inventory.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'source_hashes.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
for name in hashes:
    subset=[r for r in rows if r['file']==name]
    content='\n\n'.join(f"[{r['line']}] {r['zh']}" for r in subset)
    (OUT/(Path(name).stem+'_zh.txt')).write_text(content,encoding='utf-8')
print(len(rows),'current engine units captured')
