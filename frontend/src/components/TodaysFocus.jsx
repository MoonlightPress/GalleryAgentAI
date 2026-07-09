import { useState, useEffect } from 'react'
import { useLanguage } from '../i18n/LanguageContext'
import OppDetailPanel from './OppDetailPanel'
import { locF, localizeDeadline, daysUntilDeadline } from '../utils/localize.js'
import { getCache, setCache } from '../utils/apiCache'
import { trackAction } from '../utils/track'
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
    accent:    '#8a6a7a',
    bgLight:   '#f6eff1',
    border:    '#dcc6cf',
    labelKey:  'tf.role.stretchGoal',
    timeKey:   'tf.time.longer',
  },
}

function TodayCard({ card, role, isOpen, onDetails }) {
  const { t: tFn, lang } = useLanguage()
  if (!card) return null
  const loc = (field) => locF(card, field, lang, tFn)
  const cfg = ROLE_CONFIG[role] || ROLE_CONFIG.high_impact
  const deadlineText = localizeDeadline(card, lang, tFn)

  return (
    <div
      className="tf-card"
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
          onClick={() => {
            if (!isOpen) trackAction('open_card', card, { surface: 'today_focus', role })
            onDetails()
          }}
        >
          {isOpen ? tFn('card.close') : tFn('card.details')}
        </button>
        {card.submission_page && (
          <a
            className="tf-action-link"
            href={card.submission_page}
            target="_blank"
            rel="noreferrer"
            onClick={() => trackAction('external_link_click', card,
              { surface: 'today_focus', role, link_type: 'submission_page' })}
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
            onClick={() => trackAction('external_link_click', card,
              { surface: 'today_focus', role, link_type: 'official_website' })}
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
  const [today, setToday] = useState(() => getCache('/api/today') ?? null)
  const [loading, setLoading] = useState(() => getCache('/api/today') === undefined)
  const [activeRole, setActiveRole] = useState(null)

  function handleDetails(role) {
    setActiveRole(prev => prev === role ? null : role)
  }

  useEffect(() => {
    fetch('/api/today')
      .then(r => r.ok ? r.json() : null)
      .then(d => { setCache('/api/today', d); setToday(d); setLoading(false) })
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

  // The subtitle must match what's actually shown — never promise three and
  // render two. tf.sub is the three-pick copy; tf.subN is count-aware.
  const subKey = orderedSlots.length === 3 ? 'tf.sub' : 'tf.subN'

  return (
    <section className="tf-section">
      <div className="tf-header">
        <div className="tf-title-art">
          <h2 className="tf-section-title">{t('tf.title')}</h2>
        </div>
        <p className="tf-section-sub">{t(subKey, { n: orderedSlots.length })}</p>
      </div>
      <div className={`tf-grid tf-grid--${Math.min(orderedSlots.length, 3)}`}>
        {orderedSlots.map(s => (
          <TodayCard
            key={s.key}
            card={today[s.key]}
            role={s.role}
            isOpen={activeRole === s.key}
            onDetails={() => handleDetails(s.key)}
          />
        ))}
      </div>

      {activeRole && today[activeRole] && (
        <OppDetailPanel
          opp={today[activeRole]}
          onClose={() => setActiveRole(null)}
        />
      )}
    </section>
  )
}
