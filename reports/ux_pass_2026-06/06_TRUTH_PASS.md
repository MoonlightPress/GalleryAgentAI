# Truth Pass — top 20 recommendations vs. reality (2026-06-13)

Method: the exact top 20 the artist would see (12 Immediate Best Moves + top 8 of
the next sections) checked against their live pages (plain HTTP + headless
browser). Raw fetches: `truth_pass_fetches.json`.

**Score: 8 PASS · 4 PARTIAL · 8 FAIL — top-20 accuracy ≈ 40-60%. NOT handoff-ready.**
The 18/20 bar is far from met. The failures are systematic, not random — five
patterns, each now addressed as an engine rule (see bottom).

## Verdicts

| # | Opportunity | Verdict | Evidence |
|---|---|---|---|
| 1 | Tokyo Art Book Fair | PARTIAL | Site live; stored deadline "2027-01-21" looks wrong (TABF exhibitor apps typically close mid-year for the autumn fair) — deadline unverified |
| 2 | 水性繪畫展覽 (Taoyuan watercolor) | **FAIL** | bhuntr.com aggregator listed as the venue; deadline "February 26" yearless → Feb 2026, past |
| 3 | アートオリンピア2026 | **PASS** | Live page confirms 締切 2026-07-31, watercolor eligible, open nationality/age — matches stored data exactly |
| 4 | 第113回 日本水彩展 | **FAIL** | "Official website" is 彩美堂 — a picture-framing & art-transport company's schedule page, not the Japan Watercolor Society |
| 5 | CSPWC Open Water 2026 | **PASS** | artcall.org confirms: opens May 15 2026, deadline June 30 2026 2pm EDT, transparent watercolour — exact match |
| 6 | UTRECHT | **PASS** | Venue alive (browser-verified; python SSL store issue). "1 July 2025" deadline is event residue on an evergreen consignment venue — now blanked by rule |
| 7 | ZINEフェス東京 | **PASS+URGENT** | Event July 11 2026 confirmed; booths close at capacity "~June 20" — stored 06-27 slightly optimistic. **Apply this week.** |
| 8 | MOUNT ZINE | **PASS** | Live, 出品 (submission) program confirmed, twice-yearly cycle as stored |
| 9 | TERAVARNA 9th WATER | **FAIL** | Aggregator link; TERAVARNA is a pay-to-enter online-gallery competition mill — poor fit for tier strategy; "May 15th" yearless |
| 10 | Book and Sons | **PASS** | Live, art-book shop confirmed, rolling consignment |
| 11 | flotsam books | **PASS** | Live, zine/photobook shop confirmed |
| 12 | B&B Shimokitazawa | PARTIAL | Venue live & real; stored deadline 2026-06-06 is past event residue (evergreen venue) — blanked by rule |
| 13 | Aesthetica Art Prize | **PASS** | "Art Prize Entry 2026" shop page live (browser-verified); Oct deadline plausible, unconfirmed |
| 14 | FACE Exhibition 2026 | **FAIL** | 404 — smaf.jp/face/ gone (FACE is real, lives at sompo-museum.org; URL corrected in data) |
| 15 | NIKA spring S20号 | **FAIL** | "Official website" is a Twitter hashtag search; deadline Feb 2026 past |
| 16 | 金风车插画大赛 2026 | PARTIAL | Official page live, 2026 call launched Mar 26; stored deadline 2026-06-05 just passed — actual close date needs confirming |
| 17 | 国际大学生数字艺术设计大赛 | **FAIL** | Aggregator page; March 2026 deadline past; student digital-design contest — weak fit for a 26-year-old watercolor painter |
| 18 | NIKA+ S20号 (duplicate of #15) | **FAIL** | Same competition as #15 listed twice; link is the artkoubo portal homepage; deadline 2026-03-15 past |
| 19 | Applied Arts 2026 Illustration | **FAIL** | Aggregator page literally displays "已过期！" (EXPIRED) — deadline was Feb 8 2026 |
| 20 | ZINEイベント (zindies.co) | PARTIAL | Genuinely useful national ZINE-event calendar with open booth calls — but it's a *resource*, not a single opportunity; mislabeled |

## The five failure patterns → engine rules

1. **Aggregator-as-venue** (#2, #9, #17, #18, #19, #4, #15): bhuntr.com,
   graphiccompetitions.com, shejijingsai.com, artkoubo.jp portal pages, Twitter
   searches, even a framing company. → RULE: aggregator/portal domains can never
   be `official_website`-only entries in action sections; demoted to
   research_needed until a real venue URL exists.
2. **Yearless deadlines never expire** (#2, #9): "May 15th" passes the old
   `_confirmed_deadline` length check and can't be parsed as past. → RULE:
   deadlines without a year are never "confirmed."
3. **Event-date residue on evergreen venues** (#6, #12): consignment/relationship
   venues carry stale one-off event dates. → RULE: relationship categories with a
   past-parsing deadline serve "rolling" (blank date), everywhere — not just in
   Today's Focus.
4. **Duplicates** (#15/#18): same call, two entries. → RULE: dedup by normalized
   title at serving time, keep highest-scored.
5. **404/expired pages not feeding back** (#14, #19): liveness existed as an
   agent but never ran. → Already wired into the pipeline this session; "已过期 /
   expired / 受付終了 / 締め切りました" keywords added to the closed-detection.

## Honest bottom line

The 8 passes include the genuinely best things in the system (Art Olympia, CSPWC,
ZINE Fest with a real urgent deadline, and 4 solid evergreen Tokyo venues) — the
core thesis works. But 8 of 20 top recommendations would have wasted her time or
embarrassed the product. After the rules below are applied and the engine re-run,
re-score; the bar remains 18/20 before handoff.

## Post-fix state (same session)

Rules implemented: aggregator-as-venue guard (bucket engine), yearless-deadline
never confirmed (api), evergreen-residue blanking in shape_card (api, all cards),
title dedup in load_opportunities (api), closed_this_cycle excluded from action
sections (api). Data corrections: FACE → sompo-museum.org, 日本水彩展 →
nihonsuisai.or.jp, both NIKA + Applied Arts + digital-design contest marked
closed (page-confirmed), ZINE Fest deadline tightened to 2026-06-20.

After engine re-run + API restart: IBM = 10 entries, all venue-verified live;
open calls = 6 (every page-confirmed-expired entry gone). Estimated top-20
accuracy now ~16-17/20. Remaining to reach the 18/20 bar:
- TABF "2027-01-21" deadline unverified (suspicious) — confirm on tokyoartbookfair.com
- 水性繪畫展覽 yearless "February 26" — confirm year or drop
- 金风车 deadline 2026-06-05 just passed — confirm whether extended
These three need a follow-up check (one Tavily-free session or the next
maintenance run + manual confirm).
