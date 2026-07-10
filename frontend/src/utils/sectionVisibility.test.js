import { test } from 'node:test'
import assert from 'node:assert/strict'
import { landedRatio, LANDED_RATIO } from './sectionVisibility.js'

const PHONE = 800   // viewport height

test('a short section fully on screen has landed', () => {
  const r = landedRatio({ intersectionHeight: 300, sectionHeight: 300, viewportHeight: PHONE })
  assert.equal(r, 1)
  assert.ok(r >= LANDED_RATIO)
})

test('a section TALLER than the viewport can still land — the old bug', () => {
  // open_calls is a long grid: ~3000px on a phone. It can never be 50% of
  // ITSELF on screen, so the old ratio-vs-self test never fired for it.
  const filling = landedRatio({ intersectionHeight: 800, sectionHeight: 3000, viewportHeight: PHONE })
  assert.equal(filling, 1, 'a tall section filling the whole screen has landed')
  assert.ok(filling >= LANDED_RATIO)

  const oldRatio = 800 / 3000
  assert.ok(oldRatio < 0.5, 'sanity: the old test could never reach its own threshold')
})

test('a tall section barely peeking in has not landed', () => {
  const r = landedRatio({ intersectionHeight: 100, sectionHeight: 3000, viewportHeight: PHONE })
  assert.equal(r, 0.125)
  assert.ok(r < LANDED_RATIO)
})

test('half the screen filled by a tall section counts as landed', () => {
  const r = landedRatio({ intersectionHeight: 400, sectionHeight: 3000, viewportHeight: PHONE })
  assert.equal(r, 0.5)
  assert.ok(r >= LANDED_RATIO)
})

test('a short section half on screen has not landed', () => {
  const r = landedRatio({ intersectionHeight: 100, sectionHeight: 200, viewportHeight: PHONE })
  assert.equal(r, 0.5)
})

test('degenerate sizes never divide by zero or return NaN', () => {
  for (const args of [
    { intersectionHeight: 0, sectionHeight: 0, viewportHeight: 0 },
    { intersectionHeight: 10, sectionHeight: 0, viewportHeight: PHONE },
    { intersectionHeight: 10, sectionHeight: 100, viewportHeight: 0 },
  ]) {
    const r = landedRatio(args)
    assert.ok(Number.isFinite(r), `expected finite, got ${r} for ${JSON.stringify(args)}`)
    assert.ok(r >= 0 && r <= 1)
  }
})

test('ratio is clamped to 1 even if the browser over-reports', () => {
  assert.equal(landedRatio({ intersectionHeight: 900, sectionHeight: 300, viewportHeight: PHONE }), 1)
})
