# Weekend Site Review — 2026-09-03

Research only, no code changed. Prepared for Scott's Saturday planning session.

**Confidence caveat:** her three confirmed devices (`e89b8a70`, `05754ada`, `fc7eb61e`) show ~10 real
sessions across 9 distinct days (Jul 3, 4, 5, 9, 15; Aug 19, 20, 27 ×2; Sep 1). Small sample —
read the rankings below as directional, not statistical. I didn't have time to fully audit
`OpportunitiesSection.jsx`, `RelationshipTargets.jsx`, `DeadlineCalendar.jsx`, or Saffron's
`calendar`/`relationships`/`money` tabs — flagged where relevant, not covered in depth here.

## 1. Priority candidates from usage

Total engaged time per page (sum of inter-event gaps, capped at 90s/step to avoid inter-session
noise, across her confirmed sessions):

| Page | Total engaged time |
|---|---|
| discover (Mochi) | ~399s |
| refine (Peppercorn) | ~292s |
| observe (Saffron) | ~148s |

Top sections by the same method:

| Section | Time |
|---|---|
| discover/today_focus | 111s |
| discover/open_calls | 41s |
| observe/career_position | 25s |
| discover/people | 23s |
| observe/profile | 19s |
| refine/saffron-questions | 17s |
| discover/tracker | 14s |
| observe/strategy (tab switch) | 8s |
| refine/venue-log | 7s |
| observe/long_term_scenarios | 6s |
| observe/career_unlock_tree | 5s |

Ranked candidates for weekend attention:

1. **today_focus** — most engaged section by a wide margin. Already well-built (see §2). Protect,
   don't restructure.
2. **Peppercorn's saffron-questions + venue-log** — second-highest total page time of anywhere on
   the site, but a completion dead end: real reading, zero saves, ever, on any device. Highest
   leverage gap on the whole site (see §4).
3. **Saffron career_position/profile** — moderate, sustained engagement on content she had to
   actively expand (see §2 — it's collapsed by default). Worth the depth investment you were
   already planning.
4. **Saffron long_term_scenarios** — lowest engagement of anything she's actually opened. See §5.

## 2. Persona findings

### Mochi (discover)
**TodaysFocus** is the strongest-built piece of the site: exactly-3 discipline, role badges
(quick win / high impact / stretch), urgency-aware ordering, truncated summaries, a real detail
panel. It matches CLAUDE.md's design philosophy precisely and it's also the most-used surface.
Usage and quality agree here — nothing to fix, protect it from scope creep.

### Peppercorn (refine)
More built-out than the "missing feedback loop" framing suggests: ArtistStatement, SaffronQuestions,
CareerGoals, Preferences, SubmissionLog, **ExhibitionLog**, VenueLog, Contacts — a real CRM-adjacent
feature set.

**The single most consequential finding of this review:** `ExhibitionLogSection` is a working,
real self-service feature for her to log her own shows. `memory/exhibition_log.json` is `[]` —
completely empty. She has never used it. Her actual exhibition record (13 entries as of tonight,
including the two shows Scott just hand-added) lives entirely in `artist_master_profile.json`,
populated by research and manual entry — never by her. If she'd used this feature even once, the
manual profile patch that happened earlier tonight wouldn't have been necessary, and her career
page would already reflect her current Harajuku show without anyone telling the system by hand.
This is worth surfacing to her more directly than it currently is (it's one collapsed section
among eight on a page she doesn't save from).

### Saffron (observe)
- **CareerPosition**: synopsis is well-written but was hardcoded/static (flagged and fixed
  earlier this session — now generated from live data).
- **CareerReadiness**: this is the FIRST section shown in the default-open `profile` tab — it
  renders *before* CareerPosition, which is itself collapsed by default. Yet CareerReadiness has
  no `TrackedSection` wrapper at all. It's very likely the single most-seen piece of Saffron
  (default-open, first in view) and we have zero behavioral data on it. That's a bigger
  instrumentation blind spot than long_term_scenarios's low dwell time — see §4.
- **LongTermScenarios** ("three possible lives"): collapsed by default; she's opened it more than
  once but spends less time there than in profile/career_position even after opening it. See §5.
- money/calendar/relationships tabs: not audited this pass.

## 3. Where usage and persona judgment agree
- **today_focus**: most-used and best-built. No changes needed.
- **career_position/profile**: moderate, real engagement on genuinely substantive content (once
  the synopsis fix lands). Matches the investment you were already planning.

## 4. Where usage contradicts persona judgment
- **Peppercorn getting the second-most total engaged time on the site is surprising.** Project
  memory frames it as "the missing feedback loop she bounces off unanswered." The data says she
  reads a real amount there — she just never clicks save, on any device, ever. That reframes the
  problem: it's not an attention problem, it's a **completion-funnel** problem. Worth designing
  for "lower the activation energy to save" rather than "get her to look at this at all."
- **CareerReadiness's silence in the logs is not evidence she skips it** — it's the one
  default-open section with no tracking, positioned first. Don't read "no data" as "no interest."

## 5. Is Scott right that long_term_scenarios is the weakest?

Partially. It genuinely gets the least sustained attention of anything she's opened in Saffron —
but that's not obviously a design-quality problem. Each scenario card actually carries *more*
structured information than CareerPosition's checklist (name, tagline, fit label, description,
requires-now list, bottleneck, "right if" signal — 7 pieces × 3 cards). The likely cause is
cognitive load and redundancy, not weak writing: it's collapsed by default, sits below
StrategicPathway, and partially overlaps with CareerReadiness's simpler `next_milestone`
framing directly above it in the other tab. Three different components are all trying to answer
"where is this going," at three different levels of density.

**What would make it better:** less about deepening the content and more about resolving the
overlap — decide which ONE surface owns "here's your future direction" (my vote: CareerReadiness's
single next-step framing for the near-term, LongTermScenarios for the genuinely long-horizon
branching paths only), and cut what the other duplicates. Right now she's being asked to
synthesize three overlapping career narratives herself.
