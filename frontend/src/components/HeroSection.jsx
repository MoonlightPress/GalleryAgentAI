import { useState, useEffect } from 'react'
import './HeroSection.css'
import { mochiHero } from '../utils/heroImages'
import { useLanguage } from '../i18n/LanguageContext'

const POEM_COUNT = 4

export default function HeroSection() {
  const { t } = useLanguage()
  const [poem, setPoem]   = useState(() => Math.floor(Math.random() * POEM_COUNT))
  const [shown, setShown] = useState(true)

  // Gently rotate the poem.
  useEffect(() => {
    const id = setInterval(() => {
      setShown(false)
      setTimeout(() => {
        setPoem(i => (i + 1) % POEM_COUNT)
        setShown(true)
      }, 600)
    }, 60000)
    return () => clearInterval(id)
  }, [])

  return (
    <section className="hero">
      <img
        src={mochiHero}
        alt="Mochi's watercolor atelier"
        className="hero-img"
      />
      <p className={`hero-poem${shown ? '' : ' hero-poem--out'}`}>{t(`mochi.poem.${poem}`)}</p>
    </section>
  )
}
