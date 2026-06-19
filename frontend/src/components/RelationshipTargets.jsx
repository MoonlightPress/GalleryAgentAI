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
  // No direct channel — make "Look them up" a real web search for the venue.
  const q = encodeURIComponent([c.name, c.city].filter(Boolean).join(' '))
  return `https://www.google.com/search?q=${q}`
}

function patchContact(name, fields) {
  // Best-effort write back to her CRM — silently ignore failures.
  fetch('/api/contacts/update', {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, ...fields }),
  }).catch(() => {})
}

function ContactCard({ c, t, onHide }) {
  const [open, setOpen] = useState(false)
  const [reached, setReached] = useState(false)
  const [toast, setToast] = useState(null)

  const why = c.why_relevant || ''
  const ca = c.crm_analysis || {}
  const summary = ca.contact_summary || ''
  const href = reachHref(c)
  const email = c.contact_email || ''
  const site = c.official_website || c.contact_page || ''
  const submit = c.submission_page || ''
  const notes = c.notes || ''
  const statusKey = `people.status.${c.status}`
  const statusLabel = c.status && t(statusKey) !== statusKey ? t(statusKey) : null

  function markReached() {
    setReached(true)
    patchContact(c.name, {
      last_contacted: new Date().toISOString().slice(0, 10),
      status: 'in_contact',
    })
    setToast(t('people.toast.reached'))
    setTimeout(() => setToast(null), 2500)
  }

  return (
    <div className={`rt-card${reached ? ' rt-card--reached' : ''}`}>
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

      <div className="rt-actions">
        <a className="rt-reach" href={href} target="_blank" rel="noreferrer">
          {t(`people.reach.${c.reachVia}`)}
        </a>
        <button className="rt-details-btn" onClick={() => setOpen(o => !o)}>
          {open ? t('people.hide') : t('people.details')}
        </button>
      </div>

      {open && (
        <div className="rt-details">
          {summary && summary !== why && <p className="rt-summary">{summary}</p>}
          {ca.next_action && (
            <p className="rt-analysis"><strong>{t('people.field.nextAction')}</strong> {ca.next_action}</p>
          )}
          {ca.follow_up_timing && (
            <p className="rt-analysis"><strong>{t('people.field.followUp')}</strong> {ca.follow_up_timing}</p>
          )}
          {ca.risk_notes && (
            <p className="rt-analysis rt-risk"><strong>{t('people.field.risk')}</strong> {ca.risk_notes}</p>
          )}
          <div className="rt-channels">
            {email && <a href={`mailto:${email}`} className="rt-channel">✉ {email}</a>}
            {site && <a href={site} target="_blank" rel="noreferrer" className="rt-channel">🔗 {site.replace(/^https?:\/\//, '')}</a>}
            {submit && <a href={submit} target="_blank" rel="noreferrer" className="rt-channel">📝 {t('people.field.submit')}</a>}
          </div>
          {notes && <p className="rt-note"><strong>{t('people.field.notes')}:</strong> {notes}</p>}
          {c.last_contacted && (
            <p className="rt-meta">{t('people.field.lastContacted')}: {c.last_contacted}</p>
          )}
        </div>
      )}

      <div className="rt-feedback">
        <button
          className={`rt-fb-btn${reached ? ' rt-fb-btn--on' : ''}`}
          onClick={markReached}
        >
          ✓ {t('people.act.reached')}
        </button>
        <button className="rt-fb-btn rt-fb-btn--hide" onClick={() => onHide?.(c.name)}>
          ✕ {t('people.act.notForMe')}
        </button>
        {toast && <span className="rt-toast">{toast}</span>}
      </div>
    </div>
  )
}

export default function RelationshipTargets() {
  const { t } = useLanguage()
  const [contacts, setContacts] = useState(null)
  const [shown, setShown] = useState(PAGE_SIZE)
  const [hidden, setHidden] = useState(() => new Set())

  useEffect(() => {
    let alive = true
    fetch('/api/contacts')
      .then(r => (r.ok ? r.json() : Promise.reject(new Error('bad response'))))
      .then(d => { if (alive) setContacts(Array.isArray(d) ? d : []) })
      .catch(() => { if (alive) setContacts([]) })
    return () => { alive = false }
  }, [])

  if (contacts === null) return null
  const targets = prepareRelationshipTargets(contacts).filter(c => !hidden.has(c.name))
  if (!targets.length) return null

  const visible = targets.slice(0, shown)
  const remaining = targets.length - shown

  function hide(name) {
    setHidden(prev => new Set([...prev, name]))
  }

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
          <ContactCard key={`${c.name || 'c'}-${i}`} c={c} t={t} onHide={hide} />
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
