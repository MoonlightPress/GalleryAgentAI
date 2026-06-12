# Mochi v2 — Redesign Spec (the alternate build)

Lives in `frontend2/` (port **5178**, proxy `/api` → :8001). `frontend/` stays untouched.
Stack: Vite + React, zero new runtime deps. Hash-based routing (hand-rolled, ~30 lines)
so pages get URLs and a working back button: `#/mochi`, `#/peppercorn`, `#/saffron`.

## The organizing axiom

**She only has to paint and copy/paste emails.** Every screen is judged by: does this
reduce her work to those two things? The most important button in the entire product
is **"Copy email"** — it appears on every actionable card, one click, pre-tailored,
in the right language for the venue.

## The three laws of v2 (from the findings)

1. **Never show a dead date as a live action.** Client-side deadline guard
   (`utils/deadlines.js`): parse; if past → item is excluded from Focus/Best Moves and
   moved to a quiet "Mochi is re-checking these" drawer. No exceptions.
2. **No naked numbers.** Scores render as fit-words with evidence on hover/expand:
   ≥8.5 "Strong fit" · ≥7 "Good fit" · ≥5 "Worth a look" · else "Quiet lead".
   Evidence = three_bullets + verified chips (deadline ✓ / contact ✓ / link ✓).
3. **No amputated sentences.** CSS line-clamp only (word-boundary ellipsis), never
   `slice()`. Where text exists in full, prefer showing the full first sentence.

## Shared shell (all pages)

- **Companion band** (replaces text nav): three painted roundels (cropped from the
  existing hero PNGs in `frontend/src/assets/heroes/`, copied into frontend2) with
  names beneath — Mochi · Peppercorn · Saffron. Active companion: full color + warm
  ring + short voice line under the name. Inactive: 70% opacity, gentle hover wake.
  The animals ARE the navigation (Bible08). Keyboard accessible (buttons, aria).
- **Mochi status strip**: slim, `position: sticky` bottom, persists on ALL pages.
  Content is honest: "Mochi is happy and full" + real signal (e.g., "fresh hunt:
  {date} · {n} things ready") + celebration override when a submission was accepted
  (existing /api/submissions logic). No fake progress bar, no fake mood meter.
- **Language toggle**: 中文 · 日本語 · English, visible top-right of companion band.
- i18n: copy `frontend/src/i18n/` wholesale; new keys added in all three languages
  under a `v2.` prefix (don't collide with old keys).
- Assets: copy `frontend/public/assets` → `frontend2/public/assets`; copy hero pngs
  to `frontend2/src/assets/heroes/`. Painted icons replace ALL emoji in chrome.

### Design system (`src/styles/atelier.css`)
- Tokens (keep + extend): `--paper #FFFAF3, --parchment #EDE5D2, --ink #3d2b20,
  --ink-medium #5d4b3b, --ink-muted #8a7563, --border #e6d4b8, --gold #c49a3e,
  --leaf #7a9e7e, --rose #d4897a`, shadows as today. Add `--wash-amber`, `--wash-leaf`,
  `--wash-rose` translucent washes for section headers; subtle paper-grain overlay on
  body (CSS-only, layered radial-gradients at 2-3% opacity — no image dependency).
- Type: Georgia/serif. Display 1.9rem, section 1.4rem, card title 1.05rem,
  body 0.95rem/1.65. Italic reserved for companion voice lines only (currently
  italics are used for everything, which flattens the voice).
- Primitives: `.card`, `.pill`, `.chip-verified`, `.btn-warm` (gold), `.btn-quiet`
  (outline), `.voice` (companion speech), `.drawer`. No cold blues/greys anywhere;
  the stretch-goal accent becomes plum/rose instead of the current blue-violet.

## Page 1 — Mochi (`#/mochi`)

1. **Hero = Today's Focus, once.** Shorter hero band (~380px) of the desk painting;
   overlaid greeting + Mochi's line: "Mochi found three things worth your attention."
   Directly under it, the three focus cards (Quick Win / High Impact / Stretch — keep
   the time estimates). One rendering of the data, not two.
   - Each card: full-sentence summary + why-it-fits (line-clamped), verified chips,
     deadline rendered ONLY if future (guard law #1), and the action row:
     **[Copy email]** (primary, when a draft exists) · [Open page] · [Details].
   - "Copy email" copies the venue-appropriate language draft (ja for Japan, zh for
     China, en otherwise — same rule as api.py email templates) and toasts
     "Drafted and copied — paste it into Instagram DM or email."
2. **The Hunt Board** — replaces the seven stacked sections. One section, one grid:
   - Filter chips with painted mini-icons: All · Best Moves · Open Calls ·
     Publications · Competitions · Zines & Print · Galleries & Cafés · Watch List
     (counts on each chip). Chips map 1:1 to the existing API buckets.
   - View toggle with equal billing: **Cards | Deadlines** (the calendar timeline is
     promoted, same component logic as v1's DeadlineCalendar — it was already good).
   - Card v2: painted category icon (correct per-category mapping), name, org, city
     pill, fit-word (law #2) with evidence popover, full-sentence why, action row
     (Copy email / Open / Details), and the four feedback actions always visible in
     the card footer at reduced opacity (★ ✓ ◷ ✕) — Peppercorn learns from every
     glance, not only from opened cards.
   - Details expand **in place**: the card grows to span the full row, content stays
     anchored to its card (no orphaned bottom panel). Checklist, bullets, email
     drafts with per-language copy buttons, soft warnings.
   - Stale items (past deadline) live in a collapsed drawer at the bottom: "Mochi is
     re-checking these {n} — they may have closed." Muted styling.
3. **Empty states**: warm copy + small illustration (existing section SVGs in
   public/assets/illustrations).

## Page 2 — Saffron (`#/saffron`)

1. **"From up here" — the synthesis.** Hero band (window painting) then ONE opening
   panel in Saffron's voice that answers the page's question in three short beats,
   composed from live data (/api/saffron + /api/career_strategy):
   - *Where she stands*: confirmed shows/publications count, IG 26k.
   - *What's blocking*: the `blocking_now` sentence (already computed server-side).
   - *What the field looks like*: total opportunities, Tokyo vs international, how
     many are actionable now.
   Three key numbers displayed large beside the prose (shows · ready-now · deadlines
   this month).
2. **The Journey** — the 7-step pathway as a horizontal path (watercolor stepping
   stones): done steps inked, the blocking step marked with Saffron's note. This is
   the page's only big visual. Data: `pathway.steps` (already served).
3. **The Field** — one compact band: category breakdown as warm horizontal bars,
   Tokyo/international split, actionability counts. No SaaS chart library; plain
   divs.
4. **Perch row** — comparable artists as 4 small cards (name, region, one line, what
   to learn from them).
5. **Field Notes** — everything else (the other ~20 sections) becomes a *library*:
   small index cards grouped under five shelves — Audience & Press · Money ·
   Places & People · Timing · The Long View. Clicking opens ONE reading pane at a
   time (accordion-of-one), with Saffron voice subtitles. Keeps every piece of
   research reachable, but the page stops being 24 drawers of equal weight.
   - Mapping: Instagram/Audience/Press/PressPitch → Audience & Press; Pricing/
     Revenue/Licensing/Grants/Collectors → Money; Venues/Collaboration/Geographic/
     Publications → Places & People; Seasonal/Timing/Momentum → Timing;
     Scenarios/Timeline/Benchmarks/Gap/Dependency → The Long View.
6. Career Readiness + Pipeline at a Glance + Momentum collapse into the synthesis
   panel (they all restate the same facts — say it once, well).

## Page 3 — Peppercorn (`#/peppercorn`)

1. **Hero band** (burrow painting) + Peppercorn's line: "Peppercorn keeps your
   answers. He's wondering about a few things."
2. **The Wondering** — front and center: ONE question at a time (reuse the existing
   question component's logic: 8 keys, options, why-this-matters, skip, clear),
   progress as 8 small pebbles. When all answered: "Nothing to ask today. Peppercorn
   is content." This is the page's opening move, not section #4.
3. **What Peppercorn knows** — a compact two-column readout with inline editing:
   artist statement (with the generic-vs-specific example kept), goals (add/check),
   preferences (tiers, track, avoid, geo, fees, more/less — same controls, tighter
   layout, one Save).
4. **The Record Book** — ONE ledger replacing four separate form sections, with tabs:
   Submissions · Exhibitions · Venues & Contacts · Quick log. Shared add-entry row
   (date / name / what / outcome / note), shared outcome color language (warm),
   existing endpoints unchanged. CRM contact cards keep status editing.
5. **Milestones** — replaces the arc carousel: a single quiet strip of honest counts:
   "Group shows 2 of 3 · Publications 2 of 3 · Instagram 26k → 50k · Statement:
   draft". Each with its one-line meaning. No rings, no double fractions.
6. Dismissal-insight banner stays (it's a good feedback loop surface).

## Build phases & ownership (for parallel agents)

- **Phase 1 (orchestrator)**: scaffold frontend2 complete & runnable with shell,
  router, design system, i18n, utils (`api.js`, `deadlines.js`, `fitWords.js`),
  assets copied, placeholder pages. MUST be committed/working before page agents run.
- **Phase 2 (3 parallel agents)**: each owns exactly `src/pages/{mochi|saffron|peppercorn}/`
  (page component + page CSS + subcomponents). Nothing else. They read this spec +
  findings doc first, reuse primitives from atelier.css, add i18n keys ONLY under
  `v2.mochi.*` / `v2.saffron.*` / `v2.peppercorn.*` in their own
  `src/pages/<page>/strings.js` (merged at runtime via i18n helper — avoids three
  agents editing translations.js concurrently).
- **Phase 3 (orchestrator)**: integration, screenshots old-vs-new, fix pass,
  `03_BEFORE_AFTER.md`.

## What v2 deliberately does NOT do

- No backend changes in this build (the /api/today staleness gate is a backend fix —
  documented in 04_LOGIC_EFFECTIVENESS.md; v2's client-side guard makes the UI safe
  regardless).
- No new reports, no new scoring. Presentation + interaction only.
- No invented Peppercorn/Saffron palettes beyond existing tokens (Bible: their visual
  identities are TBD; we stay inside the confirmed atelier tokens).
