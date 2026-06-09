import { useState, useEffect } from 'react'
import { useLanguage } from '../i18n/LanguageContext'
import OppDetailPanel from './OppDetailPanel'
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

const EN_MONTHS_TF = ['January','February','March','April','May','June','July','August','September','October','November','December']
const JA_WEEKDAYS_TF = ['日','月','火','水','木','金','土']

function fmtDeadline(str, lang) {
  if (!str) return str
  const s = str.trim()
  if (/^(tbd|check|n\/a|unknown|no fixed|ongoing|rolling|open)/i.test(s)) return s
  let d = null
  if (/^\d{4}-\d{2}-\d{2}/.test(s)) d = new Date(s.slice(0,10)+'T00:00:00')
  if (!d) { const jp=s.match(/(\d{4})年(\d{1,2})月(\d{1,2})日/); if(jp) d=new Date(+jp[1],+jp[2]-1,+jp[3]) }
  if (!d) { const mdy=s.match(/([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})/); if(mdy) d=new Date(`${mdy[1]} ${mdy[2]}, ${mdy[3]}`) }
  if (!d || isNaN(d.getTime())) return s.slice(0, 40)
  if (lang==='zh') return `${d.getFullYear()}年${d.getMonth()+1}月${d.getDate()}日`
  if (lang==='ja') return `${d.getFullYear()}年${d.getMonth()+1}月${d.getDate()}日（${JA_WEEKDAYS_TF[d.getDay()]}）`
  return `${EN_MONTHS_TF[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`
}

function TodayCard({ card, role, isOpen, onDetails }) {
  if (!card) return null
  const { t: tFn, lang } = useLanguage()
  const loc = (field) => {
    if (lang === 'zh' && card[field + '_zh']) return card[field + '_zh']
    if (lang === 'ja' && card[field + '_ja']) return card[field + '_ja']
    return card[field]
  }
  const cfg = ROLE_CONFIG[role] || ROLE_CONFIG.high_impact
  const hasDeadline = card.deadline && !['tbd','unknown','check site','n/a','未定','随時','要確認','待定'].some(s => (card.deadline || '').toLowerCase().includes(s.toLowerCase()))

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

      <h3 className="tf-name">{loc('name')}</h3>

      {card.city && (
        <div className="tf-location">{card.city}{card.country && card.country !== card.city ? ` · ${card.country}` : ''}</div>
      )}

      {(() => { const s = loc('summary') || ''; return s && <p className="tf-summary">{s.slice(0,120)}{s.length>120?'…':''}</p> })()}

      {loc('why_card') && (
        <p className="tf-why">{(() => { const w=loc('why_card'); return w.slice(0,100)+(w.length>100?'…':'') })()}</p>
      )}

      <div className="tf-footer">
        {hasDeadline && (
          <span className="tf-deadline">📅 {fmtDeadline(card.deadline, lang)}</span>
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
        <h2 className="tf-section-title">{t('tf.title')}</h2>
        <p className="tf-section-sub">{t('opps.loading')}</p>
      </div>
    </section>
  )
  if (!today || (!today.quick_win && !today.high_impact && !today.stretch_goal)) {
    return (
      <section className="tf-section">
        <div className="tf-header">
          <h2 className="tf-section-title">{t('tf.title')}</h2>
          <p className="tf-section-sub">{t('tf.noItems')}</p>
        </div>
      </section>
    )
  }

  // Build the ordered slot list; skip null slots so the grid never shows empty columns
  const slots = [
    { key: 'quick_win',    role: 'quick_win' },
    { key: 'high_impact',  role: 'high_impact' },
    { key: 'stretch_goal', role: 'stretch_goal' },
  ].filter(s => today[s.key])

  return (
    <section className="tf-section">
      <div className="tf-header">
        <h2 className="tf-section-title">{t('tf.title')}</h2>
        <p className="tf-section-sub">{t('tf.sub')}</p>
      </div>
      <div className="tf-grid" style={slots.length < 3 ? { gridTemplateColumns: `repeat(${slots.length}, 1fr)` } : undefined}>
        {slots.map(s => (
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
