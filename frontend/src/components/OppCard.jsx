import { useState } from 'react'
import './OppCard.css'

export const CAT_LABELS = {
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

const BASE = '/assets/illustrations/'

const CAT_ILLUS = {
  gallery:           BASE + 'galleries.svg',
  gallery_event:     BASE + 'galleries.svg',
  artist_space:      BASE + 'galleries.svg',
  event_space:       BASE + 'galleries.svg',
  cafe_gallery:      BASE + 'cafes.svg',
  zine_print:        BASE + 'zines_and_print.svg',
  bookstore_gallery: BASE + 'zines_and_print.svg',
  bookstore_event:   BASE + 'zines_and_print.svg',
  fair_popup:        BASE + 'open_calls.svg',
  institutional:     BASE + 'open_calls.svg',
  market_event:      BASE + 'open_calls.svg',
  residency:         BASE + 'watch_list.svg',
}

const CAT_BG = {
  gallery:           '#f5e8dc',
  gallery_event:     '#f5e8dc',
  artist_space:      '#e8f0e0',
  event_space:       '#f5e4d8',
  cafe_gallery:      '#f5ead8',
  zine_print:        '#e8dce8',
  bookstore_gallery: '#dce4f0',
  bookstore_event:   '#dce4f0',
  fair_popup:        '#f5dcd8',
  institutional:     '#e4e8e0',
  market_event:      '#f5ecd8',
  residency:         '#e0e4f0',
}

export function scoreClass(score) {
  const s = parseFloat(score) || 0
  if (s >= 7) return 'score-high'
  if (s >= 4) return 'score-mid'
  return 'score-low'
}

const FEEDBACK_ACTIONS = [
  { id: 'follow',       label: 'Follow',       icon: '★' },
  { id: 'applied',      label: 'Applied',       icon: '✓' },
  { id: 'maybe_later',  label: 'Maybe Later',   icon: '◷' },
  { id: 'not_for_me',   label: 'Not for Me',    icon: '✕' },
]

async function saveFeedback(oppId, action) {
  try {
    await fetch('/api/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ opp_id: oppId, action }),
    })
  } catch (_) {
    // silently fail — feedback is best-effort
  }
}

export default function OppCard({ opp, isOpen, onDetails }) {
  const [feedback, setFeedback] = useState(null)
  const illus = CAT_ILLUS[opp.category]
  const bg    = CAT_BG[opp.category] || '#f0e8d8'

  const imgSrc = opp._section === 'immediate_best_moves'
    ? BASE + 'immediate_best_moves.svg'
    : illus

  function handleFeedback(actionId) {
    const next = feedback === actionId ? null : actionId
    setFeedback(next)
    if (next) saveFeedback(opp.id, next)
  }

  return (
    <div className={`opp-card${isOpen ? ' opp-card--open' : ''}`}>
      {/* Thumbnail — left strip */}
      <div className="opp-card-thumb" style={{ background: bg }}>
        {imgSrc
          ? <img src={imgSrc} alt="" className="opp-card-illus" />
          : <span className="opp-card-emoji">•</span>
        }
        {opp.overall_score > 0 && (
          <span className={`opp-card-score-badge ${scoreClass(opp.overall_score)}`}>
            {opp.overall_score}
          </span>
        )}
      </div>

      {/* Content — right column */}
      <div className="opp-card-body">
        <h3 className="opp-card-title">{opp.name}</h3>

        <div className="opp-card-pills">
          <span className="opp-pill opp-pill-cat">
            {CAT_LABELS[opp.category] || opp.category}
          </span>
          {opp.city && (
            <span className="opp-pill opp-pill-loc">{opp.city}</span>
          )}
          {opp.effort && opp.effort !== 'Check' && (
            <span className={`opp-pill opp-pill-effort opp-effort-${opp.effort.toLowerCase()}`}>
              {opp.effort}
            </span>
          )}
        </div>

        <p className="opp-card-desc">{opp.summary}</p>

        {/* Primary action */}
        <div className="opp-card-actions">
          <button
            className={`opp-btn-details${isOpen ? ' opp-btn-details--active' : ''}`}
            onClick={onDetails}
          >
            {isOpen ? 'Close' : 'Details'}
          </button>
        </div>

        {/* Feedback row — visible only when card is open */}
        {isOpen && (
          <div className="opp-feedback-row">
            {FEEDBACK_ACTIONS.map(a => (
              <button
                key={a.id}
                className={`opp-feedback-btn opp-feedback-${a.id}${feedback === a.id ? ' opp-feedback-btn--active' : ''}`}
                onClick={() => handleFeedback(a.id)}
                title={a.label}
              >
                <span className="opp-feedback-icon">{a.icon}</span>
                <span className="opp-feedback-label">{a.label}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
