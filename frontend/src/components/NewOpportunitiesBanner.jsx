import { useEffect, useState } from 'react'
import './NewOpportunitiesBanner.css'
import { useLanguage } from '../i18n/LanguageContext'
import { getCache, setCache } from '../utils/apiCache'
import { freshToHer, bannerCount, markFreshSeen } from '../utils/newOpportunities'

// "Mochi found something new" — a warm, prominent banner at the TOP of Mochi's
// page. Counts opportunities that are new TO THIS DEVICE (added since she last
// visited — see newOpportunities.js), still open, and a ready pick. It persists
// however long she's away, shows the whole visit, and clears next visit (marked
// seen on session end / dismiss). Renders nothing on a quiet return.
export default function NewOpportunitiesBanner() {
  const { t } = useLanguage()
  const [sections, setSections] = useState(() => getCache('/api/opportunities')?.sections ?? null)
  const [hidden, setHidden] = useState(false)

  useEffect(() => {
    if (sections) return
    fetch('/api/opportunities')
      .then(r => (r.ok ? r.json() : null))
      .then(d => { if (d) { setCache('/api/opportunities', d); setSections(d.sections) } })
      .catch(() => { /* best-effort — simply no banner if this fails */ })
  }, [sections])

  const fresh = sections ? freshToHer(sections) : new Set()
  const count = sections ? bannerCount(sections, fresh) : 0
  if (hidden || count < 1) return null

  function dismiss() {
    markFreshSeen()   // clears the session cache too, so it won't reappear on re-nav
    setHidden(true)
  }

  return (
    <div className="new-opps-banner" role="status">
      <span className="new-opps-paw" aria-hidden="true">🐾</span>
      <span className="new-opps-text">{t('newOpps.found', { n: count })}</span>
      <button
        className="new-opps-dismiss"
        onClick={dismiss}
        aria-label={t('intro.dismiss') || 'Dismiss'}
        title={t('intro.dismiss') || 'Dismiss'}
      >×</button>
    </div>
  )
}
