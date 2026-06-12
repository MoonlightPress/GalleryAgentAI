# 04 — Logic Effectiveness Audit: The Gap to "She Only Paints and Copy/Pastes"

**Date:** 2026-06-13 · **Scope:** read-only audit of verification, outreach readiness, follow-up loop, and Today's Focus logic
**North-star test:** the artist should only (1) paint and (2) copy/paste emails the system drafted. Everything else is the system's job.

**Verdict:** The system is roughly **half-automated against the north star.** Discovery, ranking, bucketing, and email drafting for Tier 1–2 venues genuinely work — 7 of 13 Immediate Best Moves are literally copy/paste-ready today, with tailored, sendable drafts. But the back half of the loop is missing: deadlines are "verified" without ever reading a date off a live page, nothing happens after she presses Applied, Today's Focus serves the same three cards until a human reruns the pipeline, and the scheduler that would keep data fresh has never run (`memory/last_run.json` does not exist).

---

## 1. Verification Layer — what it actually checks (and doesn't)

Five engines match `verif` in `engines/`:

| Engine | Lines | In active pipeline? | What it actually does |
|---|---|---|---|
| `engines/url_verification_engine.py` | 76 | **Yes** (`run_full_mochi_pipeline.py:16`) | One `requests.get`, `status<400` → `url_verification_status="ok"` (`url_verification_engine.py:30-38`). Reachability only. |
| `engines/verification_report_engine.py` | 251 | **Yes** (`run_full_mochi_pipeline.py:55`) | Recomputes a 0–10 composite from six boolean flags (`verification_report_engine.py:12-19`). Checks nothing live — it aggregates flags other engines set. |
| `engines/targeted_verification_agent.py` | 274 | No (weekly tier of `scripts/scheduler.py:51`) | HEAD+GET on top-50 by score; 403/429 treated as alive (`:115-119`). Sets `deadline_verified` and `last_verified`. |
| `engines/deep_verification_agent.py` | 245 | No (weekly tier, `scheduler.py:52`) | Fetches venue page, Claude Haiku extracts contact email / fees / submission process (`deep_verification_agent.py:78-121`). The best verification asset in the repo. |
| `engines/opportunity_verification_engine.py` | 71 | No | Field-*presence* scoring ("has a deadline string" = +2, `:30-39`). Writes to `deploy_data/verified_opportunities.json`, a file the pipeline no longer reads (`run_full_mochi_pipeline.py:17-18` removed its consumer). Effectively dead. |

### The headline problem: `deadline_verified` is a lie

`targeted_verification_agent.py:74-83` (`_deadline_is_real`) marks a deadline "verified" if the **string** is non-placeholder and longer than 4 characters. It never reads a date off the venue's page. Consequence, measured in `deploy_data/compact_opportunities.json` today:

- All **13/13** `immediate_best_moves` entries have `deadline_verified: true` and `last_verified: 2026-06-08`.
- **UTRECHT** carries deadline `"1 July 2025"` — *eleven months stale* — and is still served (it survives via the relationship-venue evergreen rule, `api.py:243-245`, but the card shows a 2025 deadline as verified).
- **第九屆水主題國際評審藝術比賽** has deadline `"May 15th"` — no year. `_parse_deadline_date` (`api.py:186-221`) cannot parse a yearless date, so `_deadline_past` (`api.py:224-229`) returns False **forever**. May 15 has almost certainly passed. She would prepare a submission to a closed call.
- **水性繪畫展覽 (Watercolor Exhibition)** — deadline `"2月26日 (February 26)"`, no year, same parser hole, ~3.5 months past.
- **B&B Shimokitazawa** — deadline `2026年06月06日`, 7 days ago; survives only because `_deadline_past` uses a `> 7` grace window. It expires from IBM tomorrow with no flag raised.

### What is missing for "she never wastes time on a dead opportunity"

1. **No engine reads a deadline off a live page.** `deep_verification_agent` already fetches pages and runs Claude extraction — its prompt (`deep_verification_agent.py:90-99`) asks for contact/fees/process but **not** `deadline_date` or `submissions_open`. This is a one-prompt-field gap, not an architecture gap.
2. **No open/closed detection.** Nothing distinguishes "call open" from "call closed for this cycle" by reading the page. `status="closed_this_cycle"` exists as a field (`api.py:241`) but no engine sets it from evidence.
3. **The two real verification agents never run.** Only `url_verification_engine` + `verification_report_engine` are in the 72-step pipeline. `targeted_verification_agent` and `deep_verification_agent` live in the weekly tier of `scripts/scheduler.py:50-64`, and the scheduler has **never executed** — `memory/last_run.json` does not exist, and no Windows scheduled task references Mochi.
4. **Yearless/unparseable deadlines are immortal.** `_deadline_past` returns False for anything it cannot parse, which silently whitelists exactly the worst data.
5. `engines/dead_url_pruner.py` correctly hides 404/410 entries — that part works.

CLAUDE.md's "Verification: 30%" rating is accurate, and it is overwhelmingly a *wiring + one prompt field* problem rather than missing code.

---

## 2. Email/Outreach Readiness — counts for the 13 Immediate Best Moves

Measured directly from `deploy_data/compact_opportunities.json` (379 entries; bucket counts: research_needed 165, reject 53, low_priority 47, publication_targets 28, competitions_awards 25, stretch_targets 24, relationship_builders 22, **immediate_best_moves 13**, publication_editorial 2):

| Readiness criterion | Count (of 13 IBM) |
|---|---|
| `submission_page` present | 13 |
| `url_verification_status == "ok"` | 13 |
| `contact_verified == true` | 13 |
| `deadline_verified == true` (string-level only — see §1) | 13 |
| Concrete contact **email** (`@` in contact field) | **8** |
| Per-entry tailored draft (`email_en`/`email_ja` written by Claude) | **7** |
| **All four (email + live page + verified deadline + tailored draft)** | **7 (54%)** |

**Copy/paste-ready today (7):** Tokyo Art Book Fair, UTRECHT, ZINE Fest Tokyo, MOUNT ZINE, Book and Sons, flotsam books, B&B Shimokitazawa. The drafts (from `engines/ibm_email_writer.py`, Claude Sonnet, `run_full_mochi_pipeline.py:85`) are genuinely venue-specific — the TABF draft references TABF's publishing focus, *Colour Diary*, the daily diary practice, and contains no placeholders. This part of the system delivers the north star. 42 entries repo-wide have tailored drafts; standalone copies in `reports/inquiry_drafts/`.

**The 6 without drafts** — 水性繪畫展覽, アートオリンピア2026, 第113回日本水彩展, CSPWC, 第九屆水主題比賽, Northwest Watercolor Society — are all tier-3/4 watercolor competitions submitted through portals (bhuntr.com, callforentry.org, contact forms), where a copy/paste email is the wrong artifact. But the system produces **nothing** for them instead — no entry-form checklist, no pre-filled statement/image-list packet. `ibm_email_writer.py:253` explicitly skips them: `tier12 = [o for o in opps if o.get("career_tier") in (1, 2)]`.

**Two factual bugs in the outreach path:**

1. **`engines/ibm_email_writer.py:51` and `:76` hardcode "~90,000 followers"** into the artist context sent to Claude. Per CLAUDE.md and memory, Instagram is **~26k** (90k was Twitter, never to be referenced). One live draft — *Jinny Street Gallery Open Call* — already contains the 90,000 claim. She could copy/paste a falsifiable claim to a gallery.
2. The fallback templates (`api.py:335-392`, used whenever a card lacks a per-entry draft) sign off with literal `[portfolio link]` — not sendable as-is, contradicting `shape_card`'s presentation of them in the same Email Draft panel (`api.py:555-557`, `OppDetailPanel.jsx:281-296`).

---

## 3. Follow-Up Loop — it does not exist in the live system

**What happens when she presses Applied** (`OppCard.jsx:79-120` → `POST /api/feedback`, `api.py:673-744`): a `submission_log.json` entry is auto-created with `outcome: "pending"` (`api.py:728-742`). Pending venues are then suppressed from the IBM section of `/api/opportunities` (`api.py:621`). That's the entire chain. After that:

- **No follow-up date is ever set.** No reminder. No "no reply in 14 days → nudge." The `outcome` stays `"pending"` forever unless she hand-edits it via the Peppercorn venue log.
- **The 14-day machinery exists but is orphaned.** `engines/opportunity_status_engine.py:191-199` (`mark_contacted`) sets `follow_up_date = today + 14d`, and `recommended_action` (`:74-77`) would say "Waiting for response. Follow up on {date}." But `mark_contacted` is only imported by the **retired** Streamlit UI (`ui/mochi_action_components.py:15`, `app.py:5`). The live FastAPI/React stack never calls it. Evidence: `memory/opportunity_status.json` has 426 records, **0** with `contacted` or `follow_up_date` set.
- **The one live follow-up rule can never fire.** `/api/today` checks CRM contacts for `status == "in_contact"` with `last_contacted > 30 days` (`api.py:2402-2426`). `memory/contact_memory.json` has 52 contacts: 41 `cold`, 10 `researching`, 1 `ready_to_review` — **zero `in_contact`**, and `last_contacted` is `null` on all 52. The grep for `"in_contact"` in the file returns 0. Dead branch in practice.
- **Copying an email draft is not an event.** The copy button (`OppDetailPanel.jsx:286-291`) writes to the clipboard and tells no one. The system cannot distinguish "she sent the intro email" from "she looked at it," so it can never follow up on outreach — only on the Applied button.
- Current state: `memory/submission_log.json` = `[]`, `memory/feedback.json` = 1 test record. The loop has never carried real data.

`scripts/patches/generate_crm_next_actions.py` writes prose `follow_up_timing` strings into `crm_analysis`, but nothing parses or schedules them.

---

## 4. Today's Focus Engine — deterministic, deadline-blind, and never marks things done

The engine is `GET /api/today` in `api.py:2317-2469` (not in `engines/` — the React `TodaysFocus.jsx` just renders it).

**How it chooses:**
- **High Impact** = highest `_ranked_score` item in `immediate_best_moves` passing `_ibm_eligible` (`api.py:2322-2327`).
- **Quick Win** = highest-scoring relationship-category IBM with an `@` contact (`api.py:2330-2348`).
- **Stretch Goal** = highest-scoring `stretch_targets` entry that is not Tier 4, with three fallbacks (`api.py:2352-2400`). The Tier-4 keyword guard (`api.py:2356-2368`) is correctly applied here — *but only here*.

**Findings:**

1. **Static, not fresh.** Selection is a pure function of the JSON, sorted by score. `generated_at` changes per request; the cards don't. With no pipeline run since 2026-06-08 (all `last_verified` timestamps) and no scheduler, she sees the identical three items every day. Today's deterministic output: High Impact = **Tokyo Art Book Fair**, Quick Win = **UTRECHT** (the one displaying a July **2025** deadline). No rotation, no day-seed, no "already shown N times."
2. **Completed items are not excluded.** `bucket()` suppresses applied/pending venues from `/api/opportunities` via `_match_submission` (`api.py:600-623`), but `get_today` **never calls `_load_submission_states`**. If she applies to TABF today, TABF is still tomorrow's High Impact Move. Only `not_for_me` (suppression list in `load_opportunities`, `api.py:583-592`) removes a card from Today's Focus.
3. **Deadlines don't influence priority.** Sorting is score-only. ZINE Fest Tokyo closes **2026-06-27** (14 days away) yet ranks below TABF (deadline January 2027) because both score 10.0 and tie-order wins. There is no urgency boost, so the system can let a live deadline lapse while showing a 7-months-out item.
4. **Tier-4 leak into IBM.** **Northwest Watercolor Society has `career_tier: 4` and sits in `immediate_best_moves`.** `engines/exclusive_strategy_bucket_engine.py` routes Tier 4 by a hardcoded *name list* (`tier_4_terms`, `:296-298, :410-412`) that doesn't include NWWS, and never checks the `career_tier` field that `tier_scoring_engine.py` assigns. `_ibm_eligible` (`api.py:240-252`) doesn't check tier either. CLAUDE.md's rule — "Tier 4 must never appear in Immediate Best Moves" — is violated in production data; only luck (score 9.6 vs 10.0) keeps it out of the High Impact slot.

---

## 5. Top 5 Highest-Leverage Improvements (ranked)

### 1. Make verification verify: extract deadline + open/closed from live pages — **M**
The single biggest gap between "ranked" and "actionable." Extend the `deep_verification_agent.py` Claude prompt (`:90-99`) with `deadline_date` (ISO) and `submissions_open` (true/false/unknown); write `deadline_date_iso` and set `status="closed_this_cycle"` on evidence. Replace `_deadline_is_real`'s string check (`targeted_verification_agent.py:74-83`) with "page-extracted date exists and is future." In `api.py`, make `_ibm_eligible` treat yearless/unparseable deadlines as *unconfirmed* rather than immortal (`api.py:186-229`). Add both agents to `run_full_mochi_pipeline.py` (after line 16).
**Touches:** `engines/deep_verification_agent.py`, `engines/targeted_verification_agent.py`, `api.py`, `run_full_mochi_pipeline.py`. Kills the UTRECHT-2025 / "May 15th" class of waste permanently.

### 2. Close the follow-up loop: sent → +14 days → nudge in Today's Focus — **M**
(a) Add a "Mark as sent" action when she copies a draft (`OppDetailPanel.jsx:286-291`) that POSTs to `/api/feedback` with a new `outreach_sent` action; (b) in `post_feedback` (`api.py:699-742`), stamp `follow_up_date = today + 14d` on the submission/outreach record; (c) in `get_today` (`api.py:2402-2426`), check `submission_log.json` for `pending` entries past `follow_up_date` **before** the CRM check (which can't fire — zero `in_contact` contacts) and surface "No reply from X in 14 days — send a nudge" as the Quick Win, reusing the existing `_crm_card` shape. The orphaned `mark_contacted` logic (`engines/opportunity_status_engine.py:191`) is the spec; port it, don't rewrite it.
**Touches:** `api.py`, `frontend/src/components/OppDetailPanel.jsx`, `memory/submission_log.json` schema. This is the difference between a recommendation list and a career operating system.

### 3. Today's Focus: exclude done items, respect deadlines, rotate — **S**
Three small edits to `get_today` (`api.py:2317-2400`): (a) call `_load_submission_states()` and filter pending/rejected venues exactly as `bucket()` already does at `api.py:621-622`; (b) add a deadline-urgency term to the sort key (e.g. +2.0 if parsed deadline within 21 days) so ZINE Fest Tokyo outranks a January-2027 fair in mid-June; (c) seed a daily rotation among score-ties (`date.today()` hash) so the page feels alive between pipeline runs. Also add `career_tier == 4` to the `_ibm_eligible` rejection and to `choose_bucket` in `engines/exclusive_strategy_bucket_engine.py` (check the field, not just `tier_4_terms` text) — fixes the NWWS leak with two lines.
**Touches:** `api.py`, `engines/exclusive_strategy_bucket_engine.py`. Cheapest fix with daily-visible payoff.

### 4. Drafts for everything actionable + fix the 90k-follower falsehood — **S**
(a) Change `ibm_email_writer.py:253` to also draft for any `exclusive_primary_bucket == "immediate_best_moves"` entry regardless of tier; for portal-submission categories, generate a **submission packet** (entry checklist + tailored statement paragraph + image-list suggestion) instead of an email — the artifact she actually needs for CSPWC/NWWS/アートオリンピア. (b) Fix `ibm_email_writer.py:51` and `:76`: "~90,000" → "~26,000", and regenerate the Jinny Street draft that already shipped the wrong number. (c) Strip `[portfolio link]` from the fallback templates (`api.py:352, :372, :392`) or stop serving fallbacks as "drafts" — mark them clearly as templates in the UI.
**Touches:** `engines/ibm_email_writer.py`, `api.py`, one regeneration run. Moves copy/paste-ready from 7/13 to 13/13.

### 5. Actually schedule the scheduler — **S**
`scripts/scheduler.py` already defines sane daily/weekly/monthly tiers — the weekly tier contains exactly the verification agents from #1 — but it has never run (`memory/last_run.json` absent, no OS task). Register a Windows Task Scheduler entry (daily trigger; the script self-gates by tier thresholds at `scheduler.py:34-38`). Without this, every other fix decays: data is frozen at the last manual run (currently 2026-06-08) and "Mochi did the legwork while the artist was away" is fiction. Note: the weekly tier references `targeted_verification_weekly.py` and `submission_link_hunter.py` (`scheduler.py:51,54`) — confirm these resolve via `smart_pipeline_runner` or point them at `targeted_verification_agent.py` before enabling.
**Touches:** `scripts/scheduler.py`, one `schtasks` registration, no engine code. Converts the system from "tool she operates" to "agent that works while she paints."

---

## Appendix: smaller defects noticed en route

- `opportunity_verification_engine.py` writes `deploy_data/verified_opportunities.json`, which nothing consumes (its consumer was removed, `run_full_mochi_pipeline.py:17-18`) — candidate for `archive/dead_code/`.
- `verification_report_engine.py`'s composite counts `deadline_verified` (+2) and `contact_verified` (+2) — both flags are currently set by string/page-presence checks, so the 0–10 "verification score" inherits the inflation described in §1. Score inflation via proxy flags is exactly the lesson CLAUDE.md warns about.
- `_RELATIONSHIP_CATS` evergreen rule (`api.py:243-245`) is correct in spirit (bookshops don't have deadlines) but it also keeps the *stale deadline string* on the card — the card should suppress a past dated deadline for evergreen venues instead of displaying "1 July 2025."
- `memory/contact_memory.json`: 52 contacts all have `contact_email`, but 0 have `next_action` as a structured field — the CRM's actionable layer lives only inside free-text `crm_analysis` prose.
