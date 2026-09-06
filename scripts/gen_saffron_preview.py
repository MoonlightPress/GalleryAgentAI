# -*- coding: utf-8 -*-
"""Render the unshipped Saffron sections as the app itself would draw them.

Two constraints from Scott, 2026-09-05:

  1. "a lot of this is in chinese. that doesn't help me vet tone" — so English is
     the page's text, and the Chinese she actually reads is behind one toggle.
  2. "i can't picture it on the site" — so this is not a document about the
     sections. It is the app's own markup and the app's own CSS values, lifted
     from frontend/src/components/SaffronPage.css and index.css: the same
     parchment ground, the same 820px section cards, the same tab bar, the same
     break-even SVG geometry. Only the review chrome at the top is invented, and
     it is set in a sans face so it never reads as part of the product.
"""
import sys, html, os

sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import json                                                          # noqa: E402

from engines import (futures_engine, book_economics_engine,          # noqa: E402
                     outreach_kit_engine, recurring_calendar_engine)


def _record():
    """The counts behind the standing lines — same two files api.py reads."""
    def load(name):
        try:
            with open(os.path.join(ROOT, 'memory', name), encoding='utf-8') as fh:
                return json.load(fh)
        except (OSError, ValueError):
            return {}
    return {
        **load('career_strategy_report.json').get('career_evidence', {}),
        'zines': (load('artist_master_profile.json').get('market_presence', {})
                  .get('price_points', {}).get('zines_artbooks', {}).get('count_listed', 0)),
    }


D = {
    'futures':  futures_engine.build(_record()),
    'book':     book_economics_engine.build(),
    'outreach': outreach_kit_engine.build(),
    'calendar': recurring_calendar_engine.build(),
}
E = html.escape


def t(o, key=None):
    """English — the page's own text."""
    if not o:
        return ''
    v = o.get(key) if key else o
    return E((v or {}).get('en', '')) if isinstance(v, dict) else E(v or '')


def zh(o, key=None):
    """The Chinese she reads, hidden until the toggle asks for it."""
    if not o:
        return ''
    v = o.get(key) if key else o
    s = (v or {}).get('zh', '') if isinstance(v, dict) else ''
    return f'<span class="zh-alt" hidden>{E(s)}</span>' if s else ''


def both(o, key=None):
    return t(o, key) + zh(o, key)


def yen(n):
    return '&yen;' + f'{n:,}'


# ── section shell, as SectionShell renders it ────────────────────────────────
def shell(title, subtitle, body, note=None):
    n = f'<div class="rv-note">{note}</div>' if note else ''
    return f'''
<section class="sf-section">
  <div class="sf-toggle-header">
    <div class="sf-toggle-text">
      <h2 class="sf-section-title">{title}</h2>
      <p class="sf-section-subtitle">{subtitle}</p>
    </div>
    <span class="sf-chevron sf-chevron--open">&#9662;</span>
  </div>
  {n}
  <div class="sf-section-body">{body}</div>
</section>'''


# ── the first letter ─────────────────────────────────────────────────────────
def outreach_html():
    o = D['outreach']
    rules = ''.join(f'<li>{both(r)}</li>' for r in o['rules'])
    # Same order as OutreachKit in SaffronPage.jsx: note, letter, then the six
    # conventions behind a disclosure (drawn open here so they can be read).
    body = f'''
    <p class="sf-ok-note">{both(o['letter_note'])}</p>
    <pre class="sf-ok-letter" lang="ja">{E(o['letter_ja'])}</pre>
    <div class="sf-block-label">{both(o['rules_label'])} &#9662;</div>
    <ul class="sf-ok-rules">{rules}</ul>'''
    return shell(both(o['title']), both(o['intro']), body,
                 note='The six conventions sit behind a &ldquo;show me&rdquo; toggle in the app; '
                      'opened here.')


# ── disclosures ──────────────────────────────────────────────────────────────
def detail(label, body):
    """One lid, drawn open. Mirrors <Disclosure> in SaffronPage.jsx."""
    return f"""
        <div class="sf-detail sf-detail--open">
          <div class="sf-detail-head">
            <span class="sf-detail-label">{both(label)}</span>
            <span class="sf-chevron sf-chevron--sm sf-chevron--open">&#9662;</span>
          </div>
          <div class="sf-detail-body">{body}</div>
        </div>"""


# ── five routes ──────────────────────────────────────────────────────────────
def blocks_html(blocks):
    """Mirrors RealmBlocks in SaffronPage.jsx: prose · note · list · links · table."""
    out = []
    for b in blocks:
        label = (f'<div class="sf-block-label">{both(b["label"])}</div>'
                 if b.get('label') else '')
        k = b['kind']
        if k == 'note':
            out.append(f'<p class="sf-scen-gap">{both(b["text"])}</p>')
        elif k == 'prose':
            out.append(f'{label}<p class="sf-scen-para">{both(b["text"])}</p>')
        elif k == 'list':
            items = ''.join(f'<li>{both(x)}</li>' for x in b['items'])
            out.append(f'{label}<ul class="sf-scen-list">{items}</ul>')
        elif k == 'links':
            items = ''.join(
                f'<li><a class="sf-ext-link" href="{l["url"]}" target="_blank" '
                f'rel="noreferrer">{both(l["name"])} &#8599;</a></li>' for l in b['items'])
            out.append(f'{label}<ul class="sf-scen-links">{items}</ul>')
        elif k == 'table':
            head = ''.join(f'<th>{both(h)}</th>' for h in b['headers'])
            rows = ''.join(
                '<tr><th scope="row">{}</th>{}</tr>'.format(
                    both(r['cells'][0]),
                    ''.join(f'<td{" class='sf-scen-price'" if j == 0 else ""}>{both(c)}</td>'
                            for j, c in enumerate(r['cells'][1:])))
                for r in b['rows'])
            out.append(f'{label}<div class="sf-scen-tablewrap"><table class="sf-scen-table">'
                       f'<thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>')
    return f'<div class="sf-scen">{"".join(out)}</div>'


def futures_html():
    f = D['futures']
    cards = []
    for fu in f['futures']:
        cards.append(f'''
      <div class="sf-future sf-future--open">
        <div class="sf-future-head">
          <div>
            <div class="sf-future-name">{both(fu['name'])}</div>
            <div class="sf-future-tagline">{both(fu['tagline'])}</div>
            <div class="sf-future-standing">{both(fu['standing'])}</div>
          </div>
          <span class="sf-chevron sf-chevron--open">&#9662;</span>
        </div>
        <div class="sf-future-body">{blocks_html(fu['blocks'])}</div>
      </div>''')

    fs = f['first_steps']
    steps = ''.join(f'<div><dt>{both(x["route"])}</dt><dd>{both(x["step"])}</dd></div>'
                    for x in fs['steps'])
    body = (f'<p class="sf-scen-frame">{both(f["frame"])}</p>'
            f'<div class="sf-futures">{"".join(cards)}</div>'
            f'<div class="sf-firststeps">'
            f'<div class="sf-block-label">{both(fs["label"])}</div>'
            f'<p class="sf-scen-para">{both(fs["intro"])}</p>'
            f'<dl class="sf-firststeps-list">{steps}</dl>'
            f'<p class="sf-scen-gap">{both(fs["close"])}</p></div>')
    return shell('Five possible futures', '', body,
                 note='In the app each of the five is collapsed to its name, tagline and standing '
                      'line. They are drawn open here so the copy can be read.')


# ── what a book costs ────────────────────────────────────────────────────────
def be_svg():
    """The app's own chart, same geometry as BreakEvenChart in SaffronPage.jsx."""
    opts = [o for o in D['book']['options']
            if o['route'] != 'japan_offset' or o['run'] == 500]
    INK, RULE = '#c47a35', '#7a5c3a'
    W, BAR, GAP, PAD, RIGHT = 300, 14, 26, 104, 8
    mx = max(o['run'] for o in opts) * 1.5
    H = len(opts) * GAP + 20

    def x(v):
        return PAD + min(v / mx, 1) * (W - PAD - RIGHT)

    g = []
    for i, o in enumerate(opts):
        y = i * GAP + 10
        run_x = x(o['run'])
        bar_end = (W - RIGHT) if o['impossible'] else x(o['breakeven_direct'])
        val = (f'<text x="{PAD + 5}" y="{y + 11}" class="sf-be-val sf-be-val--in">'
               f"can&#39;t pay for itself</text>" if o['impossible'] else
               f'<text x="{bar_end + 5:.2f}" y="{y + 11}" class="sf-be-val">{o["breakeven_direct"]}</text>')
        g.append(f'''
      <g>
        <text x="0" y="{y + 10}" class="sf-be-label">{o['run']} &#183; {t(o['route_name'])}</text>
        <rect x="{PAD}" y="{y + 1}" width="{max(2, bar_end - PAD):.2f}" height="{BAR}" rx="3"
              fill="{INK}" opacity="{0.3 if o['impossible'] else 0.92}" />
        <line x1="{run_x:.2f}" y1="{y - 2}" x2="{run_x:.2f}" y2="{y + BAR + 3}"
              stroke="{RULE}" stroke-width="1.5" />
        {val}
      </g>''')
    tick_x = x(opts[-1]['run'])
    return f'''
  <figure class="sf-be-fig">
    <svg viewBox="0 0 {W} {H}" class="sf-be-svg" role="img" aria-label="What a book costs">
      {''.join(g)}
      <text x="{tick_x:.2f}" y="{H - 4}" class="sf-be-tick" text-anchor="middle">printed</text>
    </svg>
    <figcaption class="sf-be-cap">A bar past the marker means selling more copies than exist.</figcaption>
  </figure>'''


def book_html():
    b = D['book']
    rows = []
    for o in b['options']:
        if o['impossible']:
            continue
        ok = ('<span class="sf-be-ok"> &#183; works on consignment</span>'
              if o['consignment_viable'] else
              '<span class="sf-be-no"> &#183; consignment loses money</span>')
        rows.append(f'''
      <div class="sf-be-row">
        <div class="sf-be-row-head">{o['run']} &#183; {both(o['route_name'])}</div>
        <div class="sf-be-row-num">{yen(o['outlay_jpy'])} up front &#183;
          {o['breakeven_direct']} copies to break even{ok}</div>
        <div class="sf-be-row-note">{both(o['route_note'])}</div>
      </div>''')
    hp = b['high_price_case']

    fk = b['fork']
    cols = []
    for c in fk['columns']:
        vals = ''.join(
            f'<div class="sf-fork-row"><dt>{t(lab)}</dt><dd>{both(v)}</dd></div>'
            for lab, v in zip(fk['row_labels'], c['values']))
        cols.append(f'''
        <div class="sf-fork-col sf-fork-col--{c['id']}">
          <div class="sf-fork-name">{both(c['name'])}</div>
          <dl class="sf-fork-rows">{vals}</dl>
        </div>''')

    facts = ''.join(f'<li>{both(f)}</li>' for f in b['pace']['facts'])

    arithmetic = (be_svg()
                  + f'<div class="sf-be-rows">{"".join(rows)}</div>'
                  + f'<p class="sf-be-highprice">{both(hp["note"])}</p>')

    body = f'''
    <p class="sf-be-claim">{both(b['claim'])}</p>
    <p class="sf-be-answer">{both(b['not_a_loss'])}</p>

    <div class="sf-fork">
      <div class="sf-block-label">{both(fk['label'])}</div>
      <div class="sf-fork-cols">{''.join(cols)}</div>
      <p class="sf-fork-note">{both(fk['note'])}</p>
    </div>

    <div class="sf-pace">
      <div class="sf-block-label">{both(b['pace']['label'])}</div>
      <ul class="sf-pace-facts">{facts}</ul>
    </div>

    <div class="sf-details">{detail(b['detail_label'], arithmetic)}</div>
    <p class="sf-be-caveat">{both(b['caveat'])}</p>'''

    return shell('What a book costs', both(b['note']), body,
                 note=f'Cover price {yen(b["price_jpy"])}, ~128pp full-colour hardcover, '
                      'consignment at 70/30. Every figure sourced in '
                      '<code>reports/book_economics_2026-09-05.md</code>. The route-by-route '
                      'arithmetic is behind a lid in the app; drawn open here. Routes that cannot '
                      'break even appear on the chart and are left out of the list below it.')


# ── doors that open again ────────────────────────────────────────────────────
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']


def doors_html():
    c = D['calendar']

    def worth(d):
        p = d['in_paintings']
        r = p['fewest'] if p['same'] else f'{p["fewest"]}&ndash;{p["most"]}'
        return (f"materials, about {r} paintings' worth" if d.get('amount_in_kind')
                else f"&asymp; {r} paintings that don&rsquo;t have to be sold")

    def door(d, always=False):
        if always:
            when = '<span class="sf-door-badge">Always open</span>'
            cls = ' sf-door--always'
        elif d.get('open_now'):
            closes = ''
            if d.get('closes_month'):
                closes = (f'<span class="sf-door-closes">Closes {d["closes_day"]} '
                          f'{MONTHS[int(d["closes_month"]) - 1]}')
                if d.get('days_left') is not None and d['days_left'] <= 30:
                    closes += f' &#183; {d["days_left"]} days left'
                closes += '</span>'
            when = f'<span class="sf-door-badge sf-door-badge--open">Open now</span>{closes}'
            cls = ' sf-door--open'
        else:
            m = MONTHS[int(d['opens_month']) - 1]
            approx = '' if d.get('certain') else ' (timing approximate)'
            prep = ('<span class="sf-door-badge">Worth starting now</span>'
                    if d.get('preparing_now') else '')
            when = f'<span class="sf-door-month">{m}{approx}</span>{prep}'
            cls = ''
        note = (f'<p class="sf-door-note">{both(d["status_note"])}</p>'
                if d.get('status_note') else '')
        w = f'<p class="sf-door-worth">{worth(d)}</p>' if d.get('in_paintings') else ''
        fee = (f'<p class="sf-door-fee">Booth from {yen(d["entry_fee_jpy"])}</p>'
               if d.get('entry_fee_jpy') else '')
        p = (f'<p class="sf-door-prep"><strong>Have ready:</strong> {both(d["prepare"])}</p>'
             if d.get('prepare') else '')
        return f'''
      <div class="sf-door{cls}">
        <div class="sf-door-when">{when}</div>
        <a class="sf-door-name sf-ext-link" href="{E(d['url'])}" target="_blank" rel="noopener">{both(d['name'])} &#8599;</a>
        <p class="sf-door-gives">{both(d['gives'])}</p>
        {note}{w}{fee}{p}
      </div>'''

    soonest = next((d for d in c['doors'] if d.get('open_now') and d.get('days_left') is not None), None)
    summary = (f"{c['open_now_count']} open today. The nearest one closes in "
               f"{soonest['days_left']} days." if soonest else
               'Nothing open today. Below is what opens next, soonest first.')
    body = ('<div class="sf-doors">'
            + ''.join(door(d) for d in c['doors'])
            + ''.join(door(a, always=True) for a in c['always_open'])
            + '</div>')
    return shell('Doors that open again', summary, body,
                 note='This one sits on the <strong>Calendar</strong> tab, above the month grid. '
                      'Rebuilt 6 September: every entry re-checked against the institution&rsquo;s '
                      'own page, real opening AND closing dates, and the green badge now requires '
                      'a date read off an official page rather than an inferred one.')


# ── page ─────────────────────────────────────────────────────────────────────
TABS = ['Overview', 'Position', 'Strategy', 'Landscape', 'Peers', 'Calendar']

CSS = '''
<style>
/* Values lifted from the app: index.css tokens and SaffronPage.css.
   Single-theme on purpose — the app sets color-scheme: light and this page
   exists to show what the app looks like. */
:root{
  --parchment:#EEE0C2; --paper:#FFFAF3; --ink:#3d2b20; --ink-medium:#5d4b3b;
  --ink-muted:#8a7563; --border:#e6d4b8; --gold:#c49a3e;
  --rv-ink:#4a4034; --rv-bg:#efe7d6; --rv-line:#d9cbaa;
}
*,*::before,*::after{box-sizing:border-box}
html{color-scheme:light}
body{
  margin:0;background:var(--parchment);color:var(--ink);
  font-family:Georgia,'Palatino Linotype',serif;font-size:16px;line-height:1.5;
  -webkit-font-smoothing:antialiased;-webkit-text-size-adjust:100%;
}

/* ── review chrome (not part of the product; sans so it never reads as one) ── */
.rv-bar{
  position:sticky;top:0;z-index:60;background:var(--rv-bg);
  border-bottom:1px solid var(--rv-line);
  box-shadow:0 2px 6px rgba(80,55,30,.07);
}
.rv-bar-in{
  max-width:880px;margin:0 auto;padding:10px 20px;
  display:flex;align-items:center;gap:14px;flex-wrap:wrap;
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",sans-serif;
  font-size:12.5px;color:var(--rv-ink);
}
.rv-tag{
  font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;font-weight:600;
  color:#8a5a1c;border:1px solid #cfa964;border-radius:2px;padding:2px 7px;white-space:nowrap;
}
.rv-bar-sp{flex:1 1 auto;min-width:8px}
.rv-toggle{
  font:inherit;font-weight:600;cursor:pointer;white-space:nowrap;
  background:var(--paper);color:var(--rv-ink);
  border:1px solid var(--rv-line);border-radius:20px;padding:5px 14px;
}
.rv-toggle:hover{border-color:#b99a5e;color:#6b4420}
.rv-toggle[aria-pressed="true"]{background:#6b5638;border-color:#6b5638;color:#f7efdd}
.rv-toggle:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
.rv-lede{
  max-width:880px;margin:0 auto;padding:26px 20px 6px;
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",sans-serif;
  font-size:13.5px;line-height:1.65;color:#5f5342;
}
.rv-lede h1{
  font-family:Georgia,serif;font-size:24px;font-weight:bold;color:#3d2b1a;
  margin:0 0 8px;letter-spacing:.01em;
}
.rv-lede p{margin:0 0 8px;max-width:60ch}
.rv-lede code,.rv-note code{
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.92em;
  background:#e7dcc4;padding:1px 5px;border-radius:3px;
}
.rv-note{
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",sans-serif;
  font-size:12px;line-height:1.6;color:#7d6f5b;
  background:#f3ecdb;border:1px dashed #d9cbaa;border-radius:8px;
  padding:8px 12px;margin-top:16px;
}
.rv-frame-label{
  max-width:880px;margin:34px auto 0;padding:0 20px;
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",sans-serif;
  font-size:10.5px;letter-spacing:.11em;text-transform:uppercase;font-weight:600;color:#8f8064;
}

/* the Chinese she reads, revealed by the toggle */
.zh-alt{
  display:block;margin-top:5px;color:#8a7563;font-size:.94em;line-height:1.72;
  border-left:2px solid #ddcba2;padding-left:9px;
}
.sf-future-name .zh-alt,.sf-door-name .zh-alt,.sf-section-title .zh-alt{border-left:0;padding-left:0}

/* ── app: content column and tab bar ─────────────────────────────────────── */
.sf-content{max-width:960px;margin:0 auto;padding:0 24px 48px;width:100%}
.sf-tabs{
  display:flex;flex-wrap:wrap;justify-content:center;gap:2px;padding:12px 16px;
  background:#FAF4E6;border-bottom:1px solid #e8d5a8;
  box-shadow:0 3px 8px rgba(120,90,30,.06);margin:0 0 8px;
}
.sf-tab{
  font-family:Georgia,serif;font-size:.98rem;color:#8a7350;background:transparent;
  border:none;border-bottom:2px solid transparent;padding:6px 16px;
}
.sf-tab--active{color:#3d2b1a;font-weight:bold;border-bottom-color:#c49a3e}

.sf-section{
  max-width:820px;width:calc(100% - 36px);margin:0 auto 16px;padding:26px 30px;
  background:#fbf5e6;border:1px solid #e6d4b4;border-radius:14px;
  box-shadow:0 1px 4px rgba(120,90,30,.04);
}
.sf-section:first-of-type{margin-top:12px}
.sf-toggle-header{display:flex;align-items:flex-start;justify-content:space-between;gap:16px}
.sf-toggle-text{display:flex;flex-direction:column;gap:6px}
.sf-section-title{font-family:Georgia,serif;font-size:22px;font-weight:bold;color:#3d2b1a;margin:0;letter-spacing:.01em}
.sf-section-subtitle{font-family:Georgia,serif;font-size:14px;color:#8b6a3e;font-style:italic;margin:0}
.sf-chevron{font-size:20px;color:#c4a06a;flex-shrink:0;margin-top:2px;line-height:1;display:inline-block}
.sf-chevron--open{transform:rotate(180deg)}
.sf-section-body{margin-top:32px}
.sf-block-label{
  font-family:Georgia,serif;font-size:11px;font-weight:bold;letter-spacing:.08em;
  text-transform:uppercase;color:#c47a35;margin-bottom:14px;
}
.sf-ext-link{text-decoration:none}
.sf-ext-link:hover{color:#c47a35;text-decoration:underline}

/* ── the first letter ────────────────────────────────────────────────────── */
.sf-ok-intro{font-family:Georgia,serif;font-size:13.5px;line-height:1.72;color:#4a3826;margin:0 0 14px}
.sf-ok-letter{
  font-family:"Hiragino Mincho ProN","Yu Mincho",Georgia,serif;
  font-size:12.5px;line-height:1.85;color:#3d2b1a;background:#fffdf7;
  border:1px solid #e6d9bd;border-radius:8px;padding:14px 15px;margin:0 0 12px;
  white-space:pre-wrap;overflow-wrap:break-word;
}
.sf-ok-note{font-family:Georgia,serif;font-size:12.5px;font-style:italic;color:#7a5c3a;margin:0 0 22px}
.sf-ok-rules{font-family:Georgia,serif;font-size:12.5px;line-height:1.7;color:#4a3826;margin:10px 0 0;padding-left:20px}
.sf-ok-rules li{margin-bottom:10px}

/* ── five futures ────────────────────────────────────────────────────────── */
.sf-futures{display:flex;flex-direction:column;gap:10px}
.sf-future{border:1px solid #e6d9bd;border-radius:9px;background:#fffdf7;overflow:hidden}
.sf-future--open{background:#fffaf0;border-color:#d8c79a}
.sf-future-head{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:13px 15px}
.sf-future-name{font-family:Georgia,serif;font-size:15px;font-weight:bold;color:#7a5030}
.sf-future-standing{font-family:Georgia,serif;font-size:12px;color:#7a6448;margin-top:6px;line-height:1.55;max-width:46em}
.sf-future-tagline{font-family:Georgia,serif;font-size:12.5px;font-style:italic;color:#8a6f4a;margin-top:3px;line-height:1.45}
.sf-future-body{padding:0 15px 15px}
.sf-details{display:flex;flex-direction:column;gap:1px}
.sf-detail{border-top:1px solid #ece0c4}
.sf-detail:last-child{border-bottom:1px solid #ece0c4}
.sf-detail-head{
  width:100%;display:flex;align-items:center;justify-content:space-between;
  gap:12px;padding:9px 2px;text-align:left;
}
.sf-detail-label{
  font-family:Georgia,serif;font-size:11px;font-weight:bold;letter-spacing:.08em;
  text-transform:uppercase;color:#c47a35;
}
.sf-chevron--sm{font-size:14px;margin-top:0}
.sf-detail-body{padding:2px 2px 14px}

/* ── what a book costs ───────────────────────────────────────────────────── */
.sf-be-claim{font-family:Georgia,serif;font-size:15px;line-height:1.68;color:#3d2b1a;margin:0 0 14px}
.sf-be-answer{
  font-family:Georgia,serif;font-size:13px;line-height:1.68;color:#4a3826;
  background:#f7f4e8;border-left:3px solid #c9a86a;border-radius:0 7px 7px 0;
  padding:11px 13px;margin:0 0 24px;
}
.sf-fork{margin-bottom:24px}
.sf-fork-cols{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.sf-fork-col{background:#fffaf0;border:1px solid #e6d9bd;border-radius:9px;padding:12px 14px 10px}
.sf-fork-name{
  font-family:Georgia,serif;font-size:13.5px;font-weight:bold;color:#7a5030;
  margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid #ece0c4;
}
.sf-fork-rows{margin:0}
.sf-fork-row{margin-bottom:9px}
.sf-fork-row:last-child{margin-bottom:0}
.sf-fork-row dt{
  font-family:Georgia,serif;font-size:10px;font-weight:bold;letter-spacing:.07em;
  text-transform:uppercase;color:#a0885f;margin-bottom:2px;
}
.sf-fork-row dd{font-family:Georgia,serif;font-size:12.5px;line-height:1.55;color:#4a3826;margin:0}
.sf-fork-note{font-family:Georgia,serif;font-size:12px;line-height:1.62;color:#7a5c3a;font-style:italic;margin:12px 0 0}
.sf-pace{margin-bottom:20px}
.sf-pace-facts{
  font-family:Georgia,serif;font-size:12.5px;line-height:1.65;color:#4a3826;
  margin:0;padding-left:18px;list-style:none;
}
.sf-pace-facts li{margin-bottom:9px;position:relative}
.sf-pace-facts li:last-child{margin-bottom:0}
.sf-pace-facts li::before{
  content:'';position:absolute;left:-14px;top:.65em;width:5px;height:5px;
  border-radius:50%;background:#c9a86a;
}

.sf-be-fig{margin:4px 0 22px}
.sf-be-svg{width:100%;height:auto;display:block}
.sf-be-label{font-family:Georgia,serif;font-size:7px;fill:#6a5436}
.sf-be-val{font-family:Georgia,serif;font-size:7px;fill:#7a5c3a;font-style:italic}
.sf-be-val--in{fill:#6b4420}
.sf-be-tick{font-family:Georgia,serif;font-size:6.5px;fill:#8a6f4a;font-style:italic}
.sf-be-cap{font-family:Georgia,serif;font-size:11.5px;color:#8a6f4a;font-style:italic;margin-top:6px}
.sf-be-rows{display:flex;flex-direction:column;gap:11px}
.sf-be-row{padding:10px 13px;background:#fffaf0;border-left:3px solid #d8c79a;border-radius:0 7px 7px 0}
.sf-be-row-head{font-family:Georgia,serif;font-size:13.5px;font-weight:bold;color:#7a5030}
.sf-be-row-num{font-family:Georgia,serif;font-size:12.5px;color:#4a3826;margin-top:3px}
.sf-be-ok{color:#5a7a30}
.sf-be-no{color:#9a7040;font-style:italic}
.sf-be-row-note{font-family:Georgia,serif;font-size:12px;line-height:1.55;color:#6a5436;margin-top:5px}
.sf-be-highprice{
  font-family:Georgia,serif;font-size:12.5px;line-height:1.65;color:#3f5a34;
  background:#f7f4e8;border-left:3px solid #8fc98a;border-radius:0 7px 7px 0;
  padding:10px 13px;margin:16px 0 0;
}
.sf-be-caveat{font-family:Georgia,serif;font-size:12px;line-height:1.6;color:#7a5c3a;font-style:italic;margin:12px 0 0}

/* ── doors ───────────────────────────────────────────────────────────────── */
.sf-doors{display:flex;flex-direction:column;gap:12px}
.sf-door{padding:12px 15px;background:#fffaf0;border-left:3px solid #d8c79a;border-radius:0 8px 8px 0}
.sf-door--open{border-left-color:#5a7a30;background:#fbfcf5}
.sf-door--always{border-left-color:#c4a03a}
.sf-door-when{display:flex;align-items:center;gap:8px;margin-bottom:5px;flex-wrap:wrap}
.sf-door-month{font-family:Georgia,serif;font-size:11px;font-weight:bold;letter-spacing:.06em;text-transform:uppercase;color:#9a7040}
.sf-door-badge{
  font-family:Georgia,serif;font-size:11px;color:#7a5c3a;background:#f4ead6;
  border:1px solid #ddcba2;border-radius:20px;padding:1px 9px;white-space:nowrap;
}
.sf-door-badge--open{color:#2e6626;background:#eef7e6;border-color:#8fc98a;font-weight:bold}
.sf-door-name{font-family:Georgia,serif;font-size:14px;font-weight:bold;color:#b5701f;display:inline-block}
.sf-door-gives{font-family:Georgia,serif;font-size:12.5px;line-height:1.6;color:#4a3826;margin:4px 0 0}
.sf-door-prep{font-family:Georgia,serif;font-size:12.5px;line-height:1.6;color:#6a5436;margin:6px 0 0;font-style:italic}
.sf-door-prep strong{font-style:normal;color:#7a5c3a}
.sf-door-worth{font-family:Georgia,serif;font-size:12px;color:#5a7a30;margin:5px 0 0;letter-spacing:.01em}
.sf-door-closes{font-family:Georgia,serif;font-size:11.5px;font-weight:bold;letter-spacing:.02em;color:#8a5a1c}
.sf-door-note{
  font-family:Georgia,serif;font-size:12px;line-height:1.6;color:#7a5c3a;
  background:#f6efe0;border-radius:6px;padding:7px 10px;margin:7px 0 0;
}
.sf-door-fee{font-family:Georgia,serif;font-size:12px;color:#8a6f4a;margin:5px 0 0}

@media (max-width:640px){
  .sf-content{padding:0 12px 40px}
  .sf-section{width:100%;padding:20px 18px;border-radius:12px}
  .sf-tabs{flex-wrap:nowrap;justify-content:flex-start;overflow-x:auto;padding:10px 12px}
  .sf-tab{flex-shrink:0}
  .rv-lede{padding:20px 16px 4px}
}
@media (max-width:560px){
  .sf-fork-cols{grid-template-columns:1fr}
}
</style>'''

JS = '''
<script>
(function () {
  var btn = document.getElementById('zh-toggle');
  btn.addEventListener('click', function () {
    var on = btn.getAttribute('aria-pressed') !== 'true';
    btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    btn.textContent = on ? 'Hide the Chinese' : 'Show the Chinese she reads';
    var nodes = document.querySelectorAll('.zh-alt');
    for (var i = 0; i < nodes.length; i++) nodes[i].hidden = !on;
  });
})();
</script>'''

tabs = ''.join(
    f'<button class="sf-tab{" sf-tab--active" if x == "Strategy" else ""}" type="button" tabindex="-1">{x}</button>'
    for x in TABS)

HTML = f'''<title>Saffron Strategy Draft</title>
{CSS}
<div class="rv-bar"><div class="rv-bar-in">
  <span class="rv-tag">Local &middot; not deployed</span>
  <span>Saffron &rarr; Strategy, rendered in the app&rsquo;s own CSS</span>
  <span class="rv-bar-sp"></span>
  <button type="button" class="rv-toggle" id="zh-toggle" aria-pressed="false">Show the Chinese she reads</button>
</div></div>

<div class="rv-lede">
  <h1>Four sections, in English, drawn the way the site draws them</h1>
  <p>The live site is the rollback branch at <code>832c5ab1</code> plus the hero art &mdash; none of
     this is live. The text below is English so the tone can be read directly; the Chinese she
     actually sees is one button away, underneath each block.</p>
  <p>Everything is generated from the engines themselves, so this is the copy that would ship,
     not a summary of it.</p>
  <p><strong>6 September.</strong> The five routes were rewritten to a structure an outside
     reviewer produced after reading the whole tab. It opens on a thesis &mdash; <em>where does
     another route give you something the current one cannot</em> &mdash; then answers every route
     to it and ends on five experiments, one each. Headings are decisions rather than topics
     (&ldquo;Fill the gap between &yen;2,200 and &yen;31,900&rdquo;, not &ldquo;How it works&rdquo;).
     Each route is now a free list of blocks, so one with a single real finding says one thing
     instead of padding out to five. The computed ledger of what she has and has not done is gone
     with the schema that held it.</p>
  <p><strong>The register changed with it.</strong> Second person, addressed to a working
     professional: nothing is defined, nothing is explained back to her, and every route is
     measured against what an original already earns her (&yen;31,900&ndash;115,500 with no client,
     brief or deadline) &mdash; including where the route loses. Nothing is described by what it
     is not.</p>
</div>

<div class="rv-frame-label">The app, from here down</div>
<div class="sf-content">
  <div class="sf-tabs">{tabs}</div>
  {futures_html()}
  {book_html()}
  {outreach_html()}
  {doors_html()}
</div>
{JS}
'''

out = os.path.join(ROOT, 'reports', 'saffron_preview.html')
open(out, 'w', encoding='utf-8').write(HTML)
print('wrote', out, len(HTML), 'bytes')
