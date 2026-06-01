# Session 5 Status Report
**Date:** 2026-06-01  
**Commits this session:** db850b8, aa53c76, f6bc2a4, d1e2e5b, 782cc90, 3555cbc, d801f12, dd3c793, 8b209c5

---

## Immediate Actions for the Artist

Three deadlines are in the next 30 days. Nothing else matters until these are handled.

| Deadline | What | Fee | Link |
|---|---|---|---|
| **June 5 (4 days)** | BOOOOOOOM Art & Photo Book Award — zine submission | Free | booooooom.com |
| **June 10 (9 days)** | Women United ART MAGAZINE Issue XIV | $25 | womenunitedartmovement.com |
| **June 27 (~26 days)** | ZINEフェス東京 booth application + create something to sell | ¥5,200 | note.com/bookcultureclub/n/n053a24287fc2 |
| **June 30 (29 days)** | CSPWC Open Water — 2 watercolors via ArtCall | CAD $55 | open-water-2026.artcall.org |

Complete application packages for ZINEフェス and CSPWC are in `memory/application_packages/`. BOOOOOOOM requires: 10 images from one cohesive body + a short proposal paragraph. Zine submission is free.

---

## What Was Accomplished This Session

### 1. Pipeline Run
Full 72-step pipeline ran cleanly. 173 opportunities in the dataset. All steps completed without errors.

### 2. Venue Research — Three Deep Dives

**ZINEフェス東京 (July 11)**  
Confirmed via official note.com page: June 27 soft deadline (2-week rule), ¥5,200 solo with promotion, 90cm × 90cm booth, application via STORES link at the event page. Key clarification: this is a booth sale event, not a gallery submission. She needs to make something to sell. Full research in `memory/opportunity_research/zinefes_july2026.md`.

**NADiff a/p/a/r/t**  
Confirmed permanently closed March 31, 2025. Website down (ECONNREFUSED). Tokyo Art Beat marks it [Closed]. Three surviving NADiff branches are CCC-operated museum shops — not equivalent, not accessible for individual artist consignment. Contact info for NADiff contemporary (MOT) and NADiff BAITEN (TOP) documented. Record updated to `permanently_closed / hidden / priority: REMOVE`.

**torch press**  
Full catalog research: founded December 2013 by editor Nao Amino, invitation-only, no submissions page. They publish painters (Tomoo Gokita, Hiroshi Sugito) alongside photographers (Rinko Kawauchi × 3). Aesthetic alignment with GEGYjiji is high — quiet, atmospheric, light-focused, Tokyo-rooted. Correctly classified as Tier 4 watch target. Full research in `memory/opportunity_research/torch_press.md`.

### 3. IBM Data Quality Fixes

**Two blockers removed from Immediate Best Moves:**
- NADiff: venue closed, set `recommendation_visibility: hidden` + `verification_bucket: reject` in deploy_data. "nadiff" removed from `tier_1_terms` in the engine.
- torch press: invitation-only publisher, moved from `tier_1_terms` to `tier_4_terms` in engine. `verification_bucket: stretch_targets` set in deploy_data.

**Data flowed into opportunity records:**
- ZINEフェス: `source_url` and `submission_page` now point to the specific July 11 page. Deadline and fees were already correct.
- CSPWC: fees updated to confirmed amounts — CAD $55 non-members / $40 members, up to 2 entries, non-refundable. ArtCall URL confirmed.

**Engine hardening:**
- New `verification_bucket: stretch_targets` override path added to `exclusive_strategy_bucket_engine.py`. Individual records can now pin themselves to a specific bucket without requiring engine changes. Belt-and-suspenders protection for future cases like torch press.

IBM is now 10 entries (down from 12), all legitimate actionable items.

### 4. Pipeline Extensions

**submission_link_hunter.py** added at step 7 (after `global_opportunity_expander.py`, before `opportunity_enrichment_pipeline.py`). Reads from `memory/verified_opportunities.json`, crawls submission pages for links, emails, dates, and fee context.

**daily_digest_report.py** added as the final pipeline step (after `opportunity_status_engine.py`). Outputs `reports/daily_digest.md` every run with:
- IBM sorted by deadline (soonest first) with days-remaining badges
- Watch list for stretch/research items with deadlines within 90 days
- Diff against previous run snapshot: IBM adds/removes, score changes, opportunity count delta

First run output: ZINEフェス (26d) → CSPWC (29d) → NWWS (37d) sorted correctly. Snapshot saved to `memory/daily_digest_snapshot.json` for next-run comparison.

One bug found and fixed during implementation: the partial-date regex `(\d{1,2})` was matching "June 3" from "June 30" by taking only one digit. Fixed with `\b` word boundary.

### 5. Bible09 — Peppercorn Questline System

New bible entry documenting Peppercorn's second function (the first, the input layer, was in Bible08):

**Core document:** Questlines are structured paths toward major career milestones — name, completion condition, prerequisites, current position, horizon tier. Example: "Published by a major press: 10 anthology credits, 5 group shows, 2 solo shows, 1 small press monograph." Progress tracked automatically where the pipeline has data (exhibitions confirmed, submissions made, social metrics) and prompted where it doesn't (submission outcomes, private decisions).

**Social following as a tracked metric:** 90k Twitter / 21k Instagram / 35 posts. Instagram underperformance explained and framed by Peppercorn as an asymmetry with a clear resolution (not a weakness). Specific steps included.

**The three-companion information flow** stated as a directed chain: Saffron sees the landscape → Peppercorn maps the path → Mochi walks it one step at a time.

**Addendum:** Two modes on the same page — Mode 1 (QA minigame, 20-30 questions on first visit, feeds opportunity scoring weights and outreach tone), Mode 2 (questline tracker). Artist statement field sits alongside both, feeding the description generator and outreach email tone. The three elements together: minigame = entry point, questlines = ongoing tracker, artist statement = permanent record.

**Example questions from the minigame:**
- "Would you prefer to be known for your skill or your perspective?"
- "Famous, or financially stable?"
- "Do you prefer working alone or in community?"

### 6. Homepage Redesign — app.py

`render_hero()` replaced by four new functions:

**`render_homepage()`** — full-width hero image (mochi_hero.png) with warm paper veil gradient fading right to reveal the cat illustration. Overlaid left column: time-aware greeting ("Good morning/afternoon/evening, Mochi") + Today's Focus card showing three daily action items pulled live from IBM:
- 🌿 **Quick Win** (5 min): soonest-deadline apply item — ZINEフェス (26d)
- ✉️ **High Impact Move** (30-60 min): second apply item — CSPWC (29d)
- 🔭 **Stretch Goal** (longer term): first contact/propose item — UTRECHT

**`_render_section_cards()`** — six warm mini-cards below the hero using existing stamp assets (stamp_gallery, stamp_bookstore, stamp_cafe, stamp_market, stamp_residency).

**`render_mochi_statusbar()`** — cat avatar (header_cat.png), time-aware mood text, IBM count note ("10 things worth your attention today").

All five existing tabs unchanged and functional. Smoke-tested: server responds 200, all runtime checks pass (deadline parsing, focus card assignment, image loading).

### 7. Application Packages

Two complete packages built in `memory/application_packages/`:

**zinefes_july2026.md** — Clarifies this is a booth sale event, not a gallery submission. Three product format options (prints, zine, combination). Week-by-week pre-fair checklist to July 11. Day-of logistics. Japanese and English drafts for STORES form, booth card, organizer correspondence. Why it fits: native audience, no jury, recurring format builds compounding presence, cross-cultural position is an asset.

**cspwc_2026.md** — Timezone warning: June 30 2 PM EDT = July 1 4 AM JST. Recommends submitting June 28-29. Medium enforcement guidance (transparent watercolour only — gouache disqualifies). Work selection for an international watercolour jury. Artist bio (50-80 words), work title templates, statement draft, email template. Shipping plan if accepted: Japan Post EMS or DHL, ship by August 20-22.

### 8. Anthology Calls + Café Consignment Research

**Anthologies** (`memory/opportunity_research/anthology_calls.md`):  
Six calls surveyed. Three with imminent deadlines. Honest finding: dedicated Japan/Asia anthology open calls don't exist as a public call ecosystem — the right Japan-specific strategy is presence-building at fairs, not hunting open calls.

**Café consignment** (`memory/opportunity_research/cafe_consignment.md`):  
Eight venues across Shimokitazawa, Koenji, Nakameguro. Contact info confirmed for:
- CLOUDS Gallery+Coffee — 03-5356-9358, Koenji, confirmed international rotating exhibitions
- HATTIFNATT — 03-6762-8122, Koenji, highest aesthetic fit in the dataset
- BALLOND'ESSAI — 03-6804-7651, Shimokitazawa, confirmed accepts proposals via website

Japanese and English outreach templates included.

**5 new entries added to deploy_data pipeline** (173 → 178):
- BOOOOOOOM 2026 Art & Photo Book Award → publication_targets
- Women United ART MAGAZINE Issue XIV → publication_targets
- CLOUDS Gallery+Coffee Koenji → relationship_builders
- BALLOND'ESSAI Shimokitazawa → relationship_builders
- HATTIFNATT Koenji → relationship_builders (visual_fit_score: 4.5, highest in café category)

---

## Current State of the Pipeline

| Layer | Status | Notes |
|---|---|---|
| Discovery | Running | 178 opportunities |
| Ranking | Running | IBM clean at 10 entries |
| Watercolor | Running | No photography contamination |
| Source Purity | Running | |
| Truth Alignment | Running | |
| Verification | Partial | submission_link_hunter in pipeline; deadline data still decays |
| Daily Digest | **New this session** | daily_digest.md generated each run; first snapshot established |
| Reporting | Over-proliferated | Not addressed this session |
| Career/Questlines | **Documented, not built** | Bible09 written; no engine yet |
| CRM | 5% | relationship_targets exist but no status tracking |

**Immediate Best Moves (10):**
ZINEフェス (26d) · CSPWC (29d) · NWWS (37d) · MOUNT ZINE · TABF · Shimokitazawa Arts · UTRECHT · B&B Shimokitazawa · flotsam books · Book and Sons

**Publication Targets (58):**
Now includes BOOOOOOOM (June 5) and Women United (June 10) — both with urgent deadlines.

**Relationship Builders (12):**
Now includes CLOUDS, BALLOND'ESSAI, HATTIFNATT alongside existing Tokyo bookshop/gallery targets.

---

## Remaining Issues

1. **BOOOOOOOM deadline is June 5** — this is not in IBM because the bucket engine routes publications to `publication_targets`, not `immediate_best_moves`. The urgency is in the deadline field and daily digest. A future fix could add a deadline-proximity override to the bucket engine so near-deadline publication calls surface in IBM automatically.

2. **ZINEフェス — she needs to make something first.** The application is quick (pay fee by June 27). The harder task is having something to sell on July 11. The application package covers this but the production work is real.

3. **TABF 2026 exhibitor application status unknown.** The 2026 fair is November/December; applications typically open in spring. May already be closed for 2026. Needs urgent verification at tokyoartbookfair.com.

4. **Verification layer still 30%.** The daily_digest_report.py now tracks deadlines but depends on manually-entered data. Automated deadline crawling (re-verifying known deadlines against live pages) doesn't exist yet.

5. **Peppercorn and Saffron not built.** Bible09 documents the questline system in full. No engine or UI exists. The QA minigame and questline tracker are the next major feature gap.

6. **Homepage section cards are decorative.** The six mini-cards below the hero don't link to tabs or trigger navigation. Fine for now; wire them up when rebuilding as the three-companion architecture.

7. **daily_digest_report.py: `parse_deadline` handles most formats but not all.** "Twice-yearly (spring/autumn)" and similar soft deadlines return None. MOUNT ZINE and TABF show "no deadline" in the digest. This is correct behavior but means the watch list is sparse. As more confirmed deadlines are added to records, the digest will improve.

---

## Architecture Notes

The session deepened the system on two tracks simultaneously: pipeline data quality (IBM is cleaner and more trustworthy than it has ever been) and documentation depth (Bible09 makes the Peppercorn vision concrete enough to build against).

The `verification_bucket` data-level override mechanism added to the bucket engine is worth noting — it creates a clean path for future cases where a specific record needs to be pinned to a non-default bucket without touching the engine logic. Use it sparingly.

The daily digest is the first step toward the system having a genuine "pulse" — something that changes meaningfully each run and summarizes what's different. Right now it tracks IBM composition and deadlines. It should eventually track: relationship status changes, new opportunities discovered, score changes on tracked items, upcoming events on the watch list.

The application packages in `memory/application_packages/` set a new standard for what actionable output looks like. They are complete enough for the artist to act on without further research. Future packages should follow the same structure: exact deadline with timezone, step-by-step submission, work selection guidance, and outreach in both languages.
