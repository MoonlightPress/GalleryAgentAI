import test from 'node:test'
import assert from 'node:assert/strict'
import { oppKey } from './oppKey.js'

test('oppKey: prefers the served id (the backend hash)', () => {
  assert.equal(oppKey({ id: 'abc123', title: 'Some Title', name: 'Some Name' }), 'abc123')
})

test('oppKey: falls back to title then name when no id', () => {
  assert.equal(oppKey({ title: 'Some Title', name: 'Some Name' }), 'Some Title')
  assert.equal(oppKey({ name: 'Some Name' }), 'Some Name')
})

test('oppKey: same opp yields the same key (POST == persist == suppress)', () => {
  const opp = { id: 'deadbeef0001', title: 'X' }
  assert.equal(oppKey(opp), oppKey({ ...opp }))
})

test('oppKey: empty/missing is a stable empty string', () => {
  assert.equal(oppKey({}), '')
  assert.equal(oppKey(null), '')
})
