# Backend / API correctness & robustness review — Mochi

_Reviewer facet: Backend / API correctness and robustness. Read-only. Pre-launch._
_Date: 2026-06-24. Files in scope: `api.py` (2954 lines), `recommendation_readiness.py`, the consuming frontend (`frontend/src/...`)._
_Method: full read of both backend modules + relevant frontend consumers; ran `uvicorn api:app` locally on port 8011 against the live cached `deploy_data/compact_opportunities.json` (416 served opportunities / 522 raw) and curled every endpoint. No pipeline run, no Tavily, no Anthropic calls._

## Summary

The backend is in good shape for launch. The readiness contract is coherent end-to-end with no field-name drift; the serve-time guards are largely correct and applied to all actionable surfaces; missing-file safety is genuinely solid (the prior audit's "unguarded reads / 500s" claim is correctly debunked for the *missing-file* case); and i18n has broad coverage for dynamic opportunity strings.

Three things are worth knowing before launch, none of them a hard blocker:

1. **Corrupt-file (not missing-file) crash safety is only partial.** Every read is `.exists()`-guarded so a *missing* file returns a graceful empty — that claim holds. But most hot GET readers are **not** wrapped in `try/except`, so a file that *exists but contains malformed JSON* raises and returns a 500. Because the app itself writes these JSON files on POST/PATCH, an interrupted write (process killed mid-`write_text`) can leave truncated JSON and then *every* subsequent page load 500s until the file is repaired. This is the most launch-relevant robustness gap.

2. **Two different "is the deadline past?" functions disagree on 40 of the live items.** `_deadline_passed()` (the section gate) judges by the *latest* date in a multi-date field and is strict; `_deadline_past()` (the card-display field + `/api/today`/IBM eligibility) judges by the *first* date and has a 7-day grace. The section gate is the correct one and keeps still-open items in their sections. The only user-visible fallout is one card (Tuttle, "October 31, 2025 or August 25, 2026", still open until Aug 2026) that is shown with a red "deadline passed" pill and a sort penalty in an actionable section. All other disagreements resolve to relationship-evergreen items (handled) or land in the non-actionable watch list (honest).

3. **i18n: dynamic opportunity strings are ~100% covered in both zh and ja, but the static authored Saffron prose is zh-only.** `translation_cache.json` has a `zh` key and no `ja` key, and the frontend merges a static `SF_ZH` map for zh with no ja equivalent. So Japanese viewers see the hand-authored Saffron analysis prose in English. This is a known, documented gap, not a regression.

Plus one security item that depends on server env config: the GitHub deploy webhook **skips signature verification entirely when `MOCHI_WEBHOOK_SECRET` is unset** — confirm the secret is set on the production box.

## Endpoint inventory

All endpoints returned HTTP 200 (or the documented 400/404) against live cached data.

| Method | Path | Serves | Notes |
|---|---|---|---|
| GET | `/api/opportunities` | All buckets (immediate_best_moves, open_calls, publication_editorial, competitions_awards, zines_and_print, relationship_targets, watch_list) + meta + accepted_celebrations | Hot path. gzip-compressed. Emits the full readiness contract per card. |
| GET | `/api/today` | Today's Focus: quick_win / high_impact / stretch_goal | Quick-win precedence: submission follow-up → stale CRM → best relationship IBM. |
| POST | `/api/feedback` | Records follow/applied/maybe_later/not_for_me; auto-logs a submission on "applied"; suppresses on "not_for_me" | Own 400 path verified (invalid action → 400). |
| GET | `/api/feedback/insights` | Dismissal/boost counts by category (≥3 threshold) | |
| POST | `/api/feedback/suppress-category` | Adds a category to `learned_preferences.json` | |
| GET | `/api/submissions` | Submission log | |
| POST | `/api/submissions` | Add submission | |
| PATCH | `/api/submissions/{sub_id}` | Update outcome / followed_up / notes | 404 on unknown id. |
| GET | `/api/contacts` | CRM contacts, priority-normalized + status-sorted | |
| POST | `/api/contacts` | Upsert-by-name contact | |
| PATCH | `/api/contacts/update` | Update contact by name (body) | |
| PATCH | `/api/contacts/{contact_name}` | Update contact by path name | |
| GET | `/api/contacts/lookup?name=` | Single contact, exact then partial match | Returns `null`/200 on miss. |
| GET | `/api/saffron` | The entire Saffron observatory payload (22 top-level keys) + `_i18n` map | Hot path. ~370KB. Largest handler (~1200 lines). |
| GET | `/api/peppercorn` | Peppercorn profile + live_counts; synthesizes defaults if no file | |
| POST | `/api/peppercorn` | Overwrites `peppercorn_profile.json` | |
| POST | `/api/saffron_answer` | Writes a single `saffron_answers` field | |
| GET | `/api/career_events` | Career event log | |
| POST | `/api/career_events` | Add event | |
| PATCH | `/api/career_events/{event_id}` | Edit event note | Returns `{ok:false}` (200) on miss, not 404 — minor inconsistency. |
| DELETE | `/api/career_events/{event_id}` | Remove event | |
| GET | `/api/exhibition_log` | Exhibition log | |
| POST | `/api/exhibition_log` | Add exhibition | |
| DELETE | `/api/exhibition_log/{entry_id}` | Remove exhibition | |
| POST | `/api/issues` | User-reported issue (→ `user_reported_issues.json`) | Empty text → 400. |
| GET | `/api/issues` | List reported issues | |
| GET | `/api/career_strategy` | `career_strategy_report.json` | **404 if file missing** — the one read that intentionally surfaces an error instead of an empty. |
| GET | `/api/health` | `{status: ok}` | |
| POST | `/webhook/deploy` | GitHub push → background deploy | **Signature check skipped if secret unset** (see Issues). |

### Dead / unused / duplicated

- **No dead endpoints found** — all are consumed by the frontend or are operational (health/webhook).
- **Two ways to update a contact** (`PATCH /api/contacts/update` by body-name and `PATCH /api/contacts/{contact_name}` by path-name) overlap in purpose; not a bug, just redundancy. `ContactUpdate` carries `last_visited`; `ContactPatch` carries `personal_note`/`response_received`. They are not perfectly interchangeable, so consolidation would need care.
- **Heavy duplication of category-group dictionaries** inside `/api/saffron` (`CAT_GROUPS`, `_MS_CAT_GROUPS`, `PUB_CATS`, `EXPECTED`, plus module-level `SECTION_CATEGORIES`). Not a correctness issue but a maintenance hazard — categories must be kept in sync across ~5 maps by hand.

## What I verified (with evidence)

### 1. Readiness contract is coherent end-to-end — VERIFIED

`recommendation_readiness.assess_actionability()` returns exactly `{actionability_status, review_flags, recommendation_reasons}` (via `_result()`). `shape_card()` (api.py:607-609) copies these three keys verbatim onto every card. The frontend reads exactly these three names in `frontend/src/utils/recommendationQuality.js:178-180` (`backendRecommendation()`):

```
status: opp.actionability_status || null,
flags:  Array.isArray(opp.review_flags) ? opp.review_flags : [],
reasons: Array.isArray(opp.recommendation_reasons) ? opp.recommendation_reasons : [],
```

No field-name drift. Status values (`ready`, `check_before_acting`, `review`, `closed_or_stale`) match between the constants in `recommendation_readiness.py` and the frontend test fixtures. Live evidence — IBM[0] (Tokyo Art Book Fair):

```
status: ready | flags: [] | reasons: ['Deadline is checked', 'Fee is known', 'Submission path is clear']
```

`reasons` is correctly capped at 3 (`_unique(reasons)[:3]`). The frontend treats backend status as canonical and falls back to its own checklist heuristics only when fields are absent — the intended design.

### 2. Serve-time guards `_deadline_passed()` / `_listing_artifact()` — VERIFIED with one card-level caveat

`_listing_artifact()` correctly drops index/nav captures. Direct test:

```
True  'Browse opportunities'    True 'CuratorSpace'   True 'Open Calls'
False 'UTRECHT'                  False 'Real Gallery Name'
```

Confirmed applied in `load_opportunities()` (api.py:733), so it filters **every** surface (opportunities buckets, today, saffron all read post-filter). Live payload had 0 listing artifacts.

`_deadline_passed()` is applied to IBM (api.py:787) and every category section (api.py:806). It correctly:
- exempts relationship/evergreen categories,
- treats recurring hints (rolling/annual/…) as never-past,
- judges multi-date fields by the **latest** date (the safe choice — wrongly hiding an open call is the worse error), verified: `"October 31, 2025 or August 25, 2026"` → `passed=False` (kept), `"October 31, 2025"` alone → `passed=True` (dropped).

Live check across the six actionable sections: **0** `deadline_past=True` leaks in immediate_best_moves / open_calls / publication_editorial / competitions_awards / relationship_targets; **1** in zines_and_print (Tuttle, see Issues). The watch_list legitimately contains past items labelled `closed_or_stale`.

`/api/today` uses `_ibm_eligible()` (→ `_deadline_past`) and `_deadline_past` in its fallbacks, **not** `_deadline_passed`. Live `/api/today` returned three `ready` items (UTRECHT / Tokyo Art Book Fair / FY2026 Life with Art Grant) — none stale. The relationship-card deadline-clearing logic (api.py:2772-2774, mirror of 550-551) correctly blanks residual past dates on evergreen venues before display.

### 3. Error handling — missing-file safety VERIFIED; corrupt-file safety PARTIAL

I enumerated all 40 `json.loads(...read_text...)` sites. **Missing-file:** every one is either preceded by `path.exists()` (returning a graceful empty), an early-return guard (e.g. `/api/feedback/insights` returns `{...,total:0}` if absent; `load_opportunities` returns `[]`), or a cache fallback. The prior audit's "unguarded file reads / 500s" is correctly debunked **for missing files** — confirmed live (all GETs 200 even with empty-array data files present).

**Corrupt-file:** only a minority of reads are `try/except`-wrapped (the submission-states helper at :95-98, and the career-momentum block at :1968-1992, the translation-cache merge at :2418-2423, the live-counts helper at :2473-2477, the submission-followup at :2788-2793). The hot GET readers — `load_opportunities` (:721), `/api/saffron`'s many loads, `/api/contacts` (:1085), `/api/peppercorn` (:2498), `/api/career_strategy` (:2948) — are bare. A file that exists with malformed JSON raises `JSONDecodeError` → unhandled → HTTP 500. Confirmed `json.loads('{ this is : not json')` raises. Since POST/PATCH handlers rewrite these same files (`write_text`), an interrupted write is a realistic way to produce a corrupt-but-present file.

### 4. i18n payload — VERIFIED with a documented ja gap

`/api/saffron` builds `_i18n` (zh/ja) from the opportunity data's own `name_zh/ja`, `one_sentence_zh/ja`, `why_it_fits_zh/ja`, then merges `translation_cache.json` into **zh only** (api.py:2399-2423). Live: `_i18n.zh` = 1697 entries, `_i18n.ja` = 1148 entries. Raw data coverage: of 522 opps, `one_sentence_zh` = 522, `one_sentence_ja` = 520 — so dynamic opportunity strings are essentially fully bilingual.

The gap is the **static, hand-authored Saffron prose** generated inside the api handler (benchmark summaries, pathway/`requires_now` text, peer `fit_reason`, press notes, etc.). `translation_cache.json` has only a `zh` key (confirmed: `['zh']`, 551 entries, no `ja`). The frontend (`SaffronPage.jsx:1942-1946`) merges a static `SF_ZH` map for zh and has **no** ja equivalent (`return rawData?._i18n?.ja || null`). Net: Japanese viewers get translated opportunity names/one-liners but English authored analysis prose. Matches the CURRENT_STATE "known gap."

### 5. Other live checks

- Webhook with `X-GitHub-Event: ping` → 200 no-op; with `push` and no secret → 200 and queues deploy (script absent locally so it no-ops).
- Invalid feedback action (clean request) → 400. Empty issue text → 400. Unknown submission/contact id on PATCH → 404. Contact lookup miss → `null`/200.

## Issues found

### I-1 — Corrupt (present-but-malformed) JSON file causes 500 on hot endpoints
- **Severity:** Medium
- **Location:** `api.py:721` (`load_opportunities`), and all bare `json.loads(...read_text...)` in `/api/saffron` (e.g. :1226, :1231, :1253, :1309, :1378, :1883, :2255), `/api/contacts` (:1085, :1148, :1181, :1207), `/api/peppercorn` (:2498), `/api/career_strategy` (:2948).
- **Evidence:** Reads are `.exists()`-guarded (missing → empty) but not `try/except`-wrapped (malformed → `JSONDecodeError` → 500). The app's own POST/PATCH handlers write these files, so an interrupted write leaves truncated JSON; thereafter every load of the page that reads it 500s. `json.loads('{ this is : not json')` confirmed to raise.
- **Suggested fix (described):** Wrap each file read in a small helper, e.g. `_load_json(path, default)` that does `if not path.exists(): return default` then `try: return json.loads(...) except (ValueError, OSError): return default` (and optionally log). Apply uniformly. This is consistent with the try/except already used in the career-momentum block. Separately, harden writes (write to a temp file then `os.replace`) so a kill can't truncate a live file.

### I-2 — Multi-date item mislabelled "deadline passed" in an actionable section
- **Severity:** Low
- **Location:** card-field computation `_deadline_past()` (`api.py:266-271` via `_parse_deadline_date` :228-263, which uses `.search()` → first date) vs section gate `_deadline_passed()` (`api.py:648-691`, judges by latest date). Frontend consumes the card field at `recommendationQuality.js:15` (-18 sort penalty) and `OppCard.jsx:165-169` (red pill).
- **Evidence:** "Become an Author — Tuttle Publishing", `deadline = "October 31, 2025 or August 25, 2026"` (open until Aug 2026): served in `zines_and_print` with `deadline_past=true` and `actionability_status=closed_or_stale`. `_deadline_passed=False` (correctly kept it); `_deadline_past=True` (wrongly flags it). The source data also carries `deadline_past:true` (pipeline used first-date logic), and `assess_actionability` reads that data field, so the readiness status is wrong too. Only 1 such item leaks into the 6 actionable sections today; the other 40 inter-function disagreements resolve to relationship-evergreen (handled) or watch_list (honest).
- **Suggested fix (described):** Make `_deadline_past()` and the pipeline's `deadline_past` stamp use the same "latest date in field" logic as `_deadline_passed()` (extract all dates, compare `max`). Best done once as a shared helper so the card field, IBM eligibility, `/api/today`, and the data stamp all agree.

### I-3 — English day-less month-year ("January 2020") never treated as past by the section gate
- **Severity:** Low
- **Location:** `_deadline_passed()` day-less fallback, `api.py:686-690` — only matches the Japanese `(20\d{2})\s*年\s*(\d{1,2})\s*月` pattern; there is no English "Month YYYY" branch. `_deadline_past()` also misses it (`_parse_deadline_date` requires a day).
- **Evidence:** `_deadline_passed({"deadline":"January 2020"})` → `False`. A non-relationship section item whose deadline is a bare past English month-year would not be hidden. (No such item is in the current live actionable sections, so impact today is nil — but it's a latent correctness hole.)
- **Suggested fix (described):** Add an English month-name + 4-digit-year fallback to the day-less branch (mirror of the existing JP branch), comparing `(year, month) < (today.year, today.month)`.

### I-4 — Deploy webhook accepts unsigned requests when the secret is unset
- **Severity:** Medium (config-dependent; security)
- **Location:** `api.py:2922` (`WEBHOOK_SECRET = os.environ.get("MOCHI_WEBHOOK_SECRET", "")`) and :2932 (`if WEBHOOK_SECRET:` — verification is skipped entirely when empty).
- **Evidence:** Local POST to `/webhook/deploy` with `X-GitHub-Event: push` and no secret → 200 and `_run_deploy()` is queued (it only no-ops here because `scripts/deploy_from_git.sh` is absent locally). On the server, if that script exists and the env var is unset, any unauthenticated caller can trigger a git-pull/deploy + nginx reload.
- **Suggested fix (described):** Fail closed — if `WEBHOOK_SECRET` is empty, reject all webhook calls (return 503/403) rather than running unverified. At minimum, confirm `MOCHI_WEBHOOK_SECRET` is set in the production environment before launch (it's part of the "server autonomy" checklist already).

### I-5 — Japanese static Saffron prose renders in English
- **Severity:** Low (documented, cosmetic)
- **Location:** `translation_cache.json` (zh-only); `api.py:2420` merges cache into `zh` only; `SaffronPage.jsx:1944` has no ja static map.
- **Evidence:** cache top keys = `['zh']`; `_i18n.ja` covers opportunity strings (1148 entries) but none of the authored analysis prose.
- **Suggested fix (described):** Either generate a `ja` section in `translation_cache.json` from the same engine that fills `zh`, or accept ja-English-prose as a known limitation for launch (it is already documented in CURRENT_STATE).

### I-6 — Minor: PATCH `/api/career_events/{id}` returns 200 `{ok:false}` on not-found
- **Severity:** Trivial (consistency)
- **Location:** `api.py:2603`.
- **Evidence:** Other PATCH/DELETE-by-id handlers raise 404; this one returns 200 with `{ok:false,error:"not found"}`.
- **Suggested fix (described):** Return `HTTPException(404)` for consistency, or leave as-is if the frontend already tolerates `ok:false`.

## Launch verdict for the backend

**Ship-ready with one robustness fix recommended and one config check required.** The readiness contract, serve-time filtering, and missing-file safety are correct and verified against live data; no actionable surface leaks closed/listing/photography items, and Today's Focus respects the tier and staleness rules. Before launch: (a) confirm `MOCHI_WEBHOOK_SECRET` is set on the production server (I-4), and (b) ideally add the small `_load_json` try/except helper (I-1) so a half-written data file can't take the whole app to 500 — the app writes these files itself, so this is the realistic failure mode. The deadline-label inconsistency (I-2/I-3) and the ja prose gap (I-5) are low-severity polish items that do not block launch.
