# Domino — visual/UX punch-list (Mochi's Atelier, Saffron + Peppercorn)

**Date:** 2026-06-26
**Reviewer:** Domino (UX/visual)
**Surfaces walked:** live site `https://twilightdreamworks.com/mochi/` at laptop (1280) and phone (390/375). Got live screenshots of every surface below (saved alongside this file in `shots/`); cross-checked against `SaffronPage.{jsx,css}`, `DeadlineCalendar.css`, `PeppercornPage.jsx` (repo == live).
**Scope note:** Per brief, the Mochi/Discover section-header banner is being rebuilt — NOT flagged. Everything below is Saffron + Peppercorn.

A note on method: the live React app churns tab/section state under rapid automation, but the source confirms there is **no polling and no tab-reset** (`loadSaffron`/`loadCareer` run once on mount; the only `setTab` is the user's subtab click). So the "tab jumping" I hit was an automation artifact, **not** a real bug — not reporting it as one.

---

## TIER 0 — looks broken / ugly

### T0-1. Seasonal-calendar month list overflows horizontally on phone (whole page side-scrolls)
- **Surface:** Saffron → 日历 (Calendar) → "季节性机会日历", the per-month deadline list under the month-grid picker.
- **Viewport:** phone (reproduces ≤ ~560px; measured at 375).
- **What I saw:** at a 375px viewport the document is **840px wide** (`body.scrollWidth = 840`). Every opportunity name is cut off at the right edge and the entire page gains a horizontal scrollbar. The `.sf-cal-month` grid computes to `100px + 487px` columns — the `1fr` track blows out to its content's max-content because it can't shrink. Screenshot: `shots/phone_cal_overflow.png`.
- **Cause:** `SaffronPage.css:627` `.sf-cal-month { grid-template-columns: 100px 1fr }` has **no phone breakpoint**, and `.sf-cal-opps` (`SaffronPage.css:643`) has no `min-width: 0`, so the grid track keeps the min-content width of the longest name. `.sf-cal-name` (`:671`) also has no wrap rule.
- **Fix:**
  ```css
  .sf-cal-opps { min-width: 0; }                 /* let the 1fr track shrink */
  .sf-cal-name { min-width: 0; overflow-wrap: anywhere; }
  @media (max-width: 560px) {
    .sf-cal-month { grid-template-columns: 1fr; gap: 6px; }  /* month name stacks above its opps */
  }
  ```
- **Falsification:** after the fix, at 375px `document.body.scrollWidth === document.documentElement.clientWidth` and no opp name is clipped.

---

## TIER 1 — functional/visual correctness

### T1-1. Venue-Tracker inline editor misrepresents (and can silently downgrade) status
- **Surface:** Saffron → 人脉与媒体 → "场地关系追踪" → a row's **更新** editor. Screenshot: `shots/laptop_venrow.png`.
- **Viewport:** both.
- **What I saw:** the first row's header reads status **待审阅** (`ready_to_review`), but when you open its editor the status `<select>` shows **尚未联系** (`cold`). The header and the dropdown disagree, and pressing **保存** would write `cold` — a silent downgrade / data loss.
- **Cause:** the dropdown vocabulary `VENUE_STATUS_OPTS` (`SaffronPage.jsx:1236-1244` = cold/researching/in_contact/contacted/responded/relationship/not_a_fit) does **not** include the CRM statuses the contact store actually carries (`ready_to_review`, etc.). `VenueTrackerRow` seeds `useState(v.status || 'cold')` (`:1262-1263`), so any out-of-vocabulary status falls to `cold` in the editor.
- **Fix:** when `v.status` isn't in `VENUE_STATUS_OPTS`, prepend it as the selected option (so save preserves it), or unify the venue status set with Peppercorn's CRM statuses. Don't let an unknown status silently resolve to `cold`.
- **Falsification:** open the editor on the `ready_to_review` row → the select shows that status, not 尚未联系.

---

## TIER 2 — noticeable imbalance

### T2-1. Career Position exhibitions/publications grid is lopsided (huge empty right column)
- **Surface:** Saffron → 概况 (Profile) → "职业定位". Screenshot: `shots/laptop_careerposition.png`.
- **Viewport:** laptop (≥640; stacks to 1-col below that, so phone is fine).
- **What I saw:** the 2-up grid puts **12** exhibition rows in the left column and only **2** publication rows in the right — the right column ends after ~15% of the height, leaving ~60% of it blank. The Audience block then sits full-width *below* the grid, so it doesn't fill the void either.
- **Cause:** `.sf-career-grid { grid-template-columns: 1fr 1fr }` (`SaffronPage.css:265-269`) with three stacked blocks (`SaffronPage.jsx:513-547`): Exhibitions, Publications, Audience all rendered as siblings.
- **Fix (pick one):** (a) wrap Publications + Audience in a single right-column `<div>` so the short content stacks and fills the column; or (b) let Exhibitions span both columns (`grid-column: 1 / -1`) and put Publications + Audience side-by-side beneath. (a) is the smaller change and reads best.
- **Falsification:** no column is more than ~1.5× the other's height at 1280.

---

## TIER 3 — polish

### T3-1. Press-Kit sample bullet lists have no bullets
- **Surface:** Saffron → 人脉与媒体 → "你的新闻资料包" → sample → 资料速览 / 代表作 / 配图建议. Screenshot: `shots/laptop_pksample.png`.
- **Viewport:** both.
- **What I saw:** these `<ul>` blocks render as unmarked indented lines, while the how-to `<ol>` lists above them show numbers fine — so the fact-sheet/works/image-guidance read as a loose run of lines rather than a list.
- **Cause:** a global `ul { list-style: none }` reset is in effect; `.sf-pk-ul` (`SaffronPage.css:2356`) only sets `padding-left` and never re-asserts a marker.
- **Fix:** `.sf-pk-ul { list-style: disc; }` (matches the `.sf-collab-howto-list` ol treatment).

### T3-2. `/api/stats` 404 on load (console error)
- **Surface:** any tab (fires on initial load). Console: `Failed to load resource: 404 @ /api/stats`.
- **Viewport:** both.
- **What I saw:** one red console error every load. I did not see an obviously empty section, but a missing stats payload could leave the Momentum/stats area thin — worth a glance at "职业动能追踪".
- **Fix:** backend (`api.py`) — either restore the endpoint or drop the client call. Hygiene, not visibly broken.

### T3-3. Venue / contact notes show English in the 中文 view
- **Surface:** Venue-Tracker rows (e.g. "Official site/contact verified manually. Need to ve…") and the editor note field.
- **Viewport:** both.
- **What I saw:** her default zh view shows raw English pipeline notes. Layout is fine; this is a localization gap (matches the handoff's known zh/ja note gaps). Flag for the translate pass, not a CSS fix.

### T3-4. Career-Position marker strip feels lonely; collab card hierarchy is soft
- **Markers:** `.sf-rings` (`SaffronPage.css:142`) centers just 3 stats in an 820px section, leaving wide empty flanks. Consider left-aligning to the synopsis, or capping the strip width. Minor — the accent rules under the numbers (the dot-replacement) look good.
- **Collab cards:** within a `.sf-collab-entry`, the "who" line (12.5px italic, `:2298`) and the "why_fit" line (13.5px, `:2299`) are close enough in size/weight that the card's internal hierarchy reads a touch flat. Nudge "who" smaller or lighter. Cards are otherwise consistent and pleasant.

### T3-5. Peppercorn carousel stacks tall on phone
- **Surface:** Peppercorn top "to-do" carousel. Screenshot: `shots/phone_pp_carousel.png`.
- **Viewport:** phone.
- **What I saw:** the 5 cards stack full-width vertically, pushing the actual sections well down the page before she reaches her statement. Not broken — consider a horizontal-scroll row or a 2-up grid at phone so the cards don't eat a full screen of scroll. Low priority.

---

## What's solid (checked, no action)
- **Calendar month-grid (deadline dots):** the redesigned `.cal-grid` reads cleanly — rose dots + small counts under the day, today ringed in gold. `shots/laptop_calgrid.png`.
- **Timing Intelligence chart:** good at both widths; peak months in terracotta, month labels stack legibly per-character on phone. `shots/laptop_timing.png`, `shots/phone_timing.png`.
- **Collaboration Map / Collector Ecosystem:** consistent card language (`.sf-collab-entry`), clear 3-group structure, warm how-to box; stacks cleanly on phone. `shots/laptop_collab.png`, `shots/phone_collab.png`. Collector reuses the same markup — consistent.
- **Press-Kit how-to + sample:** thorough, legible, calm; only the ul-marker nit (T3-1).
- **Peppercorn reordered sections:** order is statement → preferences → goals → questions → logs, exactly as intended (`computeSectionOrder`), statement open by default.
- **Peppercorn filter chips:** wrap cleanly with counts and a green active state; no overflow at phone. `shots/phone_pp_chips.png`. Preferences surface grid fits phone fine. `shots/phone_pp_surface.png`.
- **No horizontal overflow** anywhere on Saffron(relationships)/Peppercorn at 375px — the only phone overflow is T0-1.
