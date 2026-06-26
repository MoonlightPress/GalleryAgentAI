import { useState, useEffect } from 'react'
import { useLanguage } from '../i18n/LanguageContext'
import OppDetailPanel from './OppDetailPanel'
import { locF, localizeDeadline, daysUntilDeadline } from '../utils/localize.js'
import './TodaysFocus.css'

const ROLE_CONFIG = {
  quick_win: {
    icon:      '⚡',
    accent:    '#6a8a3a',
    bgLight:   '#f4faef',
    border:    '#b8d898',
    labelKey:  'tf.role.quickWin',
    timeKey:   'tf.time.min5',
  },
  high_impact: {
    icon:      '✦',
    accent:    '#b8892a',
    bgLight:   '#fdf8ef',
    border:    '#e8c878',
    labelKey:  'tf.role.highImpact',
    timeKey:   'tf.time.min3060',
  },
  stretch_goal: {
    icon:      '◎',
    accent:    '#6a7ab8',
    bgLight:   '#f2f4fc',
    border:    '#b8c4e8',
    labelKey:  'tf.role.stretchGoal',
    timeKey:   'tf.time.longer',
  },
}

function TodayCard({ card, role, isOpen, onDetails, hero }) {
  const { t: tFn, lang } = useLanguage()
  if (!card) return null
  const loc = (field) => locF(card, field, lang, tFn)
  const cfg = ROLE_CONFIG[role] || ROLE_CONFIG.high_impact
  const deadlineText = localizeDeadline(card, lang, tFn)

  return (
    <div
      className={`tf-card${hero ? ' tf-card--hero' : ''}`}
      style={{ '--tf-accent': cfg.accent, '--tf-bg': cfg.bgLight, '--tf-border': cfg.border }}
    >
      <div className="tf-role-badge">
        <span className="tf-role-icon">{cfg.icon}</span>
        <span className="tf-role-label">{cfg.labelKey ? tFn(cfg.labelKey) : (card.today_label || '')}</span>
        <span className="tf-time-est">{cfg.timeKey ? tFn(cfg.timeKey) : (card.time_est || '')}</span>
      </div>

      <h3 className="tf-name">{loc('name') || card.name || card.title}</h3>

      {card.city && (
        <div className="tf-location">{card.city}{card.country && card.country !== card.city ? ` · ${card.country}` : ''}</div>
      )}

      {(() => { const s = loc('summary') || ''; return s && <p className="tf-summary">{s.slice(0,120)}{s.length>120?'…':''}</p> })()}

      {loc('why_card') && (
        <p className="tf-why">{(() => { const w=loc('why_card'); return w.slice(0,100)+(w.length>100?'…':'') })()}</p>
      )}

      <div className="tf-footer">
        {deadlineText && (
          <span className="tf-deadline">📅 {deadlineText}</span>
        )}
        <button
          className={`tf-details-btn${isOpen ? ' tf-details-btn--active' : ''}`}
          onClick={onDetails}
        >
          {isOpen ? tFn('card.close') : tFn('card.details')}
        </button>
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
  const [activeRole, setActiveRole] = useState(null)
  const [showMore, setShowMore] = useState(false)

  function handleDetails(role) {
    setActiveRole(prev => prev === role ? null : role)
  }

  useEffect(() => {
    fetch('/api/today')
      .then(r => r.ok ? r.json() : null)
      .then(d => { setToday(d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  if (loading) return (
    <section className="tf-section">
      <div className="tf-header">
        <div className="tf-title-art">
          <h2 className="tf-section-title">{t('tf.title')}</h2>
        </div>
        <p className="tf-section-sub">{t('opps.loading')}</p>
      </div>
    </section>
  )
  if (!today || (!today.quick_win && !today.high_impact && !today.stretch_goal)) {
    return (
      <section className="tf-section">
        <div className="tf-header">
          <div className="tf-title-art">
            <h2 className="tf-section-title">{t('tf.title')}</h2>
          </div>
          <p className="tf-section-sub">{t('tf.noItems')}</p>
        </div>
      </section>
    )
  }

  // Build the slot list; skip null slots so the grid never shows empty columns.
  const slots = [
    { key: 'quick_win',    role: 'quick_win' },
    { key: 'high_impact',  role: 'high_impact' },
    { key: 'stretch_goal', role: 'stretch_goal' },
  ].filter(s => today[s.key])

  // Lead with urgency: a genuinely soon deadline should surface first, even if
  // it sits in the high-impact/stretch slot, so a no-deadline item never buries
  // something closing this week. Each card keeps its role badge, so the slot's
  // meaning (Quick Win / High Impact / Stretch) is preserved — only the order
  // changes. Items with no real deadline keep their original relative order
  // (stable sort) and fall after the dated ones.
  const URGENT_CAP = 9999
  const daysFor = (s) => {
    const d = daysUntilDeadline(today[s.key]?.deadline)
    return d == null || d < 0 ? URGENT_CAP : d
  }
  const orderedSlots = slots
    .map((s, i) => ({ s, i, days: daysFor(s) }))
    .sort((a, b) => (a.days - b.days) || (a.i - b.i))
    .map(x => x.s)

  // Lead with ONE thing: the single highest-priority action stands alone, so an
  // easily-overwhelmed reader meets a clear next step instead of a buffet. Any
  // other picks wait quietly behind an opt-in "if you have more energy" toggle,
  // and the feed only begins after this calm, finite block.
  const [hero, ...rest] = orderedSlots

  return (
    <section className="tf-section">
      <div className="tf-header">
        <div className="tf-title-art">
          <h2 className="tf-section-title">{t('tf.title')}</h2>
        </div>
        <p className="tf-section-sub">{t('tf.subOne')}</p>
      </div>

      <div className="tf-hero-wrap">
        <TodayCard
          card={today[hero.key]}
          role={hero.role}
          isOpen={activeRole === hero.key}
          onDetails={() => handleDetails(hero.key)}
          hero
        />
      </div>

      {rest.length > 0 && (
        <div className="tf-more">
          <button className="tf-more-toggle" onClick={() => setShowMore(v => !v)}>
            {showMore ? t('tf.more.hide') : t('tf.more.show', { n: rest.length })}
          </button>
          {showMore && (
            <div className="tf-grid tf-more-grid" style={{ gridTemplateColumns: `repeat(${rest.length}, 1fr)` }}>
              {rest.map(s => (
                <TodayCard
                  key={s.key}
                  card={today[s.key]}
                  role={s.role}
                  isOpen={activeRole === s.key}
                  onDetails={() => handleDetails(s.key)}
                />
              ))}
            </div>
          )}
        </div>
      )}

      {activeRole && today[activeRole] && (
        <OppDetailPanel
          opp={today[activeRole]}
          onClose={() => setActiveRole(null)}
        />
      )}
    </section>
  )
}
