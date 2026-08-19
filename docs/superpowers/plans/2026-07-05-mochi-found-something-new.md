# Mochi Found Something New Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Surface a "Mochi found something new" notice when the pipeline adds opportunities, using the `imported_at` date opportunities already carry — a count banner (dismissable) in `StatusBar`, plus a passive "New" badge on individual `OppCard`s.

**Architecture:** A pure backend helper (`is_new_opportunity`) computes a stateless `is_new` boolean per opportunity from its existing `imported_at` field, served by `/api/opportunities`. `OppCard` reads `is_new` directly (no dismiss logic — same on every device). `StatusBar` layers a per-device dismiss on top via `localStorage`, using two small pure frontend helpers that are unit-tested independently of any component/DOM harness (this repo has none).

**Tech Stack:** Python/FastAPI backend (`api.py`), plain-function `engines/` pattern for the helper, React frontend, Python `pytest`/`unittest`, Node's built-in test runner (`node --test`).

## Global Constraints

- `is_new_opportunity()` never raises — malformed/missing `imported_at` degrades to `False` (existing project posture: best-effort, never fail the page over a data quirk).
- `NEW_WINDOW_DAYS = 7` — matches the ~monthly pipeline cadence.
- No new pipeline step, no `date_discovered` field, no diff/delta engine — `imported_at` is sufficient (per spec Non-Goals).
- No cross-device dismiss sync — `localStorage` only, per spec.
- The per-card badge never depends on dismissal — it always reflects `is_new` directly, on every device.

---

## Task 1: Backend — `is_new_opportunity()` + wire into `shape_card()`

**Files:**
- Modify: `api.py:429-431` (add function after `_opp_id`)
- Modify: `api.py:862` (add field to `shape_card()`'s returned dict)
- Test: Create `tests/test_is_new_opportunity.py`

**Interfaces:**
- Produces: `is_new_opportunity(imported_at, now=None, window_days=NEW_WINDOW_DAYS) -> bool`, and every opportunity dict returned by `shape_card()` (and therefore every entry `/api/opportunities` serves) gains an `"is_new"` boolean key. Later tasks (2-4) consume this exact key name from the served JSON.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_is_new_opportunity.py
import unittest
from datetime import datetime, timezone

from api import is_new_opportunity, NEW_WINDOW_DAYS


class IsNewOpportunityTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 7, 5, 12, 0, 0, tzinfo=timezone.utc)

    def test_fresh_date_is_new(self):
        self.assertTrue(is_new_opportunity("2026-07-05", now=self.now))

    def test_eight_days_old_is_not_new(self):
        self.assertFalse(is_new_opportunity("2026-06-27", now=self.now))

    def test_exactly_seven_days_old_is_new(self):
        self.assertTrue(is_new_opportunity("2026-06-28", now=self.now))

    def test_missing_imported_at_is_not_new(self):
        self.assertFalse(is_new_opportunity(None, now=self.now))
        self.assertFalse(is_new_opportunity("", now=self.now))

    def test_malformed_imported_at_is_not_new(self):
        self.assertFalse(is_new_opportunity("not-a-date", now=self.now))
        self.assertFalse(is_new_opportunity("2026-13-99", now=self.now))

    def test_future_date_is_not_new(self):
        # A data glitch (imported_at after "now") must never be flagged new.
        self.assertFalse(is_new_opportunity("2026-07-10", now=self.now))

    def test_default_window_constant_is_seven(self):
        self.assertEqual(NEW_WINDOW_DAYS, 7)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_is_new_opportunity.py -v`
Expected: FAIL — `ImportError: cannot import name 'is_new_opportunity' from 'api'`

- [ ] **Step 3: Add the constant and function**

Insert into `api.py` immediately after `_opp_id()` (currently `api.py:429-431`):

```python
def _opp_id(opp: dict) -> str:
    raw = opp.get("id") or opp.get("title") or opp.get("name") or ""
    return hashlib.md5(raw.encode()).hexdigest()[:12]


NEW_WINDOW_DAYS = 7  # how long an opportunity stays flagged "new" after import


def is_new_opportunity(imported_at, now=None, window_days: int = NEW_WINDOW_DAYS) -> bool:
    """True if imported_at (a "YYYY-MM-DD" string) falls within window_days of
    now (inclusive both ends). Missing/malformed input, or an imported_at in
    the future (a data glitch), degrades to False rather than raising —
    this must never break the opportunities feed over a bad date string."""
    if not imported_at:
        return False
    try:
        imported_date = datetime.strptime(str(imported_at)[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return False
    now = now or datetime.now(timezone.utc)
    delta_days = (now.date() - imported_date).days
    return 0 <= delta_days <= window_days
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_is_new_opportunity.py -v`
Expected: PASS (7 tests)

- [ ] **Step 5: Wire `is_new` into `shape_card()`**

In `shape_card()`, the returned dict currently ends (`api.py:861-867`):

```python
        "closed_this_cycle": opp.get("status") == "closed_this_cycle",
        # Email drafts — prefer per-entry drafts from data, fall back to templates
        "email_zh": opp.get("email_zh") or email_zh(org, category),
        "email_ja": opp.get("email_ja") or email_ja(org, category),
        "email_en": opp.get("email_en") or email_en(org, category),
    }
```

Add `is_new` right after `closed_this_cycle`:

```python
        "closed_this_cycle": opp.get("status") == "closed_this_cycle",
        "is_new":          is_new_opportunity(opp.get("imported_at")),
        # Email drafts — prefer per-entry drafts from data, fall back to templates
        "email_zh": opp.get("email_zh") or email_zh(org, category),
        "email_ja": opp.get("email_ja") or email_ja(org, category),
        "email_en": opp.get("email_en") or email_en(org, category),
    }
```

- [ ] **Step 6: Manually verify the field is served**

Run: `python -c "import api; print(api.shape_card({'title': 'Test', 'imported_at': '2026-07-05'})['is_new'])"`
Expected: `True`

Run: `python -c "import api; print(api.shape_card({'title': 'Test', 'imported_at': '2020-01-01'})['is_new'])"`
Expected: `False`

- [ ] **Step 7: Run the full backend test suite**

Run: `python -m pytest tests/test_is_new_opportunity.py tests/test_visit_tracking.py tests/test_usage_endpoint.py tests/test_geoip.py -v`
Expected: PASS (all)

- [ ] **Step 8: Commit**

```bash
git add api.py tests/test_is_new_opportunity.py
git commit -m "$(cat <<'EOF'
feat: is_new_opportunity flag on served opportunities

Stateless "was this imported in the last 7 days" signal computed from
the existing imported_at field - no new pipeline step needed. Feeds
the "Mochi found something new" banner and per-card badge.
EOF
)"
```

---

## Task 2: Frontend — pure new-opportunities helpers (dismiss/prune logic)

**Files:**
- Create: `frontend/src/utils/newOpportunities.js`
- Test: Create `frontend/src/utils/newOpportunities.test.js`

**Interfaces:**
- Consumes: opportunity objects shaped like Task 1's `shape_card()` output — specifically `{ id: string, is_new: boolean }` fields, grouped in a `sections` object (`{ [sectionKey]: opp[] }`), matching the shape `/api/opportunities` already returns and that `OpportunitiesSection.jsx` already destructures as `const { sections, meta } = data`.
- Produces: `allNewIds(sections) -> Set<string>`, `countUndismissed(sections, dismissedIds) -> number`, `pruneDismissed(sections, dismissedIds) -> Set<string>`. Task 3 imports all three by these exact names.

- [ ] **Step 1: Write the failing tests**

```javascript
// frontend/src/utils/newOpportunities.test.js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { allNewIds, countUndismissed, pruneDismissed } from './newOpportunities.js'

const SECTIONS = {
  open_calls: [
    { id: 'a', is_new: true },
    { id: 'b', is_new: false },
  ],
  zines_and_print: [
    { id: 'c', is_new: true },
  ],
}

test('allNewIds collects is_new ids across every section', () => {
  const ids = allNewIds(SECTIONS)
  assert.deepEqual([...ids].sort(), ['a', 'c'])
})

test('allNewIds ignores items without is_new', () => {
  const ids = allNewIds({ x: [{ id: 'z', is_new: false }] })
  assert.equal(ids.size, 0)
})

test('allNewIds is safe on empty/missing input', () => {
  assert.equal(allNewIds({}).size, 0)
  assert.equal(allNewIds(null).size, 0)
  assert.equal(allNewIds(undefined).size, 0)
})

test('countUndismissed counts new ids not in the dismissed set', () => {
  assert.equal(countUndismissed(SECTIONS, new Set()), 2)
  assert.equal(countUndismissed(SECTIONS, new Set(['a'])), 1)
  assert.equal(countUndismissed(SECTIONS, new Set(['a', 'c'])), 0)
})

test('countUndismissed treats a missing dismissed set as empty', () => {
  assert.equal(countUndismissed(SECTIONS, undefined), 2)
})

test('pruneDismissed drops ids no longer new/present', () => {
  const pruned = pruneDismissed(SECTIONS, new Set(['a', 'stale-id']))
  assert.deepEqual([...pruned], ['a'])
})

test('pruneDismissed is safe on empty/missing input', () => {
  assert.equal(pruneDismissed(SECTIONS, new Set()).size, 0)
  assert.equal(pruneDismissed(SECTIONS, undefined).size, 0)
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd frontend && node --test src/utils/newOpportunities.test.js`
Expected: FAIL — cannot find module `./newOpportunities.js`

- [ ] **Step 3: Write the implementation**

```javascript
// frontend/src/utils/newOpportunities.js
// Pure helpers backing the "Mochi found something new" banner. The is_new
// flag itself (from /api/opportunities) is stateless and identical on every
// device; only the banner's dismissal is per-device, tracked here.

// Every opportunity id currently flagged is_new, across all sections.
export function allNewIds(sections) {
  const ids = new Set()
  for (const items of Object.values(sections || {})) {
    for (const opp of items || []) {
      if (opp && opp.is_new && opp.id) ids.add(opp.id)
    }
  }
  return ids
}

// How many new ids haven't been dismissed yet.
export function countUndismissed(sections, dismissedIds) {
  const dismissed = dismissedIds || new Set()
  let count = 0
  for (const id of allNewIds(sections)) {
    if (!dismissed.has(id)) count++
  }
  return count
}

// Drop dismissed ids that are no longer actually new (aged out of the
// window, or gone from the feed) - keeps localStorage small and
// self-cleaning instead of growing forever.
export function pruneDismissed(sections, dismissedIds) {
  const current = allNewIds(sections)
  const pruned = new Set()
  for (const id of (dismissedIds || [])) {
    if (current.has(id)) pruned.add(id)
  }
  return pruned
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd frontend && node --test src/utils/newOpportunities.test.js`
Expected: PASS (7 tests)

- [ ] **Step 5: Run the full frontend test suite**

Run: `cd frontend && npm test`
Expected: PASS (all, including the 7 new tests — total will be existing count + 7)

- [ ] **Step 6: Commit**

```bash
git add frontend/src/utils/newOpportunities.js frontend/src/utils/newOpportunities.test.js
git commit -m "feat: pure helpers for new-opportunity dismiss tracking"
```

---

## Task 3: Frontend — StatusBar banner + dismiss

**Files:**
- Modify: `frontend/src/components/StatusBar.jsx` (full rewrite — currently 8 lines)
- Modify: `frontend/src/components/StatusBar.css` (append)

**Interfaces:**
- Consumes: `getCache`/`setCache` from `frontend/src/utils/apiCache.js` (existing, unchanged: `getCache(url)`, `setCache(url, val)`); `allNewIds`, `countUndismissed`, `pruneDismissed` from Task 2 (`frontend/src/utils/newOpportunities.js`).

- [ ] **Step 1: Replace `StatusBar.jsx`**

```jsx
import { useEffect, useState } from 'react'
import './StatusBar.css'
import { getCache, setCache } from '../utils/apiCache'
import { allNewIds, countUndismissed, pruneDismissed } from '../utils/newOpportunities'

const DISMISSED_KEY = 'mochi_new_dismissed'

function readDismissed() {
  try {
    const raw = localStorage.getItem(DISMISSED_KEY)
    return raw ? new Set(JSON.parse(raw)) : new Set()
  } catch {
    return new Set()
  }
}

function writeDismissed(ids) {
  try {
    localStorage.setItem(DISMISSED_KEY, JSON.stringify([...ids]))
  } catch {
    // localStorage unavailable — dismissal just won't persist, not fatal
  }
}

// The old status panel (Mochi mood pills, mini-calendar, buddy stats, sticky note)
// was removed per Scott — it wasn't earning its space. This is a quiet colored
// accent, plus a "Mochi found something new" notice when the pipeline has added
// opportunities recently (is_new, served by /api/opportunities). The notice is
// dismissable per-device; the underlying is_new flag itself never changes.
export default function StatusBar() {
  const [sections, setSections] = useState(() => getCache('/api/opportunities')?.sections ?? null)
  const [dismissed, setDismissed] = useState(() => readDismissed())

  useEffect(() => {
    if (sections) return
    fetch('/api/opportunities')
      .then(r => (r.ok ? r.json() : null))
      .then(d => { if (d) { setCache('/api/opportunities', d); setSections(d.sections) } })
      .catch(() => { /* best-effort — simply no banner if this fails */ })
  }, [sections])

  useEffect(() => {
    if (!sections) return
    const pruned = pruneDismissed(sections, dismissed)
    if (pruned.size !== dismissed.size) {
      setDismissed(pruned)
      writeDismissed(pruned)
    }
  }, [sections, dismissed])

  const count = sections ? countUndismissed(sections, dismissed) : 0

  function dismiss() {
    const next = new Set([...dismissed, ...allNewIds(sections)])
    setDismissed(next)
    writeDismissed(next)
  }

  return (
    <>
      {count > 0 && (
        <div className="status-new-banner">
          <span className="status-new-text">
            🐾 Mochi found {count} new thing{count === 1 ? '' : 's'} this week
          </span>
          <button className="status-new-dismiss" onClick={dismiss} aria-label="Dismiss">×</button>
        </div>
      )}
      <div className="status-accent" aria-hidden="true" />
    </>
  )
}
```

- [ ] **Step 2: Append banner styles to `StatusBar.css`**

```css
/* ── "Mochi found something new" banner ── */
.status-new-banner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 8px 16px;
  background: var(--gold-faint, #fdf5e0);
  border-top: 1px solid var(--gold, #c49a3e);
  font-family: Georgia, serif;
  font-size: 13px;
  color: var(--ink, #3a332a);
}

.status-new-dismiss {
  background: none;
  border: none;
  font-size: 16px;
  line-height: 1;
  color: var(--ink-muted, #8a7f6f);
  cursor: pointer;
  padding: 0 2px;
}

.status-new-dismiss:hover {
  color: var(--ink, #3a332a);
}
```

- [ ] **Step 3: Run the full frontend test suite (no regressions expected — this task adds no new tests of its own, per Task 2's note that this repo has no component/DOM test harness)**

Run: `cd frontend && npm test`
Expected: PASS (all)

Run: `cd frontend && npm run lint`
Expected: no NEW errors (this repo has pre-existing unrelated lint errors in other files — confirm none are in `StatusBar.jsx`/`StatusBar.css`)

- [ ] **Step 4: Manually verify in the running dev server**

This component has no automated test coverage (no jsdom harness in this repo — matches the precedent set by the `leave`-event frontend task). Verify by hand:

1. Run `start_mochi.bat` (or `npm run dev` in `frontend/` with `python api.py` running).
2. Open http://localhost:5177, open DevTools → Application → Local Storage, confirm no `mochi_new_dismissed` key yet.
3. If no opportunity in the live data has an `imported_at` within the last 7 days, temporarily edit one entry in `deploy_data/compact_opportunities.json` to have today's date, restart `api.py`, and reload the page.
4. Confirm the banner appears with the correct count and a × button.
5. Click ×, confirm the banner disappears and `localStorage['mochi_new_dismissed']` now contains that opportunity's `id`.
6. Reload the page — confirm the banner stays dismissed (doesn't reappear for the same item).
7. Revert any temporary edit to `compact_opportunities.json` made for this test.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/components/StatusBar.jsx frontend/src/components/StatusBar.css
git commit -m "$(cat <<'EOF'
feat: "Mochi found something new" dismissable banner in StatusBar

Counts is_new opportunities not yet dismissed (per-device, via
localStorage) and shows a banner on all three companion pages.
Dismissing a batch persists its ids; a later batch of new
opportunities reopens the banner for just the new ones.
EOF
)"
```

---

## Task 4: Frontend — "New" badge on `OppCard`

**Files:**
- Modify: `frontend/src/components/OppCard.jsx:181-184` (add badge span)
- Modify: `frontend/src/components/OppCard.css` (append)
- Modify: `frontend/src/i18n/translations.js` (add `card.new` key in all three language blocks)

**Interfaces:**
- Consumes: `opp.is_new` (boolean, from Task 1's `shape_card()` output, already flowing through `OpportunitiesSection.jsx` → `OppCard`'s `opp` prop with no changes needed there).

- [ ] **Step 1: Add the `card.new` translation key**

In `frontend/src/i18n/translations.js`, add one line to each of the three language blocks, next to the existing `card.close`/`card.details` keys:

Chinese block (near `frontend/src/i18n/translations.js:98-99`):
```javascript
  'card.details':            '详情',
  'card.close':              '关闭',
  'card.new':                '新',
```

Japanese block (near `frontend/src/i18n/translations.js:1313-1314`):
```javascript
  'card.details':            '詳細',
  'card.close':              '閉じる',
  'card.new':                '新着',
```

English block (near `frontend/src/i18n/translations.js:2363-2364`):
```javascript
  'card.details':            'Details',
  'card.close':              'Close',
  'card.new':                'New',
```

- [ ] **Step 2: Add the badge next to the confidence dot**

Replace `frontend/src/components/OppCard.jsx:181-184`:

```jsx
  return (
    <div className={cardClass}>
      <span className="opp-conf-dot" style={{ background: confColor }} title={t(`card.conf.${confLevel}`)} aria-hidden="true" />
      {opp.is_new && <span className="opp-new-badge">{t('card.new')}</span>}
```

- [ ] **Step 3: Add badge styles to `OppCard.css`**

Append near the existing `.opp-conf-dot` rule (`frontend/src/components/OppCard.css:18-26`):

```css
.opp-new-badge {
  position: absolute;
  top: 12px;
  right: 30px;
  font-size: 9px;
  font-weight: bold;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  color: var(--gold, #a07c2e);
  background: var(--gold-faint, #fdf5e0);
  border: 1px solid var(--gold, #c49a3e);
  border-radius: 999px;
  padding: 2px 7px;
  z-index: 2;
}
```

- [ ] **Step 4: Run the full frontend test suite**

Run: `cd frontend && npm test`
Expected: PASS (all — this task adds no new tests; `is_new`/badge rendering has no DOM harness to verify against, consistent with Task 3)

Run: `cd frontend && npm run lint`
Expected: no NEW errors

- [ ] **Step 5: Manually verify**

Using the same temporary `imported_at` edit from Task 3 Step 4 (or a genuinely fresh opportunity from tonight's pipeline run), confirm the gold "New"/"新"/"新着" badge appears next to the confidence dot on that card, in each of the three language toggles.

- [ ] **Step 6: Commit**

```bash
git add frontend/src/components/OppCard.jsx frontend/src/components/OppCard.css frontend/src/i18n/translations.js
git commit -m "feat: New badge on opportunity cards for recently-imported items"
```

---

## Self-Review Notes

- **Spec coverage:** `is_new` stateless signal (Task 1), StatusBar count banner + dismiss (Tasks 2-3), OppCard badge (Task 4). All three spec goals covered; both spec non-goals (no pipeline diff step, no cross-device sync) are respected by construction.
- **Placeholder scan:** none — every step has literal code, exact commands, expected output.
- **Type consistency:** `is_new_opportunity(imported_at, now=None, window_days=NEW_WINDOW_DAYS) -> bool` defined once in Task 1, consumed only server-side. Frontend `allNewIds`/`countUndismissed`/`pruneDismissed` signatures defined in Task 2 are used identically (same argument order, same names) in Task 3's `StatusBar.jsx`. `opp.is_new` (boolean) is the single field name used consistently by Task 3 (via the raw sections payload) and Task 4 (via the `opp` prop) — both trace back to Task 1's exact key.
