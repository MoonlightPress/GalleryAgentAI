# Mochi UX Pass — Findings (2026-06-13)

Scope: all three companion pages of the React frontend (`frontend/`), reviewed against
the Bible vision (Three Companions, CLAUDE.md), the codebase, and live screenshots of
the running app (Vite :5177 → FastAPI :8001). Screenshots referenced are in
`C:\Users\ScotA\AppData\Local\Temp\mochi_shots\`.

Verdict up front: the bones are good — warm palette, real illustrations, the
three-slot Today's Focus, the deadline calendar. But the app currently reads as a
*database with a nice hat*. The companions exist as hero images, not as presences.
And one data-trust failure undermines the entire product promise on first paint.

---

## A. Critical (trust-breaking)

### A1. Today's Focus surfaces dead deadlines as today's actions
Visible on first load (`en_todays_focus.png`): Quick Win = UTRECHT "📅 1 July 2025";
Stretch Goal = "2026 Global Grant Cycle … 📅 November 19, 2025". Today is June 2026.
The single most prominent recommendation in the product is a year stale.

- Root cause: `/api/today` selects focus slots without the `_ibm_eligible()` /
  `_deadline_past()` gate that `bucket()` applies to Immediate Best Moves
  (`api.py:240-252` gate exists; the today-slot builder doesn't use it).
- The Bible's own #1 lesson: **Verification > ranking. A closed opportunity with a
  perfect score is useless.** The UI must never present a past date as a current action.
- Fix (engine rule, per Data Patch Rule): today-slot candidates must pass the same
  eligibility gate; UI additionally renders a guard state ("deadline passed — being
  re-checked") if a stale item ever leaks through.

### A2. Scores read as fake confidence
Cards show a bare numeric badge ("10", "8.8") with no scale, no tooltip, no evidence
(`OppCard.jsx:131-135`). Three cards in a row all scored "10" (`en_ibm_section.png`).
The Bible explicitly warns: *score inflation is real; evidence must outweigh
prediction.* A naked "10" with no justification is exactly the failure mode the Truth
Alignment layer was built to stop — re-introduced at the presentation layer.

### A3. Machine-truncation everywhere
`summary.slice(0,120)` and `why.slice(0,100)` chop text mid-word: "your daily
watercolor pract…", "artist books or zin…" (`TodaysFocus.jsx:78-82`). Every card on
the page displays amputated sentences. Nothing says "a machine generated this and
nobody read it" louder. Use CSS `-webkit-line-clamp` (word-boundary ellipsis) or
serve pre-written short lines.

---

## B. The vision gap (Bible08 vs. what's built)

### B1. The animals are not the navigation
Vision: *"clicking a companion illustration takes you to their page. There are no
text tabs."* Built: three text buttons (Discover / Observe / Converse) + a quick-nav
row (`Nav.jsx`). The companions' names appear nowhere in navigation; their portraits
appear only as oversized hero banners on their own pages. The single most distinctive
design idea in the spec is unimplemented.

### B2. Mochi's status bar is not persistent
Vision: status bar *"persists across all three pages as the emotional anchor."*
Built: `StatusBar` is the last element of a ~10,000px page (`App.jsx:50`) — you meet
Mochi's mood only if you scroll past ~40 opportunity cards. It also shows three
hardcoded mood pills + a decorative progress bar that means nothing (`StatusBar.jsx:66-75`)
— a sentiment-meter with no data behind it, which is the cute version of score inflation.

### B3. Duplicate Today's Focus
The hero overlay lists the same 3 items (`HeroSection.jsx:50-88`) that the Today's
Focus section repeats immediately below (`TodaysFocus.jsx`). Two renderings of the
same data within one viewport, with different layouts and different truncations.

---

## C. Page-by-page

### C1. Mochi (Action) — a feed pretending to be a ritual
- **Seven identical stacked sections** (Immediate Best Moves → … → Watch List), each
  a 3-card grid + "Show more · N more". The page *structurally* says "here are 50
  things," while the Bible says the product is *three excellent things*. The further
  you scroll, the more it becomes the thing it was built to replace.
- Detail panel opens full-width *below the grid row* (`OppSection`), so it's visually
  orphaned from the card that opened it; opening card #1 reflows everything.
- Feedback actions (★ Follow / ✓ Applied / ◷ Maybe / ✕ Not for me) are hidden until a
  card is opened (`OppCard.jsx:197`). This is Peppercorn's entire learning signal,
  buried two clicks deep.
- The deadline **calendar view is excellent** (date-grouped, "Tomorrow"/"in 3 days"
  urgency chips) but hidden behind a tiny toggle; it deserves first-class placement.
- Identical placeholder icon on every card (same image regardless of category) —
  `/assets/icons/` has a painted per-category set, but most map to the same few files.
- Emoji section icons (⭐📅✏️🏆📚🌸👁) sit cheaply next to watercolor art.
- Section quick-nav ("Cafés" and "Galleries" both scroll to `relationship_targets`,
  "Residencies" → watch_list) — labels promise more precision than exists.

### C2. Saffron (Observatory) — a filing cabinet, not a window
- **24 stacked accordion sections**, almost all collapsed (`SaffronPage.jsx:1552-1578`,
  `saffron_full.png`). Career Position, Pipeline at a Glance, Market Landscape,
  Comparable Artists, Pathway, Instagram Strategy, Audience Geography, Benchmarks,
  Seasonal Calendar, Press, Collectors, Collaboration, Geographic Expansion,
  Publications, Scenarios, Venue Tracker, Open Questions, Momentum, Timing, Timeline,
  Pricing, Gap Analysis, Licensing, Press Pitch, Grants, Revenue, Dependency Map.
  This is the Bible's "reports multiply faster than insight" lesson rendered as UI.
- The page never answers its own question — *"what does the bigger picture look
  like?"* — anywhere. You must open drawers and synthesize it yourself.
- Redundancy: Career Readiness (top panel) vs. Strategic Pathway vs. Career Momentum
  vs. Career Benchmarks all restate "2 group shows done, need 3-4, solo show later."
- Saffron's voice (*"From up here, here are three artists doing similar work…"*) is
  absent; headings are SaaS-dashboard nouns ("Opportunity Gap Analysis", "Career
  Dependency Map") — the exact register CLAUDE.md forbids.

### C3. Peppercorn (Input) — a settings form, not a conversation
- The carousel of progress arcs shows confusing double values ("2/8 / 8/8") and
  near-empty rings that read as broken (`en_pepper_carousel.png`,
  `buildCarouselCards`).
- Below it: ~10 more accordions (statement, goals, questions, preferences,
  submission log, exhibition log, venue log, CRM contacts, event quick-log). Four of
  these are near-identical "date / name / outcome / notes" ledger forms — they should
  be one record book with tabs.
- The one genuinely Peppercorn-shaped component — **Saffron's questions, asked one at
  a time with "why this matters"** — is buried mid-page as section #4. It is the
  spine of what this page is for ("asks quiet questions and remembers the answers")
  and should *be* the page's opening move.
- The "Peppercorn is wondering" sidebar (visible in Social Presence) is exactly the
  right voice. It exists in one section only.

---

## D. Structural / technical (UX-relevant)

- **No router**: pages are `useState` (`App.jsx:34`) — no URLs, no back button, no
  deep links, refresh always returns to Mochi. A link "look at this opportunity"
  cannot exist.
- **Monoliths**: PeppercornPage.jsx 2,021 lines; SaffronPage.jsx 1,584; SaffronPage.css
  2,525. One typo risks a whole page (there is a single ErrorBoundary around all 26
  Saffron sections — one bad section blanks them all, `SaffronPage.jsx:1550`).
- **Static "insights" baked into JS** (`data/saffron_insights.js`, 869 lines; plus
  hardcoded pathway/career data inside `api.py:1067-1255`) — content updates require
  code deploys; contradicts the JSON-state architecture.
- Default language on load is zh — verify that's intended for the artist (likely yes;
  keep, but the lang toggle is unlabeled small text top-right).
- Mobile: untested by the current build (3-col grids, 1440px hero). The artist will
  open this on her phone. Needs a real responsive pass.
- `/api/today` and `/api/career_strategy` exist in api.py beyond line 1255 (not fully
  audited this pass; today-slot gate issue confirmed from rendered output).

## E. What is already right (do not lose in v2)

- The warm token system (--paper/--ink/--gold/--leaf/--rose) and Georgia serif.
- The three hero illustrations (cat/desk, mouse/burrow, bird/window) — genuinely
  beautiful, correct characters.
- Three-slot Today's Focus concept with time estimates (5 min / 30-60 min / longer).
- Deadline calendar view (date-grouped, urgency chips).
- One-question-at-a-time Saffron questions with "why this matters."
- "Peppercorn is wondering" sidebar voice.
- Eligibility gating + suppression + submission-log awareness in `/api/opportunities`.
- Email drafts in three languages per opportunity, checklists per opportunity.
- i18n coverage (zh/ja/en) across nearly everything.

## F. Note on the build moratorium

CLAUDE.md says the Three Companions UI is "do not build yet — stabilization first."
The user has explicitly directed an alternate build tonight, isolated in `frontend2/`,
leaving `frontend/` untouched. That satisfies the spirit (the working model is not
destabilized) while finally expressing the documented vision.
