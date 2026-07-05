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
