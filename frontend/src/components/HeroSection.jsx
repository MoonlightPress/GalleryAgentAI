import { useState, useEffect } from 'react'
import './HeroSection.css'
import { mochiDayPool, mochiNightPool } from '../utils/heroImages'
import { poemToneFor } from '../utils/heroPoemTone'
import { isNightNow } from '../utils/timeOfDay'
import { useLanguage } from '../i18n/LanguageContext'
import { POEM_COUNT } from '../i18n/translations'

export default function HeroSection() {
  const { t, lang } = useLanguage()
  const [poem, setPoem]   = useState(() => Math.floor(Math.random() * POEM_COUNT))
  const [shown, setShown] = useState(true)
  // Evening → Mochi's fireworks illustration; the darker wall behind the poem
  // needs the light-text treatment (.hero--night), so pick both together at mount.
  const [night] = useState(() => isNightNow())
  // A different painting each visit, and a tap for the next one. The starting
  // point stays random so an ordinary visit feels varied; stepping through is
  // what makes the whole set reviewable without reloading.
  const pool = night ? mochiNightPool : mochiDayPool
  const [heroIdx, setHeroIdx] = useState(() => Math.floor(Math.random() * Math.max(1, pool.length)))
  const heroUrl = pool.length ? pool[heroIdx % pool.length] : ''
  const hero = { webp: heroUrl, png: heroUrl, width: 1920, height: 640 }
  // Whether the verse reads depends on what is behind it, not on the hour:
  // most of the night paintings are pale exactly where the poem sits.
  const poemTone = poemToneFor(heroUrl)

  // Gently rotate the poem.
  useEffect(() => {
    // Don't auto-rotate the poem for motion-sensitive users — show one, hold it.
    if (window.matchMedia?.('(prefers-reduced-motion: reduce)').matches) return
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
    <section className={`hero${night ? ' hero--night' : ''}`}>
      {/* WebP (≈0.12 MB) preferred, PNG (≈1.9 MB) fallback. Intrinsic dims reserve
          the box so the poem/layout doesn't shift in (CLS); high priority since
          it's the above-the-fold hero on her phone. */}
      <picture
        onClick={() => pool.length > 1 && setHeroIdx(i => (i + 1) % pool.length)}
        style={pool.length > 1 ? { cursor: 'pointer' } : undefined}
        title={pool.length > 1 ? `${(heroIdx % pool.length) + 1} / ${pool.length}` : undefined}
      >
        <source srcSet={hero.webp} type="image/webp" />
        <img
          src={hero.png}
          alt={night ? "Mochi's atelier at night, watching the fireworks" : "Mochi's watercolor atelier"}
          className="hero-img"
          width={hero.width}
          height={hero.height}
          fetchPriority="high"
          decoding="async"
        />
      </picture>
      <p lang={poemLang} className={`hero-poem hero-poem--${lang} hero-poem--${poemTone}${shown ? '' : ' hero-poem--out'}`}>{t(`mochi.poem.${poem}`)}</p>
    </section>
  )
}
