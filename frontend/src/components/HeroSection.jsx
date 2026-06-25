import { useState, useEffect } from 'react'
import './HeroSection.css'
import { mochiHeroSources } from '../utils/heroImages'
import { useLanguage } from '../i18n/LanguageContext'
import { POEM_COUNT } from '../i18n/translations'

export default function HeroSection() {
  const { t, lang } = useLanguage()
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

  // The poem renders in zh/ja/en; mark the element's language so screen readers
  // and the browser pick the right typography per active language.
  const poemLang = lang === 'zh' ? 'zh-Hans' : lang === 'ja' ? 'ja' : 'en'

  return (
    <section className="hero">
      {/* WebP (≈0.12 MB) preferred, PNG (≈1.9 MB) fallback. Intrinsic dims reserve
          the box so the poem/layout doesn't shift in (CLS); high priority since
          it's the above-the-fold hero on her phone. */}
      <picture>
        <source srcSet={mochiHeroSources.webp} type="image/webp" />
        <img
          src={mochiHeroSources.png}
          alt="Mochi's watercolor atelier"
          className="hero-img"
          width={mochiHeroSources.width}
          height={mochiHeroSources.height}
          fetchPriority="high"
          decoding="async"
        />
      </picture>
      <p lang={poemLang} className={`hero-poem hero-poem--${lang}${shown ? '' : ' hero-poem--out'}`}>{t(`mochi.poem.${poem}`)}</p>
    </section>
  )
}
