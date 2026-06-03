import './HeroSection.css'
import { mochiHero } from '../utils/heroImages'
import { useLanguage } from '../i18n/LanguageContext'

export default function HeroSection() {
  const { t } = useLanguage()

  const focusItems = [
    { icon: '⭐', text: t('hero.focus.0') },
    { icon: '✉',  text: t('hero.focus.1') },
    { icon: '🔍', text: t('hero.focus.2') },
  ]

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
            {focusItems.map((item, i) => (
              <li key={i} className="focus-item">
                <span className="focus-item-icon">{item.icon}</span>
                <span>{item.text}</span>
              </li>
            ))}
          </ul>
          <a href="#" className="focus-see-all">{t('hero.seeAll')}</a>
        </div>
      </div>
    </section>
  )
}
