# UX + persona pass — 2026-06-25 (Claude)

Persona lens: **GEGYjiji** — 26, Chinese, watercolor artist, highly driven, easily
emotionally overwhelmed, reads Chinese, lives on mobile. The question through the
whole pass: *does this surface calm her and point at one clear move, or does it
pile possibility on her until she closes the tab?*

This was run live (Vite dev + restarted API), walking every Saffron tab plus the
Mochi Discover page at 390px mobile and desktop, with a programmatic English-leak
sweep of the zh view on each tab.

---

## Fixed this session (shipped)

1. **Career Readiness reframed** (the big one). It opened as a wall of gaps + four
   tier bars — i.e. "here is everything you are missing." It now leads with an
   earned **Level badge** and the foundation she's already built, shows **one**
   next-unlock with the action inline, collapses the rest, and celebrates real
   level crossings. This is the single biggest emotional-load change: the page
   now answers "where am I / what's the one next thing," not "how far behind am I."

2. **Profile tab — peer comparison collapsed by default.** The tab opened with
   three peer-COMPARISON sections fully expanded (Benchmarks, Career Timeline vs
   peers, Comparable Artists). For a driven, easily-overwhelmed person that's the
   "everyone's ahead of me" spike, served first. Those three now default to a
   one-line summary (one tap to open); the affirming sections (Readiness, her
   Record, Instagram strength) stay open. **Reversible — please sanity-check the
   call.**

3. **zh leak sweep.** Per-tab scan for English sentences in the 中文 view. Result
   is much healthier than the handoff implied — money/strategy/landscape/profile
   are clean (only proper nouns: grant names, publisher names, opportunity titles,
   which are correct to leave). The one real leak: the **Press & Pitch** `contact`
   lines ("Via WeChat official accounts or Weibo DM.", "Via pen-online.jp contact
   form…") rendered raw. Routed through `locF` + added `contact_zh`. Now clean.

4. **Dead counts now click through.** Market-Stats category counts and
   Market-Landscape actionability counts ("Immediate Best Moves: N") were inert
   numbers. They're now buttons that jump to the Discover list.

---

## Findings worth your call (NOT yet changed)

- **Endurance scroll, the other tabs.** The profile-tab collapse helps a lot, but
  Landscape / Strategy / Money each still open with 4–5 dense sections fully
  expanded. Recommendation: extend the same "first section open, rest collapsed to
  summary" default across all Saffron tabs, for consistency and calm. I held off
  because it's a broader layout decision that's yours to make — but the
  inconsistency (profile collapsed, others not) is itself a small wart, so it's
  worth deciding one way or the other.

- **Mochi card density.** Today's Focus / opportunity cards carry a full paragraph
  of body text. For this persona a tighter card (one-line "why it fits" +
  expand-for-detail) would lower the load on the busiest surface. Matches the
  earlier Codex persona note ("accumulated possibility is the emotional-load
  risk").

- **Mobile StatusBar overflow** (pre-existing, known): at 390px the StatusBar
  still expands the document width. Untouched — out of scope this pass, flagging
  for continuity.

- **Proper-noun English in the zh view is fine.** Opportunity names, venue names,
  grant/publisher names render in their real language by design — she searches by
  the real name. The leak detector correctly ignores these; don't "fix" them.

## Net read

The reframe + the profile-tab calming move address the core of what you flagged:
the site had drifted toward "comprehensive" when this user needs "one clear next
step, and proof she's already moving." The bones are good; the remaining lever is
density discipline on the other tabs and on the Mochi cards.
