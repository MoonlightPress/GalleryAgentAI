# LORE — language & voice pass (Mochi's Atelier)

Date: 2026-06-26 · Reviewer: Lore (copy/language lead, zh/ja/en)
Method: read source (== live), then walked the live site at https://twilightdreamworks.com/mochi/ in zh. Notes on what is rendered vs. source-verified are called out per item.

---

## META FINDING (read this first) — Japanese is NOT selectable in the live UI

The deployed language toggle offers only **中文 / English**. `LANGUAGES = ['zh', 'en']` — `ja` is omitted.
- File: `frontend/src/i18n/translations.js:3324` (`export const LANGUAGES = ['zh', 'en']`); label map `:3325` also omits `ja`.
- Confirmed on the live nav (only "中文 · English" buttons render on every page).

Consequence: **every Japanese leak below is currently LATENT** — GEGYjiji cannot reach the ja view today, so none of the ja fallbacks are things she would actually see. I've still catalogued them (they'll surface the moment `ja` is added back to `LANGUAGES`), but I've tiered them as "ja-latent" so the truly-visible **zh** leaks sort to the top. If the team believes ja is live (the handoff says "review live in zh," the brief says "walk the site in ja"), this gap is the thing to decide first: either re-expose ja (and the ja work below is real and incomplete) or accept ja is shelved (and the ja items are deferrable).

---

## TIER 0 — a leak she sees on a main surface, in her DEFAULT language (zh)

### T0-1 · Contact group headers render in English (zh) — KNOWN, scope confirmed
- Surface: **Mochi / 发现** page → "值得联系的人" (People) section group headers.
- Offending strings (zh view, shown in English): `High priority` · `Worth reaching out to` · `Keep on the radar`
- Confirmed rendered live (all three buckets: 8 / 33 / 11).
- Cause: no `people.group.*` keys exist, so `tfb()` falls back to the English literals.
  - `frontend/src/components/RelationshipTargets.jsx:54-58` (`GROUP_FALLBACK`) and render at `:230` (`tfb(t, \`people.group.${groupKey}\`, …)`).
  - `frontend/src/i18n/translations.js` — **no `people.group` key exists** (grep: 0 hits).
- Fix: add the three keys to translations.js for zh/ja/en:
  - `people.group.high` → zh **「优先联系」** · ja 「優先度高め」 · en "High priority"
  - `people.group.medium` → zh **「值得联系」** · ja 「連絡してみる価値あり」 · en "Worth reaching out to"
  - `people.group.low` → zh **「保持关注」** · ja 「視野に入れておく」 · en "Keep on the radar"

### T0-2 · Her own exhibition CV shows English type/note/venue (zh)
- Surface: **Saffron / 概况 (Profile)** tab → "职业定位 / Career Position" → exhibition list.
- The titles + Chinese venue names are fine (proper nouns), but the **`type` and `note` lines are pure English UI prose** in the zh view, e.g.:
  - `Group show ·`
  - `Solo show · First solo gallery exhibition on record`
  - `Group show (museum) · Institutional (museum) group exhibition`
  - `Exhibition (group/solo not specified on source) ·`
  - `Group show (6 Chinese illustrators) · First exhibition in Japan (stated explicitly in exhibition materials)`
  - venue date tails also English: `…, Shanghai, China · March–April 2021`
- Confirmed rendered live (12 rows, all English type/note).
- Cause: `data.career_position.exhibitions[].type / .note / .venue` are served in English and are **not** in any zh map (`SF_ZH` / payload `_i18n.zh`). Render: `frontend/src/components/SaffronPage.jsx:520-523`.
- Fix: localize these at the backend (`api.py` career_position payload → emit `_zh`/`_ja` siblings or `_i18n` entries) since they're data, not authored constants. Sample zh: `Group show` → 「联展」; `Solo show · First solo gallery exhibition on record` → 「个展 · 记录在册的首次画廊个展」; `Institutional (museum) group exhibition` → 「美术馆机构联展」; `March–April 2021` → 「2021年3–4月」.
- Note: this section is collapsed-by-default (Career Readiness is the open one), so it's one expand from view — but it's her entire exhibition history shown to her in English, so I'm holding it at Tier 0.

---

## TIER 1 — real leak, less prominent or ja-latent

### T1-1 · Collaboration Map body falls back to English in ja — KNOWN (ja-latent)
- Surface: Saffron / 人脉与媒体 → "合作地图". In ja the **header + summary render Japanese** (`title_ja`/`summary_ja` exist) but the **entire body is English**: the lead, all three group labels, every entry's who / why_fit / collab_form, and the how-to list. A half-Japanese, half-English section.
- Source gaps in `frontend/src/data/saffron_insights.js` (COLLABORATION_MAP): `lead` has `lead_zh` (`:909`) but **no `lead_ja`**; group `label`s have `label_zh` (`:913`, `:968`, `:1004`) but **no `label_ja`**; entries carry `who_zh/why_fit_zh/collab_form_zh` only (e.g. `:917-923`) — **no `_ja`**; `how_to_zh` (`:1057`) but **no `how_to_ja`**. Render: `SaffronPage.jsx:1076-1104` via `localizeDeep` (missing `_ja` → English).
- Fix: add `_ja` siblings for lead, the 3 group labels, every who/why_fit/collab_form, and how_to. (zh is complete and reads well — see voice note below.)

### T1-2 · Collector Ecosystem body falls back to English in ja — KNOWN (ja-latent)
- Surface: Saffron / 人脉与媒体 → "藏家生态". Same pattern: header+summary Japanese, body English (intro, every channel name/what/fit_for_her, the how-to steps).
- Source gaps (COLLECTOR_ECOSYSTEM): `intro_zh` (`:1079`) no `intro_ja`; channels carry `name_zh/what_zh/fit_for_her_zh` only (`:1082-1143`); how_to steps `step_zh` only (`:1146-1150`). Render: `SaffronPage.jsx:971-996`.
- Fix: add `_ja` for intro, each channel's name/what/fit_for_her, and each how_to step.

### T1-3 · Press Kit "How to use it" + "Keeping it updated" fall back to English in ja — NEW (ja-latent)
- The handoff claims "press kit is full zh/ja/en." It is **not**: `how_to_use` and `how_to_update` carry only `en` + `zh`, **no `ja`**.
- Surface: Saffron / 人脉与媒体 → "你的新闻资料包" → the two how-to lists render **directly in the section body** (not behind the sample disclosure), so in ja they'd show the JP labels "使い方 / 更新の仕方" over **English bullet lists**.
- Source: `saffron_insights.js:1280-1293` (`how_to_use` — en/zh only) and `:1294-1309` (`how_to_update` — en/zh only). Render: `SaffronPage.jsx:1025-1032` via `pkList(... )` → `f[lang] || f.en`.
- Fix: add `ja:` arrays to both. (Everything else in PRESS_KIT — one_line/short_bio/long_bio/statement/fact_sheet/selected_works/image_guidance — does carry ja and is fine.)
- zh side of this section verified rendered live: fully Chinese, clean, warm. No issue in zh.

---

## TIER 2 — smaller visible leaks / phrasing

### T2-1 · "Watercolor work feature" English in BOTH zh and ja (press-kit sample)
- Surface: 你的新闻资料包 → "看一份可直接用的样本" (sample disclosure) → Press field.
- `PRESS_KIT.press[].type` has no zh/ja; rendered raw as `{outlet} — {type}`, so the zh view shows `Bored Panda — Watercolor work feature` / `… Watercolor work feature, part 2`.
- Source: `saffron_insights.js:1277-1278`. Render: `SaffronPage.jsx:1058-1059`.
- Fix: give `type` zh/ja, or map it: zh 「水彩作品报道」/「水彩作品报道（第二部分）」; ja 「水彩作品の特集」/「同・第2弾」.

### T2-2 · Strategy pathway horizon shows English in zh
- Surface: Saffron / 策略, first section summary: `预计时间线：12–36 months from mid-2026` — the date phrase is English.
- Cause: `SF_ZH` maps the **stale** variant `"18–36 months from mid-2026"` (`SaffronPage.jsx:239`); the live payload now emits `12–36 months`, so it misses the map and leaks. The count changed and the translation didn't follow.
- Fix: localize the horizon at source (so it survives count changes) or add the current string: → 「自 2026 年中起 12–36 个月」.

### T2-3 · "3 paths" hardcoded English (zh + ja)
- Surface: Saffron / 策略 → "长期路径" collapsed summary: `3 paths · 未来几年` — "3 paths" is a hardcoded English literal.
- Source: `SaffronPage.jsx:1186` (`const summary = \`3 paths · ${data.horizon}\``).
- Fix: localize: zh 「3 条路径」 · ja 「3つの道」 · en "3 paths".

### T2-4 · Comparable-artist peers leak English in ja — KNOWN (ja-latent)
- The 9 new peers' `fit_reason` / `shared_traits` / `use_as` are translated for zh only — `SF_ZH_PEERS` (`SaffronPage.jsx:290-362`) is merged into the **zh** map but the **ja** map omits it (`:2310-2311`), so ja relies entirely on payload `_i18n.ja`, which doesn't cover them.
- Fix: add ja siblings for the new peers (or a `SF_JA_PEERS` merged into the ja map).

### T2-5 · Where-to-start intro lines leak English in ja (Licensing / Grants / Press&Pitch) — ja-latent
- `where_to_start` has `_zh` but no `_ja` for: LICENSING (`saffron_insights.js:7-8`), PRESS_PITCH_MAP (`:122-123`), GRANT_LANDSCAPE (`:259-260`). In ja these top-of-section "where to start" paragraphs render English. Render via `WhereToStart`, `SaffronPage.jsx:1352-1360`. (REVENUE_STREAMS does have `where_to_start_ja` — fine.)
- Fix: add `where_to_start_ja` to the three.

---

## TIER 3 — content/accuracy nits (not strictly translation)

### T3-1 · An exhibition row is titled "SARAH ANDERSEN"
- Surface: Career Position list → a row reads title **`SARAH ANDERSEN`**, venue `London, UK · December 2025`. This is the London Dec-2025 group showing (she exhibited in the same context as Sarah Andersen) being labelled with the co-exhibitor's name as if it were the show title. Reads oddly in every language. Data fix in the career_position exhibition source, not a translation fix.

### T3-2 · Saffron intro still promises the cut "Landscape" content — KNOWN/PENDING
- `sf.intro.body` (zh `translations.js:43`, en `:2231`) still says "…谁在哪里展出、市场如何流动、哪些艺术家正在崛起" / "who's showing where, how the market's moving, which artists are rising." The Landscape tab was cut, so the intro over-promises a feature that no longer exists. The handoff already has proposed replacement wording awaiting Scott's OK; apply when approved (update both zh and en, and add ja when ja is re-exposed).

---

## zh VOICE / QUALITY on the new content — PASS

I read the full zh of the career synopsis, Collaboration Map, Collector Ecosystem, Press Kit, Pricing, and the Licensing lead, and confirmed the section headers/summaries + Press Kit body render correctly in Chinese on the live site. The zh is genuinely good: natural, warm, consistent second-person, calm/optional register that matches the money-page gold standard. No machine-translation stiffness, no fabricated claims, proper nouns handled (brand names kept Latin, Chinese gloss added where helpful, e.g. 「《色彩日記》（Colour Diary）」). No zh rewrite needed beyond the leaks above.
- One micro-note (not a defect): the press-features list shows outlet "BOOOOOOOM" — correct proper noun, leave as-is.
