# 2026-06-26 Team Pass — Crema (Ops): cross-tab / integration + final features

**Scope:** whole-site coherence across the three tabs (发现·麻薯 / 观察·山楂 / 对话·胡椒粒),
with the new **editable Saffron Venue Tracker ↔ Peppercorn contact store** sync as the focus.
**Method:** live API walk (`/api/saffron`, `/api/peppercorn`, `/api/contacts`, `/api/career_strategy`)
on twilightdreamworks.com/mochi + source read of the to-be-deployed HEAD (the SHIPPED 2026-06-26
block; some of it is already live — `venue_tracker` and the canonical group-show count are serving).
Live render of the new tracker UI couldn't be eyeballed (Saffron sections are collapsed accordions and
the bundle lags api.py), so the tracker findings are source-grounded, the IG/count findings are live.

**Headline:** the two scary T0 items from the 2026-06-25 review are genuinely fixed —
the **group-show count is now unified** (one `_canonical_group_show_count()` at `api.py:3129`,
consumed by both Saffron prose and Peppercorn's `liveGroupShows`, `PeppercornPage.jsx:828`), and the
**nav now reads "verb · name"** (观察·山楂 — T4.3 done). The new problems are all in the seam the
editable Venue Tracker just opened: **three surfaces now read/write the same 52-contact store with
three different status vocabularies and two different definitions of "active,"** and there's a **live
Instagram-number contradiction (27k vs 26k) across tabs.** None of it is catastrophic; all of it is the
classic "the page doesn't yet reflect one truth."

---

## PART 1 — Cross-tab / integration punch-list (Tier 0 → Tier 3)

### TIER 0 — wrong fact shown to her, live now

**T0.1 — Instagram follower count contradicts across tabs (LIVE).**
`/api/saffron` serves `followers: "27k"` in **both** `career_position.social[0]` and
`instagram_strategy` (`api.py:2064` and `api.py:2070`, plus the `'27k'` literal fallback at
`SaffronPage.jsx:491`). `/api/peppercorn` `live_counts` serves `instagram_followers: "26k"`
(`api.py:3183`, sourced from `artist_master_profile.social_presence`). So **Saffron says 27k and the
profile/Peppercorn path says 26k for the same account.** Both are also softened to "established, growing
following" in most copy (good), but the raw number still leaks on Saffron's Career-Position marker.
*Fix:* single-source the number from `artist_master_profile.social_presence.instagram.followers`
(currently `26k`) everywhere — delete the hardcoded `"27k"` at `api.py:2064/2070` and the `|| '27k'`
fallback at `SaffronPage.jsx:491` — or drop the digit entirely and keep only "established, growing."
One number (or none) site-wide. *Falsification:* grep the served payloads for `27k` → must be zero.

### TIER 1 — the new editable-CRM seam (status sets & counts diverge)

**T1.2 — Status vocabularies don't match across the three surfaces that share `/api/contacts`.**
- Saffron Venue Tracker `VENUE_STATUS_OPTS` (`SaffronPage.jsx:1236-1244`): `cold, researching,
  in_contact, contacted, responded, relationship, not_a_fit`.
- Peppercorn CRM `CRM_STATUS_META` (`PeppercornPage.jsx:1214-1227`): adds `ready_to_review, submitted,
  ongoing, rejected`.
- Peppercorn venue-LOG `VENUE_STATUS_OPTIONS` (`PeppercornPage.jsx:956-963`): `cold, researching,
  in_contact, submitted, ongoing, rejected` — a *third*, different set.

Consequences (both real, both via the shared store + a non-validating `PATCH /api/contacts/{name}`,
`api.py:1606-1630`):
  - **`ready_to_review` is invisible to Saffron.** It's the CRM's primary status and what new contacts
    default to. In the Venue Tracker it falls through `venueStatusLabel`'s fallback
    (`SaffronPage.jsx:1250` → `String(status).replace(/_/g,' ')`) and renders the **English** "ready to
    review" even in zh (her default) — a zh leak — and the edit `<select>` has no matching `<option>`,
    so opening + saving a `ready_to_review` row risks a **silent downgrade** to whatever the dropdown
    shows. (Live store today: 1 `ready_to_review`, 10 `researching`, 41 `cold` — small now, grows the
    moment she uses either CRM.)
  - **`relationship` / `not_a_fit` (settable only from Saffron) fall out of Peppercorn's filters and
    counts.** They aren't in `FILTER_STATUS_MAP` (`PeppercornPage.jsx:1460-1464`) or the summary
    (`readyCount`/`activeCount`/`researchCount`, `1448-1455`), so a contact she marks "保持往来" in
    Saffron shows under Peppercorn's "all" tab only and is uncounted everywhere else.

  *Fix:* one shared status enum in a single module both tabs import; include `ready_to_review` in
  Saffron's set; add `relationship`/`not_a_fit` to Peppercorn's filters + counts; have the PATCH
  endpoint validate/normalize `status` against that enum so neither surface can persist a value the
  other can't render.

**T1.3 — "Active" means two different things on the two tabs.**
Saffron's `venue_tracker.active` (`api.py:2569-2573`) counts `{contacted, in_conversation, active,
responded}` + any `last_contacted`/`response_received`. Peppercorn's `activeCount`
(`PeppercornPage.jsx:1449`) counts `{in_contact, sent_inquiry, contacted, responded, ready_to_review}`.
So `in_contact` and `ready_to_review` are "active" in Peppercorn but **not** in Saffron's count, and
`relationship` counts in neither. Same 52 contacts → two different "active" totals. (Live: Saffron
`active=0`; Peppercorn would show ~1 active / 10 researching / 41 cold.) *Fix:* one shared `is_active()`
predicate used by both surfaces.

### TIER 2 — latent / fragile / unlabeled

**T2.1 — Dead-but-fragile "0–0 more group shows needed."**
`api.py:2042-2053` (the `else` of `if _foundation_complete:` at `1891`, defined at `1707` =
`group_shows>=3 and _has_solo and _has_institutional`). For her real data this branch is dead — but it
reads `"Only {N} confirmed group shows… so {max(0,3-N)}–{max(0,4-N)} more group shows needed"`, which
with N=8 renders the nonsense **"Only 8… so 0–0 more group shows needed,"** directly contradicting the
benchmark block at `api.py:2111` ("8 group shows… a real strength"). If `_has_solo`/`_has_institutional`
detection ever regresses, she sees it. *Fix:* suppress the "more needed" clause when count ≥ 3, or gate
the whole branch on count rather than the three foundation flags. (`elif _total_group_shows >= 4` at
`api.py:2162` is also dead — `_has_solo` catches her first — harmless but worth a comment.)

**T2.2 — Saffron's exhibition marker (12) vs the canonical group-show count (8), unlabeled.**
`career_position.exhibitions` has 12 entries → Saffron's "shows" marker renders **12**
(`SaffronPage.jsx:498`), while Peppercorn's exhibition log and Saffron's own benchmark prose say
**8 group shows.** Both are true (12 total exhibitions, 8 of them group), but side by side, unlabeled,
they read as "is it 8 or 12?" *Fix:* label the marker "展览 / exhibitions" distinctly from "联展 / group
shows," or show "8 group · 12 total" with a one-line note. (This is the only remaining wrinkle in
"exhibition record agrees across tabs" — the group number itself is correctly unified.)

### TIER 3 — coherence polish

**T3.1 — Mochi "People" is a snowflake AND a third surface over the same 52 contacts.**
`RelationshipTargets.jsx:32-38` still uses **emoji** `TYPE_ICON` while the rest of Mochi uses the
watercolor icon set (already handoff PENDING #2). Bigger picture: the same 52 contacts now appear on
**three** tabs — Mochi People (read-only, by priority), Saffron Venue Tracker (editable, by status),
Peppercorn Contacts (editable, by status) — i.e. two editable CRMs + one read-only view of one dataset.
Not contradictory per se, but it's triplication; the T1 status drift is what makes it bite. *Fix:* at
minimum keep icons/labels coherent; consider the "one relationships surface, three views" feature below.

**T3.2 — The "Venue Tracker" lists non-venues.**
`venue_tracker.tracked` is built from the whole `crm_list` (`api.py:2564`), so it includes
press targets like *Apartamento Magazine* (Barcelona). A "场地 / venue" tracker showing a Spanish
magazine is mildly incoherent. *Fix:* rename to "关系 / Relationships," or filter to venue-type contacts.

**T3.3 — PATCH can't clear a field.** `api.py:1619/1621` only write `last_contacted`/`notes` when
truthy, so a wrong date or note set from the tracker can't be blanked. Minor.

---

## PART 2 — FINAL FEATURES (ranked) — does the site help her *do* the next thing?

Honest read: the site is **rich on knowing, thin on doing.** It tells her where she stands, who her
peers are, what her work is worth, and lists 419 opportunities + 52 contacts — but the "what do I
actually do this week" is left to her, and for an easily-overwhelmed artist that's where it stays a
pretty read. These favor behavior change over more surfaces, and none are half-built monsters.

1. **"This week" action digest (effort: M).** One small card (top of Mochi, or a thin banner) that
   distills everything into the 2–3 highest-leverage moves *right now*: the nearest real, unactioned
   deadline; the one contact due a follow-up; the single next-unlock step (gallery rep). All the data
   already exists (`_deadline_passed`, `last_contacted`, `career_strategy.level.next_unlock`). *Why it
   fits:* collapses 419+52 into "do these three," which is exactly the antidote to her overwhelm.

2. **Follow-up reminders on the CRM (effort: S).** The pure function **already exists**
   (`is_overdue_followup`, the one real launch-audit finding). When she sets `last_contacted`, compute
   an "worth a follow-up" badge after N days and feed it into the digest above. *Why it fits:* venue and
   representation relationships die in the silent gap after first contact — her stated #1 structural
   move (gallery rep) is won by follow-through, and right now nothing nudges it. Cheapest high-value
   thing on this list.

3. **Email / pitch draft in context (effort: M).** Drafts already get generated (write-once,
   `ibm_email_writer`) but are buried and stale. Surface the ready-to-edit draft *inline* on a contact
   or opportunity once it's marked ready, with a one-tap copy. *Why it fits:* the blank-page email is
   the single highest-friction step for a shy artist; she has the openings, not the words. (Pair with
   verifying the statement-edit → regen loop actually fires on prod — still unconfirmed per
   CURRENT_STATE.)

4. **Gallery-representation playbook (effort: M; needs a real research pass — scope it, don't
   half-build).** The level model says representation is THE next move, but there's no concrete *how*.
   A short, honest path: which Tokyo galleries fit her watercolor/illustration register, how to get on
   their radar via the shows she already has, and the explicit "no cold submissions" rule — seeded from
   her existing `type: gallery` contacts. *Why it fits:* it's the one thing the entire app points at,
   and currently the most actionable surface for it is a flat contact list.

5. **Press-kit / one-PDF lookbook generator (effort: M–L).** Both the licensing and press sections
   already tell her the first real deal starts with "be findable + a one-PDF lookbook when asked" — and
   she doesn't have one. Generate it from her statement + exhibition list + a few works. *Why it fits:*
   one artifact unblocks two paths (licensing DMs and press pitches) at once.

6. **One "Relationships" surface, three views (effort: M) — folds in the T1/T3 fixes.** Replace the
   triplicated contact surfaces with a single store + tab-specific *views* (Mochi = discover-by-priority,
   Saffron = strategic map, Peppercorn = working CRM) over **one** status enum and **one** "active"
   predicate. *Why it fits:* makes the CRM trustworthy (an edit on one tab can't look broken on another)
   and kills the duplication instead of adding a fourth place to look. This is the structural version of
   the T1 punch-list; build it if the quick T1 patches start to sprawl.

---
*No code edited, nothing deployed or committed. Recommended order: T0.1 → T1.2/T1.3 → T2 → features
2 then 1 (cheap + highest behavior change first).*
