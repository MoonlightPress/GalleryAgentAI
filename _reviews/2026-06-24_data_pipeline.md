# Mochi pre-launch review — Data correctness & pipeline integrity

_Reviewer facet: does the app show TRUE, CURRENTLY-ACTIONABLE information?_
_Date: 2026-06-24 · Mode: read-only, offline. No network, no pipeline run, no writes to repo data._
_Live data inspected: `deploy_data/compact_opportunities.json` (mtime 2026-06-24 19:07, 522 entries)._

---

## Summary

The actionable surface (Today's Focus / Immediate Best Moves / strongest picks) is **trustworthy enough to
launch today**, but its safety depends almost entirely on one fragile fact: the `deadline_past` flag in the
live data is currently **correct on every parseable entry** because the monthly pipeline pass ran hours ago
(2026-06-24). The serve-time guards in `api.py` are a *weaker* second net than the flag they back up — their
date parser misses several real-world formats (English month-year, m/d/y numeric, 2-digit years, ordinal
suffixes, date ranges). As long as the stored flag is fresh, those gaps are masked. The moment the data
ages between monthly passes, or a newly-discovered opportunity in an unparsed format passes its deadline,
the serve-time net will *not* catch it.

I found **zero past-deadline items leaking into the `ready`/strongest-picks tier** right now (the highest-stakes
surface). I found **one genuinely-closed opportunity sitting in the `immediate_best_moves` bucket** (badged
`closed_or_stale`, so it cannot become a strongest pick, but it is in the wrong section). The email-draft bug
described in CURRENT_STATE is **confirmed and is worse than stated** — it fails on two independent grounds.
Source purity is clean: 0 photography rows and 0 listing-artifacts reach the served app.

The honesty gap CURRENT_STATE names is real and quantified below: of the items served in actionable
(non-watch-list) sections, only **25 of 106 carry `verification_status: verified`**; the rest are
`strong_partial` / `partial` / `research_needed` and are admitted by the narrower actionability layer
(deadline_verified + route + URL ok), not by holistic verification. This is a defensible design, but it means
"in an actionable section" ≠ "proven open right now."

---

## What I verified (concrete numbers from the live data)

Live file: `deploy_data/compact_opportunities.json`, **522 raw entries**.

**Field distributions (raw):**
- `verification_status`: `strong_partial` 197, `partial` 158, **`verified` 119**, `research_needed` 48.
- `status`: `None` 344, `closed_this_cycle` 66, `needs_reverification` 47, `research_next` 42,
  `needs_confirmation` 9, `closed` 8, `permanently_closed` 1, others ≤2.
- `deadline_verified`: `True` 226, `False` 296.
- `url_verification_status`: `ok` 471, `error` 18, `bad` 17, `no_url` 16. (URL reachability is well-proven,
  as the prior audit said.)
- `native_medium`: `unknown` 317, `painting` 111, `mixed` 85, `photography` 9.
- `exclusive_primary_bucket`: `research_needed` 236, `reject` 75, `competitions_awards` 69,
  `publication_targets` 45, `stretch_targets` 41, `relationship_builders` 27, `low_priority` 18,
  **`immediate_best_moves` 7**, `publication_editorial` 4.

**As actually served by `api.py` (`load_opportunities()` → `bucket()`):**
- `load_opportunities()` returns **416** after suppression/dedup/photography/listing filters.
- Section sizes served: `immediate_best_moves` 6, `open_calls` 12, `publication_editorial` 2,
  `competitions_awards` 37, `zines_and_print` 29, `relationship_targets` 20, `watch_list` 310.
- Photography rows served: **0**. Listing-artifact rows served: **0**.
- `closed_this_cycle` rows in any actionable (non-watch-list) section: **0**.
- Tier-4 / `stretch_targets` rows in `immediate_best_moves`: **0**.

**Past-deadline truth (using the canonical `engines/deadline_normaliser.deadline_is_past`):**
- Entries whose deadline string parses to a date **before today (2026-06-24)**: of `deadline_verified=True`
  (226), **9** are actually past.
- Stored `deadline_past=True` field present on **130** entries. Of entries the normaliser can parse as past,
  **121/121 already carry `deadline_past=True`** — i.e. the stored flag is currently in perfect agreement
  with the canonical parser. (The remaining 9 stored-True are CJK/year-only forms the normaliser leaves
  unparsed.) **Conclusion: the data was normalised immediately before this deploy; there are zero stale-flag
  leaks right now.**

**Past-deadline items appearing in actionable sections (real current count):**
- In actionable (non-watch-list) sections, items with a normaliser-past deadline: **5 cards**, of which **2
  are relationship/evergreen** (UTRECHT, SUZURI — past date intentionally suppressed/rolled, by design) and
  **3 are non-relationship** (all badged `closed_or_stale`, none `ready`):
  - `zines_and_print` — "Submissions — Clavis Publishing", deadline "April 2025" (`book_publishing`)
  - `zines_and_print` — "Become an Author - Tuttle Publishing", deadline "October 31, 2025 or August 25, 2026" (`book_publishing`)
  - `relationship_targets` — "BONUS TRACK", deadline "February 2nd, 2026" (`market_event`)
- **Past-deadline non-relationship items that reach the `ready`/strongest-picks tier: 0.** (This is the
  number that matters most, and it is clean.)

---

## Issues found

### ISSUE 1 — Serve-time `_deadline_passed()` parser is materially weaker than the canonical normaliser
**Severity: HIGH (latent; not currently leaking, but it is the designed safety net and it has holes).**
**Location:** `api.py:648-691` (`_deadline_passed`) and its sibling `api.py:228-271`
(`_parse_deadline_date` / `_deadline_past`).

**Evidence (offline parse comparison, today = 2026-06-24):**

| deadline string | normaliser `is_past` | `api._deadline_passed` | cause of api miss |
|---|---|---|---|
| `April 2025` | True | **False** | English month-year not handled (only CJK `年月` is) |
| `March 2026` | True | **False** | same |
| `February 2nd, 2026` | True | **False** | ordinal `2nd` breaks the `(\d{1,2}),?` regex |
| `6/15/2026` | True | **False** | numeric m/d/y not handled (ISO regex is year-first only) |
| `5/26/26 at 11:59 p.m. PDT` | True | **False** | 2-digit year not handled |
| `October 31, 2025 or August 25, 2026` | True | **False** | only catches dates the inline regex matches; range/"or" not normalised |

Across the live data there are **10 non-relationship entries** where the normaliser says past but
`api._deadline_passed` says not-past. They do **not** leak today only because the stored `deadline_past`
field (written by the stronger normaliser) is the actual gate read by `recommendation_readiness.assess_actionability`
(`recommendation_readiness.py:36`). The serve-time guard is meant to catch a deadline that passes *between*
monthly passes (its stated purpose, `api.py:649-651`); for any deadline in the formats above, it will fail to
do so, and the item will remain in an actionable section until the next pipeline run re-normalises the flag.

**Suggested fix (described):** Delete the duplicate inline parser in `_deadline_passed` and the
`_parse_deadline_date` family in `api.py`, and import `parse_deadline_date` / `deadline_is_past` from
`engines/deadline_normaliser.py` so there is exactly one deadline parser in the system (it already handles
ordinals, 2-digit years, English month-year, numeric m/d/y, and resolves month-only to end-of-month). Keep
the relationship-category and recurring-hint short-circuits that live in `_deadline_passed`. This removes the
divergence permanently and satisfies the single-source-of-truth intent.

### ISSUE 2 — A plain `status: "closed"` opportunity sits inside `immediate_best_moves`
**Severity: MEDIUM (badged closed, so it cannot become a strongest pick — but it is in the most
action-oriented section and inflates the IBM count).**
**Location:** `api.py:290-302` (`_ibm_eligible`) and `api.py:266-271` (`_deadline_past`).

**Evidence:** entry "Zine & Book フェス in 神保町 (Jimbocho)":
- `status = "closed"`, `deadline = "2026 edition: January 18-19 2026 (past). Watch October 2026 for next call."`,
  `exclusive_primary_bucket = "immediate_best_moves"`, `category = "fair_popup"`.
- `_ibm_eligible()` returns **True** because it only excludes `permanently_closed` and `closed_this_cycle`
  (`api.py:291`) — plain `"closed"` is not in that set.
- `_deadline_passed()` returns **False** because the date is a **range** ("January 18-19 2026") that neither
  the serve-time regex nor the normaliser parses, so the explicit "(past)" text in the field is ignored.
- Net result: it is served in the `immediate_best_moves` bucket. It *is* given `actionability_status =
  closed_or_stale` (because `recommendation_readiness.py:32` does include `"closed"`), so the frontend badges
  it and `recommendationQuality.js:100` subtracts 40 — it will not surface as a strongest pick. But it should
  not be in IBM at all.

**Suggested fix (described):** (a) add `"closed"` to the status exclusion set in `_ibm_eligible`
(`api.py:291`), matching what `assess_actionability` already treats as closed; and (b) extend the deadline
parser to handle day ranges ("January 18-19 2026" → last day 19) so a self-declared "(past)" range is caught.
Cheaper interim guard: in `bucket()`, drop any IBM candidate whose `assess_actionability` status is
`closed_or_stale` before it is placed in the section (it is already computed in `shape_card`).

### ISSUE 3 — Email drafts cannot be refreshed by editing the artist statement (confirmed; two independent causes)
**Severity: HIGH for data correctness of the outreach artifact (the drafts are the thing the artist acts
*with*; a stale draft is wrong-information at the point of action).**
**Locations:**
- `engines/ibm_email_writer.py:27` — `PROFILE_PATH = Path("memory/artist_master_profile.json")`.
- `engines/ibm_email_writer.py:38-44` — the statement is read from that file
  (`stmt.get("verbatim_source_ja")`, `verbatim_translation_en`, `synthesized_en`, `tone_signal`).
- `api.py:2540-2546` — `POST /api/peppercorn` writes the entire payload (including `artist_statement`) to
  `memory/peppercorn_profile.json`.
- `engines/ibm_email_writer.py:258` — `needs_email = [o for o in tier12 if not (o.get("email_ja") and o.get("email_en"))]` (write-once).

**Evidence / why it is worse than CURRENT_STATE states:** two unrelated breaks, either of which alone defeats
a refresh:
1. **Wrong file.** Peppercorn saves the statement to `peppercorn_profile.json`; the writer never reads that
   file — it reads `artist_master_profile.json`. The two stores are disconnected
   (`peppercorn_preference_engine.py` is the only engine that reads `peppercorn_profile.json`, and it adjusts
   preferences, not the email statement). So even a fresh full pipeline run would regenerate drafts from the
   *old* master-profile statement, ignoring whatever the artist typed into Peppercorn.
2. **Write-once.** Even if (1) were fixed, line 258 skips any entry that already has both `email_ja` and
   `email_en`, so existing drafts never regenerate when the statement changes.

**Suggested fix (described, minimal):**
- Make the statement single-sourced: have the writer's `load_artist_context()` prefer
  `memory/peppercorn_profile.json["artist_statement"]` when present and fall back to
  `artist_master_profile.json`; OR have `POST /api/peppercorn` mirror the edited statement back into the
  `artist_statement` block of `artist_master_profile.json`. (Either satisfies the Data Patch Rule because the
  fix lives in code, not in regenerated JSON.)
- Add a `--force` / `--regenerate` flag (or a `statement_fingerprint` stored per entry) so drafts rebuild when
  the source statement hash changes, instead of being permanently write-once.
- *Do not implement now* unless Scott green-lights the paid run — regenerating drafts is an Anthropic spend
  (the writer calls `claude-sonnet-4-6`, `ibm_email_writer.py:208-215`). For launch, the safer move is to keep
  the existing "Draft — review and edit before sending" label (already added, commit `7e194236`) so the artist
  treats every draft as editable, which neutralizes the severity in practice.

### ISSUE 4 — "In an actionable section" overstates verification for ~75% of served actionable items
**Severity: MEDIUM (honesty / expectation-setting; not a hard correctness bug).**
**Location:** the actionability contract in `recommendation_readiness.py:21-86`, surfaced by `api.py` `bucket()`.

**Evidence:** of the 106 cards served across actionable (non-watch-list) sections, `verification_status` is
`strong_partial` 39, `partial` 32, **`verified` 25**, `research_needed` 10. Items qualify for an actionable
section on the narrower triad (deadline_verified OR evergreen, a route exists, URL ok) rather than on
holistic `verification_status: verified`. This matches the prior audit's finding that "URL ok" is well-proven
(471/522 ok) but "open & actionable now" is not (119/522 `verified`). It is a *defensible* design — requiring
full verification would empty the board given the monthly Tavily cap — but the UI should not imply these are
all confirmed-open.

**Suggested fix (described):** no code change required for launch; ensure section copy and the per-card
`soft_warning` / checklist `check` states make the "confirm before applying" status visible (they largely
do — `_build_checklist` emits `check` states for unverified deadline/fee/route). Optionally expose a quiet
"verified open" badge only for `verification_status == "verified"` so the strongest few are distinguishable
from the merely-routable.

### ISSUE 5 — Two-net design has no alarm when the data ages (process risk, not a code bug)
**Severity: LOW-MEDIUM (operational).**
**Evidence:** correctness of the actionable surface currently rests on the stored `deadline_past` flag being
fresh (it is, today). CURRENT_STATE says cadence is monthly. Between passes, only the weaker serve-time guard
protects the board, and Issue 1 shows it has holes. There is no check that fails loudly if the data is, say,
40 days old.

**Suggested fix (described):** after fixing Issue 1 (single parser), the serve-time guard becomes a genuine
equal to the normaliser and the aging risk largely disappears. Additionally, the existing
`data_updated_at` signal (`api.py:751-756`) could drive a quiet "last refreshed N days ago" note so a missed
monthly pass is visible rather than silent.

---

## Launch verdict for data trustworthiness

**GO for launch, with one pre-launch fix strongly recommended.** The highest-stakes surface — `ready` /
strongest picks — is clean today: 0 past-deadline non-relationship items reach it, 0 photography, 0
listing-artifacts, 0 `closed_this_cycle` in actionable sections, 0 Tier-4 in IBM. The data was normalised
immediately before deploy, so the stored `deadline_past` flags are accurate.

The one fix I would do before launch is **Issue 1** (unify the deadline parser by importing
`deadline_normaliser` into `api.py`), because it is small, free, offline, and it converts the serve-time guard
from a leaky backup into a real one — removing the system's dependence on the flag never going stale. **Issue 2**
(closed fair in IBM) is a one-line status-set addition and worth bundling in. **Issue 3** (email drafts) is
real and high-value but is a paid regeneration; for launch it is adequately mitigated by the existing
"Draft — review and edit before sending" label, and the structural fix can follow Scott's go.
