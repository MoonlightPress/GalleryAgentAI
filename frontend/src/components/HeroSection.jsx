import { useState, useEffect } from 'react'
import './HeroSection.css'
import { mochiHero } from '../utils/heroImages'
import { useLanguage } from '../i18n/LanguageContext'

const ROLE_ICONS = { quick_win: '⚡', high_impact: '✦', stretch_goal: '◎' }

// Returns time-appropriate greeting key based on current hour
function greetingKey() {
  const h = new Date().getHours()
  if (h < 12) return 'hero.greeting.morning'
  if (h < 18) return 'hero.greeting.afternoon'
  return 'hero.greeting.evening'
}

export default function HeroSection() {
  const { t, lang } = useLanguage()
  const locOpp = (opp, field) => {
    if (lang === 'zh' && opp[field + '_zh']) return opp[field + '_zh']
    if (lang === 'ja' && opp[field + '_ja']) return opp[field + '_ja']
    return opp[field]
  }
  const [today, setToday] = useState(null)
  // Resolved once at mount — changes only if user stays open past midnight
  const greeting = t(greetingKey())

  useEffect(() => {
    fetch('/api/today')
      .then(r => r.ok ? r.json() : null)
      .then(d => setToday(d))
      .catch(() => {})
  }, [])

  const items = today
    ? [today.quick_win, today.high_impact, today.stretch_goal].filter(Boolean)
    : []

  return (
    <section className="hero">
      <img
        src={mochiHero}
        alt="Mochi's watercolor atelier"
        className="hero-img"
      />
      <div className="hero-overlay">
        <div className="greeting">
          <div className="greeting-main">{greeting}</div>
          <div className="greeting-sub">{t('hero.sub')}</div>
        </div>
        <div className="focus-card">
          <div className="focus-card-title">{t('hero.focusTitle')}</div>
          <ul className="focus-list">
            {items.length > 0 ? items.map((opp, i) => {
              const roleKey = opp.today_role === 'quick_win'
                ? 'quickWin'
                : opp.today_role === 'high_impact'
                  ? 'highImpact'
                  : 'stretch'
              const tierRaw = t(`hero.tier.${roleKey}`)
              const timeRaw = t(`hero.tier.${roleKey}.time`)
              // t() returns the key itself when missing — fall back to API data in that case
              const tierLabel = tierRaw.startsWith('hero.tier.') ? (opp.today_label || tierRaw) : tierRaw
              const timeLabel = timeRaw.startsWith('hero.tier.') ? (opp.time_est  || timeRaw)  : timeRaw
              return (
                <li key={i} className="focus-item">
                  <span className="focus-item-icon">{ROLE_ICONS[opp.today_role] || '·'}</span>
                  <div className="focus-item-body">
                    <div className="focus-item-tier">
                      {tierLabel}
                      <span className="focus-item-time">· {timeLabel}</span>
                    </div>
                    <div className="focus-item-name">{locOpp(opp, 'name')}</div>
                  </div>
                </li>
              )
            }) : (
              [0, 1, 2].map(i => (
                <li key={i} className="focus-item">
                  <span className="focus-item-icon">·</span>
                  <span>{t(`hero.focus.${i}`)}</span>
                </li>
              ))
            )}
          </ul>
          <a href="#immediate_best_moves" className="focus-see-all">
            {t('hero.seeAll')}
          </a>
        </div>
      </div>
    </section>
  )
}
