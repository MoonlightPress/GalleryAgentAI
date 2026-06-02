# Session 7 Status Report
**Date:** 2026-06-03
**Commits this session:** 1dfda4d through 61ce3a5 (9 commits)

---

## What Was Accomplished This Session

Session 7 was the Peppercorn session. The React frontend consolidated into a working three-companion system, the Peppercorn page was designed from scratch in spec form and then rebuilt to match, the conceptual architecture got its clearest documentation yet, and two longstanding pipeline bugs were fixed.

---

### 1. Three Bugfixes at Session Open

Three issues fixed before the main work began.

**NaN in Instagram Strategy (commit 1dfda4d):**
`parseInt("~90k")` returns `NaN` because the tilde prefix stops integer parsing immediately. Introduced `parseFollowers()` — strips `~`, handles `k` suffix via `parseFloat * 1000`, returns `null` on failure. `"~90k"` → 90000, `"21k"` → 21000, ratio = 4. No NaN rendered.

**Nav reorder + Saffron position fix (commit 1154cf5):**
Nav tab order corrected to Discover → Observe → Refine. Separately, the `<Nav>` component was rendering after `<SaffronPage>` in the DOM, so it appeared at the bottom of all Saffron content. Fixed by moving `<Nav>` above the sub-page components in `App.jsx`, while keeping `<HeroSection>` above `<Nav>` for the Discover page.

**Peppercorn checkbox/radio alignment (commit 443796a):**
A duplicate `.pp-check` rule (`margin: 0 auto; display: block`) was scoped globally, overriding the alignment of every checkbox on the page instead of only the surface grid. Scoped to `.pp-surface-row .pp-check`. Changed `align-items: flex-start` → `align-items: center` on rows; removed the `margin-top: 2px` hack that patched the old misalignment.

---

### 2. Bible12 — Peppercorn Page Full Specification (commit fa6bfda)

Before rebuilding the Peppercorn page, the full spec was written in `docs/bible/Bible12.txt` (674 lines, five parts).

**What the spec covers:**
- Philosophy: what Peppercorn is not (form, dashboard, settings panel) — the cozy corner principle
- The carousel: card anatomy (exactly five elements, nothing more), ordering logic (current/next_threshold ratio descending), all 8 card types with full threshold tables and click actions
- All six sections with content specification — Instagram Strategy, Exhibition Pathway, Artist Statement, Saffron's Questions, Career Goals, Preferences — including what each section shows at each completion state
- Visual design: full palette, typography rationale, arc vs. bar reasoning (arcs feel like growth, bars feel like loading), Peppercorn's presence (small, not a banner), Peppercorn's door at four states (deferred: needs illustration asset)
- Tone: nine wrong/right copy examples, "the page never makes her feel behind" as the governing rule

**Key principle documented:** The page receives her contributions quietly. No celebration animation on completing all 8 questions — just Peppercorn's note: "Saffron has everything she needs for now."

---

### 3. Peppercorn Page Complete Rebuild (commit 6bb570d)

Prior state: five fixed sections (Priorities, Artist Statement, Goals, Preferences, Saffron's Questions) in hard order, no carousel, no dynamic ordering, standard radio/checkbox inputs.

**Carousel (new):**
- 7 cards ordered by `current_value / next_threshold` ratio, descending
- Twitter 0.90 → Instagram 0.84 → Publications 0.67 → Artist Statement 0.50 → Group Shows 0.33 → Notes from Saffron → Career Goals
- SVG partial-arc progress indicator on each card (not a bar — spec reasoning: arcs feel like a phase, bars feel like a deadline)
- Card click → smooth scroll + auto-expand target section
- `IntersectionObserver` keeps the active carousel card highlighted as the user scrolls through sections
- Cards with no matching section on this page (Publications) are non-clickable and styled passively

**Dynamic section ordering:**
Sections sort by completion score on each load. Default order for a first-time user:

| Section | Completion Score | Why |
|---|---|---|
| Social Presence | 0.80 | Always informational, always populated |
| Artist Statement | 0.50 | Pre-populated draft exists |
| Exhibition Pathway | 0.40 | Always has 1 show on record |
| Preferences | 0.20 | Defaults set, not reviewed |
| Career Goals | 0.00 | Empty until she adds one |
| Notes from Saffron | 0.00 | Empty until she answers |

Goals and Questions float up as she fills them in on return visits.

**Two new sections:**
- **Social Presence** — threshold analysis for both platforms (Instagram 25k/50k/100k, Twitter 100k), what each threshold means professionally, four specific tactics for her practice (daily diary posts, bilingual captions, etc.), Peppercorn's gentle questions section (not a form — "Peppercorn was wondering")
- **Exhibition Pathway** — current show on record, threshold map 1→2→3→5 with professional significance of each, three specific next-venue targets (3331 Arts Chiyoda, Design Festa Gallery, Gallery IYN) with one-line rationale per venue, timeline note ("2–3 years from mid-2026. This is not slow. This is normal.")

**Artist Statement — before/after example panel:**
Collapsible panel showing a generic statement vs. a specific statement side by side. Purpose: demonstrate the actual stakes of the text field, not just label it as important.

**Mouse illustration:**
Hero image rendered at 200px centered instead of full-width bleed. Matches spec: "a presence in the corner of the frame. Not a mascot banner."

**Tone pass throughout:**
Every label, placeholder, and status message reviewed against the spec's wrong/right examples. "Skip" → "Come back to this". "0 goals entered" → "Peppercorn hasn't heard your goals yet."

---

### 4. Peppercorn Four Refinements (commit 47ead35)

Four targeted changes made after initial review of the rebuilt page.

**Rename "Saffron's Questions" → "Notes from Saffron":**
Updated throughout: section title, carousel card name, subtitle phrasing ("Saffron left 3 notes" not "3 questions").

**Carousel position pin:**
Notes from Saffron pinned to position 2 (after Twitter) regardless of completion ratio. Previously sorted last (0/8 = 0.00) — invisible at the start of the carousel when it matters most. Twitter and Notes from Saffron extracted before sort; remaining cards sort by ratio as before.

**Quick-answer chips:**
Each question now has 3–4 pre-written answer options as pill-shaped buttons above the textarea. Clicking fills the field; fully editable before saving. Answers written to reflect realistic states for this specific artist:
- Posting frequency: "Daily — it's part of my diary practice" / "A few times a week" / "Rarely" / "I'd like to but haven't yet"
- Sales history: "Yes — mostly prints through online shops" / "Yes — originals at art fairs" / "A few informally" / "Not yet"
- etc.

**Two-column layouts:**
Exhibition Pathway restructured to two-column grid: left column holds current show record + threshold list; right column holds next targets + timeline note. Social Presence was already two-column from the rebuild. Both sections now match.

---

### 5. Bible13 — The Desk Metaphor (commit cd42a88)

`docs/bible/Bible13.txt` (301 lines, four parts) documents the psychological model behind the three-page architecture.

**Core claim:** The artist is always at her desk. The companions come to her. Navigation between pages is not switching rooms — it is deciding which companion to pay attention to right now.

**Each companion's mode of arrival:**
- **Mochi** jumps through the open window and drops things on the desk. Sudden, purposeful, feline. She has been hunting. She returns with three things to act on. Not fifty.
- **Saffron** lands on the windowsill and chirps observations. She doesn't come inside. She's been high up and she reports what she saw without advising. She never tells the artist what to do.
- **Peppercorn** lives in the baseboard. He didn't arrive — he has always been here. He has been watching for months. He asks small careful questions from beside the desk.

**Navigation is attention, not travel:**
The wrong model is rooms (artist walks between companion spaces). The right model is focus (artist turns her head). This explains why Mochi's status bar persists across all three pages — Mochi is always on the desk, she is just not always the current focus.

**Design implications documented:**
- "Which companion does this belong to?" as the feature evaluation test
- Each companion's arrival mode as a brief for animation and loading states
- "The artist never asks for help" — companions offer, she accepts or ignores — as the governing copy principle

---

### 6. Daily Digest — Two Pipeline Fixes (commit 61ce3a5)

**Bug 1: BOOOOOOOM urgent deadline not surfacing**

BOOOOOOOM (June 5, 2026) was in the `publication_targets` bucket. The daily digest only read from `immediate_best_moves`. The deadline was 2 days away; it appeared nowhere in the digest's priority section.

Fix: after building the IBM list, scan all non-IBM buckets for opportunities with confirmed deadlines within `URGENT_DAYS = 3`. Any match is promoted to the top of IBM with a note: `⚠ Deadline-promoted from Publication Targets — 2d remaining`. The threshold is a named constant. BOOOOOOOM now appears first in the digest, bolded, with correct fee and link.

**Bug 2: Watch list empty despite next_cycle_watch.json existing**

The watch list code scanned only `stretch_targets` and `research_needed` inside `exclusive_strategy_buckets.json`. It never read `memory/next_cycle_watch.json`, which contains 8 tracked opportunities that have closed and should be re-checked when their next cycle opens.

Fix: loaded `next_cycle_watch.json` separately. All 8 items now appear in a new "Next Cycle — Check Dates" sub-section of the watch list, sorted by `next_cycle_check` date with cycle notes. Existing stretch/research deadline logic unchanged.

Watch list now shows:
- SCCP Guest Artist — check by 2026-08-01 (59d)
- Fukuoka Art Book Fair — check by 2026-10-01 (120d)
- Shangyuan International Residency — check by 2026-10-01 (120d)
- Zine & Book フェス in 神保町 — check by 2026-10-01 (120d)
- Little Tokyo Zine Fest — check by 2026-11-01 (151d)
- National Watercolor Society — check by 2027-01-01 (212d)
- Japan International Watercolor Institute — check by 2027-01-15 (226d)

---

## Current System State

| Layer | Status | Notes |
|---|---|---|
| Discovery | 80% | 179 quality-filtered opportunities in deployment set |
| Ranking | 75% | Watercolor-adjusted, DNA scoring, truth alignment all active |
| Artist DNA | 85% | Profile confirmed with illustration-community context |
| Verification | 35% | Urgent deadline promotion now in digest; watch list populated |
| React Frontend | 75% | Three pages fully built; Peppercorn rebuilt to spec; Saffron 16 sections |
| Reporting | Stable | Daily digest corrected; Saffron page is primary intelligence surface |
| Career | 40% | Scenarios, benchmarks, pathway in Saffron; Bible12+13 document the vision |
| CRM | 10% | 1 venue tracked; Peppercorn input layer now in place |

---

## Conceptual Architecture — Now Documented

Two key documents written this session give the project its clearest design brief yet:

**Bible12** specifies the Peppercorn page exhaustively. It functions as a build contract: any future development on that page should start from this document and deviate only with a documented reason.

**Bible13** establishes the desk metaphor as the governing psychological model for the entire three-companion system. It is the document to give to anyone who asks "why are there three pages?" or "what is each companion for?" and the test for any feature proposal: which companion does this belong to?

---

## Outstanding from Session 6 Priorities

| Item | Status |
|---|---|
| Verify June deadlines (BOOOOOOOM June 5, Women United June 10, ZINEフェス June 27, CSPWC June 30) | BOOOOOOOM now surfaces urgently in digest; others visible |
| Peppercorn page | Done — rebuilt per spec |
| Venue Tracker expansion | Not started — still 1 venue tracked |
| Icon cleanup (4 unmapped icons) | Not started |
| Production server management (port collision) | Not started |

---

## Next Session Priorities

1. **BOOOOOOOM submission** — June 5 deadline. The digest is now showing it correctly. The actual submission (10 images, proposal paragraph, booooooom.com) needs to happen today.
2. **Women United ART MAGAZINE** — June 10 deadline. $25, watercolor accepted, print credit. Straightforward submission.
3. **Venue Tracker** — Add 10–15 venues from the pipeline to contact_memory.json. The Saffron tracker section is built; it needs data.
4. **Peppercorn's door** — The Profile Completeness carousel card is deferred because it needs an illustration asset (four states: door closed, ajar, half-open, wide open). When the asset exists, this is the final carousel card to implement.
5. **Live data feedback loop** — When the artist answers Peppercorn's questions, those answers should surface as updates in Saffron's analysis. The plumbing for this (API save → profile update → Saffron re-read) needs to be wired.
