// THE RECORD BOOK — one ledger, four tabs: Submissions · Exhibitions ·
// Venues & Contacts · Quick log. Shared visual language, existing endpoints.
import { useState, useEffect } from 'react'
import { useLanguage } from '../../i18n/LanguageContext'
import { useLocalT } from '../../i18n/local'
import { api } from '../../utils/api'
import { strings } from './strings'
import { OutcomeChip, useSaved, Field, tone } from './bits'

const TABS = ['submissions', 'exhibitions', 'venues', 'quicklog']

// ── Submissions tab ────────────────────────────────────────────────────────

const SUB_OUTCOMES = ['pending', 'accepted', 'rejected', 'waitlisted', 'withdrawn']

function SubmissionsTab() {
  const { t } = useLanguage()
  const [items, setItems] = useState([])
  const [form, setForm] = useState({ date: '', venue: '', what: '', outcome: 'pending', notes: '' })
  const [saving, setSaving] = useState(false)
  const [saved, flash] = useSaved()

  useEffect(() => {
    api.submissions().then(d => setItems(Array.isArray(d) ? d : [])).catch(() => {})
  }, [])

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  async function add() {
    if (!form.venue.trim() || !form.what.trim()) return
    setSaving(true)
    try {
      await api.addSubmission({ ...form, date: form.date || new Date().toISOString().slice(0, 10) })
      const updated = await api.submissions()
      setItems(Array.isArray(updated) ? updated : [])
      setForm({ date: '', venue: '', what: '', outcome: 'pending', notes: '' })
      flash()
    } catch { /* keep the form so she can retry */ }
    setSaving(false)
  }

  const sorted = [...items].sort((a, b) => (b.date || '').localeCompare(a.date || ''))

  return (
    <div>
      <p className="small pep-note">{t('pp.sublog.note')}</p>
      <div className="pep-add-row">
        <Field label={t('pp.sublog.date')}>
          <input type="date" className="pep-input" value={form.date} onChange={e => set('date', e.target.value)} />
        </Field>
        <Field label={t('pp.sublog.venue')} wide>
          <input className="pep-input" value={form.venue} onChange={e => set('venue', e.target.value)} placeholder={t('pp.sublog.ph.venue')} />
        </Field>
        <Field label={t('pp.sublog.what')} wide>
          <input className="pep-input" value={form.what} onChange={e => set('what', e.target.value)} placeholder={t('pp.sublog.ph.what')} />
        </Field>
        <Field label={t('pp.sublog.outcome')}>
          <select className="pep-input" value={form.outcome} onChange={e => set('outcome', e.target.value)}>
            {SUB_OUTCOMES.map(o => <option key={o} value={o}>{t('pp.outcome.' + o)}</option>)}
          </select>
        </Field>
        <Field label={t('pp.sublog.notes')} wide>
          <input className="pep-input" value={form.notes} onChange={e => set('notes', e.target.value)} placeholder={t('pp.sublog.ph.notes')} />
        </Field>
        <button className="btn-warm pep-add-btn" onClick={add} disabled={saving || !form.venue.trim() || !form.what.trim()}>
          {saved ? t('pp.sublog.btn.done') : t('pp.sublog.btn')}
        </button>
      </div>

      {sorted.length === 0
        ? <p className="voice small pep-empty-line">{t('pp.sub.sublog.empty')}</p>
        : (
          <ul className="pep-entries">
            {sorted.map((s, i) => (
              <li key={s.id || `${s.date}-${s.venue}-${i}`} className={`pep-entry pep-entry--${tone(s.outcome)}`}>
                <div className="pep-entry-head">
                  <span className="pep-entry-name">{s.venue}</span>
                  <OutcomeChip status={s.outcome} label={t('pp.outcome.' + s.outcome)} />
                  {s.date && <span className="tiny pep-entry-date">{s.date}</span>}
                </div>
                <div className="small">{s.what}</div>
                {s.notes && <div className="small pep-entry-notes">{s.notes}</div>}
              </li>
            ))}
          </ul>
        )}
    </div>
  )
}

// ── Exhibitions tab ────────────────────────────────────────────────────────

const SHOW_TYPES    = ['group', 'solo', 'fair', 'residency_show']
const SHOW_OUTCOMES = ['shown', 'planned', 'cancelled']

function ExhibitionsTab() {
  const { t } = useLanguage()
  const [shows, setShows] = useState([])
  const [form, setForm] = useState({ date: '', name: '', venue: '', type: 'group', outcome: 'shown', notes: '' })
  const [saving, setSaving] = useState(false)
  const [saved, flash] = useSaved()

  useEffect(() => {
    api.exhibitions().then(d => setShows(Array.isArray(d) ? d : [])).catch(() => {})
  }, [])

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  async function add() {
    if (!form.name.trim() && !form.venue.trim()) return
    setSaving(true)
    try {
      await api.addExhibition({ ...form })
      const updated = await api.exhibitions()
      setShows(Array.isArray(updated) ? updated : [])
      setForm({ date: '', name: '', venue: '', type: 'group', outcome: 'shown', notes: '' })
      flash()
    } catch { /* keep form */ }
    setSaving(false)
  }

  async function remove(id) {
    try {
      const r = await fetch(`/api/exhibition_log/${id}`, { method: 'DELETE' })
      if (r.ok) setShows(prev => prev.filter(s => s.id !== id))
    } catch { /* leave the row on network failure */ }
  }

  const sorted = [...shows].sort((a, b) => (b.date || '').localeCompare(a.date || ''))

  return (
    <div>
      <p className="small pep-note">{t('pp.exlog.note')}</p>
      <div className="pep-add-row">
        <Field label={t('pp.exlog.date')}>
          <input type="month" className="pep-input" value={form.date} onChange={e => set('date', e.target.value)} />
        </Field>
        <Field label={t('pp.exlog.name')} wide>
          <input className="pep-input" value={form.name} onChange={e => set('name', e.target.value)} placeholder={t('pp.exlog.ph.name')} />
        </Field>
        <Field label={t('pp.exlog.venue')} wide>
          <input className="pep-input" value={form.venue} onChange={e => set('venue', e.target.value)} placeholder={t('pp.exlog.ph.venue')} />
        </Field>
        <Field label={t('pp.exlog.type')}>
          <select className="pep-input" value={form.type} onChange={e => set('type', e.target.value)}>
            {SHOW_TYPES.map(o => <option key={o} value={o}>{t('pp.showType.' + o)}</option>)}
          </select>
        </Field>
        <Field label={t('pp.exlog.outcome')}>
          <select className="pep-input" value={form.outcome} onChange={e => set('outcome', e.target.value)}>
            {SHOW_OUTCOMES.map(o => <option key={o} value={o}>{t('pp.showOutcome.' + o)}</option>)}
          </select>
        </Field>
        <Field label={t('pp.exlog.notes')} wide>
          <input className="pep-input" value={form.notes} onChange={e => set('notes', e.target.value)} placeholder={t('pp.exlog.ph.notes')} />
        </Field>
        <button className="btn-warm pep-add-btn" onClick={add} disabled={saving || (!form.name.trim() && !form.venue.trim())}>
          {saved ? t('pp.exlog.btn.done') : t('pp.exlog.btn')}
        </button>
      </div>

      <ul className="pep-entries">
        {/* Confirmed first show — system entry, kept from v1 */}
        <li className="pep-entry pep-entry--leaf">
          <div className="pep-entry-head">
            <span className="pep-entry-name">Tide from China Part 1</span>
            <OutcomeChip status="shown" label={t('pp.showOutcome.shown')} />
            <span className="tiny pep-entry-date">2023-02</span>
          </div>
          <div className="small">ACG_Labo, Harajuku, Tokyo · {t('pp.showType.group')}</div>
          <div className="small pep-entry-notes">{t('pp.exlog.systemEntry')}</div>
        </li>

        {sorted.map(s => (
          <li key={s.id} className={`pep-entry pep-entry--${tone(s.outcome)}`}>
            <div className="pep-entry-head">
              <span className="pep-entry-name">{s.name || s.venue}</span>
              <OutcomeChip status={s.outcome} label={t('pp.showOutcome.' + s.outcome)} />
              {s.date && <span className="tiny pep-entry-date">{s.date}</span>}
              <button className="pep-goal-remove" onClick={() => remove(s.id)} title={t('pp.exlog.delete')}>×</button>
            </div>
            {s.venue && s.name && <div className="small">{s.venue} · {t('pp.showType.' + s.type)}</div>}
            {s.notes && <div className="small pep-entry-notes">{s.notes}</div>}
          </li>
        ))}
      </ul>
    </div>
  )
}

// ── Venues & Contacts tab (CRM) ────────────────────────────────────────────

const CRM_FILTERS = ['all', 'active', 'research', 'cold']
const FILTER_STATUS_MAP = {
  all:      null,
  active:   ['in_contact', 'sent_inquiry', 'contacted', 'responded', 'ready_to_review', 'relationship', 'ongoing', 'submitted'],
  research: ['researching'],
  cold:     ['cold'],
}
const CONTACT_STATUSES = ['cold', 'researching', 'in_contact', 'submitted', 'ongoing', 'rejected']
const VENUE_TYPES = ['gallery', 'cafe_gallery', 'bookshop', 'zine_shop', 'artist_space', 'fair', 'institution', 'residency', 'other']

function statusLabel(t, status) {
  const key = `pp.crm.statusLabel.${status}`
  const s = t(key)
  if (s !== key) return s
  const vk = `pp.venuelog.status.${status}`
  const v = t(vk)
  return v !== vk ? v : status
}

function ContactCard({ contact: c, onUpdate }) {
  const { t } = useLanguage()
  const [expanded, setExpanded] = useState(false)
  const [editing, setEditing] = useState(false)
  const [editStatus, setEditStatus] = useState(c.status || 'cold')
  const [editNotes, setEditNotes] = useState(c.notes || '')
  const [editLast, setEditLast] = useState((c.last_contacted || '').slice(0, 10))
  const [busy, setBusy] = useState(false)

  const today = new Date().toISOString().slice(0, 10)

  async function patch(fields, closeEdit) {
    setBusy(true)
    try {
      const res = await api.patchContact(c.name, fields)
      if (res?.contact) onUpdate(res.contact)
      if (closeEdit) setEditing(false)
    } catch { /* keep edit open so nothing is lost */ }
    setBusy(false)
  }

  const showMarkContacted = !['contacted', 'responded', 'relationship'].includes(c.status)
  const showGotReply = ['contacted', 'in_contact'].includes(c.status) && !c.response_received

  return (
    <li className={`pep-entry pep-entry--${tone(c.status)} pep-contact`}>
      <button className="pep-contact-main" onClick={() => setExpanded(x => !x)}>
        <div className="pep-entry-head">
          <span className="pep-entry-name">{c.name}</span>
          {c.type && <span className="pill pill--loc">{t(`pp.venueType.${c.type}`) !== `pp.venueType.${c.type}` ? t(`pp.venueType.${c.type}`) : c.type}</span>}
          <OutcomeChip status={c.status} label={statusLabel(t, c.status)} />
          {c.city && <span className="tiny pep-entry-date">{c.city}</span>}
          <span className="tiny pep-entry-date">
            {c.last_contacted ? t('pp.crm.contactedOn', { date: c.last_contacted.slice(0, 10) }) : t('pp.crm.neverContacted')}
          </span>
        </div>
      </button>

      <div className="pep-contact-actions">
        {c.contact_email && <a className="small pep-contact-email" href={`mailto:${c.contact_email}`}>{c.contact_email}</a>}
        {showMarkContacted && (
          <button className="btn-quiet pep-mini-btn" disabled={busy} onClick={() => patch({ status: 'contacted', last_contacted: today })}>
            {t('pp.crm.markContacted')}
          </button>
        )}
        {showGotReply && (
          <button className="btn-quiet pep-mini-btn" disabled={busy} onClick={() => patch({ response_received: true, status: 'responded' })}>
            {t('pp.crm.gotReply')}
          </button>
        )}
        {!editing && (
          <button className="btn-ghost pep-mini-btn" onClick={() => { setEditing(true); setExpanded(true); setEditStatus(c.status || 'cold'); setEditNotes(c.notes || ''); setEditLast((c.last_contacted || '').slice(0, 10)) }}>
            {t('pp.crm.edit')}
          </button>
        )}
      </div>

      {expanded && !editing && (
        <div className="pep-contact-detail">
          {c.crm_analysis?.next_action && (
            <p className="small"><span className="tiny pep-block-label">{t('pp.crm.nextAction')}</span> {c.crm_analysis.next_action}</p>
          )}
          {c.why_relevant && (
            <p className="small"><span className="tiny pep-block-label">{t('pp.crm.whyRelevant')}</span> {c.why_relevant}</p>
          )}
          {c.crm_analysis?.risk_notes && (
            <p className="small pep-risk"><span className="tiny pep-block-label">{t('pp.crm.watchOut')}</span> {c.crm_analysis.risk_notes}</p>
          )}
          {c.notes && (
            <p className="small"><span className="tiny pep-block-label">{t('pp.crm.notes')}</span> {c.notes}</p>
          )}
          {(c.contact_page || c.official_website) && (
            <a className="small pep-contact-link" href={c.contact_page || c.official_website} target="_blank" rel="noopener noreferrer">
              {c.contact_page ? t('pp.crm.contactPage') : t('pp.crm.website')} ↗
            </a>
          )}
        </div>
      )}

      {editing && (
        <div className="pep-contact-edit">
          <div className="pep-add-row pep-add-row--tight">
            <Field label={t('pp.crm.status')}>
              <select className="pep-input" value={editStatus} onChange={e => setEditStatus(e.target.value)}>
                {CONTACT_STATUSES.map(s => <option key={s} value={s}>{statusLabel(t, s)}</option>)}
              </select>
            </Field>
            <Field label={t('pp.crm.lastContacted')}>
              <input type="date" className="pep-input" value={editLast} onChange={e => setEditLast(e.target.value)} />
            </Field>
            <Field label={t('pp.crm.notes')} wide>
              <input className="pep-input" value={editNotes} onChange={e => setEditNotes(e.target.value)} />
            </Field>
          </div>
          <div className="pep-q-actions">
            <button className="btn-warm" disabled={busy} onClick={() => patch({ status: editStatus, notes: editNotes, last_contacted: editLast }, true)}>
              {t('pp.crm.save')}
            </button>
            <button className="btn-ghost" onClick={() => setEditing(false)}>{t('pp.crm.cancel')}</button>
          </div>
        </div>
      )}
    </li>
  )
}

function VenuesTab() {
  const { t } = useLanguage()
  const [contacts, setContacts] = useState([])
  const [filter, setFilter] = useState('all')
  const [loading, setLoading] = useState(true)
  const [form, setForm] = useState({ name: '', type: 'gallery', city: 'Tokyo', status: 'cold', notes: '' })
  const [saving, setSaving] = useState(false)
  const [saved, flash] = useSaved()

  useEffect(() => {
    api.contacts()
      .then(d => { setContacts(Array.isArray(d) ? d : []); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  async function add() {
    if (!form.name.trim()) return
    setSaving(true)
    try {
      await api.addContact(form)
      const updated = await api.contacts()
      setContacts(Array.isArray(updated) ? updated : [])
      setForm({ name: '', type: 'gallery', city: 'Tokyo', status: 'cold', notes: '' })
      flash()
    } catch { /* keep form */ }
    setSaving(false)
  }

  function handleUpdate(updated) {
    setContacts(prev => prev.map(c => (c.name === updated.name ? updated : c)))
  }

  const filtered = filter === 'all'
    ? contacts
    : contacts.filter(c => (FILTER_STATUS_MAP[filter] || []).includes(c.status))

  return (
    <div>
      <p className="small pep-note">{t('pp.contacts.note')}</p>

      <div className="pep-add-row">
        <Field label={t('pp.venuelog.name')} wide>
          <input className="pep-input" value={form.name} onChange={e => set('name', e.target.value)} placeholder={t('pp.venuelog.ph.name')} />
        </Field>
        <Field label={t('pp.venuelog.type')}>
          <select className="pep-input" value={form.type} onChange={e => set('type', e.target.value)}>
            {VENUE_TYPES.map(o => <option key={o} value={o}>{t('pp.venueType.' + o)}</option>)}
          </select>
        </Field>
        <Field label={t('pp.venuelog.city')}>
          <input className="pep-input" value={form.city} onChange={e => set('city', e.target.value)} placeholder="Tokyo" />
        </Field>
        <Field label={t('pp.venuelog.status')}>
          <select className="pep-input" value={form.status} onChange={e => set('status', e.target.value)}>
            {CONTACT_STATUSES.map(o => <option key={o} value={o}>{statusLabel(t, o)}</option>)}
          </select>
        </Field>
        <Field label={t('pp.venuelog.notes')} wide>
          <input className="pep-input" value={form.notes} onChange={e => set('notes', e.target.value)} placeholder={t('pp.venuelog.ph.notes')} />
        </Field>
        <button className="btn-warm pep-add-btn" onClick={add} disabled={saving || !form.name.trim()}>
          {saved ? t('pp.venuelog.btn.done') : t('pp.venuelog.btn')}
        </button>
      </div>

      <div className="chip-row pep-crm-filters">
        {CRM_FILTERS.map(id => (
          <button key={id} className={`chip-filter${filter === id ? ' chip-filter--active' : ''}`} onClick={() => setFilter(id)}>
            {t('pp.contacts.filter.' + id)}
          </button>
        ))}
      </div>

      {loading && <p className="voice small pep-empty-line">{t('pp.contacts.loading')}</p>}
      {!loading && filtered.length === 0 && (
        <p className="voice small pep-empty-line">
          {filter === 'all' ? t('pp.contacts.emptyAll') : t('pp.contacts.emptyFilter')}
        </p>
      )}
      {!loading && filtered.length > 0 && (
        <ul className="pep-entries">
          {filtered.map((c, i) => <ContactCard key={c.name || i} contact={c} onUpdate={handleUpdate} />)}
        </ul>
      )}
    </div>
  )
}

// ── Quick log tab (career events) ──────────────────────────────────────────

const EVENT_TYPES = ['accepted', 'rejected', 'conversation', 'visited', 'sold', 'featured']

function QuickLogTab() {
  const { t } = useLanguage()
  const [events, setEvents] = useState([])
  const [selected, setSelected] = useState(null)
  const [note, setNote] = useState('')
  const [refresh, setRefresh] = useState(false)

  useEffect(() => {
    api.careerEvents()
      .then(d => setEvents(Array.isArray(d) ? d.slice(0, 5) : []))
      .catch(() => {})
  }, [refresh])

  async function logEvent() {
    if (!selected) return
    try {
      await api.addCareerEvent({ type: selected, note: note.trim() })
      setSelected(null)
      setNote('')
      setRefresh(f => !f)
    } catch { /* keep the note so she can retry */ }
  }

  return (
    <div>
      <p className="small pep-note">{t('pp.event.prompt')}</p>

      <div className="chip-row pep-event-chips">
        {EVENT_TYPES.map(type => (
          <button
            key={type}
            className={`pep-event-chip pep-chip--${tone(type)}${selected === type ? ' pep-event-chip--active' : ''}`}
            onClick={() => { setSelected(s => (s === type ? null : type)); setNote('') }}
          >
            {t(`pp.event.type.${type}`)}
          </button>
        ))}
      </div>

      {selected && (
        <div className="pep-event-note">
          <input
            className="pep-input"
            value={note}
            onChange={e => setNote(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && logEvent()}
            placeholder={t('pp.event.note.placeholder')}
            autoFocus
          />
          <button className="btn-warm" onClick={logEvent}>{t('pp.event.log')}</button>
          <button className="btn-ghost" onClick={() => { setSelected(null); setNote('') }}>{t('pp.event.cancel')}</button>
        </div>
      )}

      {events.length > 0 && (
        <ul className="pep-entries pep-entries--tight">
          {events.map((ev, i) => (
            <li key={ev.id || i} className={`pep-entry pep-entry--${tone(ev.type)}`}>
              <div className="pep-entry-head">
                <OutcomeChip status={ev.type} label={t(`pp.event.type.${ev.type}`)} />
                {ev.note && <span className="small">{ev.note}</span>}
                {ev.date && <span className="tiny pep-entry-date">{ev.date}</span>}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

// ── Section root ───────────────────────────────────────────────────────────

export default function RecordBook() {
  const t2 = useLocalT(strings)
  const [tab, setTab] = useState('submissions')

  const TAB_BODY = {
    submissions: <SubmissionsTab />,
    exhibitions: <ExhibitionsTab />,
    venues:      <VenuesTab />,
    quicklog:    <QuickLogTab />,
  }

  return (
    <section className="pep-recordbook" aria-label={t2('v2.peppercorn.recordbook.title')}>
      <div className="sec-head sec-head--amber">
        <h2 className="h-section">{t2('v2.peppercorn.recordbook.title')}</h2>
        <p className="sec-sub">{t2('v2.peppercorn.recordbook.sub')}</p>
      </div>

      <div className="card pep-ledger">
        <div className="pep-tabs" role="tablist">
          {TABS.map(id => (
            <button
              key={id}
              role="tab"
              aria-selected={tab === id}
              className={`pep-tab${tab === id ? ' pep-tab--active' : ''}`}
              onClick={() => setTab(id)}
            >
              {t2(`v2.peppercorn.tab.${id}`)}
            </button>
          ))}
        </div>
        <div className="pep-tab-body">{TAB_BODY[tab]}</div>
      </div>
    </section>
  )
}
