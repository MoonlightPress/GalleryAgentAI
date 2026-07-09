import { test } from 'node:test'
import assert from 'node:assert/strict'
import { track, actionPayload } from './track.js'

function withStubs(seed, run) {
  const store = { ...seed }
  globalThis.localStorage = {
    getItem: (k) => (k in store ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v) },
  }
  const calls = []
  globalThis.fetch = (url, opts) => { calls.push({ url, opts }); return Promise.resolve() }
  try { return run(calls) } finally {
    delete globalThis.fetch; delete globalThis.localStorage
  }
}

test('posts event to /api/event with the stored visitor_id attached', () => {
  withStubs({ mochi_vid: 'stored-vid' }, (calls) => {
    track({ type: 'action', action: 'follow', category: 'zine' })
    assert.equal(calls.length, 1)
    assert.equal(calls[0].url, '/api/event')
    const body = JSON.parse(calls[0].opts.body)
    assert.equal(body.type, 'action')
    assert.equal(body.action, 'follow')
    assert.equal(body.visitor_id, 'stored-vid')
    assert.equal(calls[0].opts.keepalive, true)
  })
})

test('swallows fetch errors (best-effort)', () => {
  withStubs({ mochi_vid: 'stored-vid' }, () => {
    globalThis.fetch = () => { throw new Error('network down') }
    assert.doesNotThrow(() => track({ type: 'nav', page: 'observe' }))
  })
})

// --- actionPayload: an action event must say WHICH opportunity, on WHICH surface ---

test('actionPayload names the opportunity and the surface it was clicked on', () => {
  const p = actionPayload('open_link', { name: 'Mograg Gallery', category: 'cafe_gallery' },
                          { surface: 'today_focus', role: 'quick_win' })
  assert.equal(p.type, 'action')
  assert.equal(p.action, 'open_link')
  assert.equal(p.name, 'Mograg Gallery')
  assert.equal(p.category, 'cafe_gallery')
  assert.equal(p.surface, 'today_focus')
  assert.equal(p.role, 'quick_win')
})

test('actionPayload falls back to title when the opp has no name', () => {
  const p = actionPayload('open_card', { title: 'Untitled Open Call' })
  assert.equal(p.name, 'Untitled Open Call')
})

test('actionPayload omits empty/undefined fields rather than logging nulls', () => {
  const p = actionPayload('open_card', {}, { surface: undefined, role: null, page: '' })
  assert.deepEqual(Object.keys(p).sort(), ['action', 'type'])
})

test('actionPayload never throws on a missing opp', () => {
  assert.doesNotThrow(() => actionPayload('open_card'))
  assert.equal(actionPayload('open_card').action, 'open_card')
})
