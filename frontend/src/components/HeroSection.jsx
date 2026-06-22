import { useState, useEffect } from 'react'
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

const POEM_COUNT = 4

export default function HeroSection() {
  const { t } = useLanguage()
  const greeting = t(greetingKey())
  const [poem, setPoem]   = useState(() => Math.floor(Math.random() * POEM_COUNT))
  const [shown, setShown] = useState(true)

  // Gently rotate the poem in the open space below the greeting.
  useEffect(() => {
    const id = setInterval(() => {
      setShown(false)
      setTimeout(() => {
        setPoem(i => (i + 1) % POEM_COUNT)
        setShown(true)
      }, 600)
    }, 9000)
    return () => clearInterval(id)
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
          <div className="greeting-main">{greeting}</div>
          <div className="greeting-sub">{t('hero.sub')}</div>
        </div>
        <p className={`hero-poem${shown ? '' : ' hero-poem--out'}`}>{t(`mochi.poem.${poem}`)}</p>
      </div>
    </section>
  )
}
