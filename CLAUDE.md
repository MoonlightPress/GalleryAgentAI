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

**The north star for all future UI development is the Three Companions architecture.** Full specification: `docs/bible/Bible08.txt`. Reference mockups: `Content/ChatGPT Image May 24, 2026, 09_07_39 PM.png` and `09_07_43 PM.png`.

**Do not build yet.** The current phase is stabilization. The vision is documented here so all future work is oriented correctly.

### The Three Companions

The system has three pages, each anchored by a companion animal. Navigation between them is visual — the animal illustrations are the nav, not text tabs.

| Companion | Page | Mode | Answers |
|---|---|---|---|
| **Mochi** (cat) | Action | Opportunity hunting, legwork done, ready to act | "What should I do today?" |
| **The Mouse** | Input | Artist goals, statement, preferences, feedback | "Is this system understanding me correctly?" |
| **The Bird** | Observatory | Market view, statistics, comparable artists, context | "What does the bigger picture look like?" |

**Mochi's status bar** ("Mochi is happy and full") persists across all three pages — she is the emotional anchor of the whole system.

### Mochi — The Cat (Page 1: Action)

Mochi has done the legwork while the artist was away. The pipeline has run. Opportunities are sorted. Emails are drafted. When the artist arrives, three things are ready.

- **Personality:** Watchful, patient, precise. Does not chase carelessly. Produces three options, not fifty.
- **Content:** Today's Focus (always exactly 3 actions), Immediate Best Moves (open calls + relationship targets), submission queue, next email drafts, watch list
- **Palette:** Warmest of the three — cream, amber, ochre, aged paper. The existing Mochi illustration (grey tabby, desk, art supplies) is correct.
- **Tone:** *"Mochi found three things worth your attention today."* / *"Nothing urgent. Come back tomorrow."*

The current `app.py` is a working prototype of this page.

### The Mouse — Artist Input (Page 2: Reflection)

The Mouse is where the artist's voice enters the system. Without this page the system is a monologue. The Mouse asks quiet questions and remembers the answers.

- **Personality:** Small, thorough, shy but persistent. Notices what the artist lingered on, skipped, pushed away.
- **Content:** Artist statement, monthly goals, career phase, recommendation feedback ("not this kind / more like this"), portfolio body definitions, preference review, private notes
- **Palette:** Cooler and more intimate — pale paper-white, dusty rose, pencil-grey, soft green. Delicate pencil-drawn aesthetic.
- **Tone:** *"Does this kind of opportunity feel right to you?"* / *"You skipped five gallery calls last month. Should I stop surfacing them?"*

This page does not exist yet.

### The Bird — Observatory (Page 3: Context)

The Bird sees patterns the artist cannot see from the ground. Non-interventionist. Reports without judging.

- **Personality:** Observant, patient, long-horizon. Perches and watches. Does not advise — describes.
- **Content:** Comparable artists, opportunity landscape, market context, career statistics, score trends, peer activity
- **Palette:** Coolest of the three — silver-grey, pale blue, morning mist. Still warm paper texture but wider and airier.
- **Tone:** *"From up here, here are three artists doing similar work in Tokyo right now."* / *"TOKAS has run its open call every May for the past four years."*

This page does not exist yet.

### The Aesthetic (All Three Pages)

Warm watercolor atelier across all three pages, with palette variations per companion. The CSS design tokens named in `mochi_app.py` (archived) — `--paper`, `--ink`, `--muted`, `--gold`, `--leaf`, `--rose` — remain correct for Mochi's page. Georgia serif headings throughout. No hard edges, no cold greys, nothing that feels like a SaaS dashboard.

### What This Means for Code

- The three-companion structure supersedes the six-card single-page layout described in earlier versions of this file
- The current `app.py` becomes Mochi's page when the rebuild happens — do not conflate it with the whole system
- The Mouse is the missing feedback loop; nothing should be built that assumes the system knows the artist's preferences without it
- The Bird is the missing market context; statistics and analytics belong there, not on Mochi's action page
- The Mochi status bar persists across all three pages
- Today's Focus is always three items — the pipeline must surface exactly three actionable items, not a ranked list of fifty
- Never introduce cold blue/grey colour schemes, dense tables, or aggressive CTAs on any of the three pages
- Empty states get warm copy and a small illustration, not "No data found"

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
