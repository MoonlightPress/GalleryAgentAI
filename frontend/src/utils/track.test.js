import { test } from 'node:test'
import assert from 'node:assert/strict'
import { track } from './track.js'

function withStubs(seed, run) {
  const store = { ...seed }
  global.localStorage = {
    getItem: (k) => (k in store ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v) },
  }
  const calls = []
  global.fetch = (url, opts) => { calls.push({ url, opts }); return Promise.resolve() }
  try { return run(calls) } finally {
    delete global.fetch; delete global.localStorage
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
    global.fetch = () => { throw new Error('network down') }
    assert.doesNotThrow(() => track({ type: 'nav', page: 'observe' }))
  })
})
