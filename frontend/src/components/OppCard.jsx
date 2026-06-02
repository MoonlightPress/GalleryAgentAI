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

// Maps category → SVG illustration file
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

// Fallback gradient bg per category (shown while SVG loads)
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

export default function OppCard({ opp, isOpen, onDetails }) {
  const [reported, setReported] = useState(false)
  const illus = CAT_ILLUS[opp.category]
  const bg    = CAT_BG[opp.category] || '#f0e8d8'

  // Use star illustration for section immediate_best_moves if passed via prop
  const imgSrc = opp._section === 'immediate_best_moves'
    ? BASE + 'immediate_best_moves.svg'
    : illus

  return (
    <div className={`opp-card${isOpen ? ' opp-card--open' : ''}`}>
      {/* Image / illustration area */}
      <div className="opp-card-image" style={{ background: bg }}>
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
