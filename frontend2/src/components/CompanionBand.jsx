import './CompanionBand.css'
import { useLanguage } from '../i18n/LanguageContext'
import { LANGUAGES, LANGUAGE_LABELS } from '../i18n/translations'
import { useLocalT } from '../i18n/local'
import { shellStrings } from './shellStrings'
import mochiImg from '../assets/heroes/mochi/mochi_hero.png'
import peppercornImg from '../assets/heroes/peppercorn/peppercorn_hero.png'
import saffronImg from '../assets/heroes/saffron/saffron_hero.png'

const COMPANIONS = [
  { key: 'mochi',      img: mochiImg,      pos: '72% 30%' },
  { key: 'peppercorn', img: peppercornImg, pos: '50% 38%' },
  { key: 'saffron',    img: saffronImg,    pos: '12% 18%' },
]

// The animals ARE the navigation (Bible08). No text tabs.
export default function CompanionBand({ activePage, onNav }) {
  const { lang, setLang } = useLanguage()
  const t2 = useLocalT(shellStrings)

  return (
    <header className="cband">
      <div className="cband-inner">
        <div className="cband-companions" role="navigation" aria-label="Companions">
          {COMPANIONS.map(c => {
            const active = activePage === c.key
            return (
              <button
                key={c.key}
                className={`cband-btn${active ? ' cband-btn--active' : ''}`}
                onClick={() => onNav(c.key)}
                aria-current={active ? 'page' : undefined}
              >
                <span className="cband-roundel">
                  <img src={c.img} alt="" style={{ objectPosition: c.pos }} />
                </span>
                <span className="cband-name">{t2(`v2.nav.${c.key}.name`)}</span>
                <span className={`cband-line${active ? ' cband-line--show' : ''}`}>
                  {t2(`v2.nav.${c.key}.line`)}
                </span>
              </button>
            )
          })}
        </div>

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
