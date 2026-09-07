# Handoff prompt — Saffron strategy sections, readability pass

Paste everything below the line into a fresh session.

---

Read `CLAUDE.md` first. This is Mochi, an AI career-support system built for one
real person: Nin / GEGYjiji, a 27-year-old Chinese watercolour painter on a
student visa in Tokyo. Architecture, space, light, atmosphere — cats appear in
her work but are **not** her subject. She reads the site in Chinese. I (Scott)
built it for her and do not read Chinese.

## Where things stand

Deployed: nothing but hero images. The live site is commit `08dea050` plus the
hero art. **Do not deploy.** Everything else is local and uncommitted, and we
review locally.

Four new sections exist as engines, wired into Saffron's Strategy tab
(`frontend/src/components/SaffronPage.jsx`):

| Engine | Section | Where |
|---|---|---|
| `engines/outreach_kit_engine.py` | The first letter — a real Japanese email to a gallery, plus six Tokyo conventions | Strategy |
| `engines/futures_engine.py` | Five possible futures — kinds of success, not strategies | Strategy |
| `engines/book_economics_engine.py` | What a book costs — costed print model + break-even chart | Strategy |
| `engines/recurring_calendar_engine.py` | Doors that open again — 14 recurring windows | Calendar |

To see them without running the stack:

```bash
python scripts/gen_saffron_preview.py     # -> reports/saffron_preview.html
```

That renders all four in English, in the app's own CSS, with the Chinese behind
a toggle. Publish it to this artifact URL to review it on a phone:
`https://claude.ai/code/artifact/860ed3ff-0599-4a5f-bc51-2dfbe4e2d00f`
(pass it as `url` — publishing without it makes a second artifact). Read the
artifact first, then publish over it.

Or run the app: `python api.py` (detached — a foreground launch gets reaped) and
`cd frontend && npm run dev`, then `http://localhost:5177/mochi/#observe/strategy`.

## Two problems to fix

### 1. The five futures are not readable

My words: *"this isn't very readable. it should be section header, overview,
advantages of track, her strengths in it, then dropdowns for details."*

Each future currently dumps five prose blocks in a row — life, money, what it
requires, current position, someone living it. It reads as a wall. The structure
I want per future:

1. **Header** — the name of the track
2. **Overview** — what this life actually is, short
3. **Advantages of the track** — what this one gives you that the others don't
4. **Her strengths in it** — what she already has that applies here
5. **Dropdowns** — everything else (the money, what it requires, the example)

Note that 3 and 4 are new framings, not renames. "Advantages" is a comparison
between tracks that the copy does not currently make anywhere. "Her strengths"
is the positive half of the existing position ledger — the `absent` half moves
into a dropdown or goes away, because leading with what she lacks is the thing
we are trying to stop doing.

The data shape lives in `futures_engine.build()`; change it there rather than
reshaping in the component, and update `SaffronPage.jsx` + `.css` to match.

### 2. The book section is incoherent

My words: *"the books sections is incoherent, i don't even know what it's trying
to say."*

Right. It currently shows a break-even chart, then three rows of viable routes,
then a note about pricing at ¥11,000, then a caveat about sell-through — four
things making four different points, with no single claim on top.

The underlying research is sound and lives in
`reports/book_economics_2026-09-05.md` (every figure has a source URL and a
confidence tag). The findings, in plain terms:

- At a ¥4,950 cover, **only printing in China at 300+ copies breaks even**
  (109 copies for a 300 run, ¥394,500 up front).
- Printing 100 copies — the intuitive move — **cannot break even at any
  sell-through**, anywhere.
- A small run is rescued by the cover price, not by selling harder: the same
  100 copies at ¥11,000 pay for themselves at 41.
- Consignment (70/30) only survives above roughly ¥1,500 unit cost margin, so
  run size and sales channel are one decision, not two.
- A Japanese art book fair sells a median of 20–25 copies, so a fair alone never
  clears a run.

Work out what the section is *for* before rebuilding it. The questions I was
actually asking when this got built were "so an art book is a loss leader?" and
"this is why you have a publisher, so they eat the upfront production costs" —
if the section answers those, it earns its place. If the answer is really "get a
publisher", the self-publishing arithmetic may belong in a dropdown under that,
not as the headline.

## Rules that are not up for renegotiation

- **Never chide her, never advise her.** She wants possibilities and solutions.
  I already had one pass done on this (2026-09-05) that stripped the second
  person out of `futures_engine.py` and `outreach_kit_engine.py`: no
  imperatives, no verdicts about her, no encouragement, no promises. Conditions,
  mechanics and figures, with the conclusion left to her. Keep that register in
  anything new — but note that "her strengths in it" above is deliberately a
  positive statement of fact, not praise.
- **She reads and never inputs.** Measured: 113 events over 9 days, 5 card
  opens, 1 outbound click, zero feedback presses. Do not build anything that
  needs her to type, rate, or answer.
- **Money is framed as what a door gives**, never as what anything cost her,
  and it reads better in paintings than in yen (her own prices: ¥31,900–115,500).
- **Anything hand-fixed in a JSON data file needs a matching engine rule.** See
  the Data Patch Rule in `CLAUDE.md`.
- **Never use the PowerShell tool on source files** — its `Set-Content -Encoding
  utf8` reads as ANSI and destroys every CJK character in the file. Python via
  the Bash tool, or the Edit tool. This has already cost us `SaffronPage.jsx`
  once.
- Japanese is cut from the site. `_t(en, zh)` only.
- Frontend tests: `cd frontend && npm test` (85 passing). No Python test suite —
  validate by running the engine and reading its output.

## Context worth having

- Her record, computed in `memory/career_strategy_report.json`: 3 solo shows,
  8 confirmed group shows, museum group exhibitions, one international showing,
  2 publications, 8 zines. Tier 3 established, building toward Tier 4.
- Instagram is **~26k** followers. The ~90k figure is Twitter and is never
  referenced.
- She has a solo show running now at Galerie LE MONDE in Harajuku ("Light and
  Shadows and Cats", opened 25 August).
- She is applying to grad school in about two months; if that fails it's
  designated-activities status. Immigration has been difficult lately.
- Roughly 3/4 of her shop sales are me. Volume there is not demand.
- I have not spoken to her since November. She opened the site and read it
  attentively in late August — real scrolling, no bounce. That session is why
  any of this work is happening.
