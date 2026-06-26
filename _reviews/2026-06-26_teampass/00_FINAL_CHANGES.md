# 2026-06-26 TEAM PASS — FINAL CONSOLIDATED CHANGE REPORT

**What this is.** The single prioritized change list synthesized from the six facet reports in this folder
(`flint` runtime · `crema` cross-tab/features · `domino` visual/UX · `lore` language/voice · `pip` emotional safety · `sterling` money).
Each item is deduplicated, tagged with the reviewer(s) who found it, cited to `file:line`, and given a fix + a falsification (acceptance) check where one exists.
**Surface reviewed:** the live site `https://twilightdreamworks.com/mochi/` (== repo `main`), walked in zh (her default), Playwright + source cross-check.

---

## THE BIG PICTURE (read first)

The app is **runtime-solid** — Flint walked every surface and found **zero** breaks, blank renders, error boundaries, or failed API calls; the single console error (`/api/stats` 404) is not even app code. So this is **not** a stability list. It is a list of (1) a real **data-loss bug** in the new editable CRM seam, (2) a handful of **her-facing wrongnesses** — a false self-deprecating line, a contradicting price, a contradicting follower count — and (3) **i18n leaks** where internal English shows on her zh dashboard. The deepest finding sits underneath all of it: **the site is rich on *knowing* and thin on *doing*** (Crema) — it tells her where she stands but leaves "what do I do this week" to her, which for an easily-overwhelmed artist is where it stops being useful and starts being a pretty read.

**One structural decision gates a third of the i18n work:** Japanese is **not selectable** in the live UI (`LANGUAGES = ['zh','en']`, `translations.js:3324`). Every ja-only leak below is therefore **latent** — she cannot reach it today. **Decide once:** re-expose `ja` (then the ja work is real and must be finished) or accept ja is shelved (then all "ja-latent" items defer). Until decided, **zh leaks are the only ones she actually sees.**

---

## CONVERGENT FINDINGS (≥2 reviewers — highest confidence, fix these first)

| Theme | Found by | Priority |
|---|---|---|
| Contact **status seam** → silent data downgrade + split "active" | Crema T1.2/T1.3, Domino T1-1, Flint T3 | **P0** |
| **Instagram number** contradicts (27k vs 26k) / brittle marker | Crema T0.1, Pip T2.2 | **P0** |
| **People group headers** render English in her zh home view | Flint T1-b, Lore T0-1 | **P1** |
| **Internal CRM notes** leak raw English in zh/ja | Flint T1-c, Domino T3-3 | **P1** |
| **Saffron intro** over-promises the cut "Landscape" | Flint T3, Lore T3-2, Pip T2.1 | **P2** |
| **`/api/stats` 404** console error | Flint T1-a, Domino T3-2 | **P3** (not app code) |
| **"defined Definition 02"** title corruption | Flint T2-c, Sterling T3.2 | **P3** |

---

## P0 — FIX NOW (data loss · live wrongness she sees · broken on phone)

### P0-1 · Contact status seam silently downgrades her data  · *Crema T1.2/T1.3 + Domino T1-1 + Flint*
Three surfaces share the one 52-contact store through a **non-validating** `PATCH /api/contacts/{name}` (`api.py:1606-1630`) but carry **three different status vocabularies**:
- Saffron Venue Tracker `VENUE_STATUS_OPTS` — `SaffronPage.jsx:1236-1244`
- Peppercorn CRM `CRM_STATUS_META` — `PeppercornPage.jsx:1214-1227`
- Peppercorn venue-log `VENUE_STATUS_OPTIONS` — `PeppercornPage.jsx:956-963`

**The bug:** a row whose status is `ready_to_review` (the CRM's *default* for new contacts) opens in Saffron's editor showing `cold` (`VenueTrackerRow` seeds `useState(v.status || 'cold')`, `:1262`), because `ready_to_review` isn't in the Saffron vocabulary. Press 保存 → it writes **`cold`** → **silent downgrade / data loss.** Separately, "active" is computed two ways (`api.py:2569-2573` vs `PeppercornPage.jsx:1449`), so the same 52 contacts show two different "active" totals.
**Fix:** one shared status enum module both tabs import; include `ready_to_review` (and `relationship`/`not_a_fit`) everywhere; have the PATCH endpoint **validate/normalize** status so neither surface can persist a value the other can't render; one shared `is_active()` predicate. **Quick interim patch (Domino):** if `v.status` isn't in `VENUE_STATUS_OPTS`, prepend it as the selected option so save preserves it.
**Falsification:** open the `ready_to_review` row editor → the `<select>` shows that status, not 尚未联系; saving a no-op leaves the store value unchanged.

### P0-2 · "You're in Good Company" opens by apologizing for itself — with a false claim  · *Pip T0.1 (LIVE, zh)*
The one section whose entire job is *belonging* opens with a caveat (`sf.label.peersCaveat`, `translations.js:431`, rendered unconditionally at `SaffronPage.jsx:585`) that says "此处大多数是摄影师 / most here are photographers" and "以水彩为核心的同类群体仍在发展中 / the watercolor peer set is still developing." Both are **false** — the cards directly beneath are all watercolorists — and the line exposes the machinery ("系统…数据进入系统").
**Fix:** **delete the caveat entirely** (`sf.sub.peers` already frames the section kindly). If a line is wanted, a warm, true one — e.g. "这些是与你气味相投、走在相近道路上的创作者——看看他们的世界，你本就属于其中。" No "photographers / underdeveloped / 系统 / 数据" language.
**Falsification:** the caveat string is absent from the rendered Good-Company section.

### P0-3 · Calendar month-list overflows horizontally on phone — the whole page side-scrolls  · *Domino T0-1*
Saffron → 日历 → 季节性机会日历: at 375px the document is **840px wide** (`body.scrollWidth`), every opp name clipped, page gains a horizontal scrollbar. `.sf-cal-month { grid-template-columns: 100px 1fr }` (`SaffronPage.css:627`) has no phone breakpoint and `.sf-cal-opps`/`.sf-cal-name` never get `min-width:0`, so the `1fr` track blows out to max-content.
**Fix:** `.sf-cal-opps{min-width:0}` · `.sf-cal-name{min-width:0;overflow-wrap:anywhere}` · `@media(max-width:560px){ .sf-cal-month{grid-template-columns:1fr;gap:6px} }`.
**Falsification:** at 375px `document.body.scrollWidth === document.documentElement.clientWidth` and no opp name is clipped.

### P0-4 · Pricing subtitle is stale — contradicts its own cards and overshoots her real catalog  · *Sterling T0.1*
定价情报 subtitle renders `¥37,000–135,000 原作 · ¥3,000–12,000 版画` (`sf.sum.pricing`, `translations.js:370` / ja `:1281` / en `:2322`), while the body cards inches below render the corrected `¥30,000–115,000` / `¥3,000–15,000` (`saffron_insights.js:856,861`). The ¥37k floor is **above** her cheapest real original (¥31,900); the ¥135k ceiling is a **phantom** ~¥19,500 above the highest price anyone has actually paid (¥115,500). (This was the 2026-06-25 T0.2 fix — the data file was corrected but the `translations.js` subtitle was missed.)
**Fix:** update all three langs to match the body (`¥30,000–115,000 原作 · ¥3,000–15,000 版画`). Better: lead with her real product mix (originals + zines ¥1,200–2,800) since she has **no print line** at all.
**Falsification:** subtitle range == body card range; no `¥135` / `¥37` in the served pricing copy.

### P0-5 · Instagram follower count contradicts across tabs (27k vs 26k), live  · *Crema T0.1 + Pip T2.2*
Saffron serves `27k` (`api.py:2064`, `2070`; `SaffronPage.jsx:491` `|| '27k'` fallback); Peppercorn serves `26k` (`api.py:3183`, from `artist_master_profile.social_presence`). Same account, two numbers — and a brittle hard-coded one against the standing "no brittle numbers" bar.
**Fix (Pip's, strongest):** **drop the IG marker entirely** from the `markers` array — the soft audience fact "稳固且持续增长的 Instagram 受众" (`translations.js:391`) already sits in the same section and is on-principle. If a number is kept, single-source it from `artist_master_profile.social_presence` and delete the `27k` literals.
**Falsification:** grep the served payloads for `27k` → zero; one Instagram statement site-wide (or none).

---

## P1 — REAL HER-FACING (fix soon)

### P1-1 · Deploy the kind 9-peer set — the belonging section currently serves famous masters  · *Pip T1.1*
`/api/saffron` `peer_artists` still returns the OLD 8 (Castagnet, Schaller, Haines, Chien Chung-Wei…) — world-famous legends. Under "你身处优秀的同道之中 / company, not comparison," that reads as **"13 people you're behind."** The frontend is already prepared (the 9 daily-diary/illustration peers — Liz Steel, Samantha Dion Baker, Mateusz Urbanowicz, Felicia Chiao… — are baked at `SaffronPage.jsx:290-362` `SF_ZH_PEERS`, slice `:577`); the **data was never regenerated/deployed** (two-source split). **Fix:** regenerate + deploy the peer data so the kindred set is live. **Falsification:** live Good-Company shows the diary peers, not only masters. *(Mechanics = data/deploy → Crema/Flint; this is the emotional ask behind P0-2.)*

### P1-2 · People group headers render English on her zh home view  · *Flint T1-b + Lore T0-1*
Mochi/发现 → 值得联系的人: the three buckets render `High priority` / `Worth reaching out to` / `Keep on the radar` in zh (and ja). `GROUP_FALLBACK` at `RelationshipTargets.jsx:54-58`; **no `people.group.*` keys exist** in `translations.js`. **Fix:** add `people.group.high|medium|low` to zh/ja/en (zh: 优先联系 / 值得联系 / 保持关注). **Falsification:** zh view shows Chinese group headers.

### P1-3 · Her own exhibition CV shows English type/note lines in zh  · *Lore T0-2*
Saffron → 概况 → 职业定位 exhibition list: titles + Chinese venues are fine (proper nouns), but `type`/`note` render pure English in zh ("Group show ·", "Solo show · First solo gallery exhibition on record", "Institutional (museum) group exhibition", date tails like "March–April 2021"). Served English, no zh map (`SaffronPage.jsx:520-523`). **Fix:** localize at the backend `career_position` payload (emit `_zh`/`_ja` siblings). **Falsification:** all 12 rows' type/note/date render in zh.

### P1-4 · Internal CRM research notes leak raw English on her dashboard (zh/ja)  · *Flint T1-c + Domino T3-3*
Three surfaces show operator-authored English notes verbatim — Saffron Venue Tracker (`SaffronPage.jsx:1301`), Peppercorn contacts, Mochi People (`RelationshipTargets.jsx` `loc()`). e.g. "Need to verify whether unsolicited submissions are accepted." These read as someone's **private working notes about her**. Data, not code: no `notes_zh`/`notes_ja` siblings. **Fix:** run the contact-translation path over `notes`/`why_relevant`, **or** gate raw notes behind "has a localized sibling" so untranslated internal notes never surface to her.

### P1-5 · Career Momentum can stamp a red "停滞 / Stalling" verdict on her  · *Pip T1.2*
Color `SaffronPage.jsx:1639` (`stalling:'#b03020'`), label `translations.js:328`. Latent today (live = accelerating, 52 CRM venues) but **activity-driven** — the first quiet, school-busy stretch flips it to a red "停滞," a rank/shame verdict the gold-standard register forbids, landing on a month she was simply living. **Fix:** retire red here (match `LongTermScenarios`, which already banned red); soften the word so no state is a verdict (zh 停滞→"放缓的一段"/"休整期"; en "Stalling"→"A quieter stretch"); better, when activity is low show the gentle `sf.mom.noSubmissionsYet` note instead of a trajectory tag.

### P1-6 · Licensing explainer rows render as Google-search links  · *Sterling T1.1*
授权版图 group 3: explainer headings (收入区间（实际）, 如何被主动联系 vs 如何主动提案, 实际时间线, the two category descriptions) are each wrapped as external links (`SaffronPage.jsx:1385-1390`, `href` falls through to `sfSearch(entry.name)` → a Google results page) because `LICENSING_LANDSCAPE` entries carry no `website`/`url`. Clicking an explainer throws her to a search page. **Fix:** render `↗` only for entries with a real URL; explainer rows as plain text.

---

## P2 — i18n & POLISH (zh-visible first; ja items gated on the ja decision above)

- **P2-1 · Saffron intro over-promises the cut "Landscape."** *Flint T3 · Lore T3-2 · Pip T2.1* — `sf.intro.body` (`translations.js:43` zh, `:2231` en) still says "哪些艺术家正在崛起 / which artists are rising." Apply the handoff's already-proposed reword (awaiting your wording OK); update zh+en now, ja when re-exposed.
- **P2-2 · Hardcoded/stale strategy strings (zh-visible).** "3 paths · 未来几年" (`SaffronPage.jsx:1186`) and "预计时间线：12–36 months from mid-2026" (stale dict key at `SaffronPage.jsx:239`; backend now emits 12–36, the dict has 18–36). *Flint T2-a/b · Lore T2-2/3.* **Fix:** route both through keys and **interpolate the numeric range** so a future count change can't re-leak.
- **P2-3 · Press-kit sample lists have no bullets.** *Domino T3-1* — global `ul{list-style:none}` reset; `.sf-pk-ul` (`SaffronPage.css:2356`) never re-asserts a marker. **Fix:** `.sf-pk-ul{list-style:disc}`.
- **P2-4 · Career Position grid lopsided.** *Domino T2-1* — 12 exhibition rows left, 2 publication rows right → ~60% of the right column blank (`.sf-career-grid`, `SaffronPage.css:265`). **Fix:** wrap Publications + Audience in one right-column div (smaller change) or span Exhibitions both columns.
- **P2-5 · ja-latent bodies fall back to English** — collaboration map, collector ecosystem, press-kit how-to lists, the 9 comparable peers, where-to-start intros (Licensing/Grants/Press). *Lore T1-1/T1-2/T1-3/T2-4/T2-5; gaps enumerated in `saffron_insights.js`.* **Do only if ja is being re-exposed**; otherwise defer with the ja decision.
- **P2-6 · "Watercolor work feature" English in zh+ja** (press-kit sample press list, `PRESS_KIT.press[].type`, no zh/ja). *Lore T2-1.* **Fix:** map `type` to zh/ja.

---

## P3 — NITS & DATA CORRECTIONS

- **P3-1 · Data: "defined Definition 02" title corruption.** *Flint T2-c · Sterling T3.2* — `Memory/artist_master_profile.json:284` leading "defined " is a stray label concatenated into the title; fix the field and check the generator doesn't re-prepend.
- **P3-2 · Data: an exhibition row is titled "SARAH ANDERSEN."** *Lore T3-1* — the London Dec-2025 group show is labelled with a co-exhibitor's name as the title. Fix in the `career_position` exhibition source.
- **P3-3 · `/api/stats` 404 console error.** *Flint T1-a · Domino T3-2* — Flint confirmed it is **not app code** (absent from all three JS bundles + `frontend/src`; did not reproduce on clean reload) — likely a browser-extension/prefetch probe. **Action:** confirm in a clean browser profile; only if it ever reproduces from the app, add a trivial `/api/stats` 204 stub.
- **P3-4 · `markReached` false-positive toast.** *Flint T3* — `RelationshipTargets.jsx:140-148` shows "logged" unconditionally even on a failed fire-and-forget PATCH. **Fix:** toast only on `r.ok`.
- **P3-5 · "Venue Tracker" lists non-venues** (e.g. Apartamento Magazine). *Crema T3.2* — built from the whole `crm_list` (`api.py:2564`). **Fix:** rename to 关系/Relationships, or filter to venue-type contacts.
- **P3-6 · Money links/accuracy.** *Sterling T2.1/T2.2/T2.3* — real licensing brands (Hobonichi, Midori, Mark's, Stalogy) link to name-searches not their sites (add `website` fields); the Tokyo grant entry names the wrong institution ("TACT" / links Tokyo Midtown Award) — rename to **Arts Council Tokyo** / **TOKAS** with a real domain; verify or drop "China Arts Foundation International."
- **P3-7 · Emotional warmer-word nits.** *Pip T2.3/T2.4/T3.1-3.4* — Benchmarks subtitle "横向比较" → "你已达到或领先的方面"; Momentum subtitle drop "响应率"/"自动"; suppress "0个活跃关系" when active==0; Peppercorn dismissal "您"→"你"; carousel `/8` and `/3` quota denominators → drop the goalpost; "山楂目前的分析依据不完整" → "多说一点，山楂就更懂你."
- **P3-8 · Layout polish.** *Domino T3-4/T3-5* — Career-Position 3-marker strip looks lonely in an 820px section (left-align or cap width); collab card who/why_fit hierarchy is soft; Peppercorn carousel stacks tall on phone (consider horizontal scroll / 2-up).

---

## WHAT TO BUILD NEXT — the *knowing → doing* gap  · *Crema Part 2*
The site tells her where she stands; it doesn't yet tell her what to *do this week*. Ranked by value-per-effort, cheapest-highest-impact first:
1. **Follow-up reminders (S).** `is_overdue_followup()` already exists; when she sets `last_contacted`, badge a contact "worth a follow-up" after N days. Relationships die in the silent gap after first contact — and gallery rep (her #1 structural move) is won by follow-through. Cheapest high-value item.
2. **"This week" action digest (M).** One small card distilling everything into the 2–3 highest-leverage moves: nearest unactioned deadline + the one due follow-up + the next-unlock step. Data all exists (`_deadline_passed`, `last_contacted`, `career_strategy.level.next_unlock`). The direct antidote to her overwhelm.
3. **Email/pitch draft in context (M).** Drafts already generate (write-once, buried, stale); surface the ready-to-edit draft inline with one-tap copy. The blank-page email is a shy artist's highest-friction step. *(Also verify the statement-edit → regen loop actually fires on prod — still unconfirmed.)*
4. **Gallery-representation playbook (M, needs a real research pass — scope it, don't half-build).** The level model points at representation as THE next move but offers no concrete *how*.
5. **Press-kit / one-PDF lookbook generator (M–L).** One artifact unblocks both licensing DMs and press pitches.
6. **One "Relationships" surface, three views (M).** The structural version of P0-1 — one store + one status enum + one `is_active()`, with tab-specific views (Mochi discover-by-priority, Saffron strategic map, Peppercorn working CRM). Build it if the P0-1 quick patches start to sprawl.

---

## WHAT IS SOLID — DO NOT TOUCH
- **Runtime** (Flint): 0 breaks, 0 blank renders, 0 error boundaries, every API call 200, all three interactions persist. The only console error isn't app code.
- **zh voice on the new content** (Lore: PASS): career synopsis, Collaboration Map, Collector Ecosystem, Press Kit, Pricing, Licensing lead — natural, warm, calm/optional, no MT stiffness, proper nouns handled. No zh rewrite needed beyond the leaks above.
- **Money tone** (Sterling): the gold standard is preserved — every stream `leaving_on_table:false`, no "gap/缺口/should be earning" anywhere, links resolve to real platforms only.
- **The genuinely kind surfaces** (Pip): `CAREER_SYNOPSIS` (doors-not-deficits), the Benchmarks favorable-only guard, `LongTermScenarios` (red already retired), the Peppercorn reorder + its "这里没有急事，我会记住一切" intro — one of the warmest lines on the site.
- **Visual** (Domino): calendar month-grid (rose dots, gold "today" ring), Timing Intelligence chart, Collaboration/Collector card language, Peppercorn filter chips — all clean at both widths; no horizontal overflow anywhere except P0-3.

---

## SUGGESTED EXECUTION ORDER
1. **Tiny wins, batch them:** P0-2 (delete caveat) · P0-3 (calendar CSS) · P0-4 (pricing subtitle) · P0-5 (drop IG marker). All small, all live wrongness she sees.
2. **The one engineering chunk:** P0-1 (shared status enum + validating PATCH + `is_active()`). Removes the data-loss class of bug.
3. **Decide ja** (re-expose vs shelve) — unblocks/defers a third of P2.
4. **The zh leaks + the peer deploy:** P1-2, P1-3, P1-4, P1-1.
5. **Then build:** feature #1 (follow-up reminders) → #2 (this-week digest) — the highest behavior-change-per-effort, and the real answer to her overwhelm.

*Source facet reports: `flint.md` · `crema.md` · `domino.md` · `lore.md` · `pip.md` · `sterling.md` (this folder). No code edited, nothing deployed by this pass.*
