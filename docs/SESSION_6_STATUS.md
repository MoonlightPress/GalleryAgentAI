# Session 6 Status Report
**Date:** 2026-06-02  
**Commits this session:** 8158607 through fe5befc (33 commits)

---

## What Was Accomplished This Session

This session was the largest single build in the project's history. The React frontend went from a stub to a working multi-page application with a complete Observe (Saffron) intelligence page, 18 hand-cropped watercolor icons, collapsible section architecture, and the beginning of a real design system.

---

### 1. React Frontend Built from Scratch

**Prior state:** The frontend directory existed with a basic Vite scaffold and a single Mochi hero section.

**This session:**
- Full React SPA built with three companion pages: Mochi (Action), Peppercorn/Refine (Input), Saffron/Observe (Context)
- FastAPI backend (`api.py`) wired with Vite dev proxy — all `/api` calls route to port 8001
- Companion navigation system: clicking Mochi, Peppercorn, or Saffron navigates between pages
- Hero image rotation system with per-companion image folders (`/assets/heroes/mochi/`, `/assets/heroes/peppercorn/`, `/assets/heroes/saffron/`)
- Nav bar persists across all three pages with painted Caveat font labels and watercolor wash active state
- Peppercorn and Saffron placeholder pages built with full hero banners

**Architecture:** The three-companion structure now exists in code, not just in the Bible. Each page is an independent React component. The nav renders above the hero on all pages.

---

### 2. Opportunity Card Redesign

**Prior state:** Cards were a dense list with minimal visual hierarchy.

**This session (multiple iterations):**
- Redesigned to horizontal layout: tall watercolor illustration thumbnail on the left, content on the right
- Score badge repositioned to top-right, outside the thumbnail strip
- Added feedback buttons (Follow, Applied, Maybe Later, Not for Me) — visible when card is open
- Cards sort correctly within sections by score
- Added email draft tabs (Chinese / Japanese / English) in the expanded card view
- Spacious collapsed rows with breathing room between cards

**Watercolor illustration thumbnails:**  
Initial set of 4 generic SVG illustrations (galleries, cafes, zines, open calls) replaced this session with 18 individual PNG icons cropped from two hand-drawn sprite sheets (see §7 below).

---

### 3. Saffron (Observe) Page — 16 Sections

The Observe page went from a blank placeholder to a full intelligence dashboard in two passes.

**Pass 1 — Core four sections (commit 07c7223):**
Built with real data pulled from the API:
1. **Career Position** — 1 exhibition, 2 publications, Instagram 21k, Twitter 90k, education, base
2. **Market Landscape** — 179 opportunities by category and geography, Tokyo vs. international split, actionability breakdown
3. **Comparable Artists** — 8 peers ranked by fit score from `memory/peer_artists.json`
4. **Strategic Pathway** — 7-step roadmap to first Tokyo solo show, blocking step highlighted

**Pass 2 — 12 new sections (commit 33c50b5):**
All collapsed by default. Real data where it exists; honest empty states where it doesn't.

| Section | Data source | Status |
|---|---|---|
| Instagram Strategy | `artist_master_profile.json` | Real — 21k / 90k gap analysis, 35 posts, daily diary noted |
| Audience Geography | None | Empty state — hypothesis + Peppercorn prompt |
| Career Benchmarks | Profile + hardcoded peer ranges | Real — 4-dimension table with assessment ratings |
| Seasonal Opportunity Calendar | `compact_opportunities.json` deadlines | Partial — 8 confirmed dates, 171 unknown flagged |
| Press & Features | `career_history.press` | Real — 2 Bored Panda features; art press gap documented |
| Collector Ecosystem | None | Empty state — fairs listed, what to ask Peppercorn |
| Collaboration Map | Exhibition co-exhibitors from profile | Real — 5 Tide from China co-exhibitors; peer network gap |
| Geographic Expansion | Pipeline country distribution | Real — 4 regional cards with entry points |
| Publication Landscape | `compact_opportunities.json` filtered | Real — 2 personal pubs + 36 pipeline targets + 4-tier map |
| Long-term Scenarios | Hardcoded analysis | Real — 3 paths at age 30 with bottlenecks and fit signals |
| Venue Relationship Tracker | `contact_memory.json` | Real — KAYOKOYUKI + gap note (1 venue, needs 15–20) |
| Open Questions | Hardcoded gaps | Real — 8 questions routed to Peppercorn |

**Collapsible architecture:** All 16 sections use a shared `SectionShell` component. Career Position opens by default; all others start collapsed showing a one-line data summary. Chevron animates on toggle.

---

### 4. Artist Research — GEGYjiji Biography Confirmed

**Prior state:** Artist profile contained approximate and unconfirmed data.

**This session:**
- Confirmed legal name: unconfirmed (Ren Jiawei / 任佳薇 user-suggested, not verified in any source)
- Confirmed education: Beijing Fashion Institute (北京服装学院 / BIFT), illustration/design track, approx. 2021–2023
- Confirmed base: between Tokyo and Beijing (not exclusively Tokyo)
- Confirmed social: Twitter @GegYjiji ~90k, Instagram @gegyjiji 21k / 35 posts
- Confirmed exhibition: Tide from China Part 1, ACG_Labo Harajuku, February 4–13, 2023 — first Japan show, 6 Chinese illustrators, co-exhibitors named
- Confirmed publications: Colour Diary (October 2021, solo), defined Definition 02 (group, details unverified)
- Confirmed press: 2 Bored Panda features (URLs documented)
- Confirmed community root: ACG / illustration / zine ecosystem — not fine arts

---

### 5. Illustration-Community Context Established

**The key insight this session:** GEGYjiji's formation is at a fashion/design institute, not a fine arts academy. Her first Japan show was organised by a Chinese ACG company. Her 90k Twitter following is an illustrator-community following. The publication ecosystem — zine shops, book fairs, illustration publishers — is her native territory.

This is now encoded in `artist_master_profile.json` under `practice_context`:
- `community_root: illustration`
- `primary_ecosystem: zine / artist book / illustration publisher / illustration fair`
- `secondary_ecosystem: fine art gallery / open call / watercolor society`

**Effect on scoring:**  
Artist book and zine/publishing weights raised above gallery exhibition weights. Bookshop consignment raised to primary-ecosystem. Gallery exhibition weights slightly lowered (not suppressed — still valid and aspirationally correct, but illustration/publishing consistently surfaces first in Immediate Best Moves).

---

### 6. Pipeline Fixes

**IBM (Immediate Best Moves) routing:**
- Switched from `opportunities.json` to `compact_opportunities.json` — the quality-filtered deployment set
- Added eligibility gate: opportunities filtered to `recommendation_visibility == "show"` before surfacing
- Residencies and global fellowships correctly routed to Watch List instead of IBM

**Score badge:** Repositioned to top-right of card, outside the thumbnail area. Previously overlapping content.

**Sort order:** Cards within each section now sort by `watercolor_adjusted_score` (the score after pipeline corrections), not raw `overall_score`.

**Deadline/event date separation:** Application deadline and event date extracted as separate fields across the pipeline. ZINEフェス東京 deadline vs. event date corrected.

**Passed deadlines:** Opportunities with passed deadlines now route to a holding bucket rather than surfacing in active sections.

**Opportunity research:** Batch research run on 70 high-priority opportunities; results imported back into the pipeline. Description quality improved for 6 weak entries.

---

### 7. Watercolor Icon Sprites — 18 Icons Cropped

Two hand-drawn watercolor sprite sheets provided:
- `OpportunityLogos01.png` — 4×3 grid, 12 icons
- `OpportunityLogos02.png` — 3×2 grid, 6 icons

All 18 icons individually cropped with Python Pillow (equal grid division, 10px inset) and saved to `frontend/public/assets/icons/`:

| File | Depicts | Mapped to |
|---|---|---|
| `icon_gallery.png` | Arched doorway with lamp and climbing roses | `gallery` |
| `icon_zines.png` | Stack of books with ZINE label | `zine_print`, `book_publishing`, `global_book_arts` |
| `icon_cafe.png` | Coffee cup with latte art | *(base café, not currently mapped — available)* |
| `icon_residency.png` | Vine-covered cottage with green door | `residency`, `residency_beijing` |
| `icon_open_call.png` | Envelope with gold star, "OPEN CALL" | `institutional`, `global_open_call`, `global_watercolor_open_call`, `japan_watercolor_open_call`, `photo_open_call` |
| `icon_fair.png` | Art fair tent with bunting, "ART FAIR" chalkboard | `fair_popup`, `zine_fair_booth`, `global_art_book_fair` |
| `icon_studio.png` | Paintbrush and watercolor palette | `gallery_event`, `event_space` |
| `icon_international.png` | Gothic cityscape at night | *(available for international/watch sections)* |
| `icon_bookstore.png` | Bookshelf with trailing plants | `bookstore_event`, `zine_shop_consignment`, `global_artist_book_platform` |
| `icon_submission.png` | Wax-sealed letter envelope | `group_publication_open_call`, `global_photobook` |
| `icon_prize.png` | Golden compass / eight-point star | *(available for awards/competitions)* |
| `icon_research.png` | Magnifying glass | *(available for research/watch sections)* |
| `icon_artist_space.png` | Japanese-style gallery room with shoji screens | `artist_space` |
| `icon_art_market.png` | Outdoor art market with prints on display | `market_event` |
| `icon_gallery_small.png` | Bright studio with easel and paintings | `gallery_small` |
| `icon_reading_nook.png` | Cozy window seat reading nook | `bookstore_gallery` |
| `icon_cafe_gallery.png` | Warm café interior with artworks | `cafe_gallery` |
| `icon_residency_intl.png` | Airmail envelope with stamps and postmarks | `global_residency`, `global_grant_fellowship` |

OppCard.jsx now maps 28 categories to specific icons, replacing 4 generic SVGs. The `immediate_best_moves` SVG illustration is preserved unchanged.

---

### 8. Bible 11 Written

`docs/bible/Bible11.txt` documents the living hero system and Saffron's three intelligence layers:
- **Layer 1 (confirmed):** Research data, pipeline outputs, verified facts
- **Layer 2 (derived):** Patterns computed from Layer 1 — seasonality, geography, benchmarks
- **Layer 3 (analytical):** Strategic judgment — scenarios, gap analysis, open questions

Addenda cover Peppercorn's visual design options (animated cartoon vs. refined illustration) and Saffron's intended final visual style (clean vector illustration, not AI-generated).

---

### 9. API Architecture — FastAPI on Port 8001

`api.py` now serves:
- `GET /api/opportunities` — full opportunity list for card display
- `POST /api/feedback` — saves Follow / Applied / Maybe Later / Not for Me
- `GET /api/saffron` — all 16 Saffron section payloads in one response
- `GET /api/health` — liveness check

Moved from port 8000 to 8001 to avoid collision with stale server processes that accumulate during hot-reload development sessions. Reload mode disabled (`reload=False`) for clean single-process startup.

---

## Current System State

| Layer | Status | Notes |
|---|---|---|
| Discovery | 80% | 179 quality-filtered opportunities in deployment set |
| Ranking | 75% | Watercolor-adjusted scores, truth alignment, DNA scoring all active |
| Artist DNA | 85% | Profile fully updated; illustration-community context established |
| Verification | 35% | Improving — eligibility gate and passed-deadline routing added |
| Reporting | Stable | Saffron page is now the primary report surface |
| Career | 40% | Long-term scenarios, benchmarks, and pathway all built into Saffron |
| CRM | 10% | 1 venue tracked (KAYOKOYUKI); Venue Tracker section live in Saffron |
| React Frontend | 60% | Three companion pages, card system, Saffron complete, Peppercorn empty |

---

## What Peppercorn Needs to Ask

Eight questions identified this session that would materially change Saffron's analysis — documented in the Open Questions section of the Observe page and in `memory/artist_master_profile.json`:

1. Instagram posting frequency
2. Geographic breakdown of her audience (screenshot of Insights)
3. Whether she has sold work, at what price points, through which channels
4. Whether a new publication or zine is in progress
5. Whether she has a current artist statement in any language
6. Whether she is still in contact with her Tide from China co-exhibitors
7. Whether a second Japan exhibition is already in preparation
8. What price points she uses for originals and prints

---

## Next Session Priorities

1. **Verify June deadlines** — BOOOOOOOM (June 5), Women United (June 10), ZINEフェス (June 27), CSPWC (June 30) are all imminent. Confirm which are still open.
2. **Peppercorn page** — Build the Input page with artist statement field, monthly goals, recommendation feedback, and the 8 open questions above.
3. **Venue Tracker expansion** — Add 10–15 venues from the pipeline to the CRM. The Saffron tracker section is built; it needs data.
4. **Icon cleanup** — `icon_cafe.png`, `icon_international.png`, `icon_prize.png`, and `icon_research.png` are cropped and available but not yet mapped to any category. Wire them up when appropriate categories are confirmed.
5. **Production server management** — The port-collision issue with stale uvicorn processes needs a proper solution (a `start_api.py` wrapper that kills existing processes before starting).
