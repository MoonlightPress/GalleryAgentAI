# Before / After — the v1 app vs. the v2 alternate build

Both apps run side by side against the same backend (:8001):
- **v1 (untouched):** `cd frontend && npm run dev` → http://localhost:5177
- **v2 (alternate build):** `cd frontend2 && npm run dev` → http://localhost:5178

Screenshots in `shots/` (v1 full-pages captured in zh default; v2 in en — switch
languages live to compare like-for-like).

## The one-sentence difference

v1 is a database of opportunities with a warm skin; v2 is three companions doing
their jobs — Mochi hands you three things and a finished email, Saffron answers
"what's the bigger picture" before you scroll, Peppercorn opens with a question
instead of nine forms.

## What changed, page by page

| | v1 (`frontend/`) | v2 (`frontend2/`) |
|---|---|---|
| Navigation | Text buttons (Discover/Observe/Converse) | **The painted animals are the navigation** (Bible08 realized); real URLs (#/mochi…), back button works |
| Mochi status | Bottom of a 10,000-px page, fake mood meter | **Sticky strip on every page**, honest signals only (real ready-count, real acceptance celebrations) |
| Today's Focus | Rendered twice (hero + section); served year-stale deadlines ("1 July 2025" as today's Quick Win) | Rendered once as the hero; **client deadline guard + backend gate fixed** — only live dates can appear |
| The #1 action | "Details" | **"Copy email"** — one click, venue-appropriate language (ja for Tokyo, zh for Beijing), toast confirms. The whole product now optimizes for *paint, then copy/paste* |
| Opportunity list | 7 identical stacked sections, ~50 cards of equal weight | **One Hunt Board** with painted filter chips + counts; Cards / Deadlines views at equal billing |
| Scores | Naked numbers ("10", "8.8"), three 10s in a row | **Fit-words** (Strong fit / Good fit / Worth a look / Quiet lead) with evidence chips (deadline ✓ contact ✓ link ✓ draft ✓) |
| Truncation | `slice(0,120)` mid-word amputations ("pract…", "zin…") | CSS line-clamp only — sentences end at word boundaries |
| Detail panel | Full-width below the grid, orphaned from its card | **Expands in place** — the card grows; checklist, bullets, tabbed email drafts each with copy buttons |
| Feedback (★✓◷✕) | Hidden until a card is opened | Always visible in card footers — Peppercorn learns from every glance |
| Stale entries | Mixed silently into live sections | Quarantined in a quiet drawer: "Mochi is re-checking these" |
| Saffron page | 24 collapsed accordions; never answers its own question | **"From up here" synthesis** (3 beats + 3 big numbers), Journey stepping-stones (7 steps, blocking step flagged), warm field bars, perch row, then a **5-shelf Field Notes library** — every piece of research kept, none weighted equally |
| Peppercorn page | Settings form: arc carousel with double fractions + ~10 accordions, 4 near-identical ledger forms | **Conversation-first**: The Wondering (one question + 8 pebbles) opens the page; one Record Book with 4 tabs; honest Milestones strip (no rings) |
| Error tolerance | One ErrorBoundary around all 26 Saffron sections (one bad shape blanks everything) | Per-section boundaries on Saffron and Peppercorn |
| Mobile | Untested 3-col grids | Verified at 390×844 on all three pages |
| Emoji chrome | ⭐📅✏️🏆📚🌸👁 next to watercolor art | Painted icon set from `/assets/icons` throughout |

## Backend fixes shipped alongside (api.py + engines)

1. `/api/today` staleness gates (quick-win fallback + all stretch-goal paths) —
   the root cause of the dead-deadline Focus, verified fixed live.
2. Evergreen venues no longer display stale deadline residue as action dates.
3. **~90,000 → ~26,000 follower correction** in `ibm_email_writer.py` and
   `why_it_fits_engine.py` plus all already-generated drafts — outreach emails
   were making a false claim to galleries (90k is her Twitter, not Instagram).

## What v2 deliberately leaves for the next phase

(Ranked plan in `04_LOGIC_EFFECTIVENESS.md`.)
- Real deadline/open-closed verification engine in the pipeline (M)
- Follow-up loop: applied/contacted → 14-day nudge surfacing in Today's Focus (M)
- Today's Focus freshness: done-exclusion, deadline-urgency boost, rotation (S)
- Tailored drafts for all 13 IBM entries (currently 7/13 fully copy/paste-ready) (S)
- Register the weekly scrape scheduler — it has never run (S)
- Server-side localization of strategy strings (blocking_now, step details)
