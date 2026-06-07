import { useState, useEffect } from 'react'
import './OppDetailPanel.css'
import { useLanguage } from '../i18n/LanguageContext'

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
  const [emailTab, setEmailTab] = useState('zh')
  const { t } = useLanguage()
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
          <h3 className="detail-panel-title">{opp.name}</h3>
          <button className="detail-panel-close" onClick={onClose}>✕</button>
        </div>
        <div className="detail-panel-meta">
          {opp.deadline && (
            <span className={`detail-chip${verifyNeeded ? ' chip-warn' : ''}`}>
              📅 {verifyNeeded ? t('detail.deadline.verify') : opp.deadline}
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
              🤝 {crmContact.status?.replace('_', ' ') || t('detail.crmTracked')}
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
                  <option key={s} value={s}>{t('pp.venuelog.status.' + s) || s.replace('_', ' ')}</option>
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
                  setTimeout(() => setLogSaved(false), 2000)
                }
              }}
            >
              {logSaved ? t('detail.savedCheck') : (crmContact ? t('detail.update') : t('detail.addToCrm'))}
            </button>
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
          {opp.overview && (
            <div className="detail-block">
              <div className="detail-label">{t('detail.label.overview')}</div>
              <p>{opp.overview}</p>
            </div>
          )}
          {opp.why_it_fits && (
            <div className="detail-block detail-why-fits">
              <div className="detail-label">{t('detail.label.whyFits')}</div>
              <p>{opp.why_it_fits}</p>
            </div>
          )}
          {opp.bullets?.length > 0 && (
            <div className="detail-block">
              <div className="detail-label">{t('detail.label.keyPoints')}</div>
              <ul className="detail-bullets detail-bullets--evidence">
                {opp.bullets.map((b, i) => <li key={i}>{b}</li>)}
              </ul>
            </div>
          )}
          {opp.next_action && (
            <div className="detail-block">
              <div className="detail-label">{t('detail.label.howApply')}</div>
              <p>{opp.next_action}</p>
            </div>
          )}
          {opp.soft_warning && (
            <div className="detail-block detail-warning">
              <div className="detail-label">{t('detail.label.mochiNotes')}</div>
              <p>{opp.soft_warning}</p>
            </div>
          )}
        </div>

        {/* Right: email drafts + verify checklist */}
        <div className="detail-panel-right">
          <div className="detail-email-panel">
            <div className="detail-email-header">
              <span className="detail-label">{t('detail.label.emailDraft')}</span>
              <div className="detail-email-tabs">
                {[['zh', '中文'], ['ja', '日本語'], ['en', 'English']].map(([key, label]) => (
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
            <pre className="detail-email-body">
              {(emailTab === 'zh' ? opp.email_zh : emailTab === 'ja' ? opp.email_ja : opp.email_en) || ''}
            </pre>
            <button
              className="detail-copy-btn"
              onClick={() => navigator.clipboard?.writeText(
                (emailTab === 'zh' ? opp.email_zh : emailTab === 'ja' ? opp.email_ja : opp.email_en) || ''
              )}
            >
              {t('detail.copyDraft')}
            </button>
          </div>

          {opp.checklist?.length > 0 && (
            <div className="detail-block detail-checklist">
              <div className="detail-label">{t('detail.label.checklist')}</div>
              <ul className="detail-checklist-list">
                {opp.checklist.map((item, i) => (
                  <li key={i} className={`checklist-item checklist-${item.status}`}>
                    <span className="checklist-icon">
                      {item.status === 'ready' ? '✓' : item.status === 'missing' ? '✗' : '○'}
                    </span>
                    <span className="checklist-content">
                      <strong>{item.label}</strong>
                      {item.note && <span className="checklist-note"> — {item.note}</span>}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
