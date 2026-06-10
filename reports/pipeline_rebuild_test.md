# Fresh Bucket-Rebuild Test

**Date:** 2026-06-10
**Goal:** confirm `exclusive_primary_bucket` / IBM rebuild correctly from a fresh run after the engine-ownership refactor, without re-scraping (cost-safe).

## Method
1. Deleted `memory/exclusive_strategy_buckets.json`.
2. Ran `engines/exclusive_strategy_bucket_engine.py` (rebuilds buckets onto `compact_opportunities.json` + regenerates the deleted analysis file).
3. Inspected the resulting Immediate Best Moves via api.py's real `load_opportunities()` + `bucket()` logic (what the frontend actually serves).

> Note: ran the bucketing tail only, not the full discovery pipeline. The discovery steps (`japanese_chinese_discovery_engine`, `grant_discovery_engine`) make billable Tavily calls and are off the weekly-scrape schedule; they are irrelevant to bucket/IBM reproducibility, which operates on existing scored data.

## Result: PASS — fully reproducible

- **Byte-identical output.** `git diff` on `deploy_data/compact_opportunities.json` after the rebuild was **empty** — the committed dataset already equals a fresh engine run. The bucket assignment is deterministic and idempotent. Nothing to commit.
- **Bucket counts:** Immediate Best Moves 13 · Publication Targets 28 · Competitions & Awards 25 · Stretch Targets 24 · Relationship Builders 22 · Publications & Editorial 2 · Japan Book Ecosystem 0 · Needs Research 165 · Low Priority 47 · Reject 53.

## IBM review (13 entries) — correct

All Tier 1-2 and actionable; no Tier 4 prestige leaked in; no photography-reject entries:

- Tokyo Art Book Fair (fair_popup)
- Watercolor open calls: NWWS 2026, CSPWC Annual, アートオリンピア2026, 第113回 日本水彩展, 水性繪畫展覽, 第九屆水主題國際評審藝術比賽
- Relationship venues: UTRECHT, Book and Sons, flotsam books, B&B Shimokitazawa (bookstore_gallery/event)
- Zine ecosystem: ZINEフェス東京, MOUNT ZINE

## Anomalies

1. **Stale displayed deadlines on a few IBM entries** (not a bucketing bug, not a regression):
   - UTRECHT shows `1 July 2025` (past) — correctly retained in IBM because `bookstore_gallery` is a relationship category and the `_ibm_eligible` bypass treats ongoing-venue "deadlines" as non-binding.
   - B&B Shimokitazawa shows `2026年06月06日` (a few days past) — same handling.
   - Some watercolor calls carry year-less deadlines (`May 15th`, `February 26`) that can't be evaluated for pastness without a year.
   - Root cause: per-opportunity deadline freshness. Documented in `reports/patch_exceptions.md #3` — belongs to the Verification layer (refresh deadlines from source). The bucket/IBM logic handles these entries correctly; only the displayed date is stale.

No bucketing or reproducibility anomalies found.
