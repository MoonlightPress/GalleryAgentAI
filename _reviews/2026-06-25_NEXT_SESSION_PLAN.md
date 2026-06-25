# Next-session plan & handoff (2026-06-25, end of a long session)

**Read this first in a fresh chat.** Everything below is committed + pushed to `main` and DEPLOYED
(site 200/200) unless noted. Test suite is **118/118 green**.

## What shipped this session (all live)
- **Magic loop fixed:** "act now" = real dated watercolor open calls, not evergreen bookstores
  (`exclusive_strategy_bucket_engine.choose_bucket` — japan_watercolor_open_call whitelisted, city-gate
  broadened to country==Japan, evergreen venues kept out, Tier-1 ambient venues → japan_book_ecosystem).
- **Japanese date parser** (`deadline_normaliser.parse_deadline_date`): reads `年月日` + Reiwa `令和`.
  This is ALSO the Chinese date format — Chinese dates parse for free.
- **Recurrence detector** (`_is_recurring`): reads `第N回/第N届` + JP/CN annual markers + checks the name.
- **Suggestion-queue order** (`api._feed_order_key`): live calls first → missed-but-recurring by NEXT
  round (resurface as prep targets) → dead one-offs last.
- **Readiness:** Tier-4 math fixed (no longer maxes from Tier-3 basics); bars update live (`refreshCareer`
  refetches /api/saffron + /api/career_strategy).
- **Robustness:** atomic JSON writes (`_atomic_write_json`) + crash-safe board readers (kills random 500s).
- **Evergreen venues** show "Rolling · pitch anytime" not a stale date.
- **Exhibition entries editable** (PATCH /api/exhibition_log/{id} + inline ✎ edit UI).
- **Money-bomb scheduler archived** (archive/dead_code/).
- 5 full-system **diagnostic reports** in `_reviews/diag_*_2026-06-25.md`.

## Decisions locked this session
1. **Discovery cadence:** full PAID pass = **quarterly (~3mo) + only if she's actively using the app**
   (visit telemetry is the signal). NOT monthly. ~$26/quarter ≈ $9/mo. Free weekly maintenance keeps
   deadlines/bucketing fresh between passes. (Recorded in CURRENT_STATE.)
2. **Japanese UI = dropped.** She's Chinese, reads Chinese; a Japanese interface is friction, no benefit.
   The 95-missing-ja-keys "blocker" is moot. (Her opportunities are Japanese; her UI stays zh/en.)
3. **Saffron reframe = HYBRID:** re-rank is the base (nothing hidden; opps ordered by fit-to-her-level),
   PLUS an unlock *moment* (celebration + a "newly in reach" badge when she crosses a level). Strengths-first
   framing, one "next unlock" instead of a wall of gaps.
4. **Geography = global open-calls + local venues.** Open calls / competitions / juried societies are
   global (she submits remotely → JP, CN, US, EU all count). Physical venues / relationships are local
   (Tokyo where she lives + Chinese cities where she has ties). Rank by "can she actually act on this from
   where she is."

## TWO remaining builds (in order)

### A. Saffron hybrid reframe (visual + wiring — DO WITH SCOTT'S EYE on layout)
- **Wiring (the magic, objective):** rank opportunities by fit-to-her-current-level. Her readiness/tier
  comes from `career_strategy_engine` (tier_3/tier_4 readiness). Opps have `career_tier`. Re-rank so
  tier-appropriate opps rank up and stretch opps sink, RISING as she levels. Likely a new factor in
  `api._ranked_score` / `_feed_order_key` (careful — that ranking was just stabilized; add a gentle
  level-fit term, don't rewrite). Test it.
- **UI (subjective — show Scott options):** (1) strengths-first header with a current-level badge framed
  as earned; (2) ONE "next unlock" card with the `GapCorrectionForm` inline, not a wall of gaps;
  (3) celebration moment on level-up ("Tier 3 is realistic for you now"); (4) "newly in reach" badge on
  opps the new level unlocks. Files: `SaffronPage.jsx` (CareerReadiness / CareerPosition), new i18n keys
  (zh/en only — ja dropped).
- Also fold in: walkthrough #3 "blank advice when maxed" → show a positive advanced-state line, not blank.

### B. Global free-discovery scraper (additive, green-field, SAFE)
- The free alternative to Tavily discovery. **Started this session:** see
  `engines/discovery_sources.py` (curated source catalog — JP/CN/US/EU watercolor + art-call platforms).
- Next: a generic fetch+parse engine that pulls each source → opportunity records in the
  compact_opportunities schema, dedupes against existing, runs as a FREE discovery step. Reserve Tavily
  for occasional new-venue hunting only.
- Date parsing already handles JP+CN (`年月日`). Recurrence handles `第N回/第N届`.

## Still-open smaller items (from diagnostics + walkthrough)
- **2a:** Saffron "X opportunities open" counts are dead numbers — make them click through to the list
  (MarketStats only has counts; needs opp data or a link to the Mochi page/calendar).
- **TABF dedup:** Tokyo Art Book Fair still appears multiple times (spelling/URL variants the name-dedup
  misses).
- **zh data leaks:** a few English data fields render raw in 中文 (TrackerSection outcome,
  OppDetailPanel contact_note, a hardcoded SaffronPage gaps summary). See diag_frontend report.
- **Preference loop may be stranded:** `peppercorn_preference_engine` (which applies her prefs to ranking)
  runs in the LAPTOP pipeline, but she edits on the SERVER, and deploy only syncs laptop→server. Her
  server-side preference edits likely never reach the engine. Needs a server→laptop memory sync, or move
  preference application to serve-time.

## Deploy / ops
- Deploy: `bash /c/ScottStuff/GalleryAgentAI/deploy.sh` (ships engines + frontend; snapshots + preserves
  server memory; restarts mochi-api). Key at `Web/LightsailDefaultKey-us-east-1.pem`, box
  ubuntu@18.206.62.200, app at /opt/mochi, site https://twilightdreamworks.com/mochi/.
- Pushes are authorized (Scott: "commit and push occasionally").
