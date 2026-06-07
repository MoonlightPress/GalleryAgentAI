import { useState, useEffect } from 'react'
import { useLanguage } from '../i18n/LanguageContext'
import './TodaysFocus.css'

const ROLE_CONFIG = {
  quick_win: {
    icon:    '⚡',
    accent:  '#6a8a3a',
    bgLight: '#f4faef',
    border:  '#b8d898',
  },
  high_impact: {
    icon:    '✦',
    accent:  '#b8892a',
    bgLight: '#fdf8ef',
    border:  '#e8c878',
  },
  stretch_goal: {
    icon:    '◎',
    accent:  '#6a7ab8',
    bgLight: '#f2f4fc',
    border:  '#b8c4e8',
  },
}

function TodayCard({ card, role }) {
  if (!card) return null
  const { t: tFn } = useLanguage()
  const cfg = ROLE_CONFIG[role] || ROLE_CONFIG.high_impact
  const hasDeadline = card.deadline && !['tbd','unknown','check site','n/a'].some(s => (card.deadline || '').toLowerCase().includes(s))

  return (
    <div
      className="tf-card"
      style={{ '--tf-accent': cfg.accent, '--tf-bg': cfg.bgLight, '--tf-border': cfg.border }}
    >
      <div className="tf-role-badge">
        <span className="tf-role-icon">{cfg.icon}</span>
        <span className="tf-role-label">{card.today_label}</span>
        <span className="tf-time-est">{card.time_est}</span>
      </div>

      <h3 className="tf-name">{card.name}</h3>

      {card.city && (
        <div className="tf-location">{card.city}{card.country && card.country !== card.city ? ` · ${card.country}` : ''}</div>
      )}

      <p className="tf-summary">{(card.summary || '').slice(0, 120)}{card.summary?.length > 120 ? '…' : ''}</p>

      {card.why_card && (
        <p className="tf-why">{card.why_card.slice(0, 100)}{card.why_card.length > 100 ? '…' : ''}</p>
      )}

      <div className="tf-footer">
        {hasDeadline && (
          <span className="tf-deadline">📅 {card.deadline.slice(0, 40)}</span>
        )}
        {card.submission_page && (
          <a
            className="tf-action-link"
            href={card.submission_page}
            target="_blank"
            rel="noreferrer"
          >
            {tFn('tf.open')}
          </a>
        )}
        {!card.submission_page && card.official_website && (
          <a
            className="tf-action-link"
            href={card.official_website}
            target="_blank"
            rel="noreferrer"
          >
            {tFn('tf.visit')}
          </a>
        )}
      </div>
    </div>
  )
}

export default function TodaysFocus() {
  const { t } = useLanguage()
  const [today, setToday] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/today')
      .then(r => r.ok ? r.json() : null)
      .then(d => { setToday(d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  if (loading) return null
  if (!today || (!today.quick_win && !today.high_impact && !today.stretch_goal)) return null

  return (
    <section className="tf-section">
      <div className="tf-header">
        <h2 className="tf-section-title">{t('tf.title')}</h2>
        <p className="tf-section-sub">{t('tf.sub')}</p>
      </div>
      <div className="tf-grid">
        <TodayCard card={today.quick_win}    role="quick_win" />
        <TodayCard card={today.high_impact}  role="high_impact" />
        <TodayCard card={today.stretch_goal} role="stretch_goal" />
      </div>
    </section>
  )
}
