import './StatusBar.css'
import { useLanguage } from '../i18n/LanguageContext'

function buildCalendarGrid(now) {
  const year        = now.getFullYear()
  const month       = now.getMonth()
  const today       = now.getDate()
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  // Mon-first: Sun=0 → offset 6, Mon=1 → offset 0
  const startOffset = (new Date(year, month, 1).getDay() + 6) % 7

  const cells = [
    ...Array(startOffset).fill(null),
    ...Array.from({ length: daysInMonth }, (_, i) => i + 1),
  ]
  while (cells.length % 7 !== 0) cells.push(null)

  const weeks = []
  for (let i = 0; i < cells.length; i += 7) weeks.push(cells.slice(i, i + 7))
  return { weeks, today }
}

function formatCalMonth(now, lang) {
  if (lang === 'zh' || lang === 'ja') {
    return `${now.getFullYear()}年${now.getMonth() + 1}月`
  }
  return now.toLocaleDateString('en-US', { year: 'numeric', month: 'long' })
}

export default function StatusBar() {
  const { t, lang } = useLanguage()
  const now      = new Date()
  const cal      = buildCalendarGrid(now)
  const calMonth = formatCalMonth(now, lang)
  const days     = t('status.days')

  return (
    <div className="status-bar">
      {/* Left: Mochi identity + mood */}
      <div className="status-left">
        <div className="status-cat-thumb" />
        <div className="status-info">
          <div className="status-name">
            {t('status.name')} <span className="status-heart">♡</span>
          </div>
          <div className="status-mood-pills">
            <span className="mood-pill mood-happy">{t('status.mood.happy')}</span>
            <span className="mood-sep">•</span>
            <span className="mood-pill mood-full">{t('status.mood.full')}</span>
            <span className="mood-sep">•</span>
            <span className="mood-pill mood-content">{t('status.mood.content')}</span>
          </div>
          <div className="status-bar-track">
            <div className="status-bar-fill" />
          </div>
        </div>
      </div>

      {/* Center: status message */}
      <div className="status-center">
        <div className="status-message">{t('status.message')}</div>
        <div className="status-sub">{t('status.sub')}</div>
        <div className="status-sprig">🌿</div>
      </div>

      {/* Right: mini calendar + sticky note */}
      <div className="status-right">
        <div className="mini-calendar">
          <div className="mini-cal-month">{calMonth}</div>
          <div className="mini-cal-grid">
            {days.map((d, i) => (
              <div key={i} className="mini-cal-header">{d}</div>
            ))}
            {cal.weeks.flat().map((d, i) => (
              <div
                key={i}
                className={`mini-cal-day${d === cal.today ? ' today' : ''}${!d ? ' empty' : ''}`}
              >
                {d || ''}
              </div>
            ))}
          </div>
        </div>
        <div className="sticky-note">
          {t('status.sticky')}
        </div>
      </div>
    </div>
  )
}
