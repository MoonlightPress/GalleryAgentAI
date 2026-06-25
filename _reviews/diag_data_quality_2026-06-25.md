# Mochi — Data-Quality & Recommendation-Correctness Diagnostic (2026-06-25)

**Scope:** read-only audit of `deploy_data/compact_opportunities.json` (**522** opportunities) and the
scoring/bucketing/verification engines (`exclusive_strategy_bucket_engine.py`, `career_strategy_engine.py`,
`deadline_normaliser.py`, verification path). Artist: GEGYjiji, watercolor painter, Tokyo. No edits, no paid
calls. "Today" = 2026-06-25. All counts computed against the served JSON.

Findings are prioritized blocker → low. Each: **SEVERITY — finding — evidence — one-line fix.**

---

## BLOCKER 1 — "Immediate Best Moves" contains effectively ZERO accomplishable actions

`immediate_best_moves` (the headline surface, the core product promise) holds **7** items. By the engine's
own call-deadline logic, **0 of 7** are a genuinely-open dated open call she can act on:

- **UTRECHT** — score 10.0, `bookstore_gallery`, deadline **"1 July 2025"** (a year past) still displayed;
  quick_action is *"Visit their website... get a feel for the space."* Passive + stale.
- **B&B Shimokitazawa** — `bookstore_event`, deadline **2026-06-06 (past)**, quick_action = "Research current programming."
- **MOUNT ZINE** — `zine_shop_consignment`, deadline = "Twice-yearly... watch @mountzine." No dated action.
- **Book and Sons** — `bookstore_gallery`, "Rolling consignment — contact on Instagram." Passive.
- **Zine & Book フェス in 神保町** — deadline literally says **"(past). Watch October 2026."**
- **TOKYO ART BOOK FAIR 2026** — `zine_fair_booth`, deadline **None**, quick_action = "Verify submission page and deadline before applying" (i.e. unverified).
- **Tokyo Art Book Fair** — score 9.6, deadline **2027年1月21日** (far-future / suspect; see Blocker 3).

So the act-now bucket is 6 evergreen "browse/consign anytime" venues + 1 far-future fair. None is a dated,
enterable watercolor call. This is the headline screen she will test first.

**Fix:** Gate `immediate_best_moves` to entries with a *future, dated, enterable* call deadline; move
evergreen venues to a labeled "Rolling — pitch anytime" shelf and suppress their stale `deadline` display.

---

## BLOCKER 2 — Her #1 category (`japan_watercolor_open_call`) is locked OUT of "act now"; open calls are buried

The IBM promotion rule whitelists `category == 'global_watercolor_open_call'` but **not**
`japan_watercolor_open_call` (engine lines ~487–493). Result for her single most-relevant category:

- 15 `japan_watercolor_open_call` total → routed **11 research_needed, 2 reject, 1 competitions, 1 stretch**. **0 reach immediate_best_moves.**
- **13** of them are `native_medium='painting'`, verified/strong_partial, score 7.6–10.0 — i.e. they *meet*
  the IBM bar in every dimension except the category-name whitelist.
- At least **2 are genuinely open right now** yet sit in `research_needed`:
  - **アートオリンピア2026** — score 10.0, verified, Tokyo, deadline **2026-07-31** (open).
  - **Blooming Stories 2026** — score 9.68, strong_partial, deadline **2026-06-29** (open in 4 days).

A real watercolor open call closing in days is hidden in "Needs Research" while a stale bookstore sits at #1.

**Fix:** Add `japan_watercolor_open_call` to the IBM watercolor-promotion rule (same painting + verified +
score≥7 + future-deadline guard as global), and require a future deadline so closed rounds don't leak.

---

## BLOCKER 3 — Deadline freshness: 165 past-deadline opps live; far-future "2027" artifacts surface

Of 522: **past = 165**, future/open = **61**, missing/rolling = **198**, unparseable = **98**, far-future
(≥2027) = **4**.

- **165 opps carry a deadline that has already passed.** Many are spring-2026 rounds now closed
  (e.g. World Illustration Awards 2026-03-31, Jackson's Art Prize 2026-02-11, American Illustration 2026-03-18,
  ZINEフェス東京 2026-04-08). The engine routes most to research_needed, but the past deadline is still *displayed*
  (UTRECHT "1 July 2025" survives in IBM).
- **Only 61 opps are genuinely open** across the whole corpus — and only ~2 in her top category.
- **Far-future / suspect:** "Tokyo Art Book Fair" shows **2027年1月21日** and that lone "future" date is what
  lets it sit in IBM (see Blocker 1) — a dedup/parse artifact, not a real near-term action.
- **98 unparseable deadlines** = freeform strings ("Check source", "Annual — 113th edition June 2026...") that
  no gate can evaluate, so they default through as if dateless.

**Fix:** Run `deadline_normaliser` to demote passed deadlines, hide passed dates from *display* on every
surfaced card, and treat ≥2027 single-date fairs as "watch," not "act now."

---

## HIGH 4 — Duplicate events inflate the corpus and pollute buckets

**14** near-duplicate title groups (year-stripped normalization), **29** records, **~15 excess**. Largest:

- **Tokyo Art Book Fair** event appears **5×** under non-reject/visible variants plus reject dups: "Tokyo Art
  Book Fair" (dl 2027), "TOKIO ART BOOK FAIR 2026" (typo'd domain), a MOT museum-URL capture, "TOKYO ART BOOK
  FAIR 2026" (zine_fair_booth), plus Instagram-capture rejects — **3 different URLs, 3 different deadlines, same event.**
- Others: Chinese Children's Illustration ×3; アートオリンピア ×2; Fukuoka Art Book Fair ×2; 二科展 NIKA ×2
  (a literal `+` typo split: "NIKA nika" vs "NIKA+nika"); IlloBoom! ×2; MAW 2026 ×2 (full-width vs half-width
  parens); Royal Institute of Painters ×2; INSTINC ×2.

Duplicates double-count toward bucket sizes and make the same event read as multiple "moves."

**Fix:** Dedupe on a normalized key (lowercased title with years/punctuation/width-folding stripped + domain);
keep the best-verified record, merge the rest.

---

## HIGH 5 — `native_medium='unknown'` on 317/522 (61%) degrades fit-scoring

Distribution: **unknown 317, painting 111, mixed 85, photography 9.**

Fit-scoring is medium-driven and visibly weaker when medium is unknown:
`visual_fit_score` mean by medium — **unknown 0.53**, painting 1.09, mixed 1.99, photography 0.68.
Worse, several IBM/promotion rules require `native_medium == 'painting'` *exactly*, so a watercolor call left
`unknown` can never qualify for "act now" even if it's perfect for her. 61% of the corpus is in that blind spot.

**Fix:** Improve medium inference (title/category keywords → painting/watercolor) so watercolor calls stop
defaulting to `unknown`; treat `unknown` from a watercolor-category as painting for the fit/IBM gates.

---

## HIGH 6 — Tokyo city-gate misses nationwide-JP and mislabeled-city calls

The painting→IBM rule requires `city in ('tokyo','')`. **31** painting, verified, score≥7.5 opps fall outside
that gate purely on the city *string*, including JP calls she can absolutely enter:

- **Blooming Stories 2026** city="**Japan**" (not "tokyo") → research_needed despite open dl 2026-06-29.
- **ゆめ画材公募** city="Japan", **Japan in Acquarello 2026** city="Yokohama", **第15回 九条美術展** city="Chiba".
- City strings are wildly non-normalized: "Tokyo", "Japan / Tokyo / Online", "Koenji, Tokyo", "Tokyo — Koenji",
  "Shimokitazawa, Tokyo", "Tokyo / Online" are all distinct values — substring/exact gates miss most of them.

**Fix:** Normalize city to a country/region (`is_japan`, `is_tokyo`) before gating; accept nationwide-JP
(city="Japan"/blank) for a Tokyo-resident artist.

---

## MEDIUM 7 — Listing-page / index artifacts still surfaced as "opportunities"

The ingestion `_listing_artifact` guard misses several. Surviving in non-reject buckets:

- **"Browse opportunities | CuratorSpace"** and **"CuratorSpace"** — both in `publication_targets` (the index page itself, not a call).
- **"www.curatorspace.com"** (research_needed) — a CuratorSpace *detail* capture for "Spectroscope Residency...
  East Quay open call for **disabled artists in South West England**" — an opportunity she is geographically
  and categorically ineligible for, surfaced via a raw URL-title.
- **"SUBMISSIONS - marblepress.com"**, **"Submissions - Little Press Publishing"** — bare submission-index pages.

**Fix:** Extend the listing-artifact rejecter to catch `curatorspace.com/opportunities`, bare "Submissions -
<domain>" / "<domain>" titles, and host==title URL-captures.

---

## MEDIUM 8 — Social-media-only captures used as the action venue

`source_url` hosts: **instagram.com 36, x.com 22, note.com 22, facebook.com 9, twitter.com 1.** Most are
correctly rejected, but at least one Instagram-reel-only listing survives (Creators for Tomorrow 2026 /
藝術培育計劃, research_needed). An Instagram reel is not an applicable submission page; for the visible TABF
exhibitor-call dups the *only* URL is an Instagram post.

**Fix:** Treat a social-only `source_url` (no `official_website`/`submission_page`) as
`submission_process_unknown` and keep it out of actionable buckets until a real venue URL is found.

---

## MEDIUM 9 — Eligibility marking runs in-memory but is NOT persisted to the served data

`choose_bucket` sets `student_call` / `eligibility_conflict` on the opp dict, but in the served
`compact_opportunities.json` **`student_call` is set on 0 records and `eligibility_conflict` on 0 records.**
So the "never show a call she can't enter" guard and the student-fee advantage flag aren't visible to the app —
either the bucket run that wrote this file predates the guard, or the compacting step drops these fields.
Combined with #7, ineligible calls (e.g. the disabled-artists/region-locked East Quay listing) can still reach her.

**Fix:** Persist `student_call`/`eligibility_conflict` through the compact writer and re-run the bucket engine
so the served data reflects the eligibility pass.

---

## LOW 10 — `overall_score` is differentiated, but compressed at the top

`overall_score`: min 0.7, max 10.0, mean 6.74, median 7.2, **126 distinct values** — so it is *not* "everything
~10." But the distribution is top-heavy: **~220 of 522 (42%) score 8–10** (score~8:77, ~9:78, ~10:65), which
flattens ranking within the actionable band (many perfect-10s, e.g. 9 of the 13 buried watercolor calls all sit
at 10.0). `differentiated_score` spreads better (238 distinct, but ranges to 11.5 — i.e. it can exceed the
nominal 10 ceiling, a minor scale inconsistency).

**Fix:** Use `differentiated_score` (or a deadline-urgency tiebreaker) as the within-bucket sort so the dozens
of 10.0s don't order arbitrarily; clamp/document the >10 differentiated values.

---

## Summary table

| # | Sev | Finding | Headline number |
|---|-----|---------|-----------------|
| 1 | blocker | "Act now" has no accomplishable actions | 0/7 IBM items are open dated calls |
| 2 | blocker | Her #1 category locked out of "act now" | 13 qualifying watercolor calls, 0 promoted; 2 open now buried |
| 3 | blocker | Stale/past deadlines surfaced | 165 past, only 61 open; 98 unparseable |
| 4 | high | Duplicate events | 14 groups / ~15 excess; TABF ×5 visible |
| 5 | high | Medium unknown cripples fit | 317/522 (61%) unknown; visual_fit 0.53 vs 1.09 |
| 6 | high | Tokyo gate misses nationwide JP | 31 painting calls gated out on city string |
| 7 | medium | Listing/index artifacts surfaced | ≥5 CuratorSpace/Submissions index captures live |
| 8 | medium | Social-only URLs as venue | 36 IG / 22 X / 22 note source_urls |
| 9 | medium | Eligibility flags not persisted | student_call=0, eligibility_conflict=0 in served data |
| 10 | low | Score top-compressed | 42% score 8–10; differentiated_score exceeds 10 |
