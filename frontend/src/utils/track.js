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
