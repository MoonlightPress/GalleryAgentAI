import test from 'node:test'
import assert from 'node:assert/strict'
import { isDistinct } from './textGuards.js'

// isDistinct(candidate, other): show `candidate` only when it carries real,
// non-duplicate text — used to hide a "why it fits" paragraph that merely
// repeats the summary/overview.

test('different non-empty strings are distinct', () => {
  assert.equal(isDistinct('why it fits', 'the summary'), true)
})

test('identical strings are not distinct', () => {
  assert.equal(isDistinct('same text', 'same text'), false)
})

test('whitespace-only differences are not distinct', () => {
  assert.equal(isDistinct('  same text  ', 'same text'), false)
})

test('empty / missing candidate is never distinct', () => {
  assert.equal(isDistinct('', 'x'), false)
  assert.equal(isDistinct('   ', 'x'), false)
  assert.equal(isDistinct(undefined, 'x'), false)
  assert.equal(isDistinct(null, 'x'), false)
})

test('candidate present while other is empty IS distinct (show it)', () => {
  assert.equal(isDistinct('why it fits', ''), true)
  assert.equal(isDistinct('why it fits', undefined), true)
})
