# Flint — Runtime Correctness & Robustness Pass

**Date:** 2026-06-26
**Surface:** live site https://twilightdreamworks.com/mochi/ (== repo `main`)
**Method:** Playwright walk of all 3 companion tabs + all 5 Saffron sub-tabs (strategy/profile/calendar/relationships/money), console captured after each surface, interactives exercised live (Venue Tracker PATCH, Peppercorn filter chips, Mochi show-more, tab + language nav). Source cross-checked for every finding.

## Headline
The app is runtime-solid. **No Tier 0 failures**: nothing threw, nothing rendered blank, no error boundary tripped (`.pp-section--error` = 0 everywhere), no broken images (0/69, all 68 watercolor icons load), every API call returned 200, and all three primary interactions work and persist. The whole session produced **exactly one console error — a `GET /api/stats` 404 — and it is NOT coming from the app** (see T1-a). The real punch-list is i18n leaks and one data glitch, not breakage.

## What I verified WORKS (so nobody re-checks it)
- **Saffron Venue Tracker "更新/Update"** → opening the editor on KAYOKOYUKI and Save fired `PATCH /api/contacts/KAYOKOYUKI` → **200**, returned the updated contact, and the "已保存" confirmation rendered. Endpoint `api.py:1606`. Persists. (Tested with a no-op save to avoid mutating her data.)
- **Mochi People "✓ Reached out"** → `PATCH /api/contacts/update` (`api.py:1574`) exists and is reachable; route order (specific `/update` before `/{contact_name}`) is correct.
- **Peppercorn filter chips** → contacts 全部=52 → 调研中=10 cards, active state toggles, counts match. Localized. Exhibition/submission logs correctly auto-hide chips when only one value is present (by design, `LogFilterTabs` PeppercornPage.jsx:560-566).
- **Mochi "show more"** → `再显示 4 个`, grew section 4 → 8 `.opp-card`. Localized.
- **Tab nav** (3 companions, 5 Saffron sub-tabs, zh/en language toggle) all switch cleanly; Saffron data loads once and caches; calendar renders a real month grid (6月 2026 + per-day deadline counts + linked rows); English view renders with no reverse-leak (the CJK lines there are legitimate proper-noun exhibition titles).
- Peppercorn section order is the deterministic statement → preferences → goals → questions → logs (the 2026-06-26 SHIPPED fix is live). No white-screen.

---

## Tier 0 — breaks / throws / blank
**None found.** Stated plainly because it's a real result, not padding: every surface rendered, every interaction completed, zero error boundaries, zero 4xx/5xx on app API calls.

---

## Tier 1 — errors & her-facing correctness

### T1-a. The only console error: `GET /api/stats` → 404 — but it is NOT the app
- **Surface:** observed once early in the session (Saffron walk); referer = the mochi page; GET.
- **Evidence it is not app code:** `api/stats` / `/stats` appears in **none** of the three live JS bundles (`index-DA8Fj33y.js`, `SaffronPage-CesFYQCr.js`, `PeppercornPage-AAwwwIBW.js` — I fetched and grepped each), and not in `frontend/src`. It did **not** reproduce across two subsequent clean reloads + full tab walks. The removed MarketStats/Landscape feature (cut 2026-06-25) is the only thing that ever talked to a stats-shaped endpoint, and it's gone from source and bundle.
- **Conclusion / fix:** almost certainly a browser-extension probe or a stale prefetch/service-worker hit from the very first navigation in this profile — not a code defect. **Action:** confirm in a clean browser profile (no extensions). If it ever reproduces from the app, add a trivial `/api/stats` 204 stub; otherwise nothing to fix. Listed at T1 only because the brief specifically asks whether the live site threw any console error — it did, this one, and this is the full diagnosis.

### T1-b. People-view group labels leak English in ALL languages
- **Surface:** Mochi (发现) → "值得联系的人 / People" section. Live confirmed: the three group headers render **`High priority` / `Worth reaching out to` / `Keep on the radar`** in the zh view (and ja, and en).
- **File:** `frontend/src/components/RelationshipTargets.jsx:54-58` (`GROUP_FALLBACK`). `tfb()` looks up `people.group.high|medium|low`, which **do not exist in any locale block** of `translations.js`, so all three always fall back to English.
- **Fix:** add `people.group.high/medium/low` to the zh, ja, and en blocks (next to the existing `people.*` keys at translations.js ~1010 / ~2061 / ~3155). zh e.g. 高优先 / 值得联系 / 保持关注.
- **Why:** her default language is zh; raw English group headers on her home view. (This is the leak the handoff said is being handled — confirmed scope: exactly these 3 labels, all languages, this one component.)

### T1-c. Raw English CRM notes leak in zh/ja across three contact surfaces
- **Surface 1 — Saffron Venue Tracker** (人脉与媒体 → 场地关系追踪): venue rows show internal English research notes verbatim, e.g. *"Official site/contact verified manually. Need to verify whether unsolicited submissions are accepted."*, *"Top-tier Tokyo art bookshop. Colour Diary consignment target. Research submission/consignment process first."* — rendered at `SaffronPage.jsx:1301` (`cur.notes`).
- **Surface 2 — Peppercorn contacts** (联系人): card notes show e.g. *"Via casabrutus.com contact or Instagram @casabrutus"* in the zh view.
- **Surface 3 — Mochi People**: same `notes`/`why_relevant` path (`RelationshipTargets.jsx` `loc()` only upgrades when a `_zh`/`_ja` sibling exists; many contacts have none).
- **Root cause:** these `notes` are operator-authored English in the CRM data (`memory` contacts), with no `notes_zh`/`notes_ja` siblings, so `loc()`/raw render falls through to English. This is internal back-office language showing on her dashboard.
- **Fix (data, not code):** run the contact-translation path over `notes`/`why_relevant`, OR gate raw notes behind "has a localized sibling" so untranslated internal notes don't surface to her. The code path is correct; the data is missing translations.
- **Why it matters:** these read as someone's private working notes about her ("verify whether unsolicited submissions are accepted") — exactly the kind of thing a private dashboard for one artist should not show her in a half-translated state.

---

## Tier 2 — i18n gaps & data glitch (her-facing, not breaking)

### T2-a. "3 paths" hardcoded English in the Long-Term Paths summary
- **Surface:** Saffron → 策略 → 长期路径 section header renders **`3 paths · 未来几年`** in zh.
- **File:** `SaffronPage.jsx:1186` — `` const summary = `3 paths · ${data.horizon}` ``. The count *and* the word "paths" are hardcoded; only `data.horizon` is translated.
- **Fix:** route through a key, e.g. `t('sf.paths.count', { n: data.paths?.length ?? 3 })`, and make the count data-driven while at it.

### T2-b. Pathway timeline string falls back to English in zh
- **Surface:** Saffron → 策略 → 成长路径 header: **`预计时间线：12–36 months from mid-2026`** (the timeline tail is English).
- **Root cause:** the deep-translate dictionary has `"18–36 months from mid-2026"` (`SaffronPage.jsx:239`) but the backend (`career_strategy_engine`) now emits **`12–36 months`**, so there's no dictionary hit and it falls through to English. Classic stale-key-after-a-data-change.
- **Fix:** add the `12–36 months from mid-2026` zh/ja entries; better, stop hardcoding ranges in the dict — translate the surrounding frame and pass the numeric range as an interpolated value so future range changes don't re-leak.

### T2-c. Data glitch: stray "defined" prefix on a publication title
- **Surface:** Saffron → 收入 → publications/出版生态 renders **`defined Definition 02: A Documented Journey · 未知`**.
- **File (data):** `Memory/artist_master_profile.json:284` — `"title": "defined Definition 02: A Documented Journey"`. The leading `defined ` is corruption (likely a status/label token that got concatenated into the title during some past write). The real title is *"Definition 02: A Documented Journey"*.
- **Fix:** correct the title field in `artist_master_profile.json` (and check whether a generator prepends a label that produced it, so it doesn't come back). The `· 未知` (unknown) tail is a missing year/field — minor, secondary.

---

## Tier 3 — nits / known / theoretical (no real risk)
- **Emoji still present** where the watercolor-icon migration hasn't reached: `RelationshipTargets.jsx:33-38` (`TYPE_ICON` 🖼️☕📚 etc.) and Today's-Focus glyphs (◎, 📅), plus channel glyphs (✉ 🔗 📝) in People details. Already tracked in the handoff PENDING list (icon unification). Cosmetic only.
- **`markReached` gives false-positive feedback:** `RelationshipTargets.jsx:140-148` sets `reached`, fires the PATCH, and shows the success toast **unconditionally**; the fetch is fire-and-forget with `.catch(() => {})` (line 103). On a network failure she'd see "logged" but nothing persisted. Low impact (best-effort by design), but consider only toasting on `r.ok`.
- **Route shadow (theoretical):** `PATCH /api/contacts/update` is declared before `/api/contacts/{contact_name}` (correct), but a contact literally named "update" would be unreachable by the generic PATCH. Won't happen with real data; noting for completeness.
- **Saffron intro still over-promises:** the 山楂 intro still says it tracks "who's showing where / which artists are rising" — the Landscape feature that backed that claim was cut. Already a known PENDING content retune (handoff); flagging that it is still live so it isn't forgotten.

---

## Console summary (all surfaces)
| Surface | Errors | Warnings |
|---|---|---|
| Mochi / 发现 (load) | 0 | 0 |
| Saffron / 观察 — strategy | 0 | 0 |
| Saffron — profile | 0 | 0 |
| Saffron — calendar | 0 | 0 |
| Saffron — relationships (+ Venue Tracker save) | 0 | 0 |
| Saffron — money | 0 | 0 |
| Peppercorn / 对话 (+ filter chips) | 0 | 0 |
| English language view | 0 | 0 |
| **Whole session total** | **1** (`/api/stats` 404, not app — see T1-a) | 0 |
