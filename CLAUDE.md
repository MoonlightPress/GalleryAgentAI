# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

**Mochi** is an AI-assisted artist career support system. The repo is named GalleryAgentAI; the project is named Mochi.

It was built for a real watercolor painter — not a hypothetical user. Her work: urban environments, architecture, memory, absence, atmosphere, quiet observation. That specificity shaped every major architectural decision. When the machine got something wrong, there was a real person to notice.

The central question Mochi must answer is: **"What should this artist do next?"** — not "What exists?" Artists don't lack information. They drown in it. The bottleneck is prioritization and decision-making.

The system is advisory. Humans make all decisions. The system never conducts outreach automatically.

Artist profile lives in `memory/artist_master_profile.json` and `artist_dossier.md`.

## Read Before Touching Code

The Bible files in `docs/bible/` are the canonical reference for why things exist. Read them before making architectural changes. They document 11 phases of development and 14 hard-won lessons, including which ideas failed and why.

The `docs/` numbered files (`00_START_HERE.md` through `09_INSTRUCTIONS_FOR_CLAUDE.md`) are the onboarding sequence.

## Running the App

```powershell
# Primary Streamlit dashboard (production)
python -m streamlit run app.py

# Active full pipeline (72-step, searches root + engines/ + ui/)
python run_full_mochi_pipeline.py

# Legacy 11-step pipeline (original, still functional)
python council_pipeline_agent.py

# Historical artist research
python run_historical_artist_pipeline.py
```

**Required `.env` at project root:**
```
ANTHROPIC_API_KEY=sk-ant-api03-...
TAVILY_API_KEY=tvly-dev-...
```

Install: `pip install -r requirements.txt`

No formal test suite. Validate by running pipelines and inspecting JSON output in `memory/`.

## Architecture

The architecture is a sequence of failures corrected. Each layer exists because the previous one proved insufficient. Do not remove a layer without understanding what problem it was solving.

| Layer | Purpose | Why It Exists | Maturity |
|---|---|---|---|
| Discovery | Find opportunities | Oldest layer — foundation | 80% |
| Ranking | Sort by relevance | Discovery produced too much noise | — |
| Artist DNA | Understand the artist | Generic models produced weak recommendations | 80% |
| Watercolor | Protect painters from photography flood | Visual similarity ≠ professional similarity | 75% |
| Source Purity | Distinguish real opportunities from noise | Archives/catalogs masqueraded as opportunities | 70% |
| Truth Alignment | Anchor scores to evidence | Ranking confidence drifted from reality | 70% |
| Verification | Confirm reality (site alive, submissions open) | Ranked opportunities were often unactionable | 30% |
| Reporting | Communicate findings | — | over-proliferated |
| Career | Transform opportunities into strategy | Opportunities alone ≠ career direction | 20% |
| CRM | Remember relationships | Careers are built through relationships | 5% |

**Overall maturity: 55–65%.** The project is beyond prototype, not yet production-ready.

**Highest priority unfinished system: Verification.** A perfectly ranked opportunity that is closed or unreachable is worthless.

### Active Pipeline

`run_full_mochi_pipeline.py` is the current pipeline (74 steps, 72 present). It uses `smart_pipeline_runner.py` to resolve scripts across: root → `engines/` → `ui/` → `scripts/runners` → `scripts/patches`.

`council_pipeline_agent.py` is the legacy 11-step pipeline — still functional, now superseded.

### State Management

All state is JSON files under `memory/`. No database. Key files:

- `memory/opportunities.json` — master opportunity list
- `memory/contact_memory.json` — CRM / contact tracking
- `memory/artist_master_profile.json` — structured artist profile
- `memory/verified/` — quality-verified subset

### Key Directories

- `engines/` — ~60 specialized reasoning engines; many pipeline steps live here
- `ui/` — Streamlit component modules for `app.py`
- `docs/bible/` — canonical project history and philosophy
- `docs/` — onboarding sequence, README files, pipeline docs
- `archive/dead_code/` — moved dead code (do not delete, do not modify)
- `scripts/patches/` — one-shot migration scripts (likely already run)

### Claude API Usage

Agents call Claude via the Anthropic SDK. Model calls are not cached by default — adding `cache_control` to high-frequency prompts reduces cost significantly. Most agent files include `sys.stdout.reconfigure(encoding='utf-8')` due to Windows terminal encoding requirements.

### UI

`app.py` is production. CSS theming in `styles/generated_visual_upgrade.css`. Card-based, multi-tab layout.

## UI Vision

**This is the north star for all future UI development.** Reference mockups: `Content/ChatGPT Image May 24, 2026, 09_07_39 PM.png` and `09_07_43 PM.png`.

### The Aesthetic

Warm watercolor atelier. The visual language is a cozy artist's studio — cream and warm beige backgrounds, soft botanical illustrations, natural light, books, art supplies, open sketchbooks. Every colour and texture should feel like it belongs in a watercolour painting. The CSS design tokens in `mochi_app.py` (archived) named this palette correctly: `--paper`, `--ink`, `--muted`, `--gold`, `--leaf`, `--rose`. Rounded corners throughout. Georgia serif for headings. No hard edges, no cold greys, nothing that feels like a SaaS dashboard.

### Mochi the Cat

Mochi is a fluffy grey tabby who lives in the atelier. She is the emotional anchor of the interface. She appears as a large watercolour illustration in the hero — sitting on the desk, eyes half-closed, surrounded by art supplies and plants. She has a persistent status bar at the bottom of every page showing her current mood (`Happy + Full + Content`) and a short message (`Mochi is happily napping in the sun. Come back later to feed and play.`). Her presence exists to reduce anxiety. She is not a mascot or gamification trick — she is the reason the interface feels safe rather than demanding.

### Today's Focus — The Hero Section

The most important element on the homepage. Sits in the top-left above the fold alongside the Mochi illustration. Contains exactly **three specific daily actions** — not suggestions, not a list of fifty things, three things the artist can actually do today:

1. Explore 3 new opportunities
2. Draft 1 outreach email
3. Research 1 artist

A "See all quests →" link leads to the full Quests section. This section is the answer to "What should I do today?" and must never be cluttered. Three actions maximum.

The greeting is time-aware and personal: *"Good afternoon, Mochi / let's grow today."*

### Section Cards

Six cards beneath the hero, in this order:

| Section | Purpose |
|---|---|
| **Opportunities** | Discover galleries, residencies, open calls, and more |
| **Suggested Peers** | Artists to follow, connect with, and learn from |
| **Outreach** | Track conversations and manage your outreach |
| **Quests** | Daily and weekly goals to keep your practice moving |
| **Journal** | Capture ideas, reflections, and inspiration |
| **Analytics** | See your progress and patterns over time |

Each card has a small watercolour illustration, a one-line description, and a single action link. Cards are equal-width, same height, gentle shadow.

### Tone

Every word in the interface should be gentle and encouraging. The system is a companion, not a manager. Examples from the mockup: *"let's grow today"*, *"You've got beautiful things to make."* The interface should never make the artist feel behind, overwhelmed, or judged. If a section is empty, the empty state is warm — not a red warning, not a productivity guilt trip.

### What This Means for Code

- Never introduce cold blue/grey colour schemes, dense tables, or aggressive CTAs
- Empty states get warm copy and a small illustration, not "No data found"
- New UI sections follow the card pattern — title, one-line description, watercolour icon, single action link
- The Mochi status bar persists across all pages
- Today's Focus is always three items — the pipeline must surface exactly three actionable items, not a ranked list of fifty

## Career Strategy Framework

GEGYjiji's career is structured in four tiers. **She is currently in Tier 1-2.** All opportunity scoring, bucketing, and recommendations must reflect this.

| Tier | Label | What It Is | Current Phase |
|---|---|---|---|
| **1** | Ambient Visibility | Zine shops, bookshop consignment, café prints, art book fairs, self-publishing. Low-barrier presence-building — work enters circulation without requiring pitching. | **Yes** |
| **2** | Networking | Group shows, artist-run spaces, open calls at accessible Tokyo galleries, community events. Active relationship-building with the people who will matter in 3-5 years. | **Yes** |
| **3** | Credibility | Small institutional shows (TOKAS, BankART1929, Youkobo), juried open calls (Jinny Street, Belladonna, Shoto Museum), Japan Watercolor Society. CV weight. | Not yet |
| **4** | Prestige Targets | Royal Watercolour Society, American Watercolor Society, Cité Internationale des Arts, Asian Cultural Council, Printed Matter, Offprint. For the deep-work year at 30 and beyond. | Not yet |

**Scoring rule:** Tier 1-2 opportunities score at ×1.3–1.4 weight for immediate recommendations. Tier 4 entries are always routed to `stretch_targets` — they must **never** appear in Immediate Best Moves. Tier 4 exists to be tracked and prepared for, not acted on now.

**Why this matters for code:** Any engine that surfaces "what to do today" must respect the current phase. Recommending an RWS open exhibition to a 26-year-old building her first exhibition history is worse than useless — it sets the wrong expectation and wastes attention. The tier framework is the primary guard against this.

The full tier definitions live in `memory/artist_master_profile.json` under `career_strategy`.

## Critical Lessons (Do Not Repeat)

- **More opportunities ≠ more value.** 3 excellent > 100 mediocre. Don't optimize for volume.
- **Photography floods painting.** Visual/thematic similarity between watercolor and photography is real but the professional ecosystems are entirely separate. The Watercolor Layer exists to enforce this. Do not weaken it.
- **Score inflation is real.** The system has repeatedly grown more confident while growing less accurate. Evidence must outweigh prediction.
- **Reports multiply faster than insight.** Do not add a report unless it solves a specific problem. Do not measure progress by report count.
- **Verification > ranking.** Always. A closed opportunity with a perfect score is useless.
- **Actionability is the product.** Every feature should be evaluated against: "Does this help the artist decide what to do next?" If no, it's probably unnecessary.

## Development Posture

The current phase is **consolidation, not expansion.** The roadmap priority order is:

1. Audit (done)
2. Stabilize
3. Improve verification
4. Improve submission discovery
5. Build CRM
6. Build artist career operating system

Do not add features, new scoring layers, or new reports until stabilization is complete.
