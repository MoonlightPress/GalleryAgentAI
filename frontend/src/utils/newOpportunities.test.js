import { test } from 'node:test'
import assert from 'node:assert/strict'
import { bannerWorthyIds, countUndismissed, pruneDismissed, isBannerWorthy } from './newOpportunities.js'

// Banner-worthy = new AND open AND actionability 'ready'. 'a' and 'c' qualify;
// 'b' is not new, 'd' is new but past-deadline, 'e' is new+open but not ready.
const SECTIONS = {
  open_calls: [
    { id: 'a', is_new: true, deadline_past: false, actionability_status: 'ready' },
    { id: 'b', is_new: false, deadline_past: false, actionability_status: 'ready' },
    { id: 'd', is_new: true, deadline_past: true, actionability_status: 'ready' },
  ],
  zines_and_print: [
    { id: 'c', is_new: true, deadline_past: false, actionability_status: 'ready' },
    { id: 'e', is_new: true, deadline_past: false, actionability_status: 'review' },
  ],
}

test('isBannerWorthy requires new + open + ready', () => {
  assert.equal(isBannerWorthy({ is_new: true, deadline_past: false, actionability_status: 'ready' }), true)
  assert.equal(isBannerWorthy({ is_new: false, deadline_past: false, actionability_status: 'ready' }), false)
  assert.equal(isBannerWorthy({ is_new: true, deadline_past: true, actionability_status: 'ready' }), false)
  assert.equal(isBannerWorthy({ is_new: true, deadline_past: false, actionability_status: 'review' }), false)
  assert.equal(isBannerWorthy(null), false)
})

test('bannerWorthyIds collects only new+open+ready ids', () => {
  assert.deepEqual([...bannerWorthyIds(SECTIONS)].sort(), ['a', 'c'])
})

test('bannerWorthyIds is safe on empty/missing input', () => {
  assert.equal(bannerWorthyIds({}).size, 0)
  assert.equal(bannerWorthyIds(null).size, 0)
  assert.equal(bannerWorthyIds(undefined).size, 0)
})

test('countUndismissed counts banner-worthy ids not in the dismissed set', () => {
  assert.equal(countUndismissed(SECTIONS, new Set()), 2)
  assert.equal(countUndismissed(SECTIONS, new Set(['a'])), 1)
  assert.equal(countUndismissed(SECTIONS, new Set(['a', 'c'])), 0)
})

test('countUndismissed treats a missing dismissed set as empty', () => {
  assert.equal(countUndismissed(SECTIONS, undefined), 2)
})

test('pruneDismissed drops ids no longer banner-worthy/present', () => {
  const pruned = pruneDismissed(SECTIONS, new Set(['a', 'stale-id', 'd']))
  assert.deepEqual([...pruned], ['a'])
})

test('pruneDismissed is safe on empty/missing input', () => {
  assert.equal(pruneDismissed(SECTIONS, new Set()).size, 0)
  assert.equal(pruneDismissed(SECTIONS, undefined).size, 0)
})
