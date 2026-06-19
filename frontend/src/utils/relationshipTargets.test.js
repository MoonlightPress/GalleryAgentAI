import test from 'node:test'
import assert from 'node:assert/strict'
import { reachVia, prepareRelationshipTargets } from './relationshipTargets.js'

test('reachVia prefers email, then website, then none', () => {
  assert.equal(reachVia({ contact_email: 'a@b.com', official_website: 'https://x' }), 'email')
  assert.equal(reachVia({ official_website: 'https://x' }), 'website')
  assert.equal(reachVia({ contact_page: 'https://x' }), 'website')
  assert.equal(reachVia({ submission_page: 'https://x' }), 'website')
  assert.equal(reachVia({}), 'none')
})

test('prepareRelationshipTargets sorts high priority first and annotates reachVia', () => {
  const contacts = [
    { name: 'Low', crm_analysis: { priority: 'low' }, official_website: 'https://l' },
    { name: 'High', crm_analysis: { priority: 'high' }, contact_email: 'h@x.com' },
    { name: 'Mid', priority: 'medium' },
  ]
  const out = prepareRelationshipTargets(contacts)
  assert.deepEqual(out.map(c => c.name), ['High', 'Mid', 'Low'])
  assert.equal(out[0].reachVia, 'email')
  assert.equal(out[2].reachVia, 'website')
})

test('prepareRelationshipTargets keeps input order stable within equal priority', () => {
  const contacts = [
    { name: 'A', crm_analysis: { priority: 'high' } },
    { name: 'B', crm_analysis: { priority: 'high' } },
  ]
  assert.deepEqual(prepareRelationshipTargets(contacts).map(c => c.name), ['A', 'B'])
})

test('prepareRelationshipTargets respects a limit', () => {
  const contacts = Array.from({ length: 20 }, (_, i) => ({ name: `c${i}` }))
  assert.equal(prepareRelationshipTargets(contacts, { limit: 6 }).length, 6)
})

test('prepareRelationshipTargets is safe on empty/missing input', () => {
  assert.deepEqual(prepareRelationshipTargets([]), [])
  assert.deepEqual(prepareRelationshipTargets(null), [])
  assert.deepEqual(prepareRelationshipTargets(undefined), [])
})
