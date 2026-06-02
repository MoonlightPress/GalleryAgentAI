import { useState, useEffect } from 'react'
import OppCard from './OppCard'
import OppDetailPanel from './OppDetailPanel'
import './OpportunitiesSection.css'

const SECTION_ORDER = [
  'immediate_best_moves',
  'open_calls',
  'zines_and_print',
  'relationship_targets',
  'watch_list',
]

const SECTION_ICONS = {
  immediate_best_moves: '⭐',
  open_calls:           '📅',
  zines_and_print:      '📚',
  relationship_targets: '🌸',
  watch_list:           '👁',
}

const GRID_PAGE = 3

export default function OpportunitiesSection() {
  const [data, setData]   = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/api/opportunities')
      .then(r => { if (!r.ok) throw new Error(`${r.status}`); return r.json() })
      .then(setData)
      .catch(e => setError(e.message))
  }, [])

  if (error) return (
    <div className="opps-error">
      🐾 Could not reach the Mochi API — is <code>python api.py</code> running?
    </div>
  )

  if (!data) return (
    <div className="opps-loading">
      <span className="opps-paw">🐾</span> Mochi is sorting opportunities…
    </div>
  )

  const { sections, meta } = data

  return (
    <div className="opps-root">
      {SECTION_ORDER.map(key => {
        const items = sections[key] || []
        const m = meta[key] || {}
        if (!items.length) return null
        return (
          <OppSection
            key={key}
            sectionKey={key}
            label={m.label || key}
            description={m.description || ''}
            icon={SECTION_ICONS[key] || '•'}
            items={items}
          />
        )
      })}
    </div>
  )
}

function OppSection({ sectionKey, label, description, icon, items }) {
  const [showAll, setShowAll]     = useState(false)
  const [activeId, setActiveId]   = useState(null)

  const visible   = showAll ? items : items.slice(0, GRID_PAGE)
  const remaining = items.length - GRID_PAGE
  const activeOpp = items.find(o => o.id === activeId) || null

  function handleDetails(opp) {
    setActiveId(prev => prev === opp.id ? null : opp.id)
  }

  return (
    <section id={sectionKey} className="opp-section">
      {/* Section header */}
      <div className="opp-section-header">
        <div className="opp-section-title-row">
          <span className="opp-section-icon">{icon}</span>
          <h2 className="opp-section-title">{label}</h2>
          <span className="opp-section-count">{items.length}</span>
        </div>
        <p className="opp-section-desc">{description}</p>
      </div>

      {/* 3-column card grid */}
      <div className="opp-grid">
        {visible.map(opp => (
          <OppCard
            key={opp.id}
            opp={{ ...opp, _section: sectionKey }}
            isOpen={opp.id === activeId}
            onDetails={() => handleDetails(opp)}
          />
        ))}
      </div>

      {/* Detail panel — full width, below the grid */}
      {activeOpp && (
        <OppDetailPanel
          opp={activeOpp}
          onClose={() => setActiveId(null)}
        />
      )}

      {/* Show more */}
      {!showAll && remaining > 0 && (
        <button
          className="opp-show-more"
          onClick={() => setShowAll(true)}
        >
          Show more · {remaining} more
        </button>
      )}
    </section>
  )
}
