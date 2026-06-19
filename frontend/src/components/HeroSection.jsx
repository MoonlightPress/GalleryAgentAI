import './HeroSection.css'
import { mochiHero } from '../utils/heroImages'
import { useLanguage } from '../i18n/LanguageContext'

// Returns time-appropriate greeting key based on current hour
function greetingKey() {
  const h = new Date().getHours()
  if (h < 12) return 'hero.greeting.morning'
  if (h < 18) return 'hero.greeting.afternoon'
  return 'hero.greeting.evening'
}

export default function HeroSection() {
  const { t } = useLanguage()
  const greeting = t(greetingKey())

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
      </div>
    </section>
  )
}
