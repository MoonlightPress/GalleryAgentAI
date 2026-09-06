import { useState, useEffect } from 'react'
import './HeroSection.css'
import { mochiDayPool, mochiNightPool } from '../utils/heroImages'
import { poemToneFor, focalYFor } from '../utils/heroPoemTone'
import { isNightNow } from '../utils/timeOfDay'
import { useLanguage } from '../i18n/LanguageContext'
import { POEM_COUNT } from '../i18n/translations'

// Which painting this page load settled on. Module scope on purpose: it
// survives HeroSection remounting (switching companions is in-app navigation,
// not a new visit) and dies when the page actually reloads — which is exactly
// the boundary we want. sessionStorage would be wrong here, since it survives
// a refresh; a module variable does not.
const pickedThisLoad = { day: null, night: null }

export default function HeroSection() {
  const { t, lang } = useLanguage()
  const [poem, setPoem]   = useState(() => Math.floor(Math.random() * POEM_COUNT))
  const [shown, setShown] = useState(true)
  // Evening → Mochi's fireworks illustration; the darker wall behind the poem
  // needs the light-text treatment (.hero--night), so pick both together at mount.
  const [night] = useState(() => isNightNow())
  const pool = night ? mochiNightPool : mochiDayPool

  // A different painting every time she opens the page, advancing one step per
  // load and remembered per device. Cycling rather than re-randomising matters:
  // random repeats constantly (she'd see the same painting several times before
  // seeing half the set), while stepping through guarantees the whole set
  // before any repeat. The starting point is random so two devices don't march
  // in lockstep. Nothing to click — she reads, she doesn't operate controls.
  const [heroIdx] = useState(() => {
    const n = Math.max(1, pool.length)
    const slot = night ? 'night' : 'day'
    // Already chosen for this page load — moving between companions must not
    // advance the set, or the art changes on every tap.
    if (pickedThisLoad[slot] !== null) return pickedThisLoad[slot] % n

    const key = night ? 'mochi_hero_i_night' : 'mochi_hero_i_day'
    let cur
    try {
      const raw = localStorage.getItem(key)
      cur = raw === null ? Math.floor(Math.random() * n) : (parseInt(raw, 10) || 0)
      localStorage.setItem(key, String((cur + 1) % n))
    } catch {
      // Private mode or blocked storage: still show a painting, just don't remember.
      cur = Math.floor(Math.random() * n)
    }
    pickedThisLoad[slot] = cur % n
    return cur % n
  })
  const heroUrl = pool.length ? pool[heroIdx % pool.length] : ''
  const hero = { webp: heroUrl, png: heroUrl, width: 1920, height: 640 }
  // Whether the verse reads depends on what is behind it, not on the hour:
  // most of the night paintings are pale exactly where the poem sits.
  const poemTone = poemToneFor(heroUrl)
  // Where to hold the crop. The box is far squarer than a 3:1 painting, so
  // cover discards top and bottom; centring on the measured subject keeps a
  // low-standing cat off the cutting line.
  const focalY = focalYFor(heroUrl)

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
      <picture>
        <source srcSet={hero.webp} type="image/webp" />
        <img
          src={hero.png}
          alt=""
          draggable={false}
          className="hero-img"
          style={{ objectPosition: `center ${focalY}%` }}
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
