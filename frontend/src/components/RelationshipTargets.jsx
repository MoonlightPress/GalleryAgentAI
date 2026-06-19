import { useState, useEffect } from 'react'
import './RelationshipTargets.css'
import { useLanguage } from '../i18n/LanguageContext'
import { prepareRelationshipTargets } from '../utils/relationshipTargets'

function humanizeType(type) {
  return String(type || '')
    .replace(/_/g, ' ')
    .replace(/\b\w/g, ch => ch.toUpperCase())
}

function reachHref(c) {
  if (c.reachVia === 'email') return `mailto:${c.contact_email}`
  if (c.reachVia === 'website') {
    return c.official_website || c.contact_page || c.submission_page || null
  }
  return null
}

function ContactCard({ c, t }) {
  const why = c.why_relevant || (c.crm_analysis && c.crm_analysis.contact_summary) || ''
  const href = reachHref(c)
  const statusKey = `people.status.${c.status}`
  const statusLabel = c.status && t(statusKey) !== statusKey ? t(statusKey) : null

  return (
    <div className="rt-card">
      <div className="rt-card-head">
        <h3 className="rt-card-name">{c.name}</h3>
        {statusLabel && (
          <span className={`rt-status rt-status--${c.status}`}>{statusLabel}</span>
        )}
      </div>

      <div className="rt-pills">
        {c.type && <span className="rt-pill">{humanizeType(c.type)}</span>}
        {c.city && <span className="rt-pill rt-pill--loc">{c.city}</span>}
      </div>

      {why && <p className="rt-why">{why}</p>}

      <div className="rt-actions">
        {href ? (
          <a className="rt-reach" href={href} target="_blank" rel="noreferrer">
            {t(`people.reach.${c.reachVia}`)}
          </a>
        ) : (
          <span className="rt-reach rt-reach--none">{t('people.reach.none')}</span>
        )}
      </div>
    </div>
  )
}

export default function RelationshipTargets() {
  const { t } = useLanguage()
  const [contacts, setContacts] = useState(null) // null = loading

  useEffect(() => {
    let alive = true
    fetch('/api/contacts')
      .then(r => (r.ok ? r.json() : Promise.reject(new Error('bad response'))))
      .then(d => { if (alive) setContacts(Array.isArray(d) ? d : []) })
      .catch(() => { if (alive) setContacts([]) })
    return () => { alive = false }
  }, [])

  if (contacts === null) {
    return (
      <section className="rt-section">
        <p className="rt-loading">{t('people.intro')}</p>
      </section>
    )
  }

  const targets = prepareRelationshipTargets(contacts)

  if (!targets.length) {
    return (
      <section className="rt-section">
        <p className="rt-empty">{t('people.empty')}</p>
      </section>
    )
  }

  return (
    <section className="rt-section">
      <header className="rt-head">
        <h2 className="rt-title">{t('people.title')}</h2>
        <p className="rt-intro">{t('people.intro')}</p>
      </header>
      <div className="rt-grid">
        {targets.map((c, i) => (
          <ContactCard key={`${c.name || 'c'}-${i}`} c={c} t={t} />
        ))}
      </div>
    </section>
  )
}
