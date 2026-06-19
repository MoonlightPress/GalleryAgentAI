import { useState, useEffect } from 'react'
import './RelationshipTargets.css'
import { useLanguage } from '../i18n/LanguageContext'
import { prepareRelationshipTargets } from '../utils/relationshipTargets'

const PAGE_SIZE = 9

const TYPE_ICON = {
  gallery: '🖼️', gallery_small: '🖼️', gallery_event: '🖼️',
  cafe_gallery: '☕', bookstore_gallery: '📚', bookstore_event: '📚',
  bookshop: '📖', book_publishing: '📖', book_publisher: '📖',
  zine_shop: '📰', zine_shop_consignment: '📰', zine_print: '📰',
  artist_space: '🎨', event_space: '🎨', press_target: '📣', fair: '🎪',
}

function humanizeType(type) {
  return String(type || '').replace(/_/g, ' ').replace(/\b\w/g, ch => ch.toUpperCase())
}

function reachHref(c) {
  if (c.reachVia === 'email') return `mailto:${c.contact_email}`
  if (c.reachVia === 'website') return c.official_website || c.contact_page || c.submission_page || null
  return null
}

function ContactCard({ c, t }) {
  const why = c.why_relevant || ''
  const summary = (c.crm_analysis && c.crm_analysis.contact_summary) || ''
  const href = reachHref(c)
  const statusKey = `people.status.${c.status}`
  const statusLabel = c.status && t(statusKey) !== statusKey ? t(statusKey) : null

  return (
    <div className="rt-card">
      <div className="rt-card-header">
        <span className="rt-card-icon">{TYPE_ICON[c.type] || '🌸'}</span>
        <h3 className="rt-card-name">{c.name}</h3>
      </div>

      <div className="rt-pills">
        {c.type && <span className="rt-pill">{humanizeType(c.type)}</span>}
        {c.city && <span className="rt-pill rt-pill--loc">{c.city}</span>}
        {statusLabel && <span className={`rt-pill rt-status rt-status--${c.status}`}>{statusLabel}</span>}
      </div>

      {why && <p className="rt-why">{why}</p>}
      {summary && summary !== why && <p className="rt-summary">{summary}</p>}

      <div className="rt-actions">
        {href ? (
          <a className="rt-reach" href={href} target="_blank" rel="noreferrer">
            {t(`people.reach.${c.reachVia}`)}
          </a>
        ) : (
          <span className="rt-reach rt-reach--none">{t('people.reach.none')}</span>
        )}
        {c.contact_email && c.reachVia === 'email' && (
          <span className="rt-reach-detail">{c.contact_email}</span>
        )}
      </div>
    </div>
  )
}

export default function RelationshipTargets() {
  const { t } = useLanguage()
  const [contacts, setContacts] = useState(null)
  const [shown, setShown] = useState(PAGE_SIZE)

  useEffect(() => {
    let alive = true
    fetch('/api/contacts')
      .then(r => (r.ok ? r.json() : Promise.reject(new Error('bad response'))))
      .then(d => { if (alive) setContacts(Array.isArray(d) ? d : []) })
      .catch(() => { if (alive) setContacts([]) })
    return () => { alive = false }
  }, [])

  if (contacts === null) return null
  const targets = prepareRelationshipTargets(contacts)
  if (!targets.length) return null

  const visible = targets.slice(0, shown)
  const remaining = targets.length - shown

  return (
    <section id="relationships" className="opp-section rt-section">
      <div className="opp-section-header">
        <div className="opp-section-title-row">
          <span className="opp-section-icon">🌸</span>
          <h2 className="opp-section-title">{t('people.title')}</h2>
          <span className="opp-section-count">{targets.length}</span>
        </div>
        <p className="opp-section-desc">{t('people.intro')}</p>
      </div>

      <div className="rt-grid">
        {visible.map((c, i) => (
          <ContactCard key={`${c.name || 'c'}-${i}`} c={c} t={t} />
        ))}
      </div>

      {remaining > 0 && (
        <button className="opp-show-more" onClick={() => setShown(s => s + PAGE_SIZE)}>
          {t('opps.showMoreCount', { n: Math.min(PAGE_SIZE, remaining) })}
        </button>
      )}
      {shown > PAGE_SIZE && (
        <button className="opp-show-more opp-show-less" onClick={() => setShown(PAGE_SIZE)}>
          {t('opps.showLess')}
        </button>
      )}
    </section>
  )
}
