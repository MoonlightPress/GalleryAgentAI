import { useState, useEffect, useRef } from 'react'
import './StatusStrip.css'
import { useLanguage } from '../i18n/LanguageContext'
import { useLocalT } from '../i18n/local'
import { shellStrings } from './shellStrings'
import { api } from '../utils/api'
import { formatFreshness } from '../utils/freshness'

// Mochi's status strip — persists on ALL pages (Bible08: the emotional anchor).
// Honest signals only. Also carries the artist's direct line: "tell Peppercorn"
// — one tap, a sentence, done. Reports land in the maintainer's attention queue.
export default function StatusStrip() {
  const { lang } = useLanguage()
  const t2 = useLocalT(shellStrings)
  const [celebration, setCelebration] = useState(null)
  const [readyCount, setReadyCount] = useState(null)
  const [dataUpdatedAt, setDataUpdatedAt] = useState(null)
  const [reportOpen, setReportOpen] = useState(false)
  const [reportText, setReportText] = useState('')
  const [reportDone, setReportDone] = useState(false)
  const doneTimer = useRef(null)

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
      setReadyCount((d?.sections?.immediate_best_moves || []).length)
      setDataUpdatedAt(d?.data_updated_at || null)
    }).catch(() => {})

    return () => clearTimeout(doneTimer.current)
  }, [])

  async function sendReport() {
    const text = reportText.trim()
    if (!text) return
    try {
      await fetch('/api/issues', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, page: window.location.hash, lang }),
      })
      setReportText('')
      setReportOpen(false)
      setReportDone(true)
      doneTimer.current = setTimeout(() => setReportDone(false), 3000)
    } catch { /* quiet — never make her feel an error for reporting one */ }
  }

  const updatedWhen = formatFreshness(dataUpdatedAt)

  return (
    <>
      {reportOpen && (
        <div className="sstrip-report">
          <p className="voice small">{t2('v2.report.prompt')}</p>
          <textarea
            className="sstrip-report-input"
            rows={3}
            value={reportText}
            onChange={e => setReportText(e.target.value)}
            placeholder={t2('v2.report.placeholder')}
            autoFocus
          />
          <div className="sstrip-report-actions">
            <button className="btn-warm" onClick={sendReport} disabled={!reportText.trim()}>
              {t2('v2.report.send')}
            </button>
            <button className="btn-ghost" onClick={() => setReportOpen(false)}>
              {t2('v2.report.cancel')}
            </button>
          </div>
        </div>
      )}

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
            {updatedWhen && (
              <span className="sstrip-updated"> {t2('v2.status.updated', { when: updatedWhen })}</span>
            )}
          </span>
        )}
        <button className="sstrip-report-link" onClick={() => setReportOpen(o => !o)}>
          {reportDone ? t2('v2.report.thanks') : t2('v2.report.link')}
        </button>
      </div>
    </>
  )
}
