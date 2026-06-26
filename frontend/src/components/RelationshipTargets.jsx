import { useState, useEffect, useRef } from 'react'
import './RelationshipTargets.css'
import { useLanguage } from '../i18n/LanguageContext'
import { tfb } from '../i18n/translations'
import { prepareRelationshipTargets } from '../utils/relationshipTargets'
import { cardsPerBatch } from '../utils/layout'
import { SectionHeader } from './OpportunitiesSection'

const PAGE_SIZE = cardsPerBatch()   // 6 on desktop (3 cols), 4 on smaller screens (2/1 cols)

// Hand-made watercolor icons (public/icons/*.webp under Vite's /mochi/ base),
// referenced the same way OppCard/OpportunitiesSection do. mix-blend-mode in the
// CSS melts the cream backdrop into the light card so no square edge shows.
const ICON_BASE = `${import.meta.env.BASE_URL}icons/`
const iconUrl = (name) => `${ICON_BASE}${name}.webp`

// Render a watercolor section/header icon as an <img>, matching <SectionIcon> in
// OpportunitiesSection. Used for the People section header and the per-card glyph.
function PeopleIcon({ className }) {
  return (
    <img
      className={`${className} ${className}--img`}
      src={iconUrl('ic_people')}
      alt=""
      aria-hidden="true"
      loading="lazy"
      width="40"
      height="40"
    />
  )
}

// Watercolor icons (public/icons/ic_*.webp), NOT emoji — matches the rest of Mochi.
const TYPE_ICON = {
  gallery: 'ic_gallery', gallery_small: 'ic_gallery', gallery_event: 'ic_gallery',
  cafe_gallery: 'ic_cafe', bookstore_gallery: 'ic_books', bookstore_event: 'ic_books',
  bookshop: 'ic_books', book_publishing: 'ic_books', book_publisher: 'ic_books',
  zine_shop: 'ic_books', zine_shop_consignment: 'ic_books', zine_print: 'ic_books',
  artist_space: 'ic_institution', event_space: 'ic_institution', press_target: 'ic_press', fair: 'ic_fair',
}

function humanizeType(type) {
  return String(type || '').replace(/_/g, ' ').replace(/\b\w/g, ch => ch.toUpperCase())
}

// ── Priority grouping ────────────────────────────────────────────────────────
// 52 contacts in one list is "forever to scroll" (Scott 2026-06-25). Split into
// scannable priority subsections — high relationships first — each collapsible
// with its own show-more, so she can jump instead of scroll. Priority is the
// cleanest axis in the data (high/medium/low, already the sort key) and the most
// decision-useful: "who do I reach out to first."
const PRIORITY_ORDER = ['high', 'medium', 'low']

// English fallbacks for the group labels; tfb() upgrades to a real translation
// automatically once a `people.group.*` key is added to translations.js.
const GROUP_FALLBACK = {
  high:   'High priority',
  medium: 'Worth reaching out to',
  low:    'Keep on the radar',
}

function priorityKey(c = {}) {
  const p = String((c.crm_analysis && c.crm_analysis.priority) || c.priority || '').toLowerCase()
  return p === 'high' || p === 'medium' || p === 'low' ? p : 'low'
}

// Group prepared (already priority-sorted) targets into non-empty subsections,
// preserving within-group order. Anything unrecognized lands in 'low' so it is
// never silently dropped.
function groupByPriority(targets) {
  const buckets = { high: [], medium: [], low: [] }
  for (const c of targets) buckets[priorityKey(c)].push(c)
  return PRIORITY_ORDER
    .map(key => ({ key, items: buckets[key] }))
    .filter(g => g.items.length > 0)
}

function nameSearchHref(c) {
  const q = encodeURIComponent([c.name, c.city].filter(Boolean).join(' '))
  return `https://www.google.com/search?q=${q}`
}

function reachHref(c) {
  if (c.reachVia === 'email') return `mailto:${c.contact_email}`
  if (c.reachVia === 'website') return c.official_website || c.contact_page || c.submission_page || null
  // No direct channel — make "Look them up" a real web search for the venue.
  return nameSearchHref(c)
}

// Best link to put on the contact's name so the card is actionable at a glance.
// Prefer a real website/url, then a mailto, else fall back to a name web search.
function nameHref(c) {
  const site = c.website || c.url || c.official_website || c.contact_page || c.submission_page
  if (site) return site
  if (c.contact_email) return `mailto:${c.contact_email}`
  return nameSearchHref(c)
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
  const { lang } = useLanguage()
  const [open, setOpen] = useState(false)
  const [reached, setReached] = useState(false)
  const [toast, setToast] = useState(null)
  const detailsRef = useRef(null)

  useEffect(() => {
    if (open) {
      requestAnimationFrame(() => {
        detailsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' })
      })
    }
  }, [open])

  // Localize generated CRM prose (contact_translation_engine writes _zh/_ja siblings).
  const loc = (obj, field) => {
    if (lang === 'zh' && obj[field + '_zh']) return obj[field + '_zh']
    if (lang === 'ja' && obj[field + '_ja']) return obj[field + '_ja']
    return obj[field]
  }

  const ca = c.crm_analysis || {}
  const why = loc(c, 'why_relevant') || ''
  const summary = loc(ca, 'contact_summary') || ''
  const href = reachHref(c)
  const nameLink = nameHref(c)
  const email = c.contact_email || ''
  const site = c.official_website || c.contact_page || ''
  const submit = c.submission_page || ''
  const notes = loc(c, 'notes') || ''
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
        {TYPE_ICON[c.type]
          ? <img className="rt-card-icon rt-card-icon--img" src={iconUrl(TYPE_ICON[c.type])} alt="" aria-hidden="true" loading="lazy" width="40" height="40" />
          : <PeopleIcon className="rt-card-icon" />}
        <h3 className="rt-card-name">
          <a className="rt-name-link" href={nameLink} target="_blank" rel="noreferrer">
            {c.name} <span className="rt-name-arrow" aria-hidden="true">↗</span>
          </a>
        </h3>
      </div>

      <div className="rt-pills">
        {c.type && <span className="rt-pill">{t(`cat.${c.type}`) !== `cat.${c.type}` ? t(`cat.${c.type}`) : humanizeType(c.type)}</span>}
        {c.city && <span className="rt-pill rt-pill--loc">{c.city}</span>}
        {statusLabel && <span className={`rt-pill rt-status rt-status--${c.status}`}>{statusLabel}</span>}
      </div>

      {why && <p className="rt-why">{why}</p>}

      <div className="rt-actions">
        <a className="rt-reach" href={href} target="_blank" rel="noreferrer">
          {t(`people.reach.${c.reachVia}`)}
        </a>
        <button className="opp-btn-details" onClick={() => setOpen(o => !o)}>
          {open ? t('people.hide') : t('people.details')}
        </button>
      </div>

      {open && (
        <div className="rt-details" ref={detailsRef}>
          {summary && summary !== why && <p className="rt-summary">{summary}</p>}
          {ca.next_action && (
            <p className="rt-analysis"><strong>{t('people.field.nextAction')}</strong> {loc(ca, 'next_action')}</p>
          )}
          {ca.follow_up_timing && (
            <p className="rt-analysis"><strong>{t('people.field.followUp')}</strong> {loc(ca, 'follow_up_timing')}</p>
          )}
          {ca.risk_notes && (
            <p className="rt-analysis rt-risk"><strong>{t('people.field.risk')}</strong> {loc(ca, 'risk_notes')}</p>
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

// One collapsible priority subsection: a clickable header (label + count +
// chevron) over its own card grid with a per-group show-more. High priority is
// open by default; the rest start collapsed so the whole section is 3 scannable
// rows she can jump between instead of 50 cards to scroll past.
function PriorityGroup({ groupKey, items, t, onHide, defaultOpen }) {
  const [open, setOpen] = useState(defaultOpen)
  const [shown, setShown] = useState(PAGE_SIZE)

  const visible = items.slice(0, shown)
  const remaining = items.length - shown
  const label = tfb(t, `people.group.${groupKey}`, GROUP_FALLBACK[groupKey] || groupKey)
  const panelId = `rt-group-${groupKey}`

  return (
    <div className={`rt-group rt-group--${groupKey}`}>
      <button
        type="button"
        className={`rt-group-head${open ? ' rt-group-head--open' : ''}`}
        aria-expanded={open}
        aria-controls={panelId}
        onClick={() => setOpen(o => !o)}
      >
        <span className={`rt-group-dot rt-group-dot--${groupKey}`} aria-hidden="true" />
        <span className="rt-group-label">{label}</span>
        <span className="rt-group-count">{items.length}</span>
        <span className="rt-group-chevron" aria-hidden="true">{open ? '▾' : '▸'}</span>
      </button>

      {open && (
        <div id={panelId} className="rt-group-body">
          <div className="rt-grid">
            {visible.map((c, i) => (
              <ContactCard key={`${c.name || 'c'}-${i}`} c={c} t={t} onHide={onHide} />
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
        </div>
      )}
    </div>
  )
}

export default function RelationshipTargets() {
  const { t } = useLanguage()
  const [contacts, setContacts] = useState(null)
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

  const groups = groupByPriority(targets)

  function hide(name) {
    setHidden(prev => new Set([...prev, name]))
  }

  return (
    <section id="relationships" className="opp-section rt-section">
      <SectionHeader title={t('people.title')} subtitle={t('people.intro')} />

      <div className="rt-groups">
        {groups.map((g, idx) => (
          <PriorityGroup
            key={g.key}
            groupKey={g.key}
            items={g.items}
            t={t}
            onHide={hide}
            defaultOpen={idx === 0}   // strongest group open; the rest collapsed to scan
          />
        ))}
      </div>
      {/* A little reward at the very end of the page: her favorites (Bread Thief,
          Chiikawa), if she scrolls this far. */}
      <div className="rt-reward" aria-hidden="true">
        <img
          className="rt-reward-img"
          src={`${import.meta.env.BASE_URL}headers/people_reward.webp`}
          alt=""
          loading="lazy"
        />
      </div>
    </section>
  )
}
