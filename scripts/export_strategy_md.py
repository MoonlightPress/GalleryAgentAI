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
# The Vite proxy first, because that is what the browser hits and so proves the
# whole path; the backend directly as a fallback, because the copy comes from
# api.py either way and the frontend need not be running to read it.
APIS = ['http://localhost:5177/api/saffron', 'http://127.0.0.1:8001/api/saffron']
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

## The rules this copy is written to

An earlier draft was reviewed and rewritten on 6 September. Four faults were
named and all four are meant to be gone; the first three keep coming back, so
they are worth checking every time.

1. **Never say what a thing is not.** No "X is not Y, it is Z", no "rather
   than", no "the door is unmarked, not locked". Say what a thing is.
2. **Never define anything.** She is a working professional with six years of
   daily painting, eight zines and three solo shows. Explaining what a gallery
   is, or what selling directly means, is the failure mode.
3. **Second person.** "You", not "she".
4. **Measure everything against her baseline.** One original earns
   ¥31,900–115,500 with no client, brief or deadline. Say so even where a route
   comes off worse for it.

The tab describes paths and never judges whether her goals are realistic.

Every figure in it is sourced — printer price tables, published rate cards,
platform terms, gallery commission rates. **The research is not in question.
The writing and the usefulness are.**

## What would help

Where it still condescends, where it pads, where it states a fact instead of an
implication, and what it should say instead. She reads this on a 390px phone
screen in roughly ninety seconds, in Chinese.

---
"""


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
    d = None
    for api in APIS:
        try:
            d = json.load(urllib.request.urlopen(api, timeout=90))
            break
        except Exception as exc:
            print(f'could not reach {api}: {exc}')
    if d is None:
        print('Start the app first (start_mochi.bat).')
        return 1

    futures = d.get('futures') or {}
    fut = futures.get('futures') or []

    out = [BRIEF]
    out.append('# The five areas\n')
    # The frame and the closing experiments were missing from this export, so
    # the reviewer who rewrote the routes never saw the argument joining them
    # or the layer they end on. Both are on the page; both belong here.
    if futures.get('frame'):
        out.append(en(futures['frame']) + '\n')

    for f in fut:
        out.append(f'\n## {en(f["name"])}\n')
        out.append(f'*{en(f["tagline"])}*\n')
        render_blocks(f.get('blocks') or [], out)

    fs = futures.get('first_steps')
    if fs:
        out.append(f'\n## {en(fs.get("label"))}\n')
        out.append(en(fs.get('intro')) + '\n')
        for x in fs.get('steps', []):
            out.append(f'- **{en(x.get("route"))}** — {en(x.get("step"))}')
        out.append('')
        out.append(en(fs.get('close')) + '\n')

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
