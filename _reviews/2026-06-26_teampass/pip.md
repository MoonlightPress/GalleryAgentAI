# Pip — Emotional-safety pass (2026-06-26 team pass)

Facet: does every NEW Saffron surface serve GEGYjiji without wounding her. Walked the live site in zh (Playwright + `/api/saffron`). The new authored prose — Career Position synopsis, Collaboration Map, Collector Ecosystem, Press Kit, the collapsed synopses — is genuinely kind, optional, and on-register; that work holds. The wounds are concentrated in two machine-fed surfaces (the peer list + the momentum trajectory) where the kind copy is undercut by stale/auto-generated content, plus a few warmer-word nits.

## 6-line summary
1. The one section built for *belonging* ("你身处优秀的同道之中" / You're in Good Company) opens, live, with a self-deprecating caveat that says "most here are photographers" and "the watercolor peer set is still underdeveloped" — false (all 8 are watercolorists) and machinery-exposing.
2. Worse: the kind 9-peer rewrite is NOT live — `/api/saffron` still serves the OLD 8 famous masters (Castagnet, Schaller, Haines, Chien Chung-Wei…), so "kindred company" currently reads as a wall of legends she's measured against.
3. The Career Momentum "trajectory" can render a red "停滞 / Stalling" verdict — latent today (live = "accelerating") but it WILL fire when a school-busy month dips her activity; that is a shame-verdict.
4. The Saffron intro still promises "哪些艺术家正在崛起" (which artists are rising) — comparison-priming, and it over-promises content that was cut.
5. A brittle hard-coded "27k" Instagram number still shows as a marker, despite the soft "established, growing" fact sitting right beside it.
6. Everything else (Collab Map, Collector Ecosystem, Press Kit, Peppercorn reorder + intro) reads kindly; remaining items are warmer-word nits.

## Top 3
- **T0.1** Kill the stale "most here are photographers / watercolor peer set underdeveloped" caveat in the Good-Company section — it's live, false against the cards, and deflating.
- **T1.1** Get the 9 kindred daily-diary peers actually live (the API serves the old master-heavy 8); right now "同道 / company" reads as "people she's behind."
- **T1.2** Retire red + the word "停滞/Stalling" from the momentum trajectory before a quiet month makes it appear.

---

## TIER 0 — an emotional wound she'd actually feel

**T0.1 — "You're in Good Company" opens with the system apologizing for itself, with a claim that's plainly false against the cards below it. [CONFIRMED LIVE in zh]**
Surface: Saffron → 概况 (Overview) → "你身处优秀的同道之中", caveat line.
File: `frontend/src/i18n/translations.js:431` (`sf.label.peersCaveat`, zh) — rendered unconditionally at `frontend/src/components/SaffronPage.jsx:585`.
Live string she sees:
> "系统通过主题与形式的重叠来寻找同类艺术家。此处大多数是摄影师 — 这是共同主题（安静的观察、记忆、日常空间）带来的偶然结果，并非类别错误。以水彩为核心的同类群体仍在发展中，随着更多定向数据进入系统会逐步完善。"
Why it wounds: this is the ONE section whose whole job is to make her feel she belongs. It opens by (a) exposing the machinery ("系统…数据进入系统"), (b) confessing it's half-built ("以水彩为核心的同类群体仍在发展中"), and (c) stating something visibly untrue — the 8 cards directly beneath are *all watercolorists* (Chien Chung-Wei, Keiko Tanabe, Thomas Schaller…), not photographers. A sensitive reader's takeaway: "the tool that's supposed to show me my peers is broken, and even it admits my kind isn't really here."
Exact fix: delete the caveat entirely — `sf.sub.peers` ("与你领域相近的优秀艺术家——是同道，而非高下的比较") already does the kind framing. If a line is wanted, replace with something warm and true, e.g.:
> "这些是与你气味相投、走在相近道路上的创作者——看看他们的世界，你本就属于其中。"
Do NOT keep any "photographers / underdeveloped / 系统 / 数据" language.

---

## TIER 1 — real wounds (one latent, one live-but-collapsed)

**T1.1 — The kind 9-peer rewrite is not live; the section is populated by famous masters, so "company" reads as "giants you're behind."**
Surface: same Good-Company section. Live `/api/saffron` → `peer_artists` returns the OLD 8: Chien Chung-Wei, Keiko Tanabe, Thomas W. Schaller, Cathy Read, Lian Quan Zhen, Japan Watercolor Society exhibitors, Alvaro Castagnet, Jean Haines. These are world-famous watercolor legends/teachers.
Files: frontend is already prepared — the 9 new daily-diary peers' zh is baked at `SaffronPage.jsx:290–362` (`SF_ZH_PEERS`) and the slice is `SaffronPage.jsx:577` (`artists.slice(0, 13)`) — but the API/profile data that feeds `peer_artists` was never regenerated/deployed (root cause is the two-source split; hand the data/deploy half to Crema/Flint).
Why it wounds: under "你身处优秀的同道之中 / 是同道，而非高下的比较," a list of Castagnet/Haines/Schaller invites exactly the "13 people I'm behind" read the brief warned about. The whole point of the new 9 (Liz Steel, Samantha Dion Baker, Mateusz Urbanowicz, Felicia Chiao…) is that they're at *her* register and practice — genuine company. The `use_as` "career-path reference" framing softens it, but until the kindred set is live the section under-delivers on its only emotional promise.
Exact fix: deploy the regenerated peer data so `peer_artists` carries the kindred set the frontend already expects; verify live shows the diary/illustration peers, not only the masters. (Pure emotional ask; mechanics are Crema/Flint.)

**T1.2 — Career Momentum can stamp a red "停滞 / Stalling" verdict on her.**
Surface: Saffron → 概况 → "职业动能追踪" (collapsed by default).
Files: color `frontend/src/components/SaffronPage.jsx:1639` (`stalling: '#b03020'`); label `frontend/src/i18n/translations.js:328` (`'sf.mom.traj.stalling': '停滞'`).
Status: latent — live trajectory is currently "accelerating" (green), because 52 venues are in the CRM. But the value is activity-driven, and she's in school; the first quiet stretch flips it to a red "停滞."
Why it wounds: a red, one-word "Stalling" judgment on her career is precisely the rank/shame the gold-standard register forbids — and it would land on a month she was simply living her life.
Exact fix: retire red here (match the dream-paths, which already banned red — `LongTermScenarios` lowest band is `#a07a45`), and soften the word so no state is a verdict, e.g. zh "停滞"→"放缓的一段" or "休整期", en "Stalling"→"A quieter stretch", ja "停滞"→"少しスローな時期". Better still, when submissions/activity are low, show the existing gentle `sf.mom.noSubmissionsYet` note instead of a trajectory tag at all.

---

## TIER 2 — pressure / comparison / brittleness creeping back

**T2.1 — Saffron intro still promises "which artists are rising."**
Surface: Saffron hero intro (every load). File: `frontend/src/i18n/translations.js:43` (`sf.intro.body`, zh); en at `:2231`.
> "…谁在哪里展出、市场如何流动、哪些艺术家正在崛起。上来吧，我带你看看这片风景。"
Why: "哪些艺术家正在崛起" primes a who's-winning comparison before she scrolls, and over-promises a Landscape feature that was cut. (Handoff lists this as PENDING Scott's wording — flagging the *emotional* reason to land it.)
Exact fix: the already-proposed reword — drop the rising-artists clause: "你好，我是山楂。我留意你作品的大局——你身处何处、已经建起了什么、以及下一扇值得推开的门。上来吧，我带你看看这片风景。"

**T2.2 — Brittle hard-coded Instagram number as a marker.**
Surface: Career Position, top-of-section markers. Files: `SaffronPage.jsx:491` (`igStr = ig?.followers || '27k'`) and `:497` (renders `current: igStr` via `MilestoneMarker`). Live API returns the fixed string `"27k"`.
Why: the standing bar says never a brittle number — and the soft audience fact "稳固且持续增长的 Instagram 受众" (`translations.js:391`) already sits in the same section, so the raw "27k" is redundant *and* off-principle (and already stale vs her real count).
Exact fix: drop the IG marker from the `markers` array (keep the shows=12 and publications count markers, which are honest facts); let the audience fact be the only Instagram statement.

**T2.3 — Benchmarks subtitle says "side-by-side comparison" on a favorable-only section.**
Surface: Career Benchmarks, expanded subtitle. File: `frontend/src/i18n/translations.js:297` (`sf.sub.benchmarks`, zh).
> "你与同阶段艺术家的横向比较。"
Why: the section only ever shows dimensions where she's at/above the band (guarded at `SaffronPage.jsx:713`), and the collapsed summary is already kind — but "横向比较" promises a neutral/possibly-unfavorable comparison, the opposite of the design.
Exact fix: zh → "在同阶段的艺术家中，你已经达到或领先的那些方面。" (mirror en `sf.cr.peerStrengths` intent).

**T2.4 — Momentum subtitle is clinical + faintly surveillant.**
Surface: Career Momentum expanded subtitle. File: `frontend/src/i18n/translations.js:320` (`sf.sub.momentum`, zh).
> "提交记录、场馆联系与响应率 — 基于真实数据自动更新。"
Why: "响应率" (response *rate*) invites a quantified-rejection read, and "自动更新 / 基于真实数据" leans system-is-watching — both contradict the gentle collapsed summary "随你记录而更新." (The component shows a response *count*, not a rate, so "响应率" isn't even accurate.)
Exact fix: match the summary's register: "你记录下来的投递、场馆联系与回复——随你记录而更新。" Drop "响应率" and "自动".

---

## TIER 3 — warmer-word nits

**T3.1 — Venue Tracker summary advertises "0 active relationships."**
File: `frontend/src/i18n/translations.js:315` (`sf.sum.venues`): "已追踪{n}个场地 · {active}个活跃关系" → live renders "已追踪52个场地 · 0个活跃关系". The "0个活跃关系" is a mild deflater. Fix: only append the active clause when `active > 0`; otherwise just "已追踪52个场地".

**T3.2 — Peppercorn dismissal banner switches to formal "您".**
File: `frontend/src/i18n/translations.js:1036` (`pp.dismissal.text`): "您已跳过了{n}个{cat}机会。要减少此类推荐吗？" Everywhere else Peppercorn uses intimate "你"; the lone "您" reads cooler/more transactional. Fix: 您→你.

**T3.3 — Peppercorn carousel reintroduces a faint completion-quota.**
File: `frontend/src/components/PeppercornPage.jsx:1707–1709` — the questions card shows `current: "${answeredCount}/8"` with a fill `ratio: answeredCount / 8`; goals card shows a `/3` ratio. Optional inputs rendered as a progress-to-N bar nudge toward "complete the set." Fix: drop the `/8` denominator and the ratio fill on these cards (keep them as soft, no-target prompts); a count with no goalpost is plenty.

**T3.4 — Carousel "incomplete basis" wording leans deficit.**
File: `frontend/src/i18n/translations.js:710` (`pp.carousel.qs.desc.0`): "山楂目前的分析依据不完整." Reads as "you haven't given enough." The en ("Saffron is working with incomplete context") is softer. Fix: zh → "多说一点，山楂就更懂你" (framing it as a gift she can give, not a gap she left).

---

## What's genuinely good (do not touch)
- `CAREER_SYNOPSIS` (`SaffronPage.jsx:472`) — doors-not-deficits, "growth is depth not more credits." Gold-standard.
- Collaboration Map / Collector Ecosystem / Press Kit (`saffron_insights.js:901 / 1071 / 1159`) are warm, optional, and concrete; the Press Kit is explicitly framed as doable, not homework ("It's just a small folder you build once… Copy what's useful; change anything that doesn't sound like you"). These are frontend constants, so unlike the peers, they ARE live.
- Career Benchmarks favorable-only guard (`SaffronPage.jsx:713`) holds; the deleted peer-timeline stays deleted.
- LongTermScenarios already retired red and relabels by fit ("最契合/契合/可选"), no dream gets a red tag.
- Peppercorn reorder (statement → preferences → goals → questions → logs, `PeppercornPage.jsx:1749`) is correct and kindly reasoned; the intro ("这里没有急事，我会记住一切") is one of the warmest lines on the site.

*No code edited, nothing deployed or committed.*
