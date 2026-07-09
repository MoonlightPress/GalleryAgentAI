// Best-effort UX beacon. Posts a usage event to /api/event with the anonymous,
// stable per-browser visitor id attached. Never throws into the UI.

function visitorId() {
  try {
    let v = localStorage.getItem('mochi_vid')
    if (!v) {
      v = (typeof crypto !== 'undefined' && crypto.randomUUID)
        ? crypto.randomUUID()
        : String(Date.now()) + Math.random().toString(36).slice(2)
      localStorage.setItem('mochi_vid', v)
    }
    return v
  } catch {
    return null
  }
}

export function track(event) {
  const vid = visitorId()
  const body = vid ? { ...event, visitor_id: vid } : { ...event }
  try {
    fetch('/api/event', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      keepalive: true,
    }).catch(() => {})
  } catch {
    /* ignore — tracking is best-effort */
  }
}

// Shape an `action` event around the opportunity it happened to. Two things a
// bare track() call kept getting wrong: 38 of the 653 opportunities carry
// `title` instead of `name`, and an action with no `surface` can't be told
// apart from the same action on a different part of the page — an `open_card`
// from Today's Focus looked identical to one from the browse list.
export function actionPayload(action, opp = {}, extra = {}) {
  const payload = { type: 'action', action }
  const name = (opp && (opp.name || opp.title)) || ''
  if (name) payload.name = name
  if (opp && opp.category) payload.category = opp.category
  for (const [key, value] of Object.entries(extra)) {
    if (value !== undefined && value !== null && value !== '') payload[key] = value
  }
  return payload
}

export function trackAction(action, opp, extra) {
  track(actionPayload(action, opp, extra))
}
