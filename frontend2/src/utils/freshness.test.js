import test from 'node:test'
import assert from 'node:assert/strict'

import { formatFreshness } from './freshness.js'

const noon = new Date('2026-06-18T12:00:00Z')

test('formats same-day updates without exposing technical timestamps', () => {
  assert.equal(formatFreshness('2026-06-18T03:00:00Z', noon), 'today')
})

test('formats recent updates as quiet relative language', () => {
  assert.equal(formatFreshness('2026-06-17T23:00:00Z', noon), 'yesterday')
  assert.equal(formatFreshness('2026-06-15T12:00:00Z', noon), '3 days ago')
})

test('falls back to a short date for older or invalid updates', () => {
  assert.equal(formatFreshness('2026-05-01T12:00:00Z', noon), 'May 1')
  assert.equal(formatFreshness(null, noon), null)
  assert.equal(formatFreshness('not-a-date', noon), null)
})
