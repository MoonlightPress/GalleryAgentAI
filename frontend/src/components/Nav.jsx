import './Nav.css'

const COMPANIONS = [
  { label: 'Discover', key: 'discover', active: true  },
  { label: 'Refine',   key: 'refine',   active: false },
  { label: 'Observe',  key: 'observe',  active: false },
]

const QUICK_NAV = [
  { label: 'Immediate Best Moves', target: 'immediate_best_moves' },
  { label: 'Open Calls',           target: 'open_calls'           },
  { label: 'Zines & Print',        target: 'zines_and_print'      },
  { label: 'Galleries',            target: 'relationship_targets'  },
  { label: 'Cafés',                target: 'relationship_targets'  },
  { label: 'Residencies',          target: 'watch_list'            },
]

function scrollTo(id) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

export default function Nav() {
  return (
    <nav className="site-nav">
      {/* ── Three companion page buttons ── */}
      <div className="companion-row">
        {COMPANIONS.map(c => (
          <button
            key={c.key}
            className={`companion-btn${c.active ? ' companion-btn--active' : ''}`}
          >
            {c.label}
          </button>
        ))}
      </div>

      {/* ── Horizontal category quick-nav ── */}
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
    </nav>
  )
}
