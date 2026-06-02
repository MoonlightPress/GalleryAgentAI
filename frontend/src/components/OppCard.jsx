import { useState } from 'react'
import './OppCard.css'

const CAT_LABELS = {
  gallery:           'Gallery',
  cafe_gallery:      'Café Gallery',
  artist_space:      'Artist Space',
  fair_popup:        'Art Fair / Pop-up',
  bookstore_gallery: 'Bookstore Gallery',
  bookstore_event:   'Bookstore Event',
  zine_print:        'Zine / Print',
  market_event:      'Market',
  residency:         'Residency',
  institutional:     'Institutional',
  event_space:       'Event Space',
  gallery_event:     'Gallery Event',
}

const EFFORT_COLOR = {
  Easy:   'effort-easy',
  Medium: 'effort-medium',
  Heavy:  'effort-heavy',
  Check:  'effort-check',
}

const SCORE_COLOR = {
  high:   'score-high',
  mid:    'score-mid',
  low:    'score-low',
}

function scoreClass(score) {
  const s = parseFloat(score) || 0
  if (s >= 10) return SCORE_COLOR.high
  if (s >= 5)  return SCORE_COLOR.mid
  return SCORE_COLOR.low
}

function deadlineIsReal(dl) {
  if (!dl) return false
  const low = dl.toLowerCase()
  return !low.includes('check') && !low.includes('tbd') && !low.includes('n/a')
}

export default function OppCard({ opp, sectionKey }) {
  const [open, setOpen] = useState(false)
  const [emailTab, setEmailTab] = useState('zh')

  const verifyNeeded = !deadlineIsReal(opp.deadline)

  return (
    <div className={`opp-card${open ? ' opp-card--open' : ''}`}>
      {/* ── Collapsed row ── */}
      <button
        className="opp-card-row"
        onClick={() => setOpen(v => !v)}
        aria-expanded={open}
      >
        <div className="opp-card-left">
          <span className={`opp-score ${scoreClass(opp.score)}`}>
            {opp.overall_score || '—'}
          </span>
          <div className="opp-card-name-block">
            <span className="opp-card-name">{opp.name}</span>
            <span className="opp-card-location">{opp.city}{opp.country && opp.country !== 'Japan' ? `, ${opp.country}` : ''}</span>
          </div>
        </div>
        <div className="opp-card-right">
          <span className="opp-cat-pill">{CAT_LABELS[opp.category] || opp.category}</span>
          {opp.effort && (
            <span className={`opp-effort-pill ${EFFORT_COLOR[opp.effort] || ''}`}>{opp.effort}</span>
          )}
          <span className="opp-card-summary-text">{opp.summary}</span>
          <span className="opp-chevron">{open ? '▲' : '▼'}</span>
        </div>
      </button>

      {/* ── Expanded body ── */}
      {open && (
        <div className="opp-card-body">
          {/* Header row */}
          <div className="opp-body-header">
            <div>
              <h3 className="opp-body-title">{opp.name}</h3>
              <div className="opp-body-meta">
                {opp.deadline && (
                  <span className={`opp-meta-chip${verifyNeeded ? ' chip-warn' : ''}`}>
                    📅 {verifyNeeded ? 'Deadline: verify' : opp.deadline}
                  </span>
                )}
                {opp.fees && (
                  <span className="opp-meta-chip">
                    💴 {opp.fees.toLowerCase().includes('check') ? 'Fees: verify' : opp.fees}
                  </span>
                )}
                {opp.official_website && (
                  <a
                    className="opp-meta-chip opp-meta-link"
                    href={opp.official_website}
                    target="_blank"
                    rel="noreferrer"
                  >
                    🔗 Website ↗
                  </a>
                )}
              </div>
            </div>
          </div>

          <div className="opp-body-grid">
            {/* Left column */}
            <div className="opp-body-left">
              {opp.overview && (
                <div className="opp-body-block">
                  <div className="opp-block-label">Venue overview</div>
                  <p>{opp.overview}</p>
                </div>
              )}

              {opp.why_it_fits && (
                <div className="opp-body-block">
                  <div className="opp-block-label">Why it fits</div>
                  <p>{opp.why_it_fits}</p>
                </div>
              )}

              {opp.bullets && opp.bullets.length > 0 && (
                <div className="opp-body-block">
                  <div className="opp-block-label">Key points</div>
                  <ul className="opp-bullets">
                    {opp.bullets.map((b, i) => (
                      <li key={i}>{b}</li>
                    ))}
                  </ul>
                </div>
              )}

              {opp.next_action && (
                <div className="opp-body-block">
                  <div className="opp-block-label">How to apply</div>
                  <p>{opp.next_action}</p>
                </div>
              )}

              {opp.soft_warning && (
                <div className="opp-body-block opp-soft-warning">
                  <div className="opp-block-label">Mochi notes</div>
                  <p>{opp.soft_warning}</p>
                </div>
              )}
            </div>

            {/* Right column: email drafts */}
            <div className="opp-body-right">
              <div className="opp-email-panel">
                <div className="opp-email-header">
                  <span className="opp-block-label">Email draft</span>
                  <div className="opp-email-tabs">
                    <button
                      className={`opp-email-tab${emailTab === 'zh' ? ' active' : ''}`}
                      onClick={() => setEmailTab('zh')}
                    >
                      中文
                    </button>
                    <button
                      className={`opp-email-tab${emailTab === 'ja' ? ' active' : ''}`}
                      onClick={() => setEmailTab('ja')}
                    >
                      日本語
                    </button>
                    <button
                      className={`opp-email-tab${emailTab === 'en' ? ' active' : ''}`}
                      onClick={() => setEmailTab('en')}
                    >
                      English
                    </button>
                  </div>
                </div>
                <pre className="opp-email-body">
                  {emailTab === 'zh' ? opp.email_zh : emailTab === 'ja' ? opp.email_ja : opp.email_en}
                </pre>
                <button
                  className="opp-copy-btn"
                  onClick={() => navigator.clipboard?.writeText(
                    emailTab === 'zh' ? opp.email_zh : emailTab === 'ja' ? opp.email_ja : opp.email_en
                  )}
                >
                  Copy draft
                </button>
              </div>

              {opp.what_to_verify && opp.what_to_verify.length > 0 && (
                <div className="opp-body-block opp-verify-block">
                  <div className="opp-block-label">Verify first</div>
                  <ul className="opp-verify-list">
                    {opp.what_to_verify.slice(0, 3).map((v, i) => (
                      <li key={i}>{v}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
