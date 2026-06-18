import test from 'node:test'
import assert from 'node:assert/strict'

import { feedbackToastKey, shouldRemoveAfterFeedback } from './feedbackBehavior.js'

test('not-for-me feedback removes the opportunity from the visible board', () => {
  assert.equal(shouldRemoveAfterFeedback('not_for_me'), true)
  assert.equal(shouldRemoveAfterFeedback('follow'), false)
})

test('each positive feedback action has a human toast key', () => {
  assert.equal(feedbackToastKey('follow'), 'card.toast.follow')
  assert.equal(feedbackToastKey('applied'), 'card.toast.logged')
  assert.equal(feedbackToastKey('maybe_later'), 'card.toast.maybe')
  assert.equal(feedbackToastKey('not_for_me'), 'card.toast.notForMe')
  assert.equal(feedbackToastKey(null), null)
})
