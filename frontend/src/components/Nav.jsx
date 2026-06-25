import './Nav.css'
import { useLanguage } from '../i18n/LanguageContext'
import { LANGUAGES, LANGUAGE_LABELS } from '../i18n/translations'

function scrollTo(id) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

// Companion names, per language. The tabs are verbs (发现/观察/对话) but each page's
// companion introduces herself by name; pairing the two ("观察 · 山楂") closes the
// mental-model seam the review flagged (T4.3). Names are taken from the existing
// intro/status strings already shipped in the i18n: 麻薯/モチ/Mochi, 山楂/サフラン/
// Saffron, 胡椒粒/ペッパーコーン/Peppercorn.
const COMPANION_NAMES = {
  zh: { discover: '麻薯',  observe: '山楂',     refine: '胡椒粒'       },
  ja: { discover: 'モチ',  observe: 'サフラン', refine: 'ペッパーコーン' },
  en: { discover: 'Mochi', observe: 'Saffron',  refine: 'Peppercorn'   },
}

// Top-level companion switcher + language toggle. Sits before the intro on every
// page (matches Saffron's layout). Section navigation is the separate QuickNav bar.
export default function Nav({ activePage, onNav }) {
  const { t, lang, setLang } = useLanguage()
  const names = COMPANION_NAMES[lang] || COMPANION_NAMES.en

  const COMPANIONS = [
    { label: t('nav.discover'), name: names.discover, key: 'discover' },
    { label: t('nav.observe'),  name: names.observe,  key: 'observe'  },
    { label: t('nav.refine'),   name: names.refine,   key: 'refine'   },
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
            <span className="companion-btn-verb">{c.label}</span>
            <span className="companion-btn-sep" aria-hidden="true"> · </span>
            <span className="companion-btn-name">{c.name}</span>
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
