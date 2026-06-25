# Mochi — Scott's live walkthrough findings (2026-06-25)

From a hands-on pass over the deployed app (post Discord-feed + auto-regen + backups deploy).
Root causes traced against the code. Severity is for the **send-to-GEGYjiji** decision.

## ⭐ 0. The "act now" surface isn't accomplishable (HIGHEST — found 2026-06-25 session 2)

Looking through her eyes, the headline surface shows nothing she can *do*. Evidence:
- All **7** `immediate_best_moves` items are passive evergreen venues (bookstore_gallery ×2,
  fair_popup ×2, bookstore_event, zine_shop_consignment, zine_fair_booth) — none is a dated open
  call. UTRECHT's `quick_action` is literally *"Visit their website... get a feel for the space
  before considering a zine project,"* with a year-stale deadline (1 July 2025) stuck on it.
- **Tokyo Art Book Fair appears 8× across buckets** — "Tokyo Art Book Fair" (deadline 2027!),
  "TOKIO ART BOOK FAIR 2026" (typo), a museum-URL dup, + 5 in reject/stretch. Same event, different
  spellings/dates/URLs. UTRECHT (which *runs* TABF) is also listed separately.

Root cause: the act-now bucket ranks evergreen "browse/consign anytime" venues at the top with passive
actions + fake deadlines, instead of dated, accomplishable open calls. Fix: (1) "act now" = only dated,
accomplishable actions; evergreen venues → a labeled "rolling — pitch anytime" shelf; (2) dedupe events;
(3) kill stale-deadline display on evergreen venues. **Likely a send-blocker** — it's the core promise.

## A. The feedback loop is only half-built (HIGH — undercuts the core promise)

1. **Adding accomplishments does NOT update the advice.** (Scott added 3 group shows; advice
   unchanged.) Root cause: the count badges update (`_live_career_counts` reads `exhibition_log.json`
   + profile exhibitions), but the **advice + readiness list come from `career_strategy_report.json`,
   a static precomputed file** (`engines/career_strategy_engine.py`) that nothing regenerates on edit.
   Fix shape: same fire-and-forget regen pattern we wired for email drafts — on show/event add, spawn a
   `career_strategy` regen + a "stale" flag. (Verify whether that engine is Claude-paid or deterministic.)
2. **Readiness requirements have no "I already did this" affordance.** (e.g. "join the watercolor
   society" and others.) They render from the static report with no completion state, so she can't tell
   it she's done one. Needs a per-requirement done/dismiss that persists and feeds the readiness calc.
3. **No "it takes a moment to update" feedback.** Saves show a "saved" toast but the regen is async
   (~30–90s), so nothing visibly changes and it reads as broken. At minimum: an "updating…" indicator;
   ideally optimistic/instant update of the counts and a pending state on the advice.

## B. Data-entry UX is inconsistent (MEDIUM)

4. **Two different "add a show" paths with different richness, and Saffron entries can't be edited.**
   Saffron's `sf-readiness-addshow` posts a thin record; Peppercorn's exhibition log is fuller and has
   edit/delete. So a show added in Saffron with incomplete data is stranded — visible in Peppercorn but
   uneditable. Unify the form (or let both edit the same records) and add edit on Saffron-added shows.
5. **Add-venue form: capture location (city / country)?** Open design question — venue shows read as
   incomplete without a place. Decide the field(s) and apply to both add paths.
5b. **Capture confidence/status on a show (confirmed vs mentioned/unconfirmed).** The career engine only
   counts shows with `confidence` starting "confirmed" (evidence over prediction). So the form should let
   her record an unconfirmed/featured-only collaboration without it inflating readiness until there's proof.

## C. Tracking views missing (MEDIUM)

6. **Follow (★) has no aggregated view.** Mochi opportunity cards have Follow + Applied (✓) buttons that
   POST to `/api/feedback`, but there's no single place that lists everything she's followed.
7. **No unified "already applied for" tracker.** There's a Peppercorn submission log + the card's
   Applied (✓) signal, but they're not joined into one "here's what you've applied to" view. Decide the
   canonical store (submission log) and surface it as a real tracker; route the card's Applied into it.

## D. Real data to capture (LOW, content)

8. **Sarah Andersen collaboration.** GEGYjiji featured/collaborated on "Scribbles: Winter Wonderland —
   A London Exhibition by Sarah Andersen" (Eventbrite, London); prints, she featured them. Add to her
   profile/exhibition history once entry/edit is trustworthy (depends on B).

## Verdict
The app is live and the new plumbing (Discord feed, backups, statement→drafts) works. But **#1–#3 mean
the accomplishments→advice promise visibly fails**, which is the first thing she'll test. Recommend NOT
sending until at least A is addressed.
