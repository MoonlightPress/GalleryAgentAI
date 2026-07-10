# Peppercorn — One-Tap Answers for Saffron's Questions

**Date:** 2026-07-10
**Status:** Design, approved pending spec review

## The problem

She arrives at Peppercorn's "Notes from Saffron" section and leaves without
answering. On 2026-07-07 she spent 11 seconds on it; on 2026-07-09 she opened
Mochi and went *straight past Today's Focus* to it within 6 seconds. She has
never once saved an answer — the `saffron_answer` tracking action has never
fired from her devices.

The tempting reading is that the questions ask too much of her. The evidence
points somewhere more mundane first.

Suggested answers **already exist** — four per question, written in English,
Japanese and Chinese (`pp.q.<i>.opt.<j>`). But `.pp-q-option` carries exactly
one interactive style: `:hover`. **Phones do not hover.** Tapping a chip on her
iPhone changes nothing about the chip. It silently fills a `<textarea>` below,
and she must then find and tap "Save answer", which stays disabled until that
textarea has content. The placeholder reads *"Your answer — or pick one
above…"*, framing the chips as a shortcut to writing prose rather than as an
answer in themselves.

The most likely story is not that she couldn't bring herself to answer. It is
that **she tapped one and nothing appeared to happen.**

## Goal

One tap answers a question. Nothing about the exchange should feel like
homework, and nothing should be unrecoverable.

## Non-goals

- Rewriting what the questions ask, or their copy.
- Changing any other Peppercorn section.
- Uncollapsing the section by default. She finds it on her own; we are already
  changing four things at once, and adding a fifth would make the result
  unreadable. Ship, then observe. (Scott, 2026-07-10: "she keeps looking at it.
  let's try it and see")

## Design

### Interaction

Tapping a chip answers the question:

1. The chip fills and shows a check (`aria-pressed`, plus a real `:active`
   touch state — the CSS gap that likely caused all of this).
2. The answer saves immediately.
3. The card advances to the next unanswered question.

The `<textarea>` collapses behind a quiet **"✎ say it in your own words"**
link. It remains fully available; it is no longer the default demand. Its
placeholder drops "or pick one above" — the chips are the answer now.

### Undo

Answered questions reorder to the back of the dot strip **immediately**, as she
answers (Scott's call). That means the strip moves under her finger, so a
mis-tap must be trivially recoverable. After each answer, one line appears
beneath the strip for ~5 seconds:

```
Saved "Mix of Tokyo-based and Chinese-speaking followers" · Undo
```

Undo restores the previous value **and returns the question to its original
slot**. Tapping any answered dot reopens that question with its chip selected;
choosing a different chip replaces the answer. The existing "clear answer"
button still works and returns the question to the unanswered group.

### Answers must stay changeable once all are answered

The current component renders `allAnswered ? <done note> : <dots + card>`. Once
the eighth question is answered the dots and the card **disappear entirely**,
and there is no way to revisit or change anything. That directly defeats the
requirement (Scott, 2026-07-10: "make sure it's possible to change the
answers").

Fix: when `allAnswered`, keep the dot strip and the question card mounted, with
the done note above them. Every dot is filled; tapping one reopens its question
for editing. The done note becomes the header for a reviewable list rather than
a replacement for it.

### Ordering — `frontend/src/utils/questionOrder.js` (new, pure)

React components should not own this logic. Two exported functions, no React,
no DOM:

- `orderQuestions(questions, answers, answerSequence)` → unanswered questions in
  their original order, followed by answered ones in the order she answered
  them.
- `nextUnansweredIndex(orderedQuestions, answers, fromIndex)` → the index to
  advance to, or `-1` when everything is answered.

`answerSequence` is an array of keys in answer order, held in component state.
Undo pops the key and restores the prior answer value, which restores position
for free.

### Save path

Switch the answer write to **`POST /api/saffron_answer`** with `{key, value}`.
This endpoint already exists, writes a single field to
`peppercorn_profile.json`, and **does not spawn a draft regeneration.**

The current code posts the entire profile to `/api/peppercorn`, whose handler
calls `apply_peppercorn_edits` and can fire `spawn_draft_regen`. Under one-tap
answering that path would run on every tap. `saveProfile` stays as-is for the
rest of the page.

Each tap continues to fire the existing `saffron_answer` tracking action, so the
Discord feed will show which question she answered.

### Copy and i18n

New strings — the undo line, "say it in your own words", the revised
placeholder, "tap to change" — need **English, Japanese and Chinese**. Chinese
is where i18n leaks have bitten repeatedly; verify against the rendered page,
not just the presence of a `_zh` key.

Tone follows Peppercorn: quiet, small, never nagging. No "Complete your
profile!" No progress-bar guilt. Per `feedback_no_negative_framing`, state what
a thing is, never what it isn't.

## Testing

Unit tests (`node --test`) for `questionOrder.js`:

- unanswered stay in original order; answered append in answer order
- `nextUnansweredIndex` advances correctly, returns `-1` when all answered
- undo restores both the prior value **and** the original slot
- a question answered, undone, and re-answered lands in the right place
- degenerate input: empty questions, all answered, unknown key

Component-level checks by inspection (no DOM harness in this repo): chip shows a
selected state; textarea starts collapsed; a tap issues exactly one
`/api/saffron_answer` request and no `/api/peppercorn` request.

Manual: drive the real page, tap a chip, confirm the network panel shows the
cheap endpoint and that the answer survives a reload.

## How we will know it worked

`saffron_answer` has never fired from her devices. If it fires at all after
this ships, the CSS hover bug was the cause. If she still doesn't answer, the
hesitation is about the questions — or about what answering them means — and
that is a different problem, not a UI one.

## Risks

- **Accidental answers.** One tap commits. Mitigated by undo, by the editable
  answered dots, and by "clear answer".
- **Reshuffle disorientation.** Accepted deliberately; undo is the mitigation.
- **The premise could be wrong.** If she tapped a chip, saw the textarea fill,
  and *still* declined to press Save, then the friction was never the chip.
  Shipping this is also the cheapest way to find that out.
