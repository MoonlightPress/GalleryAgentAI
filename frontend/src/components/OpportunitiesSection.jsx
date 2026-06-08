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

function isPressTarget(opp) {
  return (
    opp.opportunity_type === 'press_target' ||
    opp.exclusive_primary_bucket === 'press_target' ||
    opp.category === 'press_target'
  )
}

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

  // Collect press targets from all sections
  const pressItems = Object.values(sections)
    .flat()
    .filter(isPressTarget)

  return (
    <div className="opps-root">
      {SECTION_ORDER.map(key => {
        const items = (sections[key] || []).filter(o => !isPressTarget(o))
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
      <PressSection items={pressItems} />
    </div>
  )
}

// ── Press & Visibility section ────────────────────────────────────────────────

function PressCard({ opp }) {
  const [expanded, setExpanded] = useState(false)
  const { t, lang } = useLanguage()
  const loc = (field) => {
    if (lang === 'zh' && opp[field + '_zh']) return opp[field + '_zh']
    if (lang === 'ja' && opp[field + '_ja']) return opp[field + '_ja']
    return opp[field]
  }

  const actionType = (opp.action_type || '').toLowerCase()
  const badgeKey   = actionType === 'relationship'
    ? 'press.action.relationship'
    : 'press.action.pitch'
  const badgeClass = actionType === 'relationship'
    ? 'press-badge press-badge--rel'
    : 'press-badge press-badge--pitch'

  const name    = loc('name') || opp.title || ''
  const summary = loc('summary') || opp.one_sentence || ''
  const contact = opp.contact || ''
  const note    = opp.relationship_note || ''
  const website = opp.official_website || opp.source_url || ''

  return (
    <div className="press-card">
      <div className="press-card-top">
        <div className="press-card-left">
          <span className="press-icon">📰</span>
          <div className="press-card-body">
            <div className="press-card-name-row">
              <span className="press-card-name">{name}</span>
              <span className={badgeClass}>{t(badgeKey)}</span>
            </div>
            {summary && <p className="press-card-summary">{summary}</p>}
          </div>
        </div>
        {website && (
          <a
            className="press-card-link"
            href={website}
            target="_blank"
            rel="noopener noreferrer"
          >
            ↗
          </a>
        )}
      </div>

      {(contact || note) && (
        <div className="press-card-expand">
          <button
            className="press-expand-btn"
            onClick={() => setExpanded(v => !v)}
          >
            {expanded ? '▲ ' : '▶ '}{t('press.howToPitch')}
          </button>
          {expanded && (
            <div className="press-expand-content">
              {contact && (
                <p className="press-contact"><strong>联系方式：</strong>{contact}</p>
              )}
              {note && <p className="press-note">{note}</p>}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function PressSection({ items }) {
  const { t } = useLanguage()

  return (
    <section id="press_visibility" className="opp-section press-section">
      <div className="opp-section-header">
        <div className="opp-section-title-row">
          <span className="opp-section-icon">📰</span>
          <h2 className="opp-section-title">{t('press.section.title')}</h2>
          {items.length > 0 && (
            <span className="opp-section-count">{items.length}</span>
          )}
        </div>
        <p className="opp-section-desc">
          {t('press.section.desc')}
        </p>
      </div>

      {items.length === 0 ? (
        <p className="press-empty">{t('press.empty')}</p>
      ) : (
        <div className="press-grid">
          {items.map((opp, i) => (
            <PressCard key={opp.id || opp.title || i} opp={opp} />
          ))}
        </div>
      )}
    </section>
  )
}

// ── Opportunity section ───────────────────────────────────────────────────────

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
