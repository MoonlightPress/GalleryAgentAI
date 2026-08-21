# Next phase: identity, then recurrence

_Written 2026-08-20, the night the August pass nearly doubled the catalog._
_**Not scheduled.** Gated on one condition — see "When to start" at the bottom._

This is a design note, not a report. It exists because the August run surfaced a
structural limit that the current roadmap ("improve discovery") does not address.

## The observation

Most opportunities recur annually. The catalog is therefore not an expanding universe —
it is a few hundred institutions that run something every year, plus a thin layer of
genuine one-offs. We are photographing the same orbit repeatedly and filing each photo
as a new planet.

## The measurement

Run on `deploy_data/compact_opportunities.json` (1,394 entries) on 2026-08-20:

- **There is no recurrence field anywhere in the data.** Every key on every entry was
  searched for `recur|annual|edition|frequency|cadence`. Zero hits. The system has no
  concept that anything happens twice.
- **184 entries are the same 80 things repeating**, by year-stripped name stem:
  世界絵画大賞展 ×5, Tokyo Metropolitan Art Museum ×6, Royal Institute of Painters in
  Water Colours ×4, FACE ×4. Each year's edition is a stranger to the last.

Reproduce it by stripping `20\d\d`, `第N回`, `Nth`, `vol. N` from names and counting stems.

## The two steps

**1. Identity.** "TOKAS Open Call 2026" and "TOKAS Open Call 2027" are one entity with two
instances, not two entries. Without this the catalog inflates every year and dedup gets
monotonically harder — the Tokyo Grant title variants and the TABF triplicates were both
this problem in miniature.

**2. Recurrence.** Once instances hang off an entity you have a history, so you can predict
the next opening. The app stops being a feed of what is open and becomes a **calendar of
what is coming**.

## What it changes

**The advice she gets.** From "this is open, apply" to *"TOKAS opens in May, it's February,
the body of work starts now."* That is what a Tier-3-going-on-4 artist actually needs, and
it is already promised in the spec — Saffron's example line in `bible/Bible08.txt` is
literally *"TOKAS has run its open call every May for the past four years."* The promise
exists; the data model under it does not.

**The pipeline splits into three jobs that barely overlap:**

| Job | Cost | What it does |
|---|---|---|
| Maintain the calendar | cheap | For known entities: has next year's edition been announced, did the date move, did the fee change. Fetching known pages, not paying for search. |
| Hunt one-offs | paid, but narrow | Only what a calendar cannot predict — pop-ups, new artist-run spaces, one-time themed calls. |
| Anticipate | free | Pure arithmetic over the calendar. "Opens in May, it's February." No search at all. |

**Discovery spend.** Today discovery spent 204 credits and returned 591 entries, of which
at least 184 were things already held under a different year's name. Every run re-buys a
chunk of what it already owns. With identity, discovery can be told *"you know these 300,
don't bring them back"* and every credit goes to genuinely new work. This is a better
answer to the cost problem than capping `rumor_mill`.

**Absence becomes meaningful.** If something ran every May for four years and it is June
with silence, that is worth surfacing — it moved or it ended. The system currently cannot
notice a thing that *didn't* happen.

**The volume problem dissolves.** 1,100 entries is overwhelming. ~300 institutions, most
dormant until their month comes round, is not. This is the real answer to the
"accumulated possibility" load flagged in the June UX review.

## What it unlocks: a second and third kind of alert

Today Mochi can only say one thing: **"I found new things."** Strangers, in a pile. That
message cannot help being overwhelming, because it scales with how much the internet
coughed up, not with her attention.

Identity + recurrence unlock two more, and they feel completely different:

| Alert | Says | Feels like | Bounded by |
|---|---|---|---|
| **New** (today's only one) | "47 things found" | a pile | how much discovery returned |
| **Reopened** | "3 things you were watching are open again" | a reminder | how many she watches |
| **Opening soon** | "Kyoto Art Center opens in ~3 weeks" | a plan | the calendar |

**Reopened cannot flood her** — it is capped by her own watch list, not by discovery volume.
That is the direct answer to the "accumulated possibility" load: the same catalog, delivered
as returning familiars instead of new strangers.

**Opening soon is the only alert that arrives while there is still time to make work for it.**
For a painter, three weeks' notice is worth more than the announcement itself.

The 2026-08-21 research pass makes the case concrete: of 172 deadlines it found, **114 had
already passed**. Filed as "missed it, hide it" those are waste. Filed as recurrence data
they are next year's calendar — 114 things now known to exist, run on a schedule, with a
known month. The watch list stops being a graveyard and becomes the dataset.

## The hard part — do not underestimate it

Deciding two records are the same thing is genuinely difficult: across years, across
languages, across renamings and translations and abbreviations. The 2026-07-29 dedup work
(`d3209049`, `f99142d8`) was exactly this problem at small scale and it was fiddly. This
is the work of the phase, not a weekend job. Expect to need a review surface where a human
confirms merges rather than trusting the matcher.

## When to start

**Only if Nin keeps coming back.** As of 2026-08-20 the evidence is one real visit
(06:41 JST, from Instagram, ~3 minutes, three opportunities opened, one external click).
That is encouraging and it is not yet a pattern. The test is whether she returns and finds
new things worth opening.

If she does not come back, this phase is not worth building, and the maintenance posture
in `CLAUDE.md` stands.
