# -*- coding: utf-8 -*-
"""Dump the Strategy tab's CHINESE ONLY, for a cold read.

The English is deliberately absent. A reviewer who can see the English reads the
Chinese as a translation and grades the mapping; a reviewer who cannot has to
read it as Chinese, which is the only way to catch prose that is technically
correct and still sounds like it was thought in another language.

    python scripts/export_strategy_zh.py  ->  reports/saffron_strategy_zh_only.md
"""
import json, os, sys, urllib.request

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'reports', 'saffron_strategy_zh_only.md')
APIS = ['http://localhost:5177/api/saffron', 'http://127.0.0.1:8001/api/saffron']


def zh(o):
    if isinstance(o, dict):
        return (o.get('zh') or '').strip()
    return (o or '').strip()


def blocks(bs, out):
    for b in bs:
        if b.get('label'):
            out.append(f'### {zh(b["label"])}\n')
        k = b['kind']
        if k in ('prose', 'note'):
            out.append(zh(b['text']) + '\n')
        elif k == 'list':
            out += [f'- {zh(x)}' for x in b['items']] + ['']
        elif k == 'defs':
            for x in b['items']:
                out.append(f'**{zh(x["term"])}** — {zh(x["body"])}\n')
        elif k == 'links':
            out += [f'- {zh(l["name"])}' for l in b['items']] + ['']
        elif k == 'table':
            out.append('| ' + ' | '.join(zh(h) or ' ' for h in b['headers']) + ' |')
            out.append('|' + '---|' * len(b['headers']))
            for r in b['rows']:
                out.append('| ' + ' | '.join(zh(c) for c in r['cells']) + ' |')
            out.append('')
        elif k == 'component':
            # A disclosure whose body React builds. Dropping it silently printed
            # a heading with nothing under it, and the first cold reader
            # reasonably reported the file as truncated. Say what is behind the
            # lid instead.
            out.append(f'（这一节后面是一块可以展开的内容：{zh(b["label"])}。'
                       f'本次导出未包含，因为它由页面另行绘制。）\n')
        elif k == 'letter':
            out.append('（此处是一封日文邮件范本，不在本次审阅范围内。）\n')


def main():
    d = None
    for a in APIS:
        try:
            d = json.load(urllib.request.urlopen(a, timeout=90)); break
        except Exception:
            continue
    if d is None:
        print('start the app first'); return 1
    f = d.get('futures') or {}
    out = ['# 「策略」——五条路（中文原文）\n', zh(f.get('frame')) + '\n']
    for r in f.get('futures') or []:
        out.append(f'\n## {zh(r["name"])}\n')
        out.append(f'*{zh(r["tagline"])}*\n')
        if r.get('standing'):
            out.append(zh(r['standing']) + '\n')
        blocks(r.get('blocks') or [], out)
    fs = f.get('first_steps')
    if fs:
        out.append(f'\n## {zh(fs.get("label"))}\n')
        out.append(zh(fs.get('intro')) + '\n')
        out += [f'- **{zh(x["route"])}** — {zh(x["step"])}' for x in fs.get('steps', [])]
        out += ['', zh(fs.get('close')) + '\n']
    text = '\n'.join(out).replace('\n\n\n', '\n\n')
    open(OUT, 'w', encoding='utf-8').write(text)
    print(f'wrote {OUT}\n{len(text):,} characters')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
