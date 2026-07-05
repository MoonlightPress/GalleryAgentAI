import { useEffect, useState } from 'react'
import './StatusBar.css'
import { getCache, setCache } from '../utils/apiCache'
import { allNewIds, countUndismissed, pruneDismissed } from '../utils/newOpportunities'

const DISMISSED_KEY = 'mochi_new_dismissed'

function readDismissed() {
  try {
    const raw = localStorage.getItem(DISMISSED_KEY)
    return raw ? new Set(JSON.parse(raw)) : new Set()
  } catch {
    return new Set()
  }
}

function writeDismissed(ids) {
  try {
    localStorage.setItem(DISMISSED_KEY, JSON.stringify([...ids]))
  } catch {
    // localStorage unavailable — dismissal just won't persist, not fatal
  }
}

// The old status panel (Mochi mood pills, mini-calendar, buddy stats, sticky note)
// was removed per Scott — it wasn't earning its space. This is a quiet colored
// accent, plus a "Mochi found something new" notice when the pipeline has added
// opportunities recently (is_new, served by /api/opportunities). The notice is
// dismissable per-device; the underlying is_new flag itself never changes.
export default function StatusBar() {
  const [sections, setSections] = useState(() => getCache('/api/opportunities')?.sections ?? null)
  const [dismissed, setDismissed] = useState(() => readDismissed())

  useEffect(() => {
    if (sections) return
    fetch('/api/opportunities')
      .then(r => (r.ok ? r.json() : null))
      .then(d => { if (d) { setCache('/api/opportunities', d); setSections(d.sections) } })
      .catch(() => { /* best-effort — simply no banner if this fails */ })
  }, [sections])

  // Derived at render time rather than synced into state via an effect: drop
  // dismissed ids that are no longer actually new (aged out or gone from the
  // feed). Persisting the pruned set to localStorage is a real side effect
  // (writing to an external system), so that alone lives in its own effect —
  // it never calls setState, only writeDismissed.
  const prunedDismissed = sections ? pruneDismissed(sections, dismissed) : dismissed

  useEffect(() => {
    if (prunedDismissed.size !== dismissed.size) writeDismissed(prunedDismissed)
  }, [prunedDismissed, dismissed])

  const count = sections ? countUndismissed(sections, prunedDismissed) : 0

  function dismiss() {
    const next = new Set([...prunedDismissed, ...allNewIds(sections)])
    setDismissed(next)
    writeDismissed(next)
  }

  return (
    <>
      {count > 0 && (
        <div className="status-new-banner">
          <span className="status-new-text">
            🐾 Mochi found {count} new thing{count === 1 ? '' : 's'} this week
          </span>
          <button className="status-new-dismiss" onClick={dismiss} aria-label="Dismiss">×</button>
        </div>
      )}
      <div className="status-accent" aria-hidden="true" />
    </>
  )
}
