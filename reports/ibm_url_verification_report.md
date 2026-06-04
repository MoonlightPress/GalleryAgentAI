# IBM Submission URL Verification Report

**Run:** 2026-06-04  
**Scope:** All IBM-eligible entries with submission_page URLs (53 checked)

## Results

| Status | Count |
|--------|-------|
| 200 OK (live) | 44 |
| 403 Blocked (likely live) | 2 |
| Connection error (checked separately) | 0 |
| 404 Dead | 2 |
| Malformed DDG redirect → decoded + fixed | 7 |

## Dead URLs (404) — hidden from recommendations

| Entry | URL |
|-------|-----|
| NY公募展2026夏（NY Open Call Exhibition Summer 2026） | https://art-incubation.com/index.php/b-1/ |
| Watercolor Open Call Exhibition | https://www.joyinart.cc/chi-joyinart-watercolour-open |

Both flagged: `url_check_status: dead_404`, `recommendation_visibility: hide`

## Malformed DuckDuckGo Redirects — Decoded and Fixed

7 submission_page URLs were stored as DuckDuckGo tracking redirects (//duckduckgo.com/l/...).
These have been decoded to their real target URLs and set back to `show`. Re-verification
recommended on next pipeline pass.

## 403 Blocked (HEAD requests rejected by server — assumed live)

- Northwest Watercolor Society 2026 Annual International  
- Art Fair Tokyo 2026 (artsy.net)

## Next Steps

- Run `python run_full_mochi_pipeline.py` to propagate dead-URL flags to buckets
- Re-verify the 7 decoded URLs with a GET request on next rumor mill pass
