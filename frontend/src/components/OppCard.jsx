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

const CAT_STYLE = {
  gallery:           { bg: 'linear-gradient(155deg,#f8e8dc 0%,#f0d8c8 100%)', emoji: '🖼' },
  cafe_gallery:      { bg: 'linear-gradient(155deg,#f8ead8 0%,#eedcc8 100%)', emoji: '☕' },
  artist_space:      { bg: 'linear-gradient(155deg,#e4f0e0 0%,#d8e8d4 100%)', emoji: '🏛' },
  fair_popup:        { bg: 'linear-gradient(155deg,#f8dcd8 0%,#f0d0c8 100%)', emoji: '🎪' },
  bookstore_gallery: { bg: 'linear-gradient(155deg,#dce4f0 0%,#d0dce8 100%)', emoji: '📖' },
  bookstore_event:   { bg: 'linear-gradient(155deg,#dce4f0 0%,#d0dce8 100%)', emoji: '📚' },
  zine_print:        { bg: 'linear-gradient(155deg,#e8dce8 0%,#e0d4e0 100%)', emoji: '📰' },
  market_event:      { bg: 'linear-gradient(155deg,#f8ecd8 0%,#f0e0c8 100%)', emoji: '🌿' },
  residency:         { bg: 'linear-gradient(155deg,#e0e4f0 0%,#d8dce8 100%)', emoji: '🏡' },
  institutional:     { bg: 'linear-gradient(155deg,#e4e8e0 0%,#dce0d8 100%)', emoji: '🏛' },
  event_space:       { bg: 'linear-gradient(155deg,#f8e4d8 0%,#f0d8cc 100%)', emoji: '✨' },
  gallery_event:     { bg: 'linear-gradient(155deg,#f4e0e4 0%,#ecd8dc 100%)', emoji: '🎨' },
}

const DEFAULT_STYLE = { bg: 'linear-gradient(155deg,#f0e8d8 0%,#e8e0d0 100%)', emoji: '•' }

export function scoreClass(score) {
  const s = parseFloat(score) || 0
  if (s >= 7) return 'score-high'
  if (s >= 4) return 'score-mid'
  return 'score-low'
}

export default function OppCard({ opp, isOpen, onDetails }) {
  const [reported, setReported] = useState(false)
  const style = CAT_STYLE[opp.category] || DEFAULT_STYLE

  return (
    <div className={`opp-card${isOpen ? ' opp-card--open' : ''}`}>
      {/* Image / illustration area */}
      <div className="opp-card-image" style={{ background: style.bg }}>
        <span className="opp-card-emoji">{style.emoji}</span>
        {opp.overall_score > 0 && (
          <span className={`opp-card-score-badge ${scoreClass(opp.overall_score)}`}>
            {opp.overall_score}
          </span>
        )}
      </div>

      {/* Card body */}
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

        <div className="opp-card-actions">
          <button
            className={`opp-btn-details${isOpen ? ' opp-btn-details--active' : ''}`}
            onClick={onDetails}
          >
            {isOpen ? 'Close' : 'Details'}
          </button>
          <button
            className={`opp-btn-report${reported ? ' opp-btn-report--done' : ''}`}
            onClick={() => setReported(v => !v)}
          >
            {reported ? '✓ Noted' : 'Report'}
          </button>
        </div>
      </div>
    </div>
  )
}
