import { useState, useEffect } from 'react'
import './HeroSection.css'
import { mochiHero } from '../utils/heroImages'
import { useLanguage } from '../i18n/LanguageContext'

const TIERS = [
  {
    icon:      '⭐',
    labelKey:  'hero.tier.quickWin',
    timeKey:   'hero.tier.quickWin.time',
    bucket:    'immediate_best_moves',
    fallback:  0,
  },
  {
    icon:      '✉',
    labelKey:  'hero.tier.highImpact',
    timeKey:   'hero.tier.highImpact.time',
    bucket:    'open_calls',
    fallback:  1,
  },
  {
    icon:      '🔍',
    labelKey:  'hero.tier.stretch',
    timeKey:   null,
    bucket:    'watch_list',
    fallback:  2,
  },
]

export default function HeroSection() {
  const { t } = useLanguage()
  const [sections, setSections] = useState(null)

  useEffect(() => {
    fetch('/api/opportunities')
      .then(r => r.ok ? r.json() : null)
      .then(d => { if (d?.sections) setSections(d.sections) })
      .catch(() => {})
  }, [])

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
            {TIERS.map((tier, i) => {
              const opp = sections?.[tier.bucket]?.[0]
              return (
                <li key={i} className="focus-item">
                  <span className="focus-item-icon">{tier.icon}</span>
                  {opp ? (
                    <div className="focus-item-body">
                      <div className="focus-item-tier">
                        {t(tier.labelKey)}
                        {tier.timeKey && (
                          <span className="focus-item-time">· {t(tier.timeKey)}</span>
                        )}
                      </div>
                      <div className="focus-item-name">{opp.name}</div>
                    </div>
                  ) : (
                    <span>{t(`hero.focus.${tier.fallback}`)}</span>
                  )}
                </li>
              )
            })}
          </ul>
          <a href="#immediate_best_moves" className="focus-see-all">
            {t('hero.seeAll')}
          </a>
        </div>
      </div>
    </section>
  )
}
