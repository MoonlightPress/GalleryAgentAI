import { useState, useEffect } from 'react'
import OppCard from './OppCard'
import OppDetailPanel from './OppDetailPanel'
import './OpportunitiesSection.css'
import { useLanguage } from '../i18n/LanguageContext'

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
  const { t } = useLanguage()

  useEffect(() => {
    fetch('/api/opportunities')
      .then(r => { if (!r.ok) throw new Error(`${r.status}`); return r.json() })
      .then(setData)
      .catch(e => setError(e.message))
  }, [])

  if (error) return (
    <div className="opps-error">
      🐾 {t('opps.error')}
    </div>
  )

  if (!data) return (
    <div className="opps-loading">
      <span className="opps-paw">🐾</span> {t('opps.loading')}
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
  const [showAll, setShowAll]       = useState(false)
  const [activeId, setActiveId]     = useState(null)
  const [suppressed, setSuppressed] = useState(new Set())
  const { t } = useLanguage()

  const filtered  = items.filter(o => !suppressed.has(o.id))
  const visible   = showAll ? filtered : filtered.slice(0, GRID_PAGE)
  const remaining = filtered.length - GRID_PAGE
  const activeOpp = filtered.find(o => o.id === activeId) || null

  function handleDetails(opp) {
    setActiveId(prev => prev === opp.id ? null : opp.id)
  }

  function handleSuppressed(id) {
    setSuppressed(prev => new Set([...prev, id]))
    setActiveId(prev => prev === id ? null : prev)
  }

  return (
    <section id={sectionKey} className="opp-section">
      {/* Section header */}
      <div className="opp-section-header">
        <div className="opp-section-title-row">
          <span className="opp-section-icon">{icon}</span>
          <h2 className="opp-section-title">{label}</h2>
          <span className="opp-section-count">{filtered.length}</span>
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
            onSuppressed={handleSuppressed}
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
          {t('opps.showMore')} · {t('opps.moreCount', { n: remaining })}
        </button>
      )}
    </section>
  )
}
