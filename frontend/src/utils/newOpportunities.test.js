import { test } from 'node:test'
import assert from 'node:assert/strict'
import {
  collectIds, initialSeen, freshIds, isBannerWorthy, bannerCount,
  freshToHer, isFresh, markFreshSeen, _resetForTest,
} from './newOpportunities.js'

function sections(...opps) {
  return { a: opps.slice(0, 2), b: opps.slice(2) }
}
const READY = (id, extra = {}) => ({ id, deadline_past: false, actionability_status: 'ready', ...extra })

// ── Pure helpers ──────────────────────────────────────────────────────────

test('collectIds gathers every id, or only those matching a predicate', () => {
  const s = sections({ id: 'a', is_new: true }, { id: 'b', is_new: false }, { id: 'c', is_new: true })
  assert.deepEqual([...collectIds(s)].sort(), ['a', 'b', 'c'])
  assert.deepEqual([...collectIds(s, o => o.is_new)].sort(), ['a', 'c'])
  assert.equal(collectIds(null).size, 0)
})

test('initialSeen seeds everything except the server-new batch', () => {
  const s = sections({ id: 'a', is_new: true }, { id: 'b', is_new: false }, { id: 'c', is_new: true })
  assert.deepEqual([...initialSeen(s)], ['b'])   // b already seen; a,c stay fresh
})

test('freshIds = served minus seen', () => {
  const s = sections({ id: 'a' }, { id: 'b' }, { id: 'c' })
  assert.deepEqual([...freshIds(s, new Set(['b']))].sort(), ['a', 'c'])
  assert.deepEqual([...freshIds(s, new Set())].sort(), ['a', 'b', 'c'])
})

test('isBannerWorthy requires open + ready', () => {
  assert.equal(isBannerWorthy(READY('x')), true)
  assert.equal(isBannerWorthy({ id: 'x', deadline_past: true, actionability_status: 'ready' }), false)
  assert.equal(isBannerWorthy({ id: 'x', deadline_past: false, actionability_status: 'review' }), false)
  assert.equal(isBannerWorthy(null), false)
})

test('bannerCount counts fresh AND banner-worthy only', () => {
  const s = sections(
    READY('a'),
    { id: 'b', deadline_past: false, actionability_status: 'review' }, // fresh but not worthy
    READY('c', { deadline_past: true }),                                // fresh, worthy? no (past)
    READY('d'),
  )
  const fresh = new Set(['a', 'b', 'c', 'd'])
  assert.equal(bannerCount(s, fresh), 2)              // a, d
  assert.equal(bannerCount(s, new Set(['b'])), 0)     // only b fresh, not worthy
})

// ── localStorage orchestration ────────────────────────────────────────────

function withStorage(seed, run) {
  const store = { ...seed }
  globalThis.localStorage = {
    getItem: (k) => (k in store ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v) },
  }
  _resetForTest()
  try { return run(store) } finally { delete globalThis.localStorage; _resetForTest() }
}

test('first load seeds: server-new shows as fresh, the rest is pre-seen', () => {
  withStorage({}, () => {
    const s = sections({ id: 'a', is_new: true }, { id: 'b', is_new: false }, { id: 'c', is_new: true })
    const fresh = freshToHer(s)
    assert.deepEqual([...fresh].sort(), ['a', 'c'])   // the recent batch, not the whole catalog
    assert.equal(isFresh('a'), true)
    assert.equal(isFresh('b'), false)
  })
})

test('after markFreshSeen, nothing is fresh next session (survives long gaps)', () => {
  withStorage({}, () => {
    const s = sections({ id: 'a', is_new: true }, { id: 'b', is_new: false }, { id: 'c', is_new: true })
    freshToHer(s)          // session 1: a,c fresh
    markFreshSeen()        // she's seen them
    _resetForTest()        // session 2 (fresh page load), same localStorage
    const s2 = sections({ id: 'a', is_new: false }, { id: 'b', is_new: false }, { id: 'c', is_new: false })
    assert.equal(freshToHer(s2).size, 0)   // gone — even though time passed / is_new aged off

    // A future pipeline adds 'd' — it's fresh regardless of any time window.
    _resetForTest()
    const s3 = { a: [{ id: 'a' }, { id: 'b' }], b: [{ id: 'c' }, { id: 'd', is_new: false }] }
    assert.deepEqual([...freshToHer(s3)], ['d'])
  })
})

test('empty payload never seeds (avoids locking in an all-seen state)', () => {
  withStorage({}, (store) => {
    assert.equal(freshToHer({}).size, 0)
    assert.equal(store[ 'mochi_new_seeded' ], undefined)   // not seeded yet
  })
})

test('bannerCount ignores the watch list — those are next-edition reminders, not open calls', () => {
  // Found 2026-07-29: passed recurring entries get moved to watch_list with
  // deadline cleared and past reset for display, so they satisfied
  // isBannerWorthy and inflated "Mochi found N new things" with items she
  // cannot act on.
  const s = {
    todays_focus: [READY('a', { is_new: true })],
    watch_list:   [READY('w1', { is_new: true }), READY('w2', { is_new: true })],
  }
  const fresh = new Set(['a', 'w1', 'w2'])
  assert.equal(bannerCount(s, fresh), 1)
})
