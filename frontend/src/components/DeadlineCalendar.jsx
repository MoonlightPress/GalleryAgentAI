import { useState, useEffect } from 'react'
import { useLanguage } from '../i18n/LanguageContext'
import OppCard from './OppCard'
import OppDetailPanel from './OppDetailPanel'
import './DeadlineCalendar.css'

function parseDeadline(str) {
  if (!str) return null
  const s = str.trim()
  if (/^(tbd|check|n\/a|unknown|no fixed|ongoing|rolling|open|twice|entry period)/i.test(s)) return null

  // ISO: 2026-06-27
  if (/^\d{4}-\d{2}-\d{2}/.test(s)) {
    const d = new Date(s.slice(0, 10) + 'T00:00:00')
    return isNaN(d.getTime()) ? null : d
  }

  // Japanese: 2026年06月06日 or 2026年6月11日（木）23:59
  const jpMatch = s.match(/(\d{4})年(\d{1,2})月(\d{1,2})日/)
  if (jpMatch) {
    const d = new Date(+jpMatch[1], +jpMatch[2] - 1, +jpMatch[3])
    return isNaN(d.getTime()) ? null : d
  }

  // English month-first: June 7, 2026
  const mdy = s.match(/([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})/)
  if (mdy) {
    const d = new Date(`${mdy[1]} ${mdy[2]}, ${mdy[3]}`)
    return isNaN(d.getTime()) ? null : d
  }

  // Day-month-year: 19th December 2025
  const dmy = s.match(/(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)\s+(\d{4})/)
  if (dmy) {
    const d = new Date(`${dmy[2]} ${dmy[1]}, ${dmy[3]}`)
    return isNaN(d.getTime()) ? null : d
  }

  return null
}

const WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const MONTHS   = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

function formatDate(date) {
  return `${MONTHS[date.getMonth()]} ${date.getDate()} · ${WEEKDAYS[date.getDay()]}`
}

function urgencyClass(days) {
  if (days <= 3) return 'cal-urgent'
  if (days <= 7) return 'cal-soon'
  return 'cal-normal'
}

export default function DeadlineCalendar() {
  const { t } = useLanguage()
  const [data, setData]           = useState(null)
  const [activeId, setActiveId]   = useState(null)
  const [suppressed, setSuppressed] = useState(new Set())

  useEffect(() => {
    fetch('/api/opportunities')
      .then(r => r.ok ? r.json() : null)
      .then(setData)
      .catch(() => {})
  }, [])

  if (!data) return null

  const now = new Date(); now.setHours(0, 0, 0, 0)
  const limit = new Date(now); limit.setDate(limit.getDate() + 30)

  // Flatten + deduplicate all sections
  const seen = new Set()
  const allOpps = []
  for (const items of Object.values(data.sections || {})) {
    for (const opp of items) {
      if (!seen.has(opp.id)) { seen.add(opp.id); allOpps.push(opp) }
    }
  }

  // Group by deadline date within the window
  const byDate = new Map()
  for (const opp of allOpps) {
    if (suppressed.has(opp.id)) continue
    const d = parseDeadline(opp.deadline)
    if (!d || d < now || d >= limit) continue
    const key = d.toISOString().slice(0, 10)
    if (!byDate.has(key)) byDate.set(key, { date: d, opps: [] })
    byDate.get(key).opps.push(opp)
  }

  const entries    = [...byDate.entries()].sort(([a], [b]) => a.localeCompare(b))
  const activeOpp  = allOpps.find(o => o.id === activeId) || null
  const totalItems = entries.reduce((n, [, { opps }]) => n + opps.length, 0)

  if (entries.length === 0) return (
    <div className="cal-empty">
      <span className="cal-empty-icon">🐾</span>
      <p>{t('cal.noDeadlines')}</p>
    </div>
  )

  function handleDetails(opp) {
    setActiveId(prev => prev === opp.id ? null : opp.id)
  }

  function handleSuppressed(id) {
    setSuppressed(prev => new Set([...prev, id]))
    setActiveId(prev => prev === id ? null : prev)
  }

  return (
    <div className="cal-root">
      <div className="cal-section-header">
        <h2 className="cal-section-title">📅 {t('cal.title')}</h2>
        <p className="cal-section-sub">{t('cal.sub', { n: totalItems, dates: entries.length })}</p>
      </div>

      <div className="cal-timeline">
        {entries.map(([key, { date, opps }]) => {
          const daysLeft = Math.round((date - now) / 86400000)
          const chipLabel = daysLeft === 0 ? t('cal.today')
            : daysLeft === 1 ? t('cal.tomorrow')
            : t('cal.daysLeft', { n: daysLeft })
          const hasActive = opps.some(o => o.id === activeId)

          return (
            <div key={key} className="cal-date-group">
              <div className="cal-date-header">
                <span className="cal-date-label">{formatDate(date)}</span>
                <span className={`cal-days-chip ${urgencyClass(daysLeft)}`}>{chipLabel}</span>
                {opps.length > 1 && (
                  <span className="cal-count">{opps.length}</span>
                )}
              </div>
              <div className="cal-opp-row">
                {opps.map(opp => (
                  <OppCard
                    key={opp.id}
                    opp={opp}
                    isOpen={opp.id === activeId}
                    onDetails={() => handleDetails(opp)}
                    onSuppressed={handleSuppressed}
                  />
                ))}
              </div>
              {activeOpp && hasActive && (
                <OppDetailPanel
                  opp={activeOpp}
                  onClose={() => setActiveId(null)}
                />
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
