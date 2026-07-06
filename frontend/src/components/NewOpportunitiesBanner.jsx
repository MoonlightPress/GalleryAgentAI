import { useEffect, useState } from 'react'
import './NewOpportunitiesBanner.css'
import { useLanguage } from '../i18n/LanguageContext'
import { getCache, setCache } from '../utils/apiCache'
import { bannerWorthyIds, countUndismissed, pruneDismissed } from '../utils/newOpportunities'

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

// "Mochi found something new" — a warm, prominent banner at the TOP of Mochi's
// page (the first thing seen), announcing opportunities the pipeline added
// recently (is_new, served by /api/opportunities). Dismissable per-device; the
// underlying is_new flag never changes. Renders nothing when there's nothing new
// or it's been dismissed, so a quiet week shows no banner.
export default function NewOpportunitiesBanner() {
  const { t } = useLanguage()
  const [sections, setSections] = useState(() => getCache('/api/opportunities')?.sections ?? null)
  const [dismissed, setDismissed] = useState(() => readDismissed())

  useEffect(() => {
    if (sections) return
    fetch('/api/opportunities')
      .then(r => (r.ok ? r.json() : null))
      .then(d => { if (d) { setCache('/api/opportunities', d); setSections(d.sections) } })
      .catch(() => { /* best-effort — simply no banner if this fails */ })
  }, [sections])

  // Prune dismissed ids that are no longer new at render time; persist only the
  // real side effect (the localStorage write) in an effect, never setState.
  const prunedDismissed = sections ? pruneDismissed(sections, dismissed) : dismissed
  useEffect(() => {
    if (prunedDismissed.size !== dismissed.size) writeDismissed(prunedDismissed)
  }, [prunedDismissed, dismissed])

  const count = sections ? countUndismissed(sections, prunedDismissed) : 0
  if (count < 1) return null

  function dismiss() {
    const next = new Set([...prunedDismissed, ...bannerWorthyIds(sections)])
    setDismissed(next)
    writeDismissed(next)
  }

  const msg = t('newOpps.found', { n: count })

  return (
    <div className="new-opps-banner" role="status">
      <span className="new-opps-paw" aria-hidden="true">🐾</span>
      <span className="new-opps-text">{msg}</span>
      <button
        className="new-opps-dismiss"
        onClick={dismiss}
        aria-label={t('intro.dismiss') || 'Dismiss'}
        title={t('intro.dismiss') || 'Dismiss'}
      >×</button>
    </div>
  )
}
