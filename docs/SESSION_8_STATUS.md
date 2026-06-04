# Session 8 Status — 2026-06-04

## What Was Done

### 1. Tightened Japanese/Chinese Discovery Engine Queries
**Commit:** `e7a6fe9`  
**File:** `engines/japanese_chinese_discovery_engine.py`

All queries now carry explicit medium-specific terms. Previously, several queries were medium-agnostic and could surface literary publishers or non-visual-art open calls.

Changes made:
- `jp_twitter_gallery_koubo` — added 絵画 水彩
- `jp_bijutsutecho_open_call` — added 絵画 水彩 イラスト (was fully agnostic: "アーティスト 公募 open call 募集 2026")
- `cn_lofter_art_recruit` — added 水彩 绘画 插画 (was: "艺术家 征集 公募 展示 2026")
- `cn_zcool_open_call` — added 水彩 插画 绘画 (was: "艺术家 公开征集 展示 2026 截止")
- `cn_illustration_magazine_call` — removed 杂志 (magazine; literary-publisher risk), replaced with 绘画 展览
- `diaspora_tokyo_chinese_art` — added 水彩 绘画 插画
- `diaspora_tokyo_chinese_gallery` — added watercolor illustration
- `diaspora_sg_chinese` — added 水彩 插画
- `diaspora_van_chinese` — added 水彩 插画

**Result:** 9 queries tightened. All 31 query IDs remain unique.

---

### 2. Rumor Mill Gap-Filler Run
**Commit:** `6864683`  
**Command:** `python engines/rumor_mill_engine.py --max 30`

All 282 items in the `needs_research` bucket were already searched on 2026-06-03 to 2026-06-04 (within the 7-day cache window). Zero new searches were triggered; zero items moved. Log timestamp updated.

---

### 3. IBM Submission URL Verification (HEAD requests)
**Commit:** `7fbf4ed`  
**Files:** `deploy_data/compact_opportunities.json`, `memory/ibm_url_check_results.json`, `reports/ibm_url_verification_report.md`

53 IBM-eligible entries with `submission_page` URLs were checked via HTTP HEAD request.

| Result | Count |
|--------|-------|
| 200 OK (live) | 44 |
| 403 Blocked (HEAD rejected; assumed live) | 2 |
| 404 Dead | 2 |
| Malformed DuckDuckGo redirect → decoded & fixed | 7 |

**Dead URLs flagged** (`url_check_status: dead_404`, `recommendation_visibility: hide`):
- NY公募展2026夏 → `https://art-incubation.com/index.php/b-1/`
- Watercolor Open Call Exhibition → `https://www.joyinart.cc/chi-joyinart-watercolour-open`

**Malformed URLs fixed:** 7 DuckDuckGo tracking redirects decoded to real target URLs (e.g., biscuitgallery.com, gallery219.com, tokyoartsandspace.jp). Set back to `show` with `url_check_status: malformed_url_fixed`.

---

### 4. Medium Confirmation Gate — Full Re-run
**Commit:** `f215316`  
**Command:** `python engines/medium_confirmation_gate.py`  
**File:** `reports/medium_confirmation_gate_report.md`

| Result | Count |
|--------|-------|
| Confirmed (explicit medium signal) | 185 |
| Rerouted to needs_research | 85 |
| Skipped (reject/low_priority) | 16 |
| **Total** | **286** |

The tightened discovery queries from step 1 do not affect currently indexed opportunities (discovery engine hasn't been re-run yet), so the gate numbers reflect the existing corpus.

---

## Pipeline State After Session 8

- **Total opportunities:** 286
- **Dead submission URLs:** 2 (hidden from recommendations)
- **Fixed malformed URLs:** 7
- **Needs_research bucket:** 282 items (all searched within last 7 days)
- **Confirmed medium:** 185 of 286
- **Discovery engine:** tightened; queries will be fresher on next run (7-day cache will expire)

## What's Next

1. **Re-run discovery engine** after cache expires — tightened queries will take effect, reducing literary-publisher noise
2. **Re-verify the 7 decoded DDG URLs** with GET requests (rumor mill will catch them on next pass)
3. **Verify remaining 101 IBM-eligible entries** that lack a submission_page URL — rumor mill is the right tool
4. **Stabilization** remains the priority phase (see CLAUDE.md) — no new features until verification improves
