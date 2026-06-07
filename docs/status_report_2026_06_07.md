# Mochi — Status Report
**2026-06-07**

---

## What This Document Is

A complete picture of where the system stands, written for handoff to a new Claude session or for your own planning. Read it front to back once. After that, the sections are independent.

---

## What Works

### The card feed (Mochi page)

The main view works end to end. 185 opportunities are visible after cleanup. Each card shows:

- Name, category, city, score
- A one-sentence description
- A "why it fits" line when it adds something beyond the summary (amber border, left-side accent)
- A Details panel with: full overview, green "Why it fits" callout, evidence bullets (from the pipeline's `three_bullets` field — previously silently discarded), email drafts in 3 languages, and a submission prep checklist

The checklist is new as of tonight. It evaluates deadline confidence, fee verification, whether a submission link or email exists, whether the artist statement is on file, whether portfolio images are available, whether a language-appropriate intro email exists, and whether a physical publication (zine/artist book) is needed. Each item shows ✓ ready / ○ check / ✗ missing.

### Feedback system

All four feedback buttons work: Follow ★, Applied ✓, Maybe Later ◷, Not For Me ✕.

"Not For Me" now writes the opportunity ID to `memory/suppressed_opportunities.json`. The suppressed list is checked on every load — dismissed opportunities don't come back.

### Peppercorn page (the mouse)

The Peppercorn tab is the artist-voice side of the system. It has:

- **Artist statement** — text editor, saves to `peppercorn_profile.json`
- **Saffron's questions** — 8 structured questions (Instagram frequency, audience geography, sales history, etc.) with preset option chips and free text, answered one at a time
- **Career goals** — freeform goal list with done/active tracking
- **Preferences** — active career tiers, primary track (publication/gallery/hybrid), avoid filters, geo focus, fee tolerance, surface-more/less per category
- **Exhibition pathway** — read-only view of the 4-step show history tracker with next targets (3331 Arts Chiyoda, Design Festa Gallery, Gallery IYN)
- **Instagram/Twitter strategy** — threshold milestones and tactics
- **Submission log** — NEW as of tonight: form to log date, venue, what submitted, outcome (pending/accepted/rejected/waitlisted/withdrawn). Saves to `memory/submission_log.json`. Colour-coded history list. The API reads it and could be used for re-scoring in future pipeline passes.

All sections save immediately to the backend via `POST /api/peppercorn`. No page reload required.

### Saffron page (the bird)

The Observatory tab works and is data-rich. It shows:

- Career position (confirmed exhibition record, publications, social following)
- Market landscape breakdown (185 opportunities by category, Tokyo vs. international split)
- Peer artists (from `memory/peer_artists.json`)
- Strategic pathway (7 steps toward first solo Tokyo show, blocking step highlighted)
- Instagram/Twitter gap analysis
- Audience geography (flagged as unknown — requires artist to share Insights)
- Career benchmarks (vs. peer range)
- Seasonal opportunity calendar
- Press features (confirmed Bored Panda coverage; art press gap documented)
- Collector ecosystem (gap — pipeline doesn't track buyers)
- Collaboration map (5 Tide from China co-exhibitors named)
- Geographic expansion (by country with pipeline counts)
- Publication landscape (artist book tier hierarchy)
- Long-term scenarios (Gallery Track / Publication Track / Hybrid Track — each with concrete next actions)
- Venue relationship tracker (from `memory/contact_memory.json`)
- Open questions (8 items flagged for Peppercorn)

### Data quality

After the cleanup run earlier in this session:

- **89 entries rejected** (photography calls, poetry presses, internal planning docs that got into the database, duplicates)
- **67 entries had names derived and populated** (previously blank `name` field)
- **40 duplicate-URL rejections** across 25 duplicate groups
- **185 visible opportunities** (down from 245 before cleanup — this is correct; fewer, better)
- `medium_confirmation_gate.py` fixed: no longer confirms opportunities using pipeline-generated `recommended_body_of_work` field (was causing false positives like Porkbelly Press appearing under zines)

---

## What Doesn't Work or Is Incomplete

### Verification (the biggest gap — 30% maturity)

This is the system's most important unfinished layer. The verification problem: an opportunity with a perfect score that is closed, moved, or unreachable is worthless. Right now:

- URL verification runs but coverage is partial
- Deadline verification is thin — many deadlines are flagged "check site" with no confirmed date
- The system has no way to know whether a submission portal is currently accepting entries vs. showing last year's results
- No re-verification schedule — an opportunity verified 3 months ago may have changed

**What it would take:** A targeted re-verification pass that hits the top 50 IBM-eligible opportunities, confirms URL status, looks for a current deadline, and updates `deadline_verified` and `url_verification_status` fields. This is a single focused agent job, 1–2 hours of pipeline work.

### The "Not For Me" button doesn't hide the card immediately

The suppression is saved correctly but the card stays on screen until next page load. The fix is a local state update in `OppCard.jsx` or the parent grid — on `not_for_me` feedback, filter the card out of the rendered list without waiting for a reload.

### Submission log not yet read by the pipeline

The log saves correctly and would be useful for re-scoring (avoid recommending a venue you've already submitted to, or boost venues that previously accepted you), but no pipeline step currently reads `memory/submission_log.json`. This is a future engine — not urgent now.

### CRM (5% maturity)

`memory/contact_memory.json` exists and feeds the Saffron venue tracker, but:
- Only 1 venue tracked
- No UI to add/edit contacts on Peppercorn
- No follow-up reminder system
- No connection between the opportunity cards and the contact record for the same venue

A working CRM needs 15–20 entries minimum to be useful. The Peppercorn page is the right place to build the input UI — one more section (similar to Submission Log) that lets the artist log venue visits, conversations, and follow-up notes.

### Today's Focus — not implemented

The CLAUDE.md describes "Today's Focus" as always exactly 3 items: a Quick Win (5 min), a High Impact Move (30–60 min), and a Stretch Goal. The current Mochi page shows ranked sections, not a curated 3-item focus. This is the biggest gap between the current prototype and the CLAUDE.md vision.

**What it would take:**
1. A backend endpoint that applies the Today's Focus rules: pick the highest-scoring IBM-eligible opportunity as the High Impact Move, pick the easiest (lowest effort, confirmed contact) as the Quick Win, pick a stretch_target as the Stretch Goal
2. A React component at the top of the Mochi page that renders these 3 items in the warm atelier style described in CLAUDE.md
3. A pipeline step that runs selection logic and caches the result

### The Three Companions architecture (not built yet)

The full system (Mochi / Peppercorn / Saffron as navigation anchors, no text tabs, persistent status bar) is documented in `docs/bible/Bible08.txt`. The current navigation is a tab bar with text labels. The illustrated companion animals are not navigation elements yet.

This is a design-and-rebuild task, not a small fix. The current tabs work fine as a placeholder. Do not start this until stabilization is complete.

### Peppercorn page: no "Not For Me" card integration

When the artist marks an opportunity as "Not For Me" on the Mochi page, Peppercorn has no way to know about it or ask "you keep dismissing gallery calls — should I stop surfacing them?" That feedback loop doesn't exist yet.

---

## What You Can Accomplish This Week

These are ordered by value. Each one is completable in a single session.

**1. Fix "Not For Me" immediate hide (30 min)**
In `MochiPage.jsx` or the card grid component, handle the `not_for_me` feedback action locally: remove the card from the rendered list immediately after the feedback button is clicked. No backend change needed — the suppression write already works.

**2. Top-50 verification pass (2 hours)**
Write a targeted verification agent that:
- Takes the top 50 IBM-eligible opportunities from `deploy_data/compact_opportunities.json`
- Fetches each URL and submission_page
- Records `url_verification_status`, `deadline_verified`, and a `last_verified` timestamp
- Writes back to `compact_opportunities.json`

This alone would make the system meaningfully more trustworthy. The checklist item "Submission path confirmed live" would go from ○ check to ✓ ready for real entries.

**3. Today's Focus — 3-item selection (2–3 hours)**
Add a `GET /api/today` endpoint that returns exactly 3 opportunities:
- `quick_win`: category in `_RELATIONSHIP_CATS`, has contact, low effort
- `high_impact`: highest-scoring IBM-eligible that isn't `quick_win`
- `stretch`: highest-scoring `stretch_targets` entry

Then add a `TodaysFocus` component to the top of `MochiPage.jsx` with warm watercolor styling — the 3 cards side by side, each labeled Quick Win / High Impact Move / Stretch Goal.

**4. CRM input on Peppercorn (2 hours)**
Add a `VenueLogSection` to `PeppercornPage.jsx` (same pattern as `SubmissionLogSection`). Form: venue name, type, city, last visited, status (cold/in contact/applied/ongoing), notes. Saves to `memory/contact_memory.json`. Peppercorn's question about whether she's still in contact with her Tide from China co-exhibitors becomes actionable.

**5. Submission log → pipeline re-scoring (1 hour)**
Add a pipeline step that reads `memory/submission_log.json` and:
- Marks opportunities as `already_submitted` if they match a log entry
- Gives a small score boost to opportunities similar to accepted ones
- Flags venues that rejected as `prior_rejection`

---

## What Is Required to Finish the Project

The CLAUDE.md roadmap, in order: Audit → Stabilize → Improve verification → Improve submission discovery → Build CRM → Build artist career operating system.

**Current phase: Stabilization (mostly done).**

Here is what "finished" would mean for each remaining phase, in plain terms:

### Verification (next phase)

Done when:
- Every IBM-eligible opportunity has a confirmed URL status and deadline verified within the last 30 days
- The system re-verifies automatically when the pipeline runs (not just on demand)
- The checklist item "Submission path confirmed live" is accurate for ≥ 80% of visible opportunities

Estimated effort: 2–3 sessions. The verification infrastructure exists; it needs to be made comprehensive and scheduled.

### Submission discovery (following phase)

Done when:
- The system actively searches for new opportunities on a weekly cadence
- New opportunities are ingested, scored, and quality-gated before reaching the feed
- The discovery layer understands the difference between "this gallery exists" and "this gallery is currently accepting submissions"

Currently the system has a scraper and ingestion pipeline but they are run manually and the quality gate (especially the visual-art confirmation gate) still lets through false positives occasionally. The Porkbelly Press issue this session is an example.

Estimated effort: 3–5 sessions, mostly spent improving the quality gate and building a scheduled trigger.

### CRM (after submission discovery)

Done when:
- The artist can log every significant gallery interaction (visit, conversation, submission, outcome) from Peppercorn
- The system surfaces "you visited Gallery X 6 months ago and never followed up" in Today's Focus
- The contact record for a venue links to the opportunity card for that venue

Estimated effort: 2–3 sessions.

### Artist career operating system (final phase)

This is the CLAUDE.md vision fully realized:
- Today's Focus always shows exactly 3 items
- The Three Companions navigation is implemented (clicking the cat/mouse/bird illustration navigates)
- Peppercorn has asked all its questions and uses the answers to personalize recommendations
- The system has a weekly email-style digest summarizing what changed, what's due, and what the artist should do

Estimated effort: 4–6 sessions.

---

## Timeline (Rough)

| Week | Work |
|------|------|
| This week (June 7–14) | Immediate hide on Not For Me · Top-50 verification pass · Today's Focus 3-item endpoint |
| Week 2 (June 14–21) | CRM input on Peppercorn · Submission log → pipeline re-scoring · Scheduled discovery trigger |
| Week 3 (June 21–28) | Full verification coverage · Quality gate improvements · Review and reduce false positives |
| Week 4+ | Three Companions navigation rebuild · Peppercorn personalization loop · Weekly digest |
| End of July | System feature-complete at 80% maturity across all layers |
| End of August | 90%+ maturity, ready for daily use as primary career tool |

This timeline assumes one working session (1–3 hours) every 2–3 days, focused on the roadmap order above. The system is already useful now — the weekly sessions improve it incrementally rather than building from scratch.

---

## File Map (Key Files Only)

```
api.py                          — FastAPI backend, all endpoints
deploy_data/compact_opportunities.json  — master opportunity list (185 visible)
memory/
  artist_master_profile.json    — structured artist profile
  peppercorn_profile.json       — artist answers and preferences (from UI)
  suppressed_opportunities.json — IDs dismissed with "Not For Me"
  submission_log.json           — submission history log (new)
  contact_memory.json           — CRM contacts
  peer_artists.json             — comparable artists
frontend/src/
  components/OppCard.jsx        — opportunity card component
  components/OppDetailPanel.jsx — expanded card detail
  components/PeppercornPage.jsx — entire Peppercorn page
  components/SaffronPage.jsx    — Saffron observatory (reads /api/saffron)
  components/MochiPage.jsx      — main opportunity feed
docs/bible/                     — canonical project history (read before changes)
engines/                        — ~60 pipeline reasoning engines
```

---

## For the Next Claude Session

Start by reading `CLAUDE.md` (project instructions) and `docs/bible/Bible08.txt` (Three Companions vision). The current working stack is:

- Frontend: Vite/React on localhost:5177 (`cd frontend && npm run dev`)
- Backend: FastAPI/uvicorn on localhost:8001 (`python -m uvicorn api:app --host 127.0.0.1 --port 8001`)
- All state in JSON files under `memory/`

The most impactful single thing to do next is the immediate-hide fix for "Not For Me" (30 min, all in `MochiPage.jsx`) followed by the top-50 verification pass. Both make the system more trustworthy without touching any existing architecture.

Do not add new scoring layers, new reports, or new pipeline steps until verification is at 70%+ maturity. The current problem is not that we're missing analysis — it's that we can't trust the analysis we have.
