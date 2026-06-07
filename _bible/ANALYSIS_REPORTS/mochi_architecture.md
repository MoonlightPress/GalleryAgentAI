# Mochi Architecture Report
**Prepared:** 2026-06-04  
**Source:** Systems Architect analysis of C:\ScottStuff\GalleryAgentAI\  
**Audience:** Pip — identifying marketing-relevant tools for Moonlight Press studio use

---

## 1. What Mochi Is

Mochi is an AI-assisted artist career support system built for a specific real person: GEGYjiji, a 26-year-old Chinese watercolor painter based between Tokyo and Beijing (~90k Twitter, 21k Instagram, 1 Japan exhibition on record, 2 publications).

**The problem it solves:** Artists are not suffering from information scarcity. They are drowning in information. The real bottleneck is prioritization, emotional burden, and deciding where to spend limited time and energy. Mochi's central question is: "What should this artist do next?" — not "What exists?"

**Who it is for:** Built for one artist. The architecture is documented as adaptable to other artists or creative professionals, but the current implementation is entirely specific to GEGYjiji's career, goals, ecosystem (Tokyo/Beijing/international), and medium (watercolor, works on paper, zines/artist books).

**What it is not:** Not a CRM. Not a portfolio site. Not a spam engine. Not an opportunity database. The system never conducts outreach automatically. Humans make all decisions. The system is advisory.

**The long-term vision (documented, not yet built):** An "Artist Career Operating System" — a full operating system for an artist's professional life, spanning daily action, weekly planning, relationship management, submission strategy, and long-horizon career development.

---

## 2. System Architecture Overview

The project has two parallel architectures that are actively in use simultaneously:

### Architecture A: The Streamlit Pipeline System (older, Python-native)
The original system. A Python backend with ~80 standalone agent scripts, a 74-step pipeline orchestrator, and a Streamlit dashboard frontend. All state is JSON files. No database. This is where the actual AI work runs.

### Architecture B: The React/FastAPI Deployed System (newer, production)
A React SPA frontend + FastAPI backend, built from Session 6 onward. This is the "production" UI the artist actually uses. It reads from pre-built JSON data files (`deploy_data/compact_opportunities.json`) and serves them through a typed API (`api.py`). The pipeline writes data; the API serves it.

**The relationship between them:** The Streamlit pipeline does the research and scoring work. Its output files (especially `deploy_data/compact_opportunities.json`) feed the React/FastAPI app. The React app is the user-facing interface. The Streamlit `app.py` is a developer/operator dashboard for inspecting pipeline state.

### Key Components Map

```
Pipeline Layer (Python, operator-run)
  run_full_mochi_pipeline.py (74 steps)
  ├── engines/ (~80 engine files)
  │   ├── Discovery engines (web scraping, Tavily search)
  │   ├── Scoring/ranking engines
  │   ├── Verification engines
  │   ├── Outreach/draft generators
  │   └── Reporting engines
  └── smart_pipeline_runner.py (resolves scripts across dirs)

Data Layer (JSON files, no DB)
  deploy_data/compact_opportunities.json   ← primary opportunity set
  memory/artist_master_profile.json        ← artist profile
  memory/contact_memory.json              ← CRM (1 entry)
  memory/peer_artists.json                ← comparable artists
  memory/exclusive_strategy_buckets.json  ← bucket assignments
  memory/rumor_mill.json                  ← research cache

API Layer (FastAPI, production)
  deploy_package/app/api.py
  ├── GET /api/opportunities  ← bucketed opportunity data
  ├── GET /api/saffron        ← intelligence/context data
  ├── GET /api/peppercorn     ← artist profile/goals
  ├── POST /api/feedback      ← card action recording
  ├── POST /api/peppercorn    ← artist preference saving
  └── GET /api/health

Frontend Layer (React SPA, Vite)
  frontend/src/
  ├── Mochi page (Action)      ← opportunity cards, today's focus
  ├── Peppercorn page (Input)  ← artist goals, preferences, feedback
  └── Saffron page (Context)   ← market intelligence, career analysis

Streamlit Dashboard (operator/developer)
  app.py                       ← primary Streamlit dashboard
  stable_atelier_portal.py     ← minimal stable fallback
  atelier_portal.py            ← another variant
  mochi_deploy_app.py          ← deploy-focused variant
```

---

## 3. Data Layer

**No database.** Everything is JSON files. This is a deliberate architectural choice documented in CLAUDE.md.

### Primary Data Files

| File | Contents | Status |
|------|----------|--------|
| `deploy_data/compact_opportunities.json` | Master opportunity set served to the React frontend. ~286 entries as of Session 8. Includes scores, categories, deadlines, email drafts, verification status. | Active — the production data file |
| `memory/artist_master_profile.json` | Structured artist profile: demographics, visual profile, dominant subjects, motifs, composition patterns, color palette, emotional tone, career history, social presence, career strategy tiers | Active, well-populated |
| `memory/contact_memory.json` | CRM-style contact tracking. Currently 1 entry (KAYOKOYUKI gallery). Has fields for status, last contacted, next action, CRM analysis. | Active but nearly empty |
| `memory/peer_artists.json` | List of comparable artists with fit scores and shared traits. Used by Saffron page. | Active |
| `memory/exclusive_strategy_buckets.json` | Opportunity bucket assignments: immediate_best_moves, publication_targets, stretch_targets, relationship_builders, research_needed, reject | Active |
| `memory/rumor_mill.json` | Cache of research searches on needs_research items. 7-day cache window. | Active |
| `memory/next_cycle_watch.json` | Closed opportunities with future check dates. 8 entries tracked. | Active |
| `memory/artist_intelligence.json` | AI-generated artist intelligence output | Generated by pipeline |
| `memory/watercolor_artist_profile.json` | Hand-authored watercolor-specific positioning profile | Active |
| `memory/pathway_progress.json` | Career questline progress tracking | Generated |
| `memory/generated_analysis/` | Per-opportunity markdown analysis files, numbered 004–046+ | Generated by pipeline, many duplicate-numbered |

### Legacy/Superseded Files

| File | Status |
|------|--------|
| `Memory/opportunities.json.txt`, `Memory/artist_profile.json.txt` | Original Phase 1 files, preserved as .txt references |
| `memory/opportunities_phase1_backup.json` | Phase 1 backup |
| `memory/contact_memory_phase1_backup.json` | Phase 1 backup |
| `memory/opportunities_master.json` | Older master list, superseded by compact_opportunities.json |

### Deploy Package Data

`deploy_package/app/` contains a production snapshot:
- `deploy_data/compact_opportunities.json` — production opportunity set
- `memory/artist_master_profile.json` — production artist profile
- `memory/contact_memory.json` — production CRM (1 entry)
- `memory/peer_artists.json` — production peer artists

---

## 4. Agent and Pipeline Inventory

### Active Pipelines

**`run_full_mochi_pipeline.py`** — The current 74-step pipeline. Runs via `smart_pipeline_runner.py` which searches root → `engines/` → `ui/` → `scripts/runners` → `scripts/patches`. Key steps in order:

| Step Range | Function |
|-----------|----------|
| 1–11 | Ingestion: web scraping, candidate extraction, quality gate, importer, URL verification |
| 12–20 | Medium/type filtering: Japanese/Chinese discovery, watercolor profile building, painting discovery, quality gate |
| 21–32 | Scoring: truth checking, source purity, medium classification, DNA boost, deep match scoring, lineage scoring |
| 33–39 | Intelligence: feedback learning, preference rescoring, portfolio match, submission strategy, score sanity |
| 40–50 | Ecosystem: rumor mill, career strategy, differentiation, artist ecosystem mapping, peer artist engine, publisher matching |
| 51–65 | Advanced: fit audit, institution network, discovery, curator intelligence, daily quests, opportunity report |
| 66–74 | Outreach: inquiry drafts, portfolio pitches, cover letters, timeline, strategy explainer, final guard, email/exhibition/project engines |

**`council_pipeline_agent.py`** — The legacy 11-step pipeline (discovery → ranking → filter → submission packet → council scoring → compact view). Still functional, now superseded. More conservative; skips many new engines.

**`career_intelligence_pipeline.py`** — A 6-step career-focused pipeline: career reconstruction → artist graph builder → trajectory scoring → ecosystem bridge → compound scoring → fast local pipeline.

**`artist_intelligence_pipeline.py`** — Standalone artist intelligence pipeline.

**`mochi_mouse_pipeline.py`** — Named for the Mochi/Mouse pairing. Contents not inspected in detail; likely a focused subset.

### Key Engine Files (by layer)

**Discovery / Ingestion**
| Engine | What it does | Maturity |
|--------|-------------|----------|
| `engines/web_ingestion_engine.py` | Web scraping with BeautifulSoup; reads from `source_targets.json`; outputs to `ingestion/scraped_pages.json` | Working |
| `engines/japanese_chinese_discovery_engine.py` | Tavily searches across JP/CN art communities (Twitter, note.com, Weibo, Lofter, Zcool, Bijutsutecho); 31 queries across JP/CN/Diaspora groups; 7-day cache | Working — tightened in Session 8 |
| `engines/global_opportunity_expander.py` | Global opportunity discovery beyond Tokyo | Working |
| `engines/approved_candidate_importer.py` | Imports quality-gated candidates into main opportunity set | Working |
| `engines/url_verification_engine.py` | HEAD requests to verify submission URLs; tags dead/OK/error | Working (30% complete) |

**Scoring / Intelligence**
| Engine | What it does | Maturity |
|--------|-------------|----------|
| `engines/artist_dna_engine.py` | Hand-authored artist DNA profile (visual language, mediums, career contexts, strong/weak opportunity types). Static document, not ML. | Working — 80% |
| `engines/watercolor_artist_profile_engine.py` | Watercolor-specific positioning profile; excludes photography pollution | Working — 75% |
| `engines/score_sanity_engine.py` | Caps inflated scores based on verification evidence. Formula: no source → max 6.5; verified URL + no details → max 8.6; full verification → max 9.4 | Working |
| `engines/exclusive_strategy_bucket_engine.py` | Assigns opportunities to strategy buckets (immediate_best_moves, publication_targets, stretch_targets, etc.) using keyword + category logic | Working |
| `engines/medium_confirmation_gate.py` | Confirms medium matches before including in recommendations; 185 of 286 confirmed as of Session 8 | Working |
| `engines/feedback_learning_engine.py` | Reads relationship_memory.json positive/negative states; produces learned_artist_preferences.json | Working |
| `engines/lineage_scoring_engine.py` | Historical/legacy scoring layer | Working |
| `engines/portfolio_match_engine.py` | Matches opportunities against portfolio bodies | Working |
| `engines/deep_match_scoring_engine.py` | Deep match scoring (optional in pipeline) | Working |
| `engines/rumor_mill_engine.py` | Weekly research engine: Claude + Tavily; searches needs_research items in EN/JP/CN; populates missing fields or logs "no data found" | Working — key tool |
| `engines/rumor_mill_propagation_engine.py` | Propagates rumor mill findings | Working |

**Ecosystem / Career**
| Engine | What it does | Maturity |
|--------|-------------|----------|
| `engines/peer_artist_engine.py` | Scores peer artists from seed data against visual profile; outputs ranked peer list | Working |
| `engines/artist_ecosystem_mapper.py` | Maps artist ecosystem relationships | Partial |
| `engines/career_strategy_engine.py` | Applies career stage bucketing and strategic labeling; reads `career_stage_profiles.py` | Working |
| `engines/career_path_engine.py` | Career path modeling | Partial |
| `engines/career_pathway_engine.py` | Career pathway computation | Partial |
| `engines/daily_quest_generator.py` | Generates daily quests for the artist | Working |
| `engines/daily_digest_report.py` | Comprehensive daily digest with urgent deadline promotion, watch list, IBM summary | Working — fixed in Session 7 |
| `engines/curator_intelligence_engine.py` | Curator personality and intelligence modeling | Partial |
| `engines/institution_network_engine.py` | Maps institution relationships and networks | Partial |
| `engines/serendipity_engine.py` | Surfaces unexpected but relevant opportunities | Partial |
| `engines/reputation_engine.py` | Reputation and credibility scoring | Partial |

**Outreach / Drafting**
| Engine | What it does | Maturity |
|--------|-------------|----------|
| `engines/inquiry_draft_generator.py` | Generates inquiry email drafts for venues missing key information (contact, deadline, submission process); template-based | Working |
| `engines/smart_cover_letter_engine.py` | Structure + tone guidance for cover letters; uses opportunity's `why_this_fits_short` and `recommended_body_of_work` | Working — template only |
| `engines/portfolio_pitch_generator.py` | Portfolio pitch generation | Working |
| `engines/next_email_engine.py` | Generates next email drafts for tracked contacts | Working |
| `engines/next_exhibition_engine.py` | Identifies next exhibition targets | Working |
| `engines/summary_translation_engine.py` | Translates opportunity summaries to ZH/JA | Working |

**Reporting**
| Engine | What it does | Maturity |
|--------|-------------|----------|
| `engines/opportunity_report_engine.py` | Generates per-opportunity analysis reports | Working |
| `engines/analysis_cache_builder.py` | Builds analysis cache for UI display | Working |
| `engines/research_queue_report.py` | Report on research queue status | Working |
| `engines/global_research_queue_builder.py` | Builds global research queue | Working |
| `engines/ecosystem_report.py` | Ecosystem analysis report | Partial |

### Root-Level Agents (older, many superseded)

Approximately 40+ standalone agent files exist at the root level. The majority are superseded by the engines/ system. Active/relevant ones:

| Agent | Status |
|-------|--------|
| `opportunity_discovery_agent.py` | Legacy discovery; used in council_pipeline |
| `council_agent.py` | Legacy Claude-based council scoring | 
| `incremental_council_agent.py` | Cached council scoring for new opportunities only |
| `compact_view_agent.py` | Builds compact view JSON |
| `opportunity_ranking_agent.py` | Legacy ranking |
| `outreach_email_agent.py` | Legacy email drafting |
| `career_reconstruction_agent.py` | Career history reconstruction |
| `trajectory_scoring_agent.py` | Career trajectory scoring |
| Many others | Mixture of partially active, superseded, and never-run |

---

## 5. Frontend

### React SPA (Production)

**Technology:** React 18, Vite, plain CSS. No component library. Custom CSS with CSS variables (`--paper`, `--ink`, `--gold`, etc.).

**State:** Built in Sessions 6–7. Three pages fully implemented as of Session 7.

**Structure:** `frontend/src/` with `main.jsx` as entry point, `App.jsx` as root. Individual page components per companion. `frontend/dist/` contains a built copy. `deploy_package/www/` contains the production build with all assets.

**Pages:**

| Page | Status | Notes |
|------|--------|-------|
| Mochi (Discover/Action) | Working, 75% | Opportunity cards organized into 5 sections (Immediate Best Moves, Open Calls, Zines & Print, Relationship Targets, Watch List). Cards expand/collapse. Four feedback actions (Follow, Applied, Maybe Later, Not for Me). Email draft tabs (ZH/JA/EN). Score badges, verification indicators. |
| Peppercorn (Refine/Input) | Working, 65% | Full rebuild in Session 7. Carousel with 7 cards ordered by completion ratio. Six sections: Social Presence, Artist Statement, Exhibition Pathway, Preferences, Career Goals, Notes from Saffron. SVG arc progress indicators. Quick-answer chips. Dynamic section ordering. |
| Saffron (Observe/Context) | Working, 70% | 16 collapsible sections. Real data in most. Built from hardcoded analysis in `api.py` + `compact_opportunities.json` + `peer_artists.json`. |

**Saffron's 16 sections (all in `api.py`):**
1. Career Position — confirmed research, hard-coded facts
2. Market Landscape — computed from compact_opportunities.json
3. Comparable Artists — from peer_artists.json
4. Strategic Pathway — 7-step roadmap to first Tokyo solo show, hardcoded
5. Instagram Strategy — 21k/90k gap analysis
6. Audience Geography — empty state with hypothesis
7. Career Benchmarks — 4-dimension peer range table
8. Seasonal Opportunity Calendar — parsed from deadlines
9. Press & Features — 2 Bored Panda articles; art press gap documented
10. Collector Ecosystem — empty state
11. Collaboration Map — 5 Tide from China co-exhibitors
12. Geographic Expansion — 4 regional cards
13. Publication Landscape — 2 personal publications + 36 pipeline targets
14. Long-term Scenarios — 3 age-30 scenarios (Gallery Track, Publication Track, Hybrid Track)
15. Venue Relationship Tracker — reads contact_memory.json
16. Open Questions — 8 Peppercorn-routed questions

**Navigation:** Animal-based. Clicking Mochi/Peppercorn/Saffron illustrations navigates between pages. No text tabs. Mochi status bar persists across all three pages.

**Hero images:** Per-companion image pools with time-of-day and seasonal weighting (specification exists in Bible11; partial implementation). Three hero images currently in deploy package.

**Icons:** 18 category icons hand-cropped from watercolor sprite sheets. Used in opportunity cards.

**CSS:** Warm atelier palette: cream (`--paper: #f7efe2`), ink (`--ink: #3f3027`), amber, ochre. Georgia serif headings throughout.

### Streamlit Dashboard (Developer/Operator)

**`app.py`** — The primary Streamlit dashboard. Complex multi-tab layout importing from `ui/` modules. Shows opportunity cards with all metadata, fit analysis, verification badges, email drafts, relationship components, portfolio match panel, feedback learning panel. This is the operator's view of the data.

**`stable_atelier_portal.py`** — Minimal tab-based fallback. Four tabs: Mochi Atelier, Mousehole, Observatory, Archive. Simpler than app.py.

**`atelier_portal.py`** — Another Streamlit variant with similar functionality.

**`mochi_deploy_app.py`** — Deploy-focused Streamlit variant.

**`demo_app.py`** — Demo version.

**`app_mochi_polished_carousel.py`** — Experimental polished carousel variant.

**UI modules (`ui/`):**
- `strategy_homepage_components.py` — Strategy homepage rendering
- `best_moves_streamlit_section.py` — Immediate Best Moves section
- `report_ui_components.py` — Report rendering
- `relationship_ui_components.py` — Relationship/CRM components
- `feedback_ui_components.py` — Feedback learning panel
- `portfolio_match_ui_components.py` — Portfolio match panel
- `zine_opportunity_section.py` — Zine/print section
- `publishing_opportunity_section.py` — Publishing section
- `category_context_streamlit_section.py` — Category context
- `opportunity_review_sections.py` — Opportunity review
- `compact_detail_components.py` — Compact detail view

---

## 6. The Ingestion Pipeline

**Entry points:** New opportunities enter through multiple parallel channels:

1. **Web ingestion (`web_ingestion_engine.py`):** Scrapes URLs from `source_targets.json` using BeautifulSoup. Outputs raw scraped pages to `ingestion/scraped_pages.json`.

2. **Candidate extraction (`scraped_candidate_extractor.py`):** Extracts structured candidates from scraped content.

3. **Quality gate (`candidate_quality_gate.py`):** Filters candidates before import.

4. **Approved import (`engines/approved_candidate_importer.py`):** Imports approved candidates into main opportunity set.

5. **Japanese/Chinese discovery (`engines/japanese_chinese_discovery_engine.py`):** Active AI-powered discovery using Tavily + Claude. 31 queries across JP/CN/Diaspora source groups. 7-day cache prevents re-querying. Outputs directly to `deploy_data/compact_opportunities.json`.

6. **Global expander (`engines/global_opportunity_expander.py`):** Broadens beyond Tokyo.

7. **Rumor mill (`engines/rumor_mill_engine.py`):** Processes the `needs_research` bucket. Uses Tavily (EN/JP/CN) + Claude to find missing factual data (deadline, fees, contact, submission URL). Runs weekly. On Session 8, all 282 needs_research items were already within the 7-day cache.

**Current corpus:** 286 opportunities total in the deploy set. 185 of 286 confirmed medium-match. 44 of 53 IBM-eligible submission URLs confirmed live (Session 8 verification pass).

**The photography pollution problem:** A historical crisis — photography opportunities dominated watercolor painter recommendations because visual similarity scoring couldn't distinguish professional ecosystems. Addressed by the Watercolor Layer (dedicated medium profile engine + medium confirmation gate). The `watercolor_artist_profile_engine.py` explicitly lists photography-related opportunity types as `bad_opportunity_types`.

---

## 7. The Intelligence Layer

### Scoring Architecture (multi-layered, sequential)

The pipeline applies scoring in roughly this order, each layer writing to opportunity JSON fields:

1. **Base scoring** — initial score from discovery context
2. **Artist DNA match** — from `artist_dna_engine.py`; static hand-authored profile, not ML
3. **Watercolor adjustment** — medium-specific scoring corrections
4. **Source purity** — `source_purity_enforcer.py`; demotes archive/catalog noise
5. **Truth alignment** — `opportunity_truth_checker.py`; anchors scores to evidence
6. **Deep match scoring** — `deep_match_scoring_engine.py`; optional
7. **Lineage scoring** — `lineage_scoring_engine.py`; historical precedent
8. **DNA boost** — `dna_recommendation_booster.py`; DNA alignment bonus
9. **Feedback learning** — `feedback_learning_engine.py`; adjusts based on artist behavior
10. **Preference rescoring** — `preference_rescoring_engine.py`; artist preference application
11. **Score sanity cap** — `score_sanity_engine.py`; maximum score bounded by verification evidence (no source → max 6.5; full verification → max 9.4)
12. **Portfolio match** — `portfolio_match_engine.py`; specific body-of-work alignment

**Final stored fields (per opportunity):** `overall_score`, `watercolor_adjusted_score`, `dna_adjusted_score`, `differentiated_score`, `visual_fit_score`. The API uses whichever is non-null.

### Artist DNA

The DNA engine (`engines/artist_dna_engine.py`) is hand-authored, not machine-learned. It defines a static profile:
- `visual_language` — 8 descriptors (quiet observational work, muted urban atmosphere, etc.)
- `strong_fit_opportunity_types` — 9 types (artist book fairs, zine shops, etc.)
- `weak_fit_opportunity_types` — 4 types (traditional painting societies, large competitions, etc.)
- `positioning_sentence` — single canonical positioning statement

The watercolor profile engine (`watercolor_artist_profile_engine.py`) is similarly hand-authored with `best_opportunity_types` and `bad_opportunity_types` lists.

**Neither engine uses machine learning.** They are curated rule systems based on the specific artist's practice. This is intentional — the CLAUDE.md notes that "generic models produced weak recommendations."

### Bucketing System

`exclusive_strategy_bucket_engine.py` assigns each opportunity to exactly one primary bucket:

| Bucket | Meaning |
|--------|---------|
| `immediate_best_moves` | Confirmed deadline or submission path; act now |
| `publication_targets` | Zines, books, art book fairs |
| `japan_book_ecosystem` | Tokyo-specific book/zine venues |
| `stretch_targets` | Tier 4 prestige targets (RWS, Cité, etc.) |
| `relationship_builders` | Galleries, cafes, venues for long-game |
| `research_needed` | Missing key data; needs rumor mill |
| `low_priority` | Score too low |
| `reject` | Confirmed bad fit |

### Verification (The Weakest Layer)

**Self-assessed at 30% mature.** Key activities:

- `url_verification_engine.py`: HTTP HEAD requests to verify submission URLs. As of Session 8: 44 live, 2 dead (flagged and hidden), 7 malformed URLs decoded and fixed.
- `rumor_mill_engine.py`: AI-powered research to fill missing fields on `needs_research` items.
- The `score_sanity_engine.py` score cap enforces verification priority indirectly — poorly verified opportunities cannot score above 6.5 regardless of other signals.

**Critical known gap:** 101 IBM-eligible entries lack a submission_page URL. Rumor mill is the intended resolution mechanism.

---

## 8. The Outreach Layer

### Email Draft Generation

**Three-language system** (Chinese, Japanese, English) implemented at two levels:

1. **Hardcoded in `api.py`** — template-based drafts generated per opportunity in the FastAPI response. Functions `email_zh()`, `email_ja()`, `email_en()`. Category-aware: different ask language for zines vs. residencies vs. general venues. These are the live drafts in the React frontend.

2. **`engines/inquiry_draft_generator.py`** — pipeline-time draft generation. Generates inquiry emails specifically for opportunities with missing information (no submission page, no deadline, no fees). Template-based, English only. Outputs to `reports/inquiry_drafts/`.

3. **`engines/smart_cover_letter_engine.py`** — Structure guidance for cover letters using opportunity's fit analysis fields. Outputs cover letter templates to `drafts/smart_cover_letters/`.

4. **`engines/portfolio_pitch_generator.py`** — Portfolio pitch generation.

5. **`engines/next_email_engine.py`** — Next email generation for tracked contacts.

**Important:** No email is sent automatically. The system generates drafts for human review and sending.

### Submission Packet

`submission_packet_agent.py` — Generates submission packet structure (what to include, what body of work, tone).

`engines/submission_strategy_engine.py` — Strategy for which submission to prepare.

`engines/submission_timeline_engine.py` — Timeline planning for submissions.

---

## 9. What's Mature and Working

- **Opportunity discovery** — The Japanese/Chinese discovery engine with Tavily + Claude is genuinely functional and was actively improved (Session 8: 9 queries tightened for medium specificity). 286 opportunities in the corpus is a real, meaningful dataset for this niche.

- **Watercolor medium protection** — The medium confirmation gate and watercolor profile engine work. 185 of 286 opportunities have explicit medium confirmation. Photography flood is controlled.

- **Score sanity enforcement** — The evidence-based score cap works correctly. Scores cannot inflate beyond what verification supports.

- **Strategy bucketing** — The exclusive_strategy_bucket_engine reliably categorizes opportunities. The IBM eligibility gate in `api.py` (checks for real deadline or real submission page) is well-implemented.

- **The React frontend** — Three pages fully built. Mochi page is functional with real data. Saffron page has 16 sections with a substantial amount of real analysis. Peppercorn page was fully rebuilt to spec in Session 7. Navigation works. Email drafts are present and language-specific.

- **The FastAPI backend** — `api.py` is clean, well-structured, and fully operational. The Saffron endpoint in particular is a substantial piece of work — 16 data sections, seasonal calendar parsing, geographic analysis, career benchmarks, pathway modeling. All hardcoded or pipeline-computed, but real and non-trivial.

- **The daily digest** — `engines/daily_digest_report.py` works correctly including urgent deadline promotion (fixed Session 7: BOOOOOOOM promoted to IBM with 2 days remaining) and watch list population from `next_cycle_watch.json`.

- **The rumor mill** — Functional AI-powered research loop. Tavily + Claude searching EN/JP/CN sources for missing opportunity data. 7-day cache prevents wasted API calls.

- **Artist profile** — `memory/artist_master_profile.json` is a richly populated document. The artist's specific context (Chinese artist in Tokyo, watercolor, illustration-community roots, 90k Twitter, 21k Instagram, JLPT N2) is accurately modeled.

- **Deploy package** — A complete deployable artifact exists at `deploy_package/`. React build, FastAPI app, nginx config, systemd service file, and install script. This is ready to be deployed to an AWS Lightsail server.

---

## 10. What's Incomplete, Broken, or Aspirational

**Verification (30% — highest priority gap):**
- 101 IBM-eligible entries have no submission_page URL. Only the rumor mill can fix this and it runs weekly with a 7-day cache.
- Ongoing URL decay: sites go down; the verification engine only runs when the pipeline runs.
- No automated re-verification schedule.

**CRM (5% — nearly empty):**
- `contact_memory.json` has exactly 1 venue (KAYOKOYUKI). The spec calls for 15–20.
- No relationship tracking beyond a single entry.
- The Peppercorn → Saffron feedback loop for preference data is "wired in concept but not yet connected" (Session 7 notes). When the artist answers Peppercorn's questions, those answers are saved but do not yet update Saffron's analysis.

**Peppercorn's door illustration:**
- The Profile Completeness carousel card is deferred because it requires an illustration asset (four states: door closed, ajar, half-open, wide open). The card is not yet implemented.

**Saffron's three intelligence layers (as designed):**
- Bible11 specifies Market Intelligence, Artist Intelligence, and Strategic Pathways as three deep layers with compounding context.
- What exists in Saffron now is more like a sophisticated data dashboard — real data, well-presented, but the "intelligence layers" as specified (seasonality prediction, trend detection, career trajectory modeling from comparable careers) are not implemented. The current Saffron is hardcoded analysis, not a running intelligence system.

**Career planning (20%):**
- The pathway in Saffron is hardcoded (7 steps to first Tokyo solo show). Real pathway computation based on current artist state is not implemented.
- The questline system (Bible09) — structured career milestones with prerequisite tracking — is specified but not built.

**Feedback loop:**
- The four card actions (Follow, Applied, Maybe Later, Not for Me) exist in the React frontend and write to `memory/feedback.json` via the API. But the pipeline does not yet read feedback.json to re-score opportunities. The loop is open — feedback is recorded but not yet used.

**Internationalization:**
- Bible14 specifies full Chinese/Japanese/English switching for all system-generated prose.
- Email drafts are trilingual (working). All other UI copy is English only.
- The toggle does not exist in the current frontend.

**The Three Companions build:**
- The current `app.py` Streamlit dashboard is not the target architecture. The three-companion React rebuild is substantially done but still described as 75% (Session 7 assessment).

**Multiple app.py variants:**
- `app.py`, `stable_atelier_portal.py`, `atelier_portal.py`, `mochi_deploy_app.py`, `demo_app.py`, `app_mochi_polished_carousel.py` are all present. Only `app.py` is designated production. The others are unlabeled variants creating confusion.

**Many engines are aspirational scaffolding:**
- `engines/serendipity_engine.py`, `engines/reputation_engine.py`, `engines/momentum_wave_engine.py`, `engines/social_proof_engine.py`, `engines/curator_personality_engine.py`, `engines/ecosystem_expansion_engine.py`, `engines/institution_network_engine.py` — these exist and run in the pipeline but their actual implementations are likely stubs or very early. The Session 7 assessment notes "reputation_engine, serendipity_engine, curator_personality_engine" as 20% or less.

---

## 11. Structural Issues

### File Sprawl
The root directory contains approximately 80+ Python files. The reorganization effort moved some to `engines/`, `ui/`, `scripts/`, `reports/`, but many legacy agents remain at the root. This makes it difficult to identify what is active vs. superseded.

### Duplicate Scripts
Multiple copies of some functionality exist:
- `opportunity_report_engine.py` exists at both root and in `engines/`; also copied to `memory/` (apparent accident)
- `upgrade_opportunity_scores.py` exists at root and in `memory/`
- Multiple Streamlit app variants (`app.py`, `stable_atelier_portal.py`, `atelier_portal.py`, `mochi_deploy_app.py`, `demo_app.py`, `app_mochi_polished_carousel.py`)

### Naming Inconsistency
- Directory case: `Memory/` (capital M, older) vs. `memory/` (lowercase, newer). Both exist; `Memory/` contains `.json.txt` legacy files and some accidentally-copied `.py` files.
- File naming: `_agent.py` vs. `_engine.py` used inconsistently and sometimes interchangeably.

### Generated Analysis Duplication
`memory/generated_analysis/` contains per-opportunity markdown files numbered from 004 to 046 — but with multiple overlapping numbering sequences (appears the numbering was reset multiple times). Files like `016_self_publish,_be_happy.md` and `028_self_publish,_be_happy.md` cover the same venue.

### Patches Directory
`scripts/patches/` contains 15+ one-shot migration scripts. Most have likely already been run. Their presence in the pipeline search path means `smart_pipeline_runner.py` could theoretically find and run them again.

### Two Parallel App Architectures
The Streamlit `app.py` and the React+FastAPI `deploy_package/` are both described as "production" in different contexts. The React app is the designed production interface; the Streamlit app is the developer tool. This distinction is documented in CLAUDE.md but not structurally enforced.

### Hardcoded Saffron Data
The Saffron page serves ~700 lines of hardcoded analysis in `api.py`. Career benchmarks, pathway steps, Instagram strategy analysis, press features, collaboration map, long-term scenarios — all hardcoded. This will need to be refactored into data files or a proper intelligence layer as the system matures, but for now it works.

---

## 12. Deployment State

### Current Status: Ready to deploy, probably not actively deployed

**Deploy package exists:** `deploy_package/` contains a complete production artifact:
- `www/` — React SPA build (index.html, hashed JS/CSS assets, hero images for all three companions, 18+ category icons, illustration SVGs)
- `app/api.py` — FastAPI backend
- `app/requirements-api.txt` — minimal requirements (fastapi, uvicorn, pydantic, python-dotenv)
- `app/memory/` — production data snapshot
- `app/deploy_data/compact_opportunities.json` — production opportunity set
- `nginx.conf` — nginx reverse proxy config (React SPA on port 80, API on 127.0.0.1:8001)
- `mochi-api.service` — systemd unit file for uvicorn
- `install.sh` — one-shot install script for Ubuntu/Lightsail

**Target infrastructure:** AWS Lightsail (Ubuntu). The install.sh references `/opt/mochi` as the app directory and `/var/www/mochi` as the web root.

**The pipeline is not deployed.** The full pipeline (Tavily, Anthropic API, BeautifulSoup scraping) runs locally on the developer machine. The deployed artifact is read-only — it serves pre-computed data. To update the deployed site with new opportunities, the operator runs the pipeline locally, rebuilds the deploy package, and re-uploads.

**Local development setup:** `python -m streamlit run app.py` for the operator dashboard; React dev server (`npm run dev` in `frontend/`) with Vite proxy to `api.py` on port 8001 for the frontend.

**Port conflicts documented:** Session 7 notes a "production server management (port collision)" issue as unresolved.

---

## Summary for Pip

**What Mochi is, in one sentence for another context:** Mochi is a research-and-prioritization pipeline that ingests arts opportunities from web sources in three languages (EN/JP/CN), scores and categorizes them against a specific artist profile, and presents the top-ranked actionable opportunities through a warm, companion-animal-based React interface — with pre-generated email drafts in three languages for every opportunity.

**What's genuinely transferable to another creative studio:**
- The three-companion UI architecture (Mochi/action, Peppercorn/input, Saffron/context) is a strong, well-documented design pattern for any advisory creative tool
- The opportunity bucketing logic (IBM, publication targets, relationship builders, stretch targets, research needed) maps cleanly to any creative career context
- The trilingual email draft generation (hardcoded templates differentiated by opportunity category) is simple and immediately useful
- The score sanity cap tied to verification evidence is a clever epistemic safeguard against score inflation — directly applicable to any recommendation system
- The watercolor/photography separation logic is a specific example of a generalizable pattern: protecting niche creative practices from being drowned out by adjacent high-volume disciplines in recommendation systems
- The daily digest with urgent deadline promotion is a practical solved problem

**What requires significant work to adapt:**
- The artist DNA profile is entirely hand-authored for one specific artist. Adapting to another creative context requires redoing the profile from scratch.
- The Saffron page's analysis is largely hardcoded for GEGYjiji's career facts. Generalizing requires either new hardcoding per artist or a real intelligence layer.
- The Japanese/Chinese discovery engine queries are specific to GEGYjiji's ecosystem. Adapting requires domain-specific query redesign.
- The CRM is nearly empty — this would need to be built from the ground up for any new use.

**Overall maturity:** 55–65% as self-assessed in CLAUDE.md. The discovery, scoring, and frontend layers are the most mature. Verification, CRM, and career planning are the least mature. The deployed artifact (React + FastAPI) is coherent and functional but depends on pipeline-generated data files being kept current.
