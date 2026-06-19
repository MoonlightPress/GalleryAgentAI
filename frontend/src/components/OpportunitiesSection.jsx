import { useState, useEffect } from 'react'
import OppCard from './OppCard'
import OppDetailPanel from './OppDetailPanel'
import './OpportunitiesSection.css'
import { useLanguage } from '../i18n/LanguageContext'
import {
  feedbackSignalsFromActions,
  rankOpportunities,
  strongestPicks,
} from '../utils/recommendationQuality'

const SECTION_ORDER = [
  'immediate_best_moves',
  'open_calls',
  'publication_editorial',
  'competitions_awards',
  'zines_and_print',
  'relationship_targets',
  'watch_list',
]

const SECTION_ICONS = {
  immediate_best_moves:  '⭐',
  open_calls:            '📅',
  publication_editorial: '✏️',
  competitions_awards:   '🏆',
  zines_and_print:       '📚',
  relationship_targets:  '🌸',
  watch_list:            '👁',
}

const PAGE_SIZE = 6   // reveal in small batches, not all at once

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
  const [feedbackActions, setFeedbackActions] = useState({})
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
  const feedbackSignals = feedbackSignalsFromActions(feedbackActions)

  // Collect press targets from all sections
  const pressItems = Object.values(sections)
    .flat()
    .filter(isPressTarget)
  const actionSections = Object.fromEntries(
    Object.entries(sections).map(([key, items]) => [
      key,
      (items || []).filter(o => !isPressTarget(o)),
    ])
  )
  const picks = strongestPicks(actionSections, 6, feedbackSignals)

  function handleFeedback(opp, action) {
    setFeedbackActions(prev => {
      const next = { ...prev }
      if (!action) delete next[opp.id]
      else next[opp.id] = { id: opp.id, category: opp.category, action }
      return next
    })
  }

  return (
    <div className="opps-root">
      <StrongestPicksSection
        items={picks}
        feedbackSignals={feedbackSignals}
        onFeedback={handleFeedback}
      />
      {SECTION_ORDER.map(key => {
        const items = actionSections[key] || []
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
            feedbackSignals={feedbackSignals}
            onFeedback={handleFeedback}
          />
        )
      })}
      <PressSection items={pressItems} />
    </div>
  )
}

// ── Press & Visibility section ────────────────────────────────────────────────

function StrongestPicksSection({ items, feedbackSignals, onFeedback }) {
  const [activeId, setActiveId] = useState(null)
  const { t } = useLanguage()
  const visible = items.filter(o => !feedbackSignals.hiddenIds?.has(o.id))
  const activeOpp = visible.find(o => o.id === activeId) || null

  if (!visible.length) return null

  function handleSuppressed(id) {
    setActiveId(prev => prev === id ? null : prev)
  }

  return (
    <section id="mochi_strongest_picks" className="opp-section opp-section--strongest">
      <div className="opp-section-header">
        <div className="opp-section-title-row">
          <span className="opp-section-icon">✦</span>
          <h2 className="opp-section-title">{t('opps.strongest.title')}</h2>
          <span className="opp-section-count">{visible.length}</span>
        </div>
        <p className="opp-section-desc">{t('opps.strongest.desc')}</p>
      </div>

      <div className="opp-grid opp-grid--strongest">
        {visible.map(opp => (
          <OppCard
            key={opp.id}
            opp={{ ...opp, _section: opp.recommendation.sourceSection }}
            isOpen={opp.id === activeId}
            onDetails={() => setActiveId(prev => prev === opp.id ? null : opp.id)}
            onSuppressed={handleSuppressed}
            onFeedback={onFeedback}
          />
        ))}
      </div>

      {activeOpp && (
        <OppDetailPanel
          opp={activeOpp}
          onClose={() => setActiveId(null)}
        />
      )}
    </section>
  )
}

function PressCard({ opp }) {
  const [expanded, setExpanded] = useState(false)
  const { t, lang } = useLanguage()
  const loc = (field) => {
    if (lang === 'zh' && opp[field + '_zh']) return opp[field + '_zh']
    if (lang === 'ja' && opp[field + '_ja']) return opp[field + '_ja']
    if (lang === 'en' && opp[field + '_en']) return opp[field + '_en']
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
  const what    = loc('one_sentence') || loc('summary') || ''
  const why     = loc('why_it_fits') || opp.why_this_fits_short || ''
  const strategy   = opp.relationship_note || ''
  const submission = opp.submission_strategy || ''
  const lead       = opp.recommended_body_of_work || ''
  const bullets = Array.isArray(opp.three_bullets) ? opp.three_bullets.filter(Boolean) : []
  const contact = opp.contact || ''
  const website = opp.official_website || opp.source_url || ''
  const hasDetail = strategy || submission || lead || bullets.length > 0 || contact

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
            {what && <p className="press-card-summary">{what}</p>}
            {why && why !== what && (
              <p className="press-card-summary" style={{ color: 'var(--gold, #a07c2e)', fontStyle: 'italic' }}>{why}</p>
            )}
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

      {hasDetail && (
        <div className="press-card-expand">
          <button
            className="press-expand-btn"
            onClick={() => setExpanded(v => !v)}
          >
            {expanded ? t('people.hide') : t('people.details')}
          </button>
          {expanded && (
            <div className="press-expand-content">
              {strategy && <p className="press-note"><strong>{t('press.strategy')}</strong> {strategy}</p>}
              {submission && <p className="press-note"><strong>{t('press.submission')}</strong> {submission}</p>}
              {lead && <p className="press-note"><strong>{t('press.whatToLead')}</strong> {lead}</p>}
              {bullets.length > 0 && (
                <ul className="press-bullets" style={{ margin: '6px 0 0', paddingLeft: '18px', fontSize: '0.85rem', lineHeight: 1.5 }}>
                  {bullets.map((b, i) => <li key={i}>{b}</li>)}
                </ul>
              )}
              {contact && (
                <p className="press-contact"><strong>{t('press.contact')}</strong>{contact}</p>
              )}
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

function OppSection({ sectionKey, label, description, icon, items, feedbackSignals, onFeedback }) {
  const [shown, setShown]           = useState(PAGE_SIZE)
  const [activeId, setActiveId]     = useState(null)
  const [suppressed, setSuppressed] = useState(new Set())
  const { t } = useLanguage()
  const sectionLabel = t(`section.${sectionKey}.label`) || label
  const sectionDesc  = t(`section.${sectionKey}.desc`)  || description

  const ranked    = rankOpportunities(items, sectionKey, feedbackSignals)
  const filtered  = ranked.filter(o => !suppressed.has(o.id) && !feedbackSignals.hiddenIds?.has(o.id))
  const visible   = filtered.slice(0, shown)
  const remaining = filtered.length - shown
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
          <h2 className="opp-section-title">{sectionLabel}</h2>
          <span className="opp-section-count">{filtered.length}</span>
        </div>
        <p className="opp-section-desc">{sectionDesc}</p>
      </div>

      <div className="opp-section-brief">
        <span>{t('opps.browseHint')}</span>
        <span className="opp-section-visible">
          {t('opps.showingCount', { shown: visible.length, total: filtered.length })}
        </span>
        {suppressed.size > 0 && (
          <span className="opp-section-hidden">
            {t('opps.hiddenCount', { n: suppressed.size })}
          </span>
        )}
      </div>

      {/* Card grid */}
      <div className="opp-grid">
        {visible.map(opp => (
          <OppCard
            key={opp.id}
            opp={{ ...opp, _section: sectionKey }}
            isOpen={opp.id === activeId}
            onDetails={() => handleDetails(opp)}
            onSuppressed={handleSuppressed}
            onFeedback={onFeedback}
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

      {/* Show more — reveal in batches of 9, never all 221 at once */}
      {remaining > 0 && (
        <button
          className="opp-show-more"
          onClick={() => setShown(s => s + PAGE_SIZE)}
        >
          {t('opps.showMoreCount', { n: Math.min(PAGE_SIZE, remaining) })}
        </button>
      )}
      {shown > PAGE_SIZE && (
        <button
          className="opp-show-more opp-show-less"
          onClick={() => setShown(PAGE_SIZE)}
        >
          {t('opps.showLess')}
        </button>
      )}
    </section>
  )
}
