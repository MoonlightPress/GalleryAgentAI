import { useState, useEffect } from 'react'
import './HeroSection.css'
import { mochiHero } from '../utils/heroImages'
import { useLanguage } from '../i18n/LanguageContext'

const ROLE_ICONS = { quick_win: '⚡', high_impact: '✦', stretch_goal: '◎' }

export default function HeroSection() {
  const { t, lang } = useLanguage()
  const locOpp = (opp, field) => {
    if (lang === 'zh' && opp[field + '_zh']) return opp[field + '_zh']
    if (lang === 'ja' && opp[field + '_ja']) return opp[field + '_ja']
    return opp[field]
  }
  const [today, setToday] = useState(null)

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
          <div className="greeting-main">{t('hero.greeting')}</div>
          <div className="greeting-sub">{t('hero.sub')}</div>
        </div>
        <div className="focus-card">
          <div className="focus-card-title">{t('hero.focusTitle')}</div>
          <ul className="focus-list">
            {items.length > 0 ? items.map((opp, i) => (
              <li key={i} className="focus-item">
                <span className="focus-item-icon">{ROLE_ICONS[opp.today_role] || '·'}</span>
                <div className="focus-item-body">
                  <div className="focus-item-tier">
                    {opp.today_label}
                    <span className="focus-item-time">· {opp.time_est}</span>
                  </div>
                  <div className="focus-item-name">{locOpp(opp, 'name')}</div>
                </div>
              </li>
            )) : (
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
