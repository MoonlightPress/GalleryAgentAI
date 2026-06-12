import { useState, useEffect } from 'react'
import './StatusStrip.css'
import { useLocalT } from '../i18n/local'
import { shellStrings } from './shellStrings'
import { api } from '../utils/api'

// Mochi's status strip — persists on ALL pages (Bible08: the emotional anchor).
// Honest signals only: real ready-count, real acceptance celebrations.
export default function StatusStrip() {
  const t2 = useLocalT(shellStrings)
  const [celebration, setCelebration] = useState(null)
  const [readyCount, setReadyCount] = useState(null)

  useEffect(() => {
    api.submissions().then(subs => {
      if (!Array.isArray(subs)) return
      const cutoff = new Date()
      cutoff.setDate(cutoff.getDate() - 30)
      const recent = subs
        .filter(s => s.outcome === 'accepted' && new Date(s.date) >= cutoff)
        .sort((a, b) => (b.date || '').localeCompare(a.date || ''))
      if (recent.length) setCelebration(recent[0])
    }).catch(() => {})

    api.opportunities().then(d => {
      const ibm = d?.sections?.immediate_best_moves || []
      setReadyCount(ibm.length)
    }).catch(() => {})
  }, [])

  return (
    <div className={`sstrip${celebration ? ' sstrip--celebrate' : ''}`}>
      <span className="sstrip-paw" aria-hidden>🐾</span>
      {celebration ? (
        <span className="sstrip-text">
          <strong>{t2('v2.status.celebrate', { venue: celebration.venue || celebration.what || '' })}</strong>
          {' '}<span className="voice">{t2('v2.status.celebrate.sub')}</span>
        </span>
      ) : (
        <span className="sstrip-text">
          {t2('v2.status.line')}
          {readyCount !== null && readyCount > 0 && (
            <span className="sstrip-fresh"> · {t2('v2.status.fresh', { n: readyCount })}</span>
          )}
        </span>
      )}
    </div>
  )
}
