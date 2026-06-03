import './Nav.css'
import { useLanguage } from '../i18n/LanguageContext'
import { LANGUAGES, LANGUAGE_LABELS } from '../i18n/translations'

function scrollTo(id) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

export default function Nav({ activePage, onNav }) {
  const { t, lang, setLang } = useLanguage()

  const COMPANIONS = [
    { label: t('nav.discover'), key: 'discover' },
    { label: t('nav.observe'),  key: 'observe'  },
    { label: t('nav.refine'),   key: 'refine'   },
  ]

  const QUICK_NAV = [
    { label: t('nav.quick.bestMoves'),   target: 'immediate_best_moves' },
    { label: t('nav.quick.openCalls'),   target: 'open_calls'           },
    { label: t('nav.quick.zines'),       target: 'zines_and_print'      },
    { label: t('nav.quick.galleries'),   target: 'relationship_targets'  },
    { label: t('nav.quick.cafes'),       target: 'relationship_targets'  },
    { label: t('nav.quick.residencies'), target: 'watch_list'            },
  ]

  return (
    <nav className="site-nav">
      {/* ── Companion page buttons + language toggle ── */}
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
              {i < LANGUAGES.length - 1 && (
                <span className="lang-sep">·</span>
              )}
            </span>
          ))}
        </div>
      </div>

      {/* ── Quick-nav only on Discover page ── */}
      {activePage === 'discover' && (
        <div className="quick-nav-row">
          {QUICK_NAV.map((item, i) => (
            <span key={item.label} className="quick-nav-group">
              <button
                className="quick-nav-item"
                onClick={() => scrollTo(item.target)}
              >
                {item.label}
              </button>
              {i < QUICK_NAV.length - 1 && (
                <span className="quick-nav-sep">·</span>
              )}
            </span>
          ))}
        </div>
      )}
    </nav>
  )
}
