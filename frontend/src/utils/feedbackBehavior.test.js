import test from 'node:test'
import assert from 'node:assert/strict'

import { feedbackToastKey, shouldRemoveAfterFeedback } from './feedbackBehavior.js'

test('not-for-me feedback hides the opportunity from the visible board', () => {
  assert.equal(shouldRemoveAfterFeedback('not_for_me'), true)
  assert.equal(shouldRemoveAfterFeedback('follow'), false)
})

test('feedback actions map to human confirmation messages', () => {
  assert.equal(feedbackToastKey('follow'), 'card.toast.follow')
  assert.equal(feedbackToastKey('applied'), 'card.toast.logged')
  assert.equal(feedbackToastKey('maybe_later'), 'card.toast.maybe')
  assert.equal(feedbackToastKey('not_for_me'), 'card.toast.notForMe')
  assert.equal(feedbackToastKey(null), null)
})
