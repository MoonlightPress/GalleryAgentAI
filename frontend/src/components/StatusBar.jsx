import './StatusBar.css'
import { useLanguage } from '../i18n/LanguageContext'

const JUNE_2026 = {
  dates: [
    [1, 2, 3, 4, 5, 6, 7],
    [8, 9, 10, 11, 12, 13, 14],
    [15, 16, 17, 18, 19, 20, 21],
    [22, 23, 24, 25, 26, 27, 28],
    [29, 30, null, null, null, null, null],
  ],
  today: 2,
}

export default function StatusBar() {
  const { t } = useLanguage()
  const days = t('status.days')

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
          <div className="mini-cal-month">{t('status.calMonth')}</div>
          <div className="mini-cal-grid">
            {days.map((d, i) => (
              <div key={i} className="mini-cal-header">{d}</div>
            ))}
            {JUNE_2026.dates.flat().map((d, i) => (
              <div
                key={i}
                className={`mini-cal-day${d === JUNE_2026.today ? ' today' : ''}${!d ? ' empty' : ''}`}
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
