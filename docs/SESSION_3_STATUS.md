# Session 3 Status Report
**Date:** 2026-06-01  
**Commits this session:** a204fcd, 1e3bc18, 02b7b75, 87e9a64, 4c3489a

---

## What Was Accomplished

### 1. Artist Profile — GEGYjiji (v2)
Replaced the old "Nin" placeholder profile in `memory/artist_master_profile.json` with a full GEGYjiji profile:
- Chinese watercolor artist, 26, Tokyo, from Changsha
- JLPT N2, 90k Twitter, primary language Chinese / working language Japanese
- Themes: urban atmosphere, stillness, cats, interior light, memory
- Dual opportunity mix: prestigious international + intimate local Tokyo
- Opportunity weighting updated (positive: watercolor open calls, gallery exhibitions, residencies; negative: photography calls, character art, tech/NFT)
- Photography contamination audited and confirmed absent

Also updated `artist_visual_profile_v1.py`, which had the old Nin/photography profile hardcoded and was silently overwriting `memory/artist_master_profile.json` on every pipeline run. Fixed at the source.

### 2. File Consolidation — Email and Normalization
Analyzed 4 outreach/email files and 3 normalization files. Findings:

**Email files:**
- `outreach_email_agent.py` — canonical (AI, multilingual, per-opportunity)
- `outreach_email_builder.py` — kept secondary (batch, no API cost, different input)
- `email_draft_agent.py` — archived (stale inputs, superseded)
- `engines/email_draft_generator.py` — archived (primitive, called artist a "photographer")

**Normalization files:**
- `schema_normalizer_agent.py` — canonical (full superset)
- `normalize_opportunities_agent.py` — archived (strict subset)
- `archive/.../opportunity_normalizer_v1.py` — already correctly archived

**Fixes applied alongside archival:**
- `outreach_email_builder.py`: updated description from old Nin-era language to GEGYjiji framing ("watercolor painter based in Tokyo, urban atmosphere, interior light, domestic stillness")
- `schema_normalizer_agent.py`: added Changsha, Beijing, Shanghai, London, Paris to city keyword map; added country inference for China, UK, France

### 3. Pipeline — First Complete Run
The pipeline (`run_full_mochi_pipeline.py`, 72 steps) had never run to completion. Seven errors were blocking it:

| Error | File | Fix |
|---|---|---|
| `ModuleNotFoundError: opportunity_report_engine` | `opportunity_enrichment_pipeline.py` | `sys.path.insert(0, "engines")` |
| `UnicodeEncodeError` on `é` in "Cité" | `engines/global_opportunity_expander.py` | `sys.stdout.reconfigure(encoding='utf-8')` |
| `ModuleNotFoundError: opportunity_buckets` | `engines/career_strategy_engine.py` | `sys.path.insert(0, parent)` |
| Same root-import problem | `engines/analysis_cache_builder.py` | same fix |
| Same root-import problem | `engines/inquiry_draft_generator.py` | same fix |
| Same root-import problem | `engines/portfolio_pitch_generator.py` | same fix |
| Same root-import problem | `engines/smart_cover_letter_engine.py` | same fix |
| Same root-import problem | `engines/opportunity_report_engine.py` | same fix |

Root cause: `smart_pipeline_runner.py` uses `subprocess.run`, which sets `sys.path[0]` to the script's own directory. Scripts in `engines/` that import root-level modules (`opportunity_buckets`, `utils_filename`, etc.) couldn't find them. Fix pattern: `sys.path.insert(0, str(Path(__file__).parent.parent))` at top of each affected engine.

**Pipeline now runs to COMPLETE on every run.**

### 4. Photography Contamination — Full Flush
Photography content was entering through three vectors. All three fixed:

**Vector 1 — global_opportunity_seeds.json**  
Removed 6 photography-specific global seeds (Photographers' Gallery, PhotoVogue, LensCulture, Aperture, Photobook Cafe, Der Greif). Replaced with 6 watercolor-appropriate seeds:
- Royal Watercolour Society Open Exhibition (prestige, direct medium match)
- American Watercolor Society Annual International Exhibition (prestige, international)
- Cité Internationale des Arts Residency (Paris, prestigious, strong Asian artist pipeline)
- Japan Watercolor Society Annual Exhibition (local professional credibility)
- Aesthetica Art Prize (open media, international, emerging artist)
- Asian Cultural Council Fellowship (purpose-built for Asian artists building international careers)

**Vector 2 — deploy_data/compact_opportunities.json**  
Cleaned existing data:
- Merged 6 Tokyo Art Book Fair duplicate records → 1 canonical entry (score 9.4, submission URL attached)
- Removed 14 photography-contaminated entries by category and title
- Fixed Self Publish Be Happy category: `global_photobook_platform` → `global_artist_book_platform`
- Net: 191 → 172 records before pipeline rerun

**Vector 3 — source_targets.json (web scraper sources)**  
- Removed 4 photography source URLs: PhotoVogue, LensCulture, Der Greif, Aperture
- Fixed Self Publish Be Happy `source_type`: `photobook` → `artist_book`
- Removed `"photography"` and `"photobook"` from `fit_keywords` — these were causing CuratorSpace and ArtConnect to return photography-tagged open calls on every scrape
- Sources: 19 → 15

---

## Pipeline State After Session

- **176 total opportunities** (clean, no photography contamination in top results)
- **Immediate Best Moves: 2** — Tokyo Art Book Fair (9.4), torch press (6.5)
- **Top 20 by score:** all Tokyo/Japan, mix of bookstore galleries, book fairs, artist spaces, residencies — no photography
- Pipeline runs clean end-to-end, all 72 steps

---

## Remaining Issues Noted (Not Fixed This Session)

1. **Score inflation at the top.** Ten entries tied at 9.4. The scoring system isn't discriminating enough at the upper end. The CLAUDE.md flags this as a known pattern — scores have historically drifted toward confidence without evidence.

2. **Scraped title artifacts.** Entries like "出展お申込み" (application form page title) and "Clone of Japan Fair 2025" are form/page artifacts passing through the quality gate. Need better title extraction or a title validity filter.

3. **Residual photography language in generated copy.** Some engine-generated rationale text still uses "photographic work" or similar phrases (e.g., for UTRECHT). The data is clean; the copy generation hasn't been updated. Low priority but creates confusion in UI.

4. **Illustration sources still active.** HB Gallery, OPA Gallery, Pinpoint Gallery, Tokyo Illustrators Society are in the source list as illustration-adjacent. They may occasionally produce off-medium candidates. Not urgent but worth revisiting when the scraper is next touched.

5. **Verification layer still at ~30% maturity.** Flagged in CLAUDE.md as the highest-priority unfinished system. Nothing done on this in session 3 — pipeline stabilization was the priority.

---

## Architecture Notes

The pipeline is now stable and runs to completion. The data is clean of photography contamination at all three entry points. The next logical phase is improving the quality of what's in the pipeline — better verification, better deduplication upstream (title normalization before records enter the master list), and addressing the score inflation problem.
