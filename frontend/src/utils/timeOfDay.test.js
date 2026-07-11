import test from 'node:test'
import assert from 'node:assert/strict'

import { isNightNow } from './timeOfDay.js'

// Build a Date whose *local* hour is `h` (isNightNow reads getHours()).
const at = (h) => new Date(2026, 6, 11, h, 0, 0)

test('evening and overnight hours are night', () => {
  assert.equal(isNightNow(at(18)), true)   // 6pm — boundary in
  assert.equal(isNightNow(at(21)), true)
  assert.equal(isNightNow(at(0)), true)     // midnight
  assert.equal(isNightNow(at(5)), true)     // 5am — last night hour
})

test('daytime hours are not night', () => {
  assert.equal(isNightNow(at(6)), false)    // 6am — boundary out
  assert.equal(isNightNow(at(9)), false)
  assert.equal(isNightNow(at(13)), false)
  assert.equal(isNightNow(at(17)), false)   // 5pm — last day hour
})
