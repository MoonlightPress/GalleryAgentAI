import { useState, useEffect } from 'react'
import OppCard from './OppCard'
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

export default function OpportunitiesSection() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/api/opportunities')
      .then(r => {
        if (!r.ok) throw new Error(`${r.status}`)
        return r.json()
      })
      .then(setData)
      .catch(e => setError(e.message))
  }, [])

  if (error) {
    return (
      <div className="opps-error">
        <span>🐾</span> Could not reach the Mochi API — is <code>python api.py</code> running?
      </div>
    )
  }

  if (!data) {
    return (
      <div className="opps-loading">
        <span className="opps-paw">🐾</span> Mochi is sorting opportunities…
      </div>
    )
  }

  const { sections, meta } = data

  return (
    <div className="opps-root">
      {SECTION_ORDER.map(key => {
        const items = sections[key] || []
        const m = meta[key] || {}
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
  if (!items.length) return null

  return (
    <section className="opp-section">
      <div className="opp-section-header">
        <div className="opp-section-title-row">
          <span className="opp-section-icon">{icon}</span>
          <h2 className="opp-section-title">{label}</h2>
          <span className="opp-section-count">{items.length}</span>
        </div>
        <p className="opp-section-desc">{description}</p>
      </div>
      <div className="opp-cards-list">
        {items.map(opp => (
          <OppCard key={opp.id} opp={opp} sectionKey={sectionKey} />
        ))}
      </div>
    </section>
  )
}
