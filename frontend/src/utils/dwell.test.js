import { test } from 'node:test'
import assert from 'node:assert/strict'
import { createVisibilityTracker, FLAP_GRACE_MS, GLANCE_MS } from './dwell.js'

// A fake clock + timer queue, so we can drive hide/show sequences exactly.
function harness(graceMs = FLAP_GRACE_MS) {
  let now = 1_000_000
  let nextId = 1
  const timers = new Map()
  const emitted = []

  const tracker = createVisibilityTracker({
    emit: (e) => emitted.push(e),
    now: () => now,
    setTimer: (fn, ms) => { const id = nextId++; timers.set(id, { fn, at: now + ms }); return id },
    clearTimer: (id) => { timers.delete(id) },
    graceMs,
  })

  return {
    tracker,
    emitted,
    advance(ms) {
      now += ms
      for (const [id, t] of [...timers]) {
        if (t.at <= now) { timers.delete(id); t.fn() }
      }
    },
    pendingTimers: () => timers.size,
  }
}

test('a sub-second hide/show flap emits nothing at all', () => {
  const h = harness()
  h.advance(30_000)          // 30s of reading
  h.tracker.onHidden()
  h.advance(200)             // back in 200ms — the OS, not her
  h.tracker.onVisible()
  h.advance(60_000)
  assert.deepEqual(h.emitted, [], 'a 200ms flap must not manufacture a session')
})

test('a real absence emits leave, then return with time away', () => {
  const h = harness()
  h.advance(30_000)
  h.tracker.onHidden()
  h.advance(FLAP_GRACE_MS)   // grace elapses -> she really left
  assert.equal(h.emitted.length, 1)
  assert.equal(h.emitted[0].type, 'leave')
  assert.equal(h.emitted[0].reason, 'hidden')
  assert.equal(h.emitted[0].dwell_ms, 30_000)

  h.advance(120_000)         // away two minutes
  h.tracker.onVisible()
  assert.equal(h.emitted.length, 2)
  assert.equal(h.emitted[1].type, 'return')
  assert.equal(h.emitted[1].away_ms, 120_000 + FLAP_GRACE_MS)
})

test('dwell counts only foreground time, never the hidden gap', () => {
  const h = harness()
  h.advance(10_000)          // 10s visible
  h.tracker.onHidden()
  h.advance(600_000)         // 10 minutes buried
  h.tracker.onVisible()
  h.advance(5_000)           // 5s more visible
  h.tracker.onPageHide()

  const leaves = h.emitted.filter(e => e.type === 'leave')
  assert.equal(leaves.length, 2)
  assert.equal(leaves[0].dwell_ms, 10_000)
  assert.equal(leaves[1].dwell_ms, 5_000, 'the 10min hidden gap must not count as dwell')
})

test('pagehide flushes immediately — a closing tab cannot wait out the grace', () => {
  const h = harness()
  h.advance(8_000)
  h.tracker.onHidden()       // grace timer armed
  h.tracker.onPageHide()     // tab actually closing, right now
  assert.equal(h.emitted.length, 1)
  assert.equal(h.emitted[0].type, 'leave')
  assert.equal(h.emitted[0].reason, 'pagehide')
  assert.equal(h.emitted[0].dwell_ms, 8_000)
  assert.equal(h.pendingTimers(), 0, 'the pending grace timer must be cancelled')
})

test('pagehide after an already-emitted leave does not double-count', () => {
  const h = harness()
  h.advance(8_000)
  h.tracker.onHidden()
  h.advance(FLAP_GRACE_MS)   // leave emitted
  h.tracker.onPageHide()     // now the tab closes
  assert.equal(h.emitted.filter(e => e.type === 'leave').length, 1)
})

test('repeated onHidden while already hidden is idempotent', () => {
  const h = harness()
  h.advance(5_000)
  h.tracker.onHidden()
  h.tracker.onHidden()
  h.tracker.onHidden()
  h.advance(FLAP_GRACE_MS)
  assert.equal(h.emitted.filter(e => e.type === 'leave').length, 1)
})

test('changing page resets dwell and clears pending state', () => {
  const h = harness()
  h.advance(9_000)
  h.tracker.onPageChange()
  h.advance(4_000)
  h.tracker.onHidden()
  h.advance(FLAP_GRACE_MS)
  const leave = h.emitted.find(e => e.type === 'leave')
  assert.equal(leave.dwell_ms, 4_000, 'dwell restarts on the new page')
})

test('flap then genuine leave reports the full foreground time', () => {
  const h = harness()
  h.advance(20_000)
  h.tracker.onHidden(); h.advance(150); h.tracker.onVisible()   // flap
  h.advance(10_000)
  h.tracker.onHidden(); h.advance(FLAP_GRACE_MS)                // real leave
  const leave = h.emitted.find(e => e.type === 'leave')
  assert.equal(leave.dwell_ms, 30_000, '20s + 10s of real reading, flap gap excluded')
})

// --- glance: the page was shown, but never really looked at ---

test('a leave under the glance threshold is flagged as a glance', () => {
  const h = harness()
  h.advance(GLANCE_MS - 1_500)   // page visible well under the glance threshold
  h.tracker.onHidden()
  h.advance(FLAP_GRACE_MS)
  const leave = h.emitted.find(e => e.type === 'leave')
  assert.equal(leave.glance, true)
  assert.equal(leave.dwell_ms, GLANCE_MS - 1_500)
})

test('a real session is not flagged as a glance', () => {
  const h = harness()
  h.advance(30_000)
  h.tracker.onHidden()
  h.advance(FLAP_GRACE_MS)
  assert.equal(h.emitted.find(e => e.type === 'leave').glance, false)
})

test('foreground time accumulated across flaps can lift a glance into a session', () => {
  const h = harness()
  h.advance(2_000)
  h.tracker.onHidden(); h.advance(300); h.tracker.onVisible()   // flap
  h.advance(2_000)
  h.tracker.onHidden(); h.advance(FLAP_GRACE_MS)
  const leave = h.emitted.find(e => e.type === 'leave')
  assert.equal(leave.dwell_ms, 4_000)
  assert.equal(leave.glance, false, '4s of real foreground time is a short visit, not a glance')
})
