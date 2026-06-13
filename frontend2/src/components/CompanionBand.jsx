import { useEffect, useState } from 'react'
import './CompanionBand.css'
import { useLanguage } from '../i18n/LanguageContext'
import { LANGUAGES, LANGUAGE_LABELS } from '../i18n/translations'
import { useLocalT } from '../i18n/local'
import { shellStrings } from './shellStrings'
import mochiImg from '../assets/heroes/mochi/mochi_hero.png'
import peppercornImg from '../assets/heroes/peppercorn/peppercorn_hero.png'
import saffronImg from '../assets/heroes/saffron/saffron_hero.png'

// Characters stay, but the FUNCTION titles do the wayfinding (user feedback):
// Discover / Observe / Converse under each roundel; pet names live in tooltips.
const COMPANIONS = [
  { key: 'mochi',      img: mochiImg,      pos: '72% 30%', titleKey: 'nav.discover' },
  { key: 'saffron',    img: saffronImg,    pos: '12% 18%', titleKey: 'nav.observe'  },
  { key: 'peppercorn', img: peppercornImg, pos: '50% 38%', titleKey: 'nav.refine'   },
]

// In-page section anchors per page — shown in the condensed scroll nav.
const SECTIONS = {
  mochi: [
    { id: 'focus', key: 'v2.snav.mochi.focus' },
    { id: 'board', key: 'v2.snav.mochi.board' },
  ],
  saffron: [
    { id: 'overview', key: 'v2.snav.saffron.overview' },
    { id: 'journey',  key: 'v2.snav.saffron.journey' },
    { id: 'field',    key: 'v2.snav.saffron.field' },
    { id: 'peers',    key: 'v2.snav.saffron.peers' },
    { id: 'notes',    key: 'v2.snav.saffron.notes' },
  ],
  peppercorn: [
    { id: 'wondering',  key: 'v2.snav.peppercorn.wondering' },
    { id: 'knows',      key: 'v2.snav.peppercorn.knows' },
    { id: 'record',     key: 'v2.snav.peppercorn.record' },
    { id: 'milestones', key: 'v2.snav.peppercorn.milestones' },
  ],
}

function scrollToSection(id) {
  const el = document.getElementById(id)
  if (!el) return
  const top = el.getBoundingClientRect().top + window.scrollY - 64
  window.scrollTo({ top, behavior: 'smooth' })
}

export default function CompanionBand({ activePage, onNav }) {
  const { t, lang, setLang } = useLanguage()
  const t2 = useLocalT(shellStrings)
  const [condensed, setCondensed] = useState(false)

  useEffect(() => {
    let ticking = false
    const onScroll = () => {
      if (ticking) return
      ticking = true
      requestAnimationFrame(() => {
        setCondensed(window.scrollY > 160)
        ticking = false
      })
    }
    window.addEventListener('scroll', onScroll, { passive: true })
    onScroll()
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  const sections = SECTIONS[activePage] || []

  return (
    <header className={`cband${condensed ? ' cband--condensed' : ''}`}>
      <div className="cband-inner">
        <div className="cband-companions" role="navigation" aria-label="Pages">
          {COMPANIONS.map(c => {
            const active = activePage === c.key
            return (
              <button
                key={c.key}
                className={`cband-btn${active ? ' cband-btn--active' : ''}`}
                onClick={() => { onNav(c.key); window.scrollTo({ top: 0 }) }}
                aria-current={active ? 'page' : undefined}
                title={t2(`v2.nav.${c.key}.name`)}
              >
                <span className="cband-roundel">
                  <img src={c.img} alt="" style={{ objectPosition: c.pos }} />
                </span>
                <span className="cband-title">{t(c.titleKey)}</span>
              </button>
            )
          })}
        </div>

        {/* Page sections — visible only in the condensed scroll state */}
        {condensed && sections.length > 0 && (
          <nav className="cband-sections" aria-label="Page sections">
            {sections.map(s => (
              <button key={s.id} className="cband-sec-link" onClick={() => scrollToSection(s.id)}>
                {t2(s.key)}
              </button>
            ))}
          </nav>
        )}

        <div className="cband-lang">
          {LANGUAGES.map(code => (
            <button
              key={code}
              className={`cband-lang-btn${lang === code ? ' cband-lang-btn--active' : ''}`}
              onClick={() => setLang(code)}
            >
              {LANGUAGE_LABELS[code]}
            </button>
          ))}
        </div>
      </div>
    </header>
  )
}
