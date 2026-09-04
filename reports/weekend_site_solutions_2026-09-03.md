# Weekend Site Solutions — Saffron's career narrative (2026-09-03)

Research only, no code changed. Follow-up to `reports/weekend_site_review_2026-09-03.md`.
Everything below was checked against the working tree tonight: `frontend/src/components/SaffronPage.jsx`,
`api.py` (`/api/saffron`, `/api/career_strategy`), `engines/career_strategy_engine.py`,
`memory/career_strategy_report.json`, `frontend/src/components/TrackedSection.jsx`.

One caveat up front: the usage numbers in the prior report come from the server's log. The local
`memory/usage_events.jsonl` holds 101 localhost events, so I could not re-derive her dwell times.
I verified what the instrumentation *can* say (section 1c) and focused the rest on code.

---

## 1. Verdict on the redundancy claim

**Agree that the redundancy is real. It is wider than the prior report described, and it lives at
the sentence level, not the component level.** Three specific pushbacks follow.

### 1a. The three components have distinct jobs — the leak is that each one also narrates the future

| Component | Its actual job | Where it leaks into "where is this going" |
|---|---|---|
| `CareerPosition` (L517) | **The record.** Exhibitions, publications, audience — past tense, confirmed facts. Subtitle literally says "confirmed facts only." | `CAREER_SYNOPSIS` (L506) ends with a forward paragraph: "From here it's less about adding credits… gallery relationships, a representation conversation…" |
| `CareerReadiness` (L2194) | **The one next step**, plus opportunities matched to her readiness. | `careerStatusLine` (L2118) closes with "The direction from here is gallery relationships and representation" — then the `next_unlock` card directly beneath it says the same thing at paragraph length. |
| `LongTermScenarios` (L1212) | **The choice** — gallery vs. book vs. both, explicitly "yours to decide" (`saffron_view`, `api.py` L2807). | Gallery Track's `bottleneck` is `_solo_bottleneck` (`api.py` L2417): "The next barrier is structural… gallery representation, stronger solo venues…" — a third restatement. |

Past / present / future is a sound split. So the fix is to make each stay in its lane, which is
cheaper and safer than merging them. I would push back on any plan that collapses these into one
block: the record and the choice are genuinely different kinds of content, and the choice is the one
thing keeping Saffron from reading as a single-track push toward representation (Scott's 2026-06-25
note in `api.py` L2748: "the app never assumes either is the goal").

### 1b. The biggest duplicate is on the *other* tab, and it is what she sees first

`SaffronPage` initialises `tab = 'strategy'` (L2327). The default-open first section on Saffron is
therefore **`StrategicPathway`** (L684), not `CareerReadiness`. Pathway already carries the full
forward narrative from live evidence flags: goal, an 8-step ladder with done/blocking markers,
"What's blocking now", "Next move", and ShyTips. Its step-6 detail (`api.py` L2225) and
`CareerReadiness`'s `next_unlock.detail` (`career_strategy_report.json` → `level.next_unlock`) are
near-verbatim:

> Pathway: "A gallery that sells on your behalf, places you in fairs, and builds collectors — the biggest structural step available now, growing from the shows you already have."
> Readiness: "…a gallery that represents you: one that sells on your behalf, places you in art fairs… This is the most important step at this stage."

Below Pathway sits `CareerDependencyMap` ("Career Unlock Tree", L1639), a **fully static** constant
in `frontend/src/data/saffron_insights.js` L488 that restates Pathway's ladder in "completes / unlocks"
form. The `CareerReadiness` comments (L2160, L2225) record that "level up / unlock a tier" framing was
deliberately retired — yet a section titled "Unlock Tree" survives one tab over.

Counting every surface, the single engine fact `has_representation == False` is rendered as prose
in about twelve places: `pathway.goal`, step 6, `blocking_now`, `next_move`, Scenario 1's description
+ `requires_now[0]` + `bottleneck`, Unlock Tree's first item, `careerStatusLine`, `next_unlock`,
`CAREER_SYNOPSIS`, plus `next_milestone` / `phase_note` in the report JSON (not rendered, but ready).
That is the redundancy. It is one conclusion in many voices, across five sections and two tabs.

### 1c. The usage reading needs a correction, and the synopsis "fix" did not land

- **`TrackedSection` fires on visibility, not on opening.** It posts a `nav` event when the wrapped
  block fills half the screen *or half of itself* for 2s (`TrackedSection.jsx` L14–17, L30–42). A
  collapsed `SectionShell` is just its header, so scrolling past the closed "Long-term Scenarios"
  header for two seconds fires the same event as reading it. Saffron's `SectionShell` toggle
  (L433) fires nothing; only `goTab` tracks (L2376). Peppercorn does track opens
  (`dfc7f011`); Saffron never got that. So "6s on long_term_scenarios" most plausibly measures how
  fast she scrolled from that header to the Unlock Tree header directly below it. There is no
  evidence in the instrumentation that she has ever opened Scenarios, and none that she hasn't.
  The prior report's "she's opened it more than once" cannot be supported by these events.
- **`CAREER_SYNOPSIS` is still hardcoded.** `git status` shows `SaffronPage.jsx` clean, the
  constant is unchanged since `26634c65` (2026-06-26), and there are no commits since Sep 2. The
  prior report's "flagged and fixed earlier this session — now generated from live data" is not
  true of the working tree. `artist_master_profile.json` *is* dirty (the two hand-added shows), so
  the counts and lists under the synopsis are live; the paragraph above them is not. A live
  replacement already exists twice over: `careerStatusLine` (trilingual, built from
  `career_evidence`) and the engine's `phase_note` / `phase_note_zh`.

---

## 2. Approaches

Design constraints held throughout: warm narrative, no scores or percentages shown to her, nothing
she can currently see loses its home, and the Unlock-Tree-style "levels" language stays retired.

### Approach A — Stay in your lane (edit-level, one evening)

Keep every section; delete the sentences that cross lanes.

- `CareerPosition`: replace `CAREER_SYNOPSIS` with the live `careerStatusLine` **minus its closing
  clause**. Delete the constant.
- `CareerReadiness`: drop the closing clause from `careerStatusLine` (the `next_unlock` card says it).
- `LongTermScenarios`: Gallery Track `bottleneck` becomes a short, track-specific line (e.g. which
  kind of gallery fits) instead of `_solo_bottleneck`.
- Either Pathway's "Next move" callout or Readiness's next-step card goes; I'd keep Pathway's.

Trade-offs: cheapest, zero layout risk. Leaves five sections across two tabs telling one story, and
leaves the Unlock Tree. She still has to synthesise Pathway vs. Readiness herself.

### Approach B — Past / present / future, one owner each (recommended)

Give each tab one tense and each section one job. Nothing new is built; content moves and shrinks.

**Strategy tab (future) — "where it's going"**
1. `StrategicPathway` — unchanged; **it owns the next step** (blocking_now, next_move, ShyTips).
   Default open, as now.
2. `LongTermScenarios` — unchanged content except the Gallery Track bottleneck trimmed as in A.
   Fix the collapsed summary: `3 paths · The next few years` says nothing; make the header do the
   inviting, e.g. "Gallery · Book · Both — yours to choose" (zh/ja copy is Scott's call). Given 1c,
   the header is likely all she has seen of it.
3. `CareerDependencyMap` — **cut.** Static, a third copy of Pathway's ladder, and the framing the
   project already retired. Its only non-duplicate content (the "unlocks" phrasing) is a
   consequence, not a fact; nothing on it needs a new home.

**Profile tab (present) — "where you are"**
1. `CareerPosition` → **default open, first**, and it absorbs the gaps. The synopsis becomes the
   live factual line (`careerStatusLine` without its closing clause). Below the ✓ exhibitions /
   publications / audience rows, add the `blocking_gaps` as ○ "not yet on record" rows, each keeping
   its `action` line and its `GapCorrectionForm` ("I already did this"). The record and what is
   missing from it are one list; the first ○ row *is* the next step, stated as a fact about her
   record rather than as advice. `ReadinessCorrection` moves here too.
2. `CareerReadiness` → shrinks to a small collapsed section, working title **"Within reach"**
   (触手可及 / 手の届くところ): the "Getting closer" and "Keep an eye on" columns only. The "Now"
   column is Mochi's job (tier 1–2 items already surface in Today's Focus / Immediate Best Moves;
   CLAUDE.md: Saffron describes, does not advise). `CadenceTip` folds under the Audience row in
   Position. The status line and next-step card are deleted here because Position and Pathway now
   hold them.
3. Benchmarks / Peers / Momentum — unchanged.

**Where every currently visible field ends up**

| Currently shown | Home under B |
|---|---|
| `CAREER_SYNOPSIS` | Replaced by live factual line in Position (constant deleted) |
| `careerStatusLine` closing clause | Gone — Pathway `next_move` is the one copy |
| `next_unlock` card + form | Position ○ rows (first row) + `GapCorrectionForm` |
| other `blocking_gaps` + "N more" toggle | Position ○ rows (can keep the toggle for rows 2+) |
| `immediate_priorities` ("Now") | Mochi's page (already there); stays in report JSON for engines |
| `build_toward`, `watch_list` | "Within reach" |
| `CadenceTip` | Under Audience in Position |
| Unlock Tree | Cut |
| Scenarios × 3, `saffron_view` | Unchanged, strategy tab |

**Trade-offs.** Moderate edit of three components and one tab layout; the i18n keys for the new
section title need zh/ja. The profile tab no longer contains a paragraph of advice, which I think
is the point: the record implies the step, Pathway states it once. Risk to watch: the ○ rows must
read as warm ("not yet on record", `○`), never as a deficit list — the `priority` colour dots should
stay muted and there should be no count of open gaps in the collapsed summary.

**Interaction with the untracked, first-position block.** Under B the first-open section on the
profile tab is `CareerPosition`, which is already wrapped in `TrackedSection`. The blind spot the
prior report worried about closes as a side effect. Pathway on the strategy tab remains untracked;
see 3a.

### Approach C — Scenarios become a Peppercorn question (follow-on, after B)

The strongest reframe of the weakest component: "which of these three feels like you?" is a
question to her, and questions are Peppercorn's job. Recording her answer in
`peppercorn_profile.json` would let the scoring engine lean toward publication or gallery
opportunities on her say-so instead of the app hedging in prose. It is a new feature (question,
storage, engine hook), so it sits outside the consolidation posture for this weekend. Worth a line
in the backlog; do not cut Scenarios from Saffron until this exists.

### Recommendation

**B**, with A's sentence edits as its first commit (they are a strict subset). If time runs short,
land A plus the Unlock Tree cut and stop; that alone removes the two worst duplicates.

---

## 3. Two things from the original report that deserve a concrete fix

### 3a. Saffron's instrumentation cannot answer the question the review asked

Two small changes, each a few lines, so next month's review is not guessing:
- Fire a `nav` event from `SectionShell`'s toggle when a section is **opened** on Saffron
  (page `observe`, the same pattern Peppercorn's `toggleSection` uses). Opening is the only
  behaviour that distinguishes "read it" from "scrolled past it."
- Wrap the default-open first sections (`StrategicPathway`, and whichever leads the profile tab)
  in `TrackedSection` so the most-seen blocks stop being the least-measured.
Add `pathway` and the new section key to `SECTION_LABELS` in `engines/visit_tracking.py`.

### 3b. The empty exhibition log, seen from Career Position

I agree with the prior report that `exhibition_log.json` being `[]` is the most consequential
finding. One proposal, small enough for the weekend: Career Position is where she looks at her own
record (the section with the most sustained Saffron engagement in the prior numbers), so it is where
she would notice a show missing. Under B the ✓ rows are already sitting next to ○ rows with an
"I already did this" form; an "add a show" affordance at the foot of the exhibitions list, posting
to the same endpoint Peppercorn's `ExhibitionLogSection` uses, puts the logging action at the moment
of noticing rather than one collapsed section among eight on a page she does not save from. The
`from_log: true` flag and title-dedup in `api.py` L1922–2029 already handle the merge.
