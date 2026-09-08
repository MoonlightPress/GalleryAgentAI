# Next phase: goals, and the ladders that reach them

_Written 2026-09-08, out of the Saffron restructure._
_Design note, not a report. Nothing below is built._

## The observation

Saffron has one strategy and it is the gallery one.

`career_strategy_report.json` computes a single `next_milestone` — "Gallery
representation and a sustained international record" — and seven blocking gaps
behind it: `gallery_representation`, `solo_venue_quality`, `art_fairs`,
`residency`, `grant`, `critical_press`, `monograph`. Every one is institutional.

There is no lever anywhere in the system for an audience, a price ladder, a
lookbook, or a publisher relationship. So the app cannot describe how she reaches
a following or a licensing deal, no matter how the existing gaps are reordered.
The ingredients do not exist.

Scott, 2026-09-08: _"what other pathway strategies are there other than being a
gallery artist? how does she get to 500,000 followers. what does that provide
her?"_ — and then, on scope: _"it doesn't have to be 5, it's not an extension of
the 5. it's just a ladder of tasks that gets her to specific goals."_

## What this is not

**It is not an extension of the five Pathways.** Those stay exactly as they are —
practical overviews of a domain: what it is, what it pays, what she would be
taking on. Selling Direct, Galleries, Licensing, Publishing, Commissions. Do not
touch `futures_engine.py`.

A Pathway is a *place*. A Strategy is a *route*. There is no requirement that
they correspond, and forcing one strategy per pathway is the mistake this note
exists to avoid.

## The model

Three parts.

### 1. Goals — authored, few, named plainly

Not derived. Authored the way `recurring_calendar_engine.DOORS` is authored,
because a goal is a durable fact about what an artist can aim at, and authoring
it is honest where inferring it would be invention. Scott's three to start:

| id | goal |
|---|---|
| `gallery_success` | Gallery success |
| `a_following` | A following |
| `international_licensing` | International licensing |

More can be added (a book that pays for itself; commissions that find her). The
set is deliberately open — nothing in the model depends on the count.

### 2. Tasks — one shared pool, stable ids

The point of the whole design. The same task appears in several ladders at
different positions, and **a task that advances three goals at once is the most
useful thing Saffron can say**, because it is invisible from the ground.

A task is `{id, label, detail, evidence_fn}`. Sketch of the pool, drawn from what
her record actually contains:

| task | serves |
|---|---|
| `body_of_work` — ten paintings that hang together as one thing | gallery, licensing |
| `daily_cadence` — a sustained rhythm of new work | following |
| `named_series` — a repeatable series rather than a diary | following, licensing |
| `process_video` — the work in motion, not only the result | following |
| `cross_platform` — the same work where other audiences are | following |
| `recognisable_style` — one look, legible at thumbnail size | following, licensing |
| `price_ladder_middle` — something between ¥2,200 and ¥31,900 | following, licensing |
| `lookbook` — 10–20 works as product mockups, one PDF | licensing |
| `findable_for_licensing` — listed where art directors look | licensing |
| `first_licence` — one paid usage, at any size | licensing |
| `group_shows` — a record of showing alongside others | gallery |
| `solo_shows` — her own room | gallery |
| `institutional_show` — a museum or public institution | gallery |
| `better_solo_venues` — stepping up from café and small gallery | gallery |
| `critical_press` — written *about*, not featured | gallery, licensing |
| `art_fairs` — collector access | gallery |
| `representation` — a gallery that sells on her behalf | gallery |

### 3. Ladders — an order, per goal

A goal is a goal id plus an ordered list of task ids. Order is the content: the
same tasks reach different goals in different sequences.

```
gallery_success:         body_of_work -> group_shows -> solo_shows ->
                         institutional_show -> better_solo_venues ->
                         critical_press -> art_fairs -> representation

a_following:             daily_cadence -> recognisable_style -> named_series ->
                         process_video -> cross_platform -> price_ladder_middle

international_licensing: recognisable_style -> named_series -> lookbook ->
                         findable_for_licensing -> first_licence -> critical_press
```

`recognisable_style` and `named_series` sit in two ladders. `critical_press` sits
in two, at opposite ends. That overlap is the product.

## Done-ness is computed, never authored

Each task carries an `evidence_fn` reading her live record — the same discipline
that keeps `recurring_calendar_engine` from rotting. `group_shows` is done
because `career_evidence.confirmed_group_shows` is 8. `lookbook` is not done
because nothing in her data is one. Authored done-flags go stale the moment her
record moves; computed ones cannot.

This also means a ladder needs no maintenance after it is written.

## Why "a following" is a goal and not a Pathway

Reach is not a place her work goes. It is the thing that makes the other places
survivable, and her own numbers say so. Her best print route is a 300-copy run
from China: ¥394,500 outlay, break-even at 109 copies.

| audience | share who must buy to break even |
|---|---|
| 26,000 (now) | 0.42% — 1 in 240 |
| 100,000 | 0.11% — 1 in 920 |
| 500,000 | 0.022% — 1 in 4,600 |

At 26k a book is a ¥394,500 bet that one follower in 240 spends ¥4,950. At 500k
it is noise. Licensing moves the same way: Hobonichi's own model is that it
hand-picks illustrators whose Instagram work has a distinct voice — at 26k she
pitches, at 500k they arrive.

So a following earns its place as a goal because it is *load-bearing for three
others*, which the ladder overlap will show without anyone having to say it.

## The blocker: the system has never measured an audience

`memory/peer_artists.json` holds 8 peers with **zero follower counts**, and they
are watercolour-society painters — Castagnet, Schaller, Haines, Jean Haines. The
artists whose path "a following" actually is — Mateusz Urbanowicz, Tatsuro
Kiuchi, 卤猫 Oamul Lu, Puuung — are in `frontend/src/data/saffron_insights.js`, a
hand-authored constants file with no source and no date.

**Saffron cannot currently say what 500k looks like, because it has never
measured anyone's audience, including the peers it names.** Any honest version of
the `a_following` ladder needs audience figures on comparable artists first.
That is a research pass, and it is a prerequisite, not a follow-up.

## Voice

Third person, describing. `recurring_calendar_engine`'s docstring already sets
the rule and this must follow it: _the page describes; it does not talk to
anyone._

This matters more here than anywhere else in the app. "Post reels daily, name a
series, caption in English, cross-post to Xiaohongshu" is the most chore-shaped
sentence the system could produce, and her profile says plainly not to hand her
admin. The register that works is the one the doors already use — *"Have ready: a
proposal and ten paintings that hang together as one body"* — a description of
what the goal asks for, not an instruction to go and do it.

## Shape of the work

1. **Research pass** — audience figures for the comparable artists. Prerequisite.
2. `engines/strategy_ladder_engine.py` — the task pool, the goals, the ladders,
   and the evidence functions. Authored facts, computed state, one file.
3. `/api/saffron` gains `strategies`; `career_strategy_report`'s single
   `next_milestone` stops being the only answer.
4. `StrategicPathway` becomes a ladder-per-goal component. It already renders
   done / blocking / pending steps, so the shape is largely there.
5. Mark the shared tasks. This is the feature, not a detail.

## Open

- Is the goal set the three above, or four with a book?
- Does she see all ladders at once, or one at a time? Scott, 2026-09-08: show all
  of them, no picking — she has never once saved an input, so anything gated on a
  choice is gated on nothing.
- Does `career_strategy_report`'s tier framework survive this? It is an
  institutional ladder wearing the name of the whole career. It probably becomes
  the evidence source for `gallery_success` rather than the spine of the app.
