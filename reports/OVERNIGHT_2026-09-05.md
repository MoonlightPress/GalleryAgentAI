# Overnight, 5–6 September

Everything below is **local and uncommitted** unless marked otherwise. Per your
instruction, only images were deployed; the site is running the state from
commit `08dea050` plus the hero art and the `alt` change.

Run the stack and look at it:

```
python api.py                       # detached, or the harness kills it
cd frontend && npm run dev          # :5177
```

Then — and this is new tonight — you can go straight to a page:
`http://localhost:5177/mochi/#observe/strategy`

---

## What's new, in the order it appears on Saffron's strategy tab

### 1. 第一封信 — The first letter (`engines/outreach_kit_engine.py`)

Your idea, made findable. An **actual Japanese email** she can change the name
on, addressed to Gallery Kogure, plus the six Tokyo-specific conventions behind
a disclosure (one link not five JPGs; five images from one series; name the show
you attended; don't ask for a show; ten days of silence is unseen, not refused;
leave out prices).

It sits directly under the pathway line that already says "send an email first,
not an application," so the section answers the how that line raises.

**One correction worth knowing:** the draft in the design doc had her subject as
「光と猫」 — light and cats. That was written before you told me cats are
incidental. Sending that to a gallery would have misrepresented her work. It now
reads 「建築とそこに射す光を主題にしています」 — architecture and the light on it.

### 2. 一本书要花多少钱 — What a book costs (`engines/book_economics_engine.py`)

The costed model, from tonight's research. Not advice about whether to publish —
the arithmetic of the thing she's going to do anyway.

The chart draws **copies needed to break even against copies printed**, because
that comparison carries the finding a table hides: several options need to sell
more copies than exist.

| Route | Run | Up front | Break-even | Consignment |
|---|---|---|---|---|
| China | 300 | ¥394,500 | **109 copies** | works |
| China | 500 | ¥445,000 | **110 copies** | works |
| China | 100 | ¥368,500 | *impossible* | loses money |
| Japan digital | 100 | ¥320,400 | *impossible* | loses money |
| Japan offset A4 | 500 | ¥2,693,000 | *impossible* | loses money |

**Only China at 300 or more works at a ¥4,950 cover.** Printing 100 — the
intuitive move, and the one you reached for — cannot recover its cost at any
sell-through, anywhere. A small run isn't rescued by selling harder; it's
rescued by the price on the cover, which is what Takeuma's ¥11,000 book was
solving. That case is stated on the card: the same 100 copies at ¥11,000 pays
for itself at 41.

On the chart: one hue, and feasibility carried by geometry plus a written label
rather than colour. I tried two colours and the validator failed them — ochre
against ochre is invisible even to full colour vision, and sage against ochre
fails for protanopia, which is the classic red/green problem. Dropping the
second colour was the right answer anyway.

### 3. URL routing (`frontend/src/utils/route.js`)

`#discover`, `#refine`, `#observe`, and `#observe/<tab>`. Any link you send her
can now point at a specific page — previously every link landed on Mochi's.
Back/forward work, no-hash behaves exactly as before, and the hero art
deliberately does *not* change on in-app navigation.

Verified with 19 live browser checks; frontend tests 76 → 85.

---

## Fixed, from the verification passes

- **Two of the three named artists were described wrongly** and both were errors
  she'd have caught. Urbanowicz is published by MdN and does client work for
  Dentsu, NHK and JAL — he was the wrong example for "no gatekeepers" and is now
  the publisher example. Morimoto is on Almine Rech with museum collections, not
  "a Tokyo gallery that sells for him."
- **The licensing card was overselling.** The one illustrator publishing real
  numbers has licensing at 3% of income against 77% from teaching. That's now
  stated on the card rather than buried.
- **The peer list showed her only watercolour-society painters** — the
  illustration half of her field was mapped in the frontend and missing from the
  data. Added the three verified ones; dropped the entry that wasn't a person.
- **Hero `alt` text** described one painting across dozens, so hovering gave a
  wrong name. Now empty (correct for decorative art) with dragging disabled.

---

## Still open

- ~~1,064 weak why-lines~~ — **done.** 1,068 regenerated; weak count on
  servable entries went **1,064 → 1**, zero missing Chinese, zero tier leaks.
  Spend ~$7.80 of the $8 cap. The one survivor is a printmaking biennial where
  the honest line is "they may not take watercolor at all" — the serve-time
  guard blanks it, which is correct.

  Worth keeping: **Haiku 4.5 needs a 4,096-token prefix to cache**, so the 3.7k
  system block was caching nothing and paying full price every call. Sonnet 5's
  minimum is 1,024, which made the better model the cheaper one.

  Four lines still carried defects after that run — three with a literal
  `(148 characters)` appended, one leaking "a Tier-1 way / 一级途径" to her card.
  Fixed in the data, and the generator now rejects tier language on output as
  well as keeping it out of the prompt. That guard was itself broken on first
  write (my escaping put literal backspace bytes where a word-boundary escape
  matched Chinese and silently failed on English); caught by testing the
  compiled pattern rather than reading the source, since grep renders control
  characters invisibly.
- **No Japanese**, deliberately, since you cut that version.
- **The licensing example stays blank.** Nothing verifiable fits, and I won't
  invent one.
- **`CAREER_SYNOPSIS` is still hardcoded prose** rather than generated from her
  record — the same shape of problem that once had the app calling a 2023 group
  show her latest news.
- **The Saffron career-trio restructure** (`reports/design_saffron_career_trio.md`)
  is designed and not built. I left it deliberately: it rewrites the page she
  actually reads, and doing that unattended isn't worth the risk for work that
  keeps.

---

## Two judgement calls I'd flag

**The book section and the futures are both open by default.** She has clicked
five times in nine days, so anything behind two taps is effectively invisible —
but it does make the strategy tab long. If it reads as a wall, the fix is
collapsing the book section, not shortening it.

**The first letter names Gallery Kogure specifically.** That's from research
with a "fit direct, intake unverified" tag — the roster match is real, the
assumption that cold email works there is not confirmed. The letter says so.
