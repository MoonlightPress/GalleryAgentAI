import './Nav.css'
import { useLanguage } from '../i18n/LanguageContext'
import { LANGUAGES, LANGUAGE_LABELS } from '../i18n/translations'

function scrollTo(id) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

// Top-level companion switcher + language toggle. Sits before the intro on every
// page (matches Saffron's layout). Section navigation is the separate QuickNav bar.
export default function Nav({ activePage, onNav }) {
  const { t, lang, setLang } = useLanguage()

  const COMPANIONS = [
    { label: t('nav.discover'), key: 'discover' },
    { label: t('nav.observe'),  key: 'observe'  },
    { label: t('nav.refine'),   key: 'refine'   },
  ]

  return (
    <nav className="site-nav">
      <div className="companion-row">
        {COMPANIONS.map(c => (
          <button
            key={c.key}
            className={`companion-btn${activePage === c.key ? ' companion-btn--active' : ''}`}
            onClick={() => onNav(c.key)}
          >
            {c.label}
          </button>
        ))}

        <div className="lang-toggle">
          {LANGUAGES.map((code, i) => (
            <span key={code} className="lang-toggle-group">
              <button
                className={`lang-btn${lang === code ? ' lang-btn--active' : ''}`}
                onClick={() => setLang(code)}
              >
                {LANGUAGE_LABELS[code]}
              </button>
              {i < LANGUAGES.length - 1 && <span className="lang-sep">·</span>}
            </span>
          ))}
        </div>
      </div>
    </nav>
  )
}

// Discover-page section nav — a sticky bar that sits below the intro and follows on
// scroll, mirroring Saffron's section tabs. Each entry jumps to a real section id.
export function QuickNav() {
  const { t } = useLanguage()
  const items = [
    { label: t('nav.quick.bestMoves'),    target: 'immediate_best_moves'  },
    { label: t('nav.quick.openCalls'),    target: 'open_calls'            },
    { label: t('nav.quick.publication'),  target: 'publication_editorial' },
    { label: t('nav.quick.competitions'), target: 'competitions_awards'   },
    { label: t('nav.quick.zines'),        target: 'zines_and_print'       },
    { label: t('nav.quick.venues'),       target: 'relationship_targets'  },
    { label: t('nav.quick.watchList'),    target: 'watch_list'            },
    { label: t('nav.quick.press'),        target: 'press_visibility'      },
    { label: t('nav.quick.people'),       target: 'relationships'         },
  ]
  return (
    <div className="quick-nav-bar">
      {items.map((item, i) => (
        <span key={item.label} className="quick-nav-group">
          <button className="quick-nav-item" onClick={() => scrollTo(item.target)}>
            {item.label}
          </button>
          {i < items.length - 1 && <span className="quick-nav-sep">·</span>}
        </span>
      ))}
    </div>
  )
}
