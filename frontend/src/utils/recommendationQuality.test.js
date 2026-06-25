import test from 'node:test'
import assert from 'node:assert/strict'
import {
  enrichOpportunity,
  rankOpportunities,
  strongestPicks,
} from './recommendationQuality.js'

const readyWatercolor = {
  id: 'ready-watercolor',
  name: 'Quiet Tokyo Watercolor Call',
  category: 'gallery',
  city: 'Tokyo',
  country: 'Japan',
  native_medium: 'watercolor',
  overall_score: 6.2,
  checklist: [
    { label: 'Deadline', status: 'ready' },
    { label: 'Entry fee', status: 'ready', note: 'Free' },
    { label: 'Submission path', status: 'ready' },
  ],
}

test('verified artist-fit opportunities rank above raw high-score uncertain ones', () => {
  const uncertainHighScore = {
    id: 'uncertain-high',
    name: 'Unclear International Prize',
    category: 'competition',
    city: 'Online',
    native_medium: 'photography',
    overall_score: 8.9,
    checklist: [
      { label: 'Deadline', status: 'check' },
      { label: 'Entry fee', status: 'check' },
      { label: 'Submission path', status: 'check' },
    ],
  }

  const ranked = rankOpportunities([uncertainHighScore, readyWatercolor], 'open_calls')

  assert.equal(ranked[0].id, 'ready-watercolor')
  assert.equal(ranked[0].recommendation.readiness, 'ready')
  assert.equal(ranked[1].recommendation.readiness, 'review')
})

test('recommendation reasons explain fit without exposing scores', () => {
  const enriched = enrichOpportunity(readyWatercolor, 'immediate_best_moves')

  assert.deepEqual(enriched.recommendation.reasons.slice(0, 3), [
    'Matches her watercolor practice',
    'Submission path is clear',
    'Deadline is checked',
  ])
  assert.equal(String(enriched.recommendation.reasonLine).includes('6.2'), false)
  assert.equal(String(enriched.recommendation.reasonLine).includes('score'), false)
})

test('feedback reshapes ranking beyond the current card', () => {
  const similarToHidden = {
    ...readyWatercolor,
    id: 'similar-hidden',
    name: 'Another Gallery Call',
  }
  const followedBook = {
    ...readyWatercolor,
    id: 'followed-book',
    name: 'Artist Book Shelf',
    category: 'bookstore_gallery',
    native_medium: 'book_arts',
  }
  const feedback = {
    followedIds: new Set(['followed-book']),
    hiddenCategories: new Set(['gallery']),
  }

  const ranked = rankOpportunities([similarToHidden, followedBook], 'open_calls', feedback)

  assert.equal(ranked[0].id, 'followed-book')
  assert.equal(ranked[1].recommendation.readiness, 'review')
})

test('"maybe later" pushes a card back, not forward', () => {
  const plain = { ...readyWatercolor, id: 'plain' }
  const maybe = { ...readyWatercolor, id: 'maybe-me' }
  const feedback = { maybeIds: new Set(['maybe-me']) }
  // input order puts the maybe'd one first; it must end up last after ranking
  const ranked = rankOpportunities([maybe, plain], 'open_calls', feedback)
  assert.equal(ranked[ranked.length - 1].id, 'maybe-me')
  assert.ok(ranked[0].recommendation.sortScore > ranked[ranked.length - 1].recommendation.sortScore)
})

test('strongest picks pull the best ready items across sections', () => {
  const sections = {
    immediate_best_moves: [readyWatercolor],
    watch_list: [{
      id: 'needs-review',
      name: 'Needs Review',
      native_medium: 'watercolor',
      overall_score: 9,
      checklist: [{ label: 'Submission path', status: 'check' }],
    }],
  }

  const picks = strongestPicks(sections, 3)

  assert.equal(picks.length, 1)
  assert.equal(picks[0].id, 'ready-watercolor')
  assert.equal(picks[0].recommendation.sourceSection, 'immediate_best_moves')
})

test('backend actionability fields drive readiness and reasons when present', () => {
  const enriched = enrichOpportunity({
    ...readyWatercolor,
    actionability_status: 'check_before_acting',
    review_flags: ['source_needs_reverification'],
    recommendation_reasons: ['Relationship contact route exists'],
  }, 'relationship_targets')

  assert.equal(enriched.recommendation.readiness, 'review')
  assert.deepEqual(enriched.recommendation.reviewLabels, ['source_needs_reverification'])
  assert.deepEqual(enriched.recommendation.reasons, ['Relationship contact route exists'])
  assert.equal(enriched.recommendation.actionabilityStatus, 'check_before_acting')
})
