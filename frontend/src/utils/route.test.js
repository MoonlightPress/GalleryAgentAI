import test from 'node:test'
import assert from 'node:assert/strict'

import { parseHash, formatHash, sameRoute, PAGES, SAFFRON_TABS } from './route.js'

test('no hash lands on discover — the pre-routing behaviour, unchanged', () => {
  assert.deepEqual(parseHash(''), { page: 'discover', tab: null })
  assert.deepEqual(parseHash('#'), { page: 'discover', tab: null })
  assert.deepEqual(parseHash(undefined), { page: 'discover', tab: null })
  assert.deepEqual(parseHash(null), { page: 'discover', tab: null })
})

test('each companion has a hash that opens it directly', () => {
  for (const page of PAGES) {
    assert.deepEqual(parseHash(`#${page}`), { page, tab: null })
  }
})

test('a Saffron tab can be linked to', () => {
  for (const tab of SAFFRON_TABS) {
    assert.deepEqual(parseHash(`#observe/${tab}`), { page: 'observe', tab })
  }
})

test('sloppy hashes still resolve', () => {
  assert.deepEqual(parseHash('#/observe'), { page: 'observe', tab: null })
  assert.deepEqual(parseHash('#observe/'), { page: 'observe', tab: null })
  assert.deepEqual(parseHash('#OBSERVE/Calendar'), { page: 'observe', tab: 'calendar' })
  assert.deepEqual(parseHash('  #refine  '), { page: 'refine', tab: null })
})

test('an unrecognised hash falls back to discover instead of erroring', () => {
  assert.deepEqual(parseHash('#nonsense'), { page: 'discover', tab: null })
  assert.deepEqual(parseHash('#observe2'), { page: 'discover', tab: null })
  assert.deepEqual(parseHash('#section-open_calls'), { page: 'discover', tab: null })
})

test('an unknown tab keeps the page and drops the tab', () => {
  assert.deepEqual(parseHash('#observe/nope'), { page: 'observe', tab: null })
})

test('tabs belong to Saffron only — other pages ignore a second segment', () => {
  assert.deepEqual(parseHash('#discover/calendar'), { page: 'discover', tab: null })
  assert.deepEqual(parseHash('#refine/money'), { page: 'refine', tab: null })
})

test('formatHash round-trips through parseHash', () => {
  assert.equal(formatHash('observe', 'calendar'), '#observe/calendar')
  assert.equal(formatHash('observe', null), '#observe')
  assert.equal(formatHash('discover'), '#discover')
  assert.equal(formatHash('refine', 'calendar'), '#refine')   // tab is Saffron-only
  assert.equal(formatHash('bogus'), '#discover')              // never emits a dead hash
  for (const page of PAGES) {
    assert.deepEqual(parseHash(formatHash(page)), { page, tab: null })
  }
  for (const tab of SAFFRON_TABS) {
    assert.deepEqual(parseHash(formatHash('observe', tab)), { page: 'observe', tab })
  }
})

test('sameRoute treats a missing tab and a null tab as one route', () => {
  assert.equal(sameRoute({ page: 'observe' }, { page: 'observe', tab: null }), true)
  assert.equal(sameRoute({ page: 'observe', tab: 'money' }, { page: 'observe', tab: 'money' }), true)
  assert.equal(sameRoute({ page: 'observe', tab: 'money' }, { page: 'observe', tab: null }), false)
  assert.equal(sameRoute({ page: 'observe' }, { page: 'refine' }), false)
  assert.equal(sameRoute(null, { page: 'discover' }), false)
})
