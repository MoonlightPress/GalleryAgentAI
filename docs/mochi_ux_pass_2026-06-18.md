# Mochi UX Pass - 2026-06-18

## Scope

This pass targets the current Mochi app: `frontend2` plus `api.py`, launched by
`start_mochi_v2.bat`. The legacy Streamlit `app.py` was not changed.

## Intent

- Treat the three focus cards as a starting point, not the whole answer.
- Make scrolling through the full opportunity set feel expected.
- Let the artist tell Mochi what is not interesting without exposing matching,
  verification, or ranking plumbing.
- Surface freshness only as a quiet "updated ..." note.

## Changes

- Added a local Node test script in `frontend2/package.json` using `node --test`.
- Added `feedbackBehavior.js` with tested rules for feedback toasts and hiding
  `not_for_me` cards from the visible board.
- Added `freshness.js` with tested formatting for quiet update labels such as
  `today`, `yesterday`, `3 days ago`, and `May 1`.
- Updated the Hunt Board copy and summary:
  - today's three are described as the first three;
  - the board tells her to scroll the full set;
  - the board shows `Showing X of Y`;
  - hidden items are counted only after she marks something not for her.
- Updated card feedback:
  - feedback controls are labeled `Teach Mochi`;
  - all positive feedback actions produce a confirmation toast;
  - `Not for Me` still removes the card from the current board view.
- Added `data_updated_at` to `/api/opportunities`, derived from
  `deploy_data/compact_opportunities.json` file mtime.
- Updated the persistent status strip to render that timestamp as unobtrusive
  human language, for example `updated today`.

## Artist-facing boundaries

The pass intentionally does not show confidence scores, verification state,
ranking buckets, source health, or backend collection details. The only trust
signal added is freshness, phrased as a small status note.

## Verification

- `npm.cmd test` passes.
- `npm.cmd run build` passes.
- `npm.cmd run lint` still fails on pre-existing project lint issues outside
  this pass, plus existing fast-refresh complaints about files that already
  export non-components.
