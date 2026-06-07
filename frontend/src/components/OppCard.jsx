import { useState } from 'react'
import './OppCard.css'
import { useLanguage } from '../i18n/LanguageContext'

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

const ICONS = '/assets/icons/'

const CAT_ICON = {
  // ── Galleries & spaces ───────────────────────────────────────────────
  gallery:                        ICONS + 'icon_gallery.png',
  gallery_small:                  ICONS + 'icon_gallery_small.png',
  gallery_event:                  ICONS + 'icon_studio.png',
  artist_space:                   ICONS + 'icon_artist_space.png',
  event_space:                    ICONS + 'icon_studio.png',
  // ── Cafés & bookshops ────────────────────────────────────────────────
  cafe_gallery:                   ICONS + 'icon_cafe_gallery.png',
  bookstore_gallery:              ICONS + 'icon_reading_nook.png',
  bookstore_event:                ICONS + 'icon_bookstore.png',
  // ── Zines, books & publishing ────────────────────────────────────────
  zine_print:                     ICONS + 'icon_zines.png',
  book_publishing:                ICONS + 'icon_zines.png',
  global_artist_book_platform:    ICONS + 'icon_bookstore.png',
  global_art_book_fair:           ICONS + 'icon_fair.png',
  global_book_arts:               ICONS + 'icon_zines.png',
  zine_shop_consignment:          ICONS + 'icon_bookstore.png',
  group_publication_open_call:    ICONS + 'icon_submission.png',
  // ── Fairs & markets ──────────────────────────────────────────────────
  fair_popup:                     ICONS + 'icon_fair.png',
  zine_fair_booth:                ICONS + 'icon_fair.png',
  market_event:                   ICONS + 'icon_art_market.png',
  // ── Open calls & competitions ────────────────────────────────────────
  institutional:                  ICONS + 'icon_open_call.png',
  global_open_call:               ICONS + 'icon_open_call.png',
  global_watercolor_open_call:    ICONS + 'icon_open_call.png',
  japan_watercolor_open_call:     ICONS + 'icon_open_call.png',
  japan_watercolor_institution:   ICONS + 'icon_open_call.png',
  photo_open_call:                ICONS + 'icon_open_call.png',
  global_photobook:               ICONS + 'icon_submission.png',
  // ── Residencies & fellowships ────────────────────────────────────────
  residency:                      ICONS + 'icon_residency.png',
  global_residency:               ICONS + 'icon_residency_intl.png',
  global_grant_fellowship:        ICONS + 'icon_residency_intl.png',
  residency_beijing:              ICONS + 'icon_residency.png',
}

const DEFAULT_ICON = ICONS + 'icon_open_call.png'

export function scoreClass(score) {
  const s = parseFloat(score) || 0
  if (s >= 7) return 'score-high'
  if (s >= 4) return 'score-mid'
  return 'score-low'
}

const FEEDBACK_IDS = [
  { id: 'follow',      key: 'card.feedback.follow',   icon: '★' },
  { id: 'applied',     key: 'card.feedback.applied',  icon: '✓' },
  { id: 'maybe_later', key: 'card.feedback.maybe',    icon: '◷' },
  { id: 'not_for_me',  key: 'card.feedback.notForMe', icon: '✕' },
]

async function saveFeedback(opp, action) {
  try {
    await fetch('/api/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        opp_id:      opp.title || opp.name || opp.id,
        action,
        opp_name:    opp.name  || opp.title || '',
        opp_title:   opp.title || opp.name  || '',
        opp_website: opp.official_website   || '',
      }),
    })
  } catch (_) {
    // silently fail — feedback is best-effort
  }
}

export default function OppCard({ opp, isOpen, onDetails, onSuppressed }) {
  const [feedback, setFeedback] = useState(null)
  const [appliedToast, setAppliedToast] = useState(false)
  const { t } = useLanguage()
  const iconSrc = CAT_ICON[opp.category] || DEFAULT_ICON

  async function handleFeedback(actionId) {
    const next = feedback === actionId ? null : actionId
    setFeedback(next)
    if (next) {
      await saveFeedback(opp, next)
      if (next === 'not_for_me' && onSuppressed) onSuppressed(opp.id)
      if (next === 'applied') {
        setAppliedToast(true)
        setTimeout(() => setAppliedToast(false), 2500)
      }
    }
  }

  return (
    <div className={`opp-card${isOpen ? ' opp-card--open' : ''}`}>

      {/* Score badge — absolute top-right */}
      {opp.overall_score > 0 && (
        <span className={`opp-card-score-badge ${scoreClass(opp.overall_score)}`}>
          {opp.overall_score}
        </span>
      )}

      <div className="opp-card-body">

        {/* Header: 40×40 icon + title */}
        <div className="opp-card-header">
          <img src={iconSrc} alt="" className="opp-card-icon" />
          <h3 className="opp-card-title">{opp.name}</h3>
        </div>

        {/* Tags */}
        <div className="opp-card-pills">
          <span className="opp-pill opp-pill-cat">
            {t(`cat.${opp.category}`) !== `cat.${opp.category}` ? t(`cat.${opp.category}`) : (CAT_LABELS[opp.category] || opp.category)}
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

        {/* Description */}
        <p className="opp-card-desc">{opp.summary}</p>

        {/* Why it fits — the artist-specific signal, only when distinct from summary */}
        {opp.why_card && (
          <p className="opp-card-why">{opp.why_card}</p>
        )}

        {/* Primary action */}
        <div className="opp-card-actions">
          <button
            className={`opp-btn-details${isOpen ? ' opp-btn-details--active' : ''}`}
            onClick={onDetails}
          >
            {isOpen ? t('card.close') : t('card.details')}
          </button>
        </div>

        {/* Feedback row — visible only when card is open */}
        {isOpen && (
          <div className="opp-feedback-row">
            {FEEDBACK_IDS.map(a => (
              <button
                key={a.id}
                className={`opp-feedback-btn opp-feedback-${a.id}${feedback === a.id ? ' opp-feedback-btn--active' : ''}`}
                onClick={() => handleFeedback(a.id)}
                title={t(a.key)}
              >
                <span className="opp-feedback-icon">{a.icon}</span>
                <span className="opp-feedback-label">{t(a.key)}</span>
              </button>
            ))}
            {appliedToast && (
              <span className="opp-feedback-btn opp-applied-toast">
                ✓ added to submission log
              </span>
            )}
          </div>
        )}

      </div>
    </div>
  )
}
