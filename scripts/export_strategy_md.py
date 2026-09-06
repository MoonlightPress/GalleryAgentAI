# -*- coding: utf-8 -*-
"""Dump the whole Saffron Strategy tab to one markdown file, for outside review.

Reads the live local API so the output is exactly what renders, not a summary of
it. English only — the Chinese is the product but an outside reviewer cannot vet
it, and mixing them makes the file unreadable.

    python scripts/export_strategy_md.py
    -> reports/saffron_strategy_for_review.md
"""
import json
import os
import sys
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
API = 'http://localhost:5177/api/saffron'
OUT = os.path.join(ROOT, 'reports', 'saffron_strategy_for_review.md')


def en(o):
    """English text out of a {en, zh} pair, or a bare string."""
    if isinstance(o, dict):
        return (o.get('en') or '').strip()
    return (o or '').strip()


BRIEF = """# Saffron — "Strategy" tab, full text

*Generated from the running app, so this is the copy as it renders.*

---

## What this is, and what it is for

This is one tab of a private web app built for a single person: a 27-year-old
Chinese watercolour painter living in Tokyo on a student visa. Her work is urban
architecture, interiors, light, atmosphere, quiet observation — no figures. She
has about 26,000 Instagram followers, six years of daily painting, eight
self-published zines, two publications, eight group shows, three solo shows
(all in rooms she paid to rent), and museum group shows in China.

She sells directly: postcards ¥1,100 for six and ¥1,980 for ten, zines ¥1,980,
prints ¥2,200, originals ¥31,900–115,500, and commissions at negotiated prices.

**She reads the app in Chinese. She has never typed anything into it.** Nine
visits between July and September; she reads, and leaves.

The tab is supposed to answer: *what does an artist like me do to build a career
in the areas I choose to work in?* Five business areas, each with how the money
works, what it costs, and where to go.

## What it is being reviewed for

The person who commissioned it has read the draft and says, repeatedly:

1. **It patronises her.** She is a working professional. Passages that explain
   what a gallery is, or what selling directly means, tell her things she has
   done for years.
2. **It describes instead of helping.** It reads as an encyclopedia entry about
   an industry rather than something that changes what she does on Monday.
3. **It keeps saying what things are NOT.** "X is not Y, it is Z." "The door is
   unmarked, not locked." He has asked for this to stop several times and it
   keeps reappearing. Say what a thing is.
4. **The prose is weaker than the rest of the app**, which was written earlier
   and reads better.

Every figure in it is sourced — printer price tables, published rate cards,
platform terms, gallery commission rates. **The research is not in question.
The writing and the usefulness are.**

## What would help

A rewrite, or a diagnosis of what is wrong and how to fix it. Especially:
where it condescends, where it pads, where it states a fact instead of an
implication, and what it should say instead.

---
"""


def render_scenario(s, out):
    """Selling Direct carries its own body shape."""
    order = [
        ('have_label', 'have', 'p'), ('missing_label', 'missing', 'p'),
        ('fill_label', None, 'fill'), ('why_not_stock_label', 'why_not_stock', 'p'),
        ('ds_label', 'ds', 'p'), ('ds_fit_label', 'ds_fit', 'list'),
        ('ds_chart_label', None, 'ds_chart'), (None, 'ds_note', 'p'),
        ('books_label', 'books_note', 'p'), (None, None, 'books'),
        ('proof_label', 'proof', 'p'), ('today_label', None, 'links'),
    ]
    for lbl, key, kind in order:
        if lbl and s.get(lbl):
            out.append(f'### {en(s[lbl])}\n')
        if kind == 'p' and key and s.get(key):
            out.append(en(s[key]) + '\n')
        elif kind == 'list' and key:
            for x in s.get(key, []):
                out.append(f'- {en(x)}')
            out.append('')
        elif kind in ('fill', 'ds_chart', 'books'):
            rows = s.get(kind if kind != 'fill' else 'fill', [])
            heads = s.get(f'{kind}_headers') or s.get('fill_headers')
            if kind == 'books':
                heads, rows = s.get('books_headers'), s.get('books', [])
            if not rows:
                continue
            cols = [k for k in ('what', 'price', 'cost', 'upfront', 'keep',
                                'margin', 'each', 'outlay', 'be') if k in rows[0]]
            out.append('| ' + ' | '.join(en(h) or ' ' for h in heads) + ' |')
            out.append('|' + '---|' * len(heads))
            for r in rows:
                out.append('| ' + ' | '.join(en(r.get(c)) for c in cols) + ' |')
            out.append('')
        elif kind == 'links':
            for l in s.get('today', []):
                out.append(f'- [{en(l["name"])}]({l["url"]})')
            out.append('')


def render_blocks(blocks, out):
    for b in blocks:
        if b.get('label'):
            out.append(f'### {en(b["label"])}\n')
        k = b['kind']
        if k in ('prose', 'note'):
            out.append(en(b['text']) + '\n')
        elif k == 'list':
            for x in b['items']:
                out.append(f'- {en(x)}')
            out.append('')
        elif k == 'links':
            for l in b['items']:
                out.append(f'- [{en(l["name"])}]({l["url"]})')
            out.append('')
        elif k == 'table':
            out.append('| ' + ' | '.join(en(h) or ' ' for h in b['headers']) + ' |')
            out.append('|' + '---|' * len(b['headers']))
            for r in b['rows']:
                out.append('| ' + ' | '.join(en(c) for c in r['cells']) + ' |')
            out.append('')


def main():
    try:
        d = json.load(urllib.request.urlopen(API, timeout=45))
    except Exception as exc:
        print(f'could not reach {API}: {exc}\nStart the app first (start_mochi.bat).')
        return 1

    out = [BRIEF]
    fut = (d.get('futures') or {}).get('futures') or []
    out.append('# The five areas\n')
    if (d.get('futures') or {}).get('note'):
        out.append(f'*{en(d["futures"]["note"])}*\n')

    for f in fut:
        out.append(f'\n## {en(f["name"])}\n')
        out.append(f'*{en(f["tagline"])}*\n')
        if f.get('scenario'):
            render_scenario(f['scenario'], out)
        elif f.get('blocks'):
            render_blocks(f['blocks'], out)

    book = d.get('book_economics')
    if book:
        out.append('\n---\n\n# What a book costs\n')
        out.append(en(book.get('claim')) + '\n')
        out.append(en(book.get('not_a_loss')) + '\n')

    ok = d.get('outreach_kit')
    if ok:
        out.append('\n---\n\n# The first letter\n')
        out.append(en(ok.get('intro')) + '\n')
        out.append(en(ok.get('letter_note')) + '\n')
        out.append('```\n' + (ok.get('letter_ja') or '') + '\n```\n')
        out.append(f'**{en(ok.get("rules_label"))}**\n')
        for r in ok.get('rules', []):
            out.append(f'- {en(r)}')

    text = '\n'.join(out).replace('\n\n\n', '\n\n')
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write(text)
    print(f'wrote {OUT}')
    print(f'{len(text):,} characters · ~{len(text.split()):,} words · {len(fut)} areas')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
