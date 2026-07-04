import { useState, useEffect } from 'react'
import './OppDetailPanel.css'
import { useLanguage } from '../i18n/LanguageContext'
import { tfb, translatePhrase } from '../i18n/translations'
import { isDistinct } from '../utils/textGuards.js'
import { locF, localizeDeadline } from '../utils/localize.js'
import { track } from '../utils/track'

// "Mochi notes": the readiness flags that used to sit on the card face. The
// reasons/reviewLabels arrays carry canonical English phrases; translatePhrase
// maps each to the active language.
function localizedReasonLine(rec, t, lang) {
  if (!rec) return ''
  if (lang === 'en') return rec.reasonLine
  const reasons = rec.reasons || []
  if (reasons.length) return reasons.map(r => translatePhrase(r, lang)).join(' · ')
  const labels = rec.reviewLabels || []
  if (labels.length) return t('rec.needsCheck') + labels.map(f => translatePhrase(f, lang)).join(' · ')
  return t('rec.oneMoreLook')
}

// Evergreen/relationship venues you can pitch/consign anytime — a stored date is
// a past event note, not a deadline, so show "rolling" instead of a stale date.
const EVERGREEN_CATS = new Set([
  'artist_space', 'bookstore_event', 'bookstore_gallery', 'cafe_gallery',
  'event_space', 'gallery', 'gallery_event', 'gallery_small', 'zine_shop_consignment',
])

function deadlineIsReal(dl) {
  if (!dl) return false
  const low = dl.toLowerCase()
  return !low.includes('check') && !low.includes('tbd') && !low.includes('n/a')
}

function isDistinctUrl(a, b) {
  if (!a || !b) return !!a
  return a.replace(/\/$/, '') !== b.replace(/\/$/, '')
}

export default function OppDetailPanel({ opp, onClose }) {
  const [emailTab, setEmailTab] = useState('ja')   // most opportunities are Japanese
  const { t, lang } = useLanguage()
  const loc = (field) => locF(opp, field, lang, t)
  const verifyNeeded = !deadlineIsReal(opp.deadline)

  const [crmContact, setCrmContact] = useState(null)
  const [showLogForm, setShowLogForm] = useState(false)
  const [logForm, setLogForm] = useState({ status: 'in_contact', notes: '', last_contacted: new Date().toISOString().slice(0, 10) })
  const [logSaved, setLogSaved] = useState(false)

  useEffect(() => {
    if (!opp.name) return
    fetch(`/api/contacts/lookup?name=${encodeURIComponent(opp.name)}`)
      .then(r => r.ok ? r.json() : null)
      .then(c => setCrmContact(c))
      .catch(() => {})
  }, [opp.name])

  // Determine which contact action to surface
  const hasEmail     = !!(opp.contact && opp.contact.includes('@'))
  const hasFormUrl   = !!(opp.contact_url && !hasEmail)
  const hasApplyPage = !!(opp.submission_page && isDistinctUrl(opp.submission_page, opp.official_website))

  return (
    <div className="detail-panel">
      {/* Header */}
      <div className="detail-panel-header">
        <div className="detail-panel-title-row">
          <h3 className="detail-panel-title">{loc('name') || opp.name || opp.title}</h3>
          <button className="detail-panel-close" onClick={onClose}>✕</button>
        </div>
        <div className="detail-panel-meta">
          {(opp.deadline || EVERGREEN_CATS.has(opp.category)) && (
            <span className={`detail-chip${verifyNeeded && !EVERGREEN_CATS.has(opp.category) ? ' chip-warn' : ''}`}>
              📅 {EVERGREEN_CATS.has(opp.category)
                    ? t('detail.deadline.rolling')
                    : verifyNeeded ? t('detail.deadline.verify') : (localizeDeadline(opp, lang, t) || t('detail.deadline.verify'))}
            </span>
          )}
          {opp.fees && (
            <span className="detail-chip">
              💴 {opp.fees.toLowerCase().includes('check') ? t('detail.fees.verify') : opp.fees}
            </span>
          )}
          {opp.official_website && (
            <a
              className="detail-chip detail-chip-link"
              href={opp.official_website}
              target="_blank"
              rel="noreferrer"
            >
              🔗 {t('detail.website')}
            </a>
          )}

          {/* ── Primary contact action — always give a path forward ── */}
          {hasApplyPage && (
            <a
              className="detail-chip detail-chip-link detail-chip-action"
              href={opp.submission_page}
              target="_blank"
              rel="noreferrer"
            >
              ✦ {t('detail.apply')}
            </a>
          )}
          {hasEmail && (
            <a
              className="detail-chip detail-chip-link detail-chip-action"
              href={`mailto:${opp.contact}`}
            >
              ✉ {t('detail.contact.email')}
            </a>
          )}
          {hasFormUrl && (
            <a
              className="detail-chip detail-chip-link detail-chip-action"
              href={opp.contact_url}
              target="_blank"
              rel="noreferrer"
            >
              ✦ {t('detail.contact.form')}
            </a>
          )}

          {crmContact && (
            <span className={`detail-chip detail-chip-crm detail-chip-crm--${crmContact.status || 'cold'}`}>
              🤝 {crmContact.status ? (tfb(t, `crm.status.${crmContact.status}`, crmContact.status.replace('_', ' '))) : t('detail.crmTracked')}
              {crmContact.last_contacted && ` · ${crmContact.last_contacted}`}
            </span>
          )}

          <button
            className="detail-chip detail-chip-link detail-chip-log"
            onClick={() => setShowLogForm(s => !s)}
          >
            {showLogForm ? t('detail.logCancel') : t('detail.logContact')}
          </button>
        </div>

        {showLogForm && (
          <div className="detail-log-form">
            <div className="detail-log-row">
              <select
                className="detail-log-select"
                value={logForm.status}
                onChange={e => setLogForm(f => ({ ...f, status: e.target.value }))}
              >
                {['cold','researching','in_contact','submitted','ongoing','rejected'].map(s => (
                  <option key={s} value={s}>{tfb(t, 'pp.venuelog.status.' + s, s.replace('_', ' '))}</option>
                ))}
              </select>
              <input
                type="date"
                className="detail-log-input"
                value={logForm.last_contacted}
                onChange={e => setLogForm(f => ({ ...f, last_contacted: e.target.value }))}
              />
            </div>
            <input
              type="text"
              className="detail-log-input detail-log-input--wide"
              placeholder={t('detail.notes')}
              value={logForm.notes}
              onChange={e => setLogForm(f => ({ ...f, notes: e.target.value }))}
            />
            <button
              className="detail-log-btn"
              onClick={async () => {
                // If contact exists, update; otherwise create new
                const endpoint = crmContact ? '/api/contacts/update' : '/api/contacts'
                const method = crmContact ? 'PATCH' : 'POST'
                const body = crmContact
                  ? { name: opp.name, status: logForm.status, notes: logForm.notes, last_contacted: logForm.last_contacted }
                  : { name: opp.name, type: opp.category || '', city: opp.city || 'Tokyo', status: logForm.status, notes: logForm.notes, last_contacted: logForm.last_contacted, last_visited: '' }
                const r = await fetch(endpoint, {
                  method,
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify(body),
                })
                if (r.ok) {
                  const result = await r.json()
                  setCrmContact(crmContact ? result.contact : { ...body })
                  setShowLogForm(false)
                  setLogSaved(true)
                  track({ type: 'action', action: 'contact_log_save', category: opp.category, name: opp.name || opp.title })
                  setTimeout(() => setLogSaved(false), 2000)
                }
              }}
            >
              {logSaved ? t('detail.savedCheck') : (crmContact ? t('detail.update') : t('detail.addToCrm'))}
            </button>
          </div>
        )}

        {/* Prerequisites */}
        {opp.prerequisites && opp.prerequisites.length > 0 && (
          <div className="detail-prerequisites">
            <span className="prereq-label">{t('prereq.label')}</span>
            <div className="prereq-chips">
              {opp.prerequisites.map(p => (
                <span key={p} className="prereq-chip">
                  {tfb(t, `prereq.${p}`, p)}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Contact note — shown when there's no direct email (portal/form-only path) */}
        {opp.contact_note && (
          <p className="detail-contact-note">{opp.contact_note}</p>
        )}
      </div>

      {/* Two-column body */}
      <div className="detail-panel-grid">
        {/* Left: content */}
        <div className="detail-panel-left">
          {!loc('overview') && !loc('why_it_fits') && !(loc('bullets') || opp.bullets)?.length
            && !(lang === 'en' ? opp.next_action : opp[`next_action_${lang}`])
            && !loc('soft_warning') && !opp.recommendation?.reasonLine && (
            <p className="detail-content-empty">{t('detail.content.empty')}</p>
          )}
          {(loc('overview')) && (
            <div className="detail-block">
              <div className="detail-label">{t('detail.label.overview')}</div>
              <p>{loc('overview')}</p>
            </div>
          )}
          {isDistinct(loc('why_it_fits'), loc('overview')) && (
            <div className="detail-block detail-why-fits">
              <div className="detail-label">{t('detail.label.whyFits')}</div>
              <p>{loc('why_it_fits')}</p>
            </div>
          )}
          {(loc('bullets') || opp.bullets)?.length > 0 && (
            <div className="detail-block">
              <div className="detail-label">{t('detail.label.keyPoints')}</div>
              <ul className="detail-bullets detail-bullets--evidence">
                {(loc('bullets') || opp.bullets).map((b, i) => <li key={i}>{b}</li>)}
              </ul>
            </div>
          )}
          {(lang === 'en' ? opp.next_action : opp[`next_action_${lang}`]) && (
            <div className="detail-block">
              <div className="detail-label">{t('detail.label.howApply')}</div>
              <p>{lang === 'en' ? opp.next_action : opp[`next_action_${lang}`]}</p>
            </div>
          )}
          {(opp.recommendation?.reasonLine || loc('soft_warning')) && (
            <div className="detail-block detail-warning">
              <div className="detail-label">{t('detail.label.mochiNotes')}</div>
              {opp.recommendation?.reasonLine && (
                <p className={`detail-mochi-note detail-mochi-note--${opp.recommendation.readiness}`}>
                  <strong>{t(`card.recommendation.${opp.recommendation.readiness}`)}</strong>
                  {' '}{localizedReasonLine(opp.recommendation, t, lang)}
                </p>
              )}
              {loc('soft_warning') && <p>{loc('soft_warning')}</p>}
            </div>
          )}
        </div>

        {/* Right: email drafts + verify checklist */}
        <div className="detail-panel-right">
          <div className="detail-email-panel">
            <div className="detail-email-header">
              <span className="detail-label">{t('detail.label.emailDraft')}</span>
              <div className="detail-email-tabs">
                {[['ja', '日本語'], ['zh', '中文'], ['en', 'English']].map(([key, label]) => (
                  <button
                    key={key}
                    className={`detail-email-tab${emailTab === key ? ' active' : ''}`}
                    onClick={() => setEmailTab(key)}
                  >
                    {label}
                  </button>
                ))}
              </div>
            </div>
            {(() => {
              const draft = emailTab === 'zh' ? opp.email_zh : emailTab === 'ja' ? opp.email_ja : opp.email_en
              return draft ? (
                <>
                  <p
                    className="detail-draft-disclaimer"
                    style={{
                      margin: '0 0 8px',
                      padding: '6px 10px',
                      background: 'rgba(184, 137, 42, 0.08)',
                      borderRadius: '4px',
                      color: 'var(--ink-muted)',
                      fontSize: '12px',
                      fontStyle: 'italic',
                      lineHeight: 1.5,
                    }}
                  >
                    {t('detail.draftDisclaimer')}
                  </p>
                  <pre className="detail-email-body">{draft}</pre>
                  <button
                    className="detail-copy-btn"
                    onClick={() => {
                      navigator.clipboard?.writeText(draft)
                      track({ type: 'action', action: 'email_draft_copy', category: opp.category, name: opp.name || opp.title })
                    }}
                  >
                    {t('detail.copyDraft')}
                  </button>
                </>
              ) : (
                <p className="detail-email-empty">{t('detail.email.empty')}</p>
              )
            })()}
          </div>

          {opp.checklist?.length > 0 && (
            <div className="detail-block detail-checklist">
              <div className="detail-label">{t('detail.label.checklist')}</div>
              <ul className="detail-checklist-list">
                {opp.checklist.map((item, i) => {
                const clLabel = (lang === 'zh' && item.label_zh) ? item.label_zh
                              : (lang === 'ja' && item.label_ja) ? item.label_ja
                              : item.label
                const clNote  = (lang === 'zh' && item.note_zh)  ? item.note_zh
                              : (lang === 'ja' && item.note_ja)  ? item.note_ja
                              : item.note
                return (
                  <li key={i} className={`checklist-item checklist-${item.status}`}>
                    <span className="checklist-icon">
                      {item.status === 'ready' ? '✓' : item.status === 'missing' ? '✗' : '○'}
                    </span>
                    <span className="checklist-content">
                      <strong>{clLabel}</strong>
                      {clNote && <span className="checklist-note"> — {clNote}</span>}
                    </span>
                  </li>
                )
              })}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
