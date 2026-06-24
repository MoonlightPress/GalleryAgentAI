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
  // Japanese: 2026年06月06日
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

// Local YYYY-MM-DD (avoid toISOString's UTC shift).
const keyOf = (d) =>
  `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`

function formatDate(date, months, weekdays) {
  return `${months[date.getMonth()]} ${date.getDate()} · ${weekdays[date.getDay()]}`
}

function urgencyClass(days) {
  if (days <= 3) return 'cal-urgent'
  if (days <= 7) return 'cal-soon'
  return 'cal-normal'
}

// ── The literal calendar: a month grid with deadline days marked ──────────────
function CalendarMonth({ byDate, base, calMonths, calWeekdays, todayKey, selectedKey, onSelect, onShift, canGoBack }) {
  const year = base.getFullYear()
  const month = base.getMonth()
  const firstWeekday = new Date(year, month, 1).getDay()
  const daysInMonth = new Date(year, month + 1, 0).getDate()

  const cells = []
  for (let i = 0; i < firstWeekday; i++) cells.push(null)
  for (let d = 1; d <= daysInMonth; d++) cells.push(d)

  return (
    <div className="cal-grid">
      <div className="cal-grid-nav">
        <button className="cal-grid-arrow" onClick={() => onShift(-1)} disabled={!canGoBack} aria-label="previous month">‹</button>
        <span className="cal-grid-month">{calMonths[month]} {year}</span>
        <button className="cal-grid-arrow" onClick={() => onShift(1)} aria-label="next month">›</button>
      </div>
      <div className="cal-grid-weekdays">
        {calWeekdays.map((w, i) => <span key={i} className="cal-grid-wd">{w}</span>)}
      </div>
      <div className="cal-grid-days">
        {cells.map((d, i) => {
          if (d === null) return <span key={i} className="cal-grid-cell cal-grid-cell--empty" />
          const key = keyOf(new Date(year, month, d))
          const entry = byDate.get(key)
          const cls = [
            'cal-grid-cell',
            entry ? 'cal-grid-cell--has' : '',
            key === todayKey ? 'cal-grid-cell--today' : '',
            key === selectedKey ? 'cal-grid-cell--sel' : '',
          ].filter(Boolean).join(' ')
          return (
            <button
              key={i}
              className={cls}
              onClick={() => entry && onSelect(key === selectedKey ? null : key)}
              disabled={!entry}
            >
              <span className="cal-grid-daynum">{d}</span>
              {entry && <span className="cal-grid-dot">{entry.opps.length}</span>}
            </button>
          )
        })}
      </div>
    </div>
  )
}

export default function DeadlineCalendar() {
  const { t } = useLanguage()
  const calWeekdays = t('cal.weekdays')
  const calMonths   = t('cal.months')
  const [data, setData]             = useState(null)
  const [activeId, setActiveId]     = useState(null)
  const [suppressed, setSuppressed] = useState(new Set())
  const [monthOffset, setMonthOffset] = useState(0)
  const [selectedKey, setSelectedKey] = useState(null)

  useEffect(() => {
    fetch('/api/opportunities')
      .then(r => r.ok ? r.json() : null)
      .then(setData)
      .catch(() => {})
  }, [])

  if (!data) return (
    <div className="cal-empty">
      <span className="cal-empty-icon">🐾</span>
      <p>{t('cal.loading')}</p>
    </div>
  )

  const now = new Date(); now.setHours(0, 0, 0, 0)
  const todayKey = keyOf(now)

  // Flatten + dedupe
  const seen = new Set()
  const allOpps = []
  for (const items of Object.values(data.sections || {})) {
    for (const opp of items) {
      if (!seen.has(opp.id)) { seen.add(opp.id); allOpps.push(opp) }
    }
  }

  // Group every future deadline by date (the grid spans months, not just 30 days)
  const byDate = new Map()
  for (const opp of allOpps) {
    if (suppressed.has(opp.id)) continue
    const d = parseDeadline(opp.deadline)
    if (!d || d < now) continue
    const key = keyOf(d)
    if (!byDate.has(key)) byDate.set(key, { date: d, opps: [] })
    byDate.get(key).opps.push(opp)
  }

  const activeOpp = allOpps.find(o => o.id === activeId) || null

  // What the list below shows: the selected day, or the next 30 days.
  const limit = new Date(now); limit.setDate(limit.getDate() + 30)
  let entries
  if (selectedKey) {
    const e = byDate.get(selectedKey)
    entries = e ? [[selectedKey, e]] : []
  } else {
    entries = [...byDate.entries()]
      .filter(([, { date }]) => date < limit)
      .sort(([a], [b]) => a.localeCompare(b))
  }
  const totalItems = entries.reduce((n, [, { opps }]) => n + opps.length, 0)

  function handleDetails(opp) { setActiveId(prev => prev === opp.id ? null : opp.id) }
  function handleSuppressed(id) {
    setSuppressed(prev => new Set([...prev, id]))
    setActiveId(prev => prev === id ? null : prev)
  }

  const monthBase = new Date(now.getFullYear(), now.getMonth() + monthOffset, 1)

  return (
    <div className="cal-root">
      <div className="cal-section-header">
        <h2 className="cal-section-title">📅 {t('cal.title')}</h2>
        <p className="cal-section-sub">{t('cal.sub', { n: totalItems, dates: entries.length })}</p>
      </div>

      <CalendarMonth
        byDate={byDate}
        base={monthBase}
        calMonths={calMonths}
        calWeekdays={calWeekdays}
        todayKey={todayKey}
        selectedKey={selectedKey}
        onSelect={setSelectedKey}
        onShift={(dir) => { setSelectedKey(null); setMonthOffset(o => Math.max(0, o + dir)) }}
        canGoBack={monthOffset > 0}
      />

      {selectedKey && (
        <button className="cal-clear-sel" onClick={() => setSelectedKey(null)}>
          {t('cal.showAll')}
        </button>
      )}

      {entries.length === 0 ? (
        <div className="cal-empty">
          <span className="cal-empty-icon">🐾</span>
          <p>{t('cal.noDeadlines')}</p>
        </div>
      ) : (
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
                  <span className="cal-date-label">{formatDate(date, calMonths, calWeekdays)}</span>
                  <span className={`cal-days-chip ${urgencyClass(daysLeft)}`}>{chipLabel}</span>
                  {opps.length > 1 && <span className="cal-count">{opps.length}</span>}
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
                  <OppDetailPanel opp={activeOpp} onClose={() => setActiveId(null)} />
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
