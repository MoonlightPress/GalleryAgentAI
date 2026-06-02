import { useState } from 'react'
import './OppDetailPanel.css'

function deadlineIsReal(dl) {
  if (!dl) return false
  const low = dl.toLowerCase()
  return !low.includes('check') && !low.includes('tbd') && !low.includes('n/a')
}

export default function OppDetailPanel({ opp, onClose }) {
  const [emailTab, setEmailTab] = useState('zh')
  const verifyNeeded = !deadlineIsReal(opp.deadline)

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
              📅 {verifyNeeded ? 'Deadline: verify' : opp.deadline}
            </span>
          )}
          {opp.fees && (
            <span className="detail-chip">
              💴 {opp.fees.toLowerCase().includes('check') ? 'Fees: verify' : opp.fees}
            </span>
          )}
          {opp.official_website && (
            <a
              className="detail-chip detail-chip-link"
              href={opp.official_website}
              target="_blank"
              rel="noreferrer"
            >
              🔗 Website ↗
            </a>
          )}
        </div>
      </div>

      {/* Two-column body */}
      <div className="detail-panel-grid">
        {/* Left: content */}
        <div className="detail-panel-left">
          {opp.overview && (
            <div className="detail-block">
              <div className="detail-label">Venue overview</div>
              <p>{opp.overview}</p>
            </div>
          )}
          {opp.why_it_fits && (
            <div className="detail-block">
              <div className="detail-label">Why it fits</div>
              <p>{opp.why_it_fits}</p>
            </div>
          )}
          {opp.bullets?.length > 0 && (
            <div className="detail-block">
              <div className="detail-label">Key points</div>
              <ul className="detail-bullets">
                {opp.bullets.map((b, i) => <li key={i}>{b}</li>)}
              </ul>
            </div>
          )}
          {opp.next_action && (
            <div className="detail-block">
              <div className="detail-label">How to apply</div>
              <p>{opp.next_action}</p>
            </div>
          )}
          {opp.soft_warning && (
            <div className="detail-block detail-warning">
              <div className="detail-label">Mochi notes</div>
              <p>{opp.soft_warning}</p>
            </div>
          )}
        </div>

        {/* Right: email drafts + verify checklist */}
        <div className="detail-panel-right">
          <div className="detail-email-panel">
            <div className="detail-email-header">
              <span className="detail-label">Email draft</span>
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
              {emailTab === 'zh' ? opp.email_zh : emailTab === 'ja' ? opp.email_ja : opp.email_en}
            </pre>
            <button
              className="detail-copy-btn"
              onClick={() => navigator.clipboard?.writeText(
                emailTab === 'zh' ? opp.email_zh : emailTab === 'ja' ? opp.email_ja : opp.email_en
              )}
            >
              Copy draft
            </button>
          </div>

          {opp.what_to_verify?.length > 0 && (
            <div className="detail-block detail-verify">
              <div className="detail-label">Verify first</div>
              <ul className="detail-verify-list">
                {opp.what_to_verify.slice(0, 3).map((v, i) => <li key={i}>{v}</li>)}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
