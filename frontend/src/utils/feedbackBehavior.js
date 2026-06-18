const TOAST_KEYS = {
  follow: 'card.toast.follow',
  applied: 'card.toast.logged',
  maybe_later: 'card.toast.maybe',
  not_for_me: 'card.toast.notForMe',
}

export function feedbackToastKey(action) {
  return TOAST_KEYS[action] || null
}

export function shouldRemoveAfterFeedback(action) {
  return action === 'not_for_me'
}
