import { useState } from 'react'
import './OppCard.css'
import { useLanguage } from '../i18n/LanguageContext'
import { tfb } from '../i18n/translations'
import { feedbackToastKey, shouldRemoveAfterFeedback } from '../utils/feedbackBehavior'
import { isDistinct } from '../utils/textGuards.js'
import { locF, localizeDeadline, isUrgentDeadline } from '../utils/localize.js'
import { oppKey } from '../utils/oppKey.js'
import { track, trackAction } from '../utils/track'
import { isFresh } from '../utils/newOpportunities'

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

// Hand-made watercolor category icons (replacing the interim emoji). Served from
// public/icons/*.webp under Vite's /mochi/ base; the cream background blends with
// the warm cards by design (do NOT background-remove — it clips the soft edges).
// Render via iconUrl()/<img> at the render site below.
const ICON_BASE = `${import.meta.env.BASE_URL}icons/`
const iconUrl = (name) => `${ICON_BASE}${name}.webp`

const CAT_ICON = {
  // ── Galleries & spaces ───────────────────────────────────────────────
  gallery:                        'ic_gallery',
  gallery_small:                  'ic_gallery',
  gallery_event:                  'ic_gallery',
  artist_space:                   'ic_gallery',
  event_space:                    'ic_gallery',
  // ── Cafés & bookshops ────────────────────────────────────────────────
  cafe_gallery:                   'ic_cafe',
  bookstore_gallery:              'ic_books',
  bookstore_event:                'ic_books',
  // ── Zines, books & publishing ────────────────────────────────────────
  zine_print:                     'ic_books',
  book_publishing:                'ic_books',
  global_artist_book_platform:    'ic_books',
  global_art_book_fair:           'ic_fair',
  global_book_arts:               'ic_books',
  zine_shop_consignment:          'ic_books',
  group_publication_open_call:    'ic_opencall',
  // ── Fairs & markets ──────────────────────────────────────────────────
  fair_popup:                     'ic_fair',
  zine_fair_booth:                'ic_fair',
  market_event:                   'ic_fair',
  // ── Open calls & competitions ────────────────────────────────────────
  institutional:                  'ic_institution',
  global_open_call:               'ic_opencall',
  global_watercolor_open_call:    'ic_opencall',
  japan_watercolor_open_call:     'ic_opencall',
  japan_watercolor_institution:   'ic_institution',
  photo_open_call:                'ic_opencall',
  global_photobook:               'ic_books',
  // ── Residencies & fellowships ────────────────────────────────────────
  residency:                      'ic_institution',
  global_residency:               'ic_institution',
  global_grant_fellowship:        'ic_award',
  residency_beijing:              'ic_institution',
}

// Default category icon when an opp's category isn't in the map above.
const DEFAULT_ICON = 'ic_opencall'

const MEDIUM_CONFIG = {
  watercolor:   { label: '◆ Watercolor',   color: '#4a8c7a' },
  illustration: { label: '◆ Illustration', color: '#7a5a8c' },
  book_arts:    { label: '◆ Book Arts',    color: '#8c6a3a' },
  painting:     { label: '◆ Painting',     color: '#8c4a3a' },
  photography:  { label: '◆ Photography',  color: '#5a6a7a' },
}

const FEEDBACK_IDS = [
  { id: 'follow',      key: 'card.feedback.follow',   icon: '★' },
  { id: 'applied',     key: 'card.feedback.applied',  icon: '✓' },
  { id: 'maybe_later', key: 'card.feedback.maybe',    icon: '◷' },
  { id: 'not_for_me',  key: 'card.feedback.notForMe', icon: '✕' },
]

// Persisted triage state. Her choices must survive a reload on a daily-driver
// dashboard, so we mirror them into localStorage keyed by the stable opp id —
// the same pattern used for mochi_intro_dismissed / the Saffron level.
const FEEDBACK_STORE_KEY = 'mochi_card_feedback'

function readFeedbackStore() {
  try {
    const raw = localStorage.getItem(FEEDBACK_STORE_KEY)
    return raw ? JSON.parse(raw) : {}
  } catch {
    return {}
  }
}

function writeFeedbackForKey(key, action) {
  if (!key) return
  try {
    const store = readFeedbackStore()
    if (action) store[key] = action
    else delete store[key]
    localStorage.setItem(FEEDBACK_STORE_KEY, JSON.stringify(store))
  } catch {
    // localStorage unavailable — feedback persistence is best-effort
  }
}

async function saveFeedback(opp, action) {
  try {
    await fetch('/api/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        opp_id:      oppKey(opp),
        action,
        opp_name:    opp.name  || opp.title || '',
        opp_title:   opp.title || opp.name  || '',
        opp_website: opp.official_website   || '',
      }),
    })
  } catch {
    // silently fail — feedback is best-effort
  }
}

export default function OppCard({ opp, isOpen, onDetails, onSuppressed, onFeedback,
                                 surface = 'opportunity_card' }) {
  const key = oppKey(opp)
  // Hydrate triage state from persisted store so her choices don't vanish on reload.
  const [feedback, setFeedback] = useState(() => readFeedbackStore()[key] || null)
  const [toastKey, setToastKey] = useState(null)
  const { t, lang } = useLanguage()
  const iconSrc = iconUrl(CAT_ICON[opp.category] || DEFAULT_ICON)
  const loc = (field) => locF(opp, field, lang, t)

  const deadlineText = localizeDeadline(opp, lang, t)
  const deadlineUrgent = isUrgentDeadline(opp.deadline) && !opp.deadline_past

  // Confidence dot (top-right): a soft, glanceable signal that replaces the
  // clinical numeric score — green = strong fit, amber = worth a look, grey =
  // lower confidence. Derived from the same readiness the ranking uses.
  const _confStatus = opp.actionability_status || opp.recommendation?.readiness || ''
  const confLevel = _confStatus === 'ready' ? 'strong'
    : _confStatus === 'closed_or_stale' ? 'low'
    : 'medium'
  const confColor = confLevel === 'strong' ? '#5a7a30'
    : confLevel === 'low' ? '#b3a9a0' : '#d4912f'

  async function handleFeedback(actionId) {
    const next = feedback === actionId ? null : actionId
    setFeedback(next)
    writeFeedbackForKey(key, next)
    onFeedback?.(opp, next)
    if (next) {
      trackAction(next, opp, { surface })
      await saveFeedback(opp, next)
      if (shouldRemoveAfterFeedback(next) && onSuppressed) onSuppressed(oppKey(opp))
      setToastKey(feedbackToastKey(next))
      setTimeout(() => setToastKey(null), 2500)
    }
  }

  // Card hierarchy (T3.1, revised per Scott 2026-06-25: "keep the orange, they
  // just all need to be the same"). Every card now carries the SAME uniform warm
  // orange top-accent (base .opp-card in OppCard.css); the Strongest Picks band
  // gets a STRONGER tier of the same orange family via .opp-grid--strongest. We
  // no longer flag individual cards with --strong/--urgent bars (that produced
  // "some have bars, some don't"). Urgency stays as TEXT (amber deadline + "soon"
  // pill), not a structural bar.
  const cardClass = [
    'opp-card',
    isOpen ? 'opp-card--open' : '',
  ].filter(Boolean).join(' ')

  return (
    <div className={cardClass}>
      <span className="opp-conf-dot" style={{ background: confColor }} title={t(`card.conf.${confLevel}`)} aria-hidden="true" />
      {isFresh(opp.id) && <span className="opp-new-badge">{t('card.new')}</span>}

      <div className="opp-card-body">

        {/* Header: 40×40 icon + title */}
        <div className="opp-card-header">
          <img
            className="opp-card-icon"
            src={iconSrc}
            alt=""
            aria-hidden="true"
            loading="lazy"
            width="40"
            height="40"
          />
          {/* Name is a proper noun — never suppress it, even when English-only. */}
          <h3 className="opp-card-title">{loc('name') || opp.name || opp.title}</h3>
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
              {t(`card.effort.${opp.effort.toLowerCase()}`) || opp.effort}
            </span>
          )}
          {MEDIUM_CONFIG[opp.native_medium] && (
            <span
              className="opp-medium-badge"
              style={{ color: MEDIUM_CONFIG[opp.native_medium].color, borderColor: MEDIUM_CONFIG[opp.native_medium].color }}
            >
              {tfb(t, `medium.${opp.native_medium}`, MEDIUM_CONFIG[opp.native_medium].label)}
            </span>
          )}
          {opp.deadline_past && (
            <span className="opp-pill opp-pill-past-deadline" title={t('card.deadlinePast.title')}>
              {t('card.deadlinePast')}
            </span>
          )}
          {opp.closed_this_cycle && (
            <span className="opp-pill opp-pill-closed-cycle" title={t('card.closedThisCycle.title')}>
              {t('card.closedThisCycle')}
            </span>
          )}
        </div>

        {/* Description */}
        <p className="opp-card-desc">{loc('summary')}</p>

        {/* Why it fits — the artist-specific signal, only when distinct from summary */}
        {isDistinct(loc('why_card'), loc('summary')) && (
          <p className="opp-card-why">{loc('why_card')}</p>
        )}

        {/* "Why Mochi picked it" was here — moved into the Details panel under
           "Mochi notes" (it's a fixed readiness flag-set, too generic for the card face). */}

        {/* Deadline — the core ops signal. Urgent (<7 days) gets the same warm
           highlight Today's Focus uses for urgency. Localized; never raw English. */}
        {deadlineText && !opp.deadline_past && (
          <p className={`opp-card-deadline${deadlineUrgent ? ' opp-card-deadline--urgent' : ''}`}>
            <img
              className="opp-card-deadline-icon"
              src={iconUrl('ic_calendar')}
              alt=""
              aria-hidden="true"
              loading="lazy"
              width="16"
              height="16"
            />
            <span className="opp-card-deadline-text">{deadlineText}</span>
            {deadlineUrgent && (
              <span className="opp-card-deadline-soon">{t('card.deadline.soon')}</span>
            )}
          </p>
        )}

        {/* Primary action */}
        <div className="opp-card-actions">
          <button
            className={`opp-btn-details${isOpen ? ' opp-btn-details--active' : ''}`}
            onClick={() => {
              if (!isOpen) trackAction('open_card', opp, { surface })
              onDetails()
            }}
          >
            {isOpen ? t('card.close') : t('card.details')}
          </button>
          {(opp.submission_page || opp.official_website || opp.source_url) && (
            <a
              className="opp-btn-open"
              href={opp.submission_page || opp.official_website || opp.source_url}
              target="_blank"
              rel="noreferrer"
              onClick={() => trackAction('external_link_click', opp, { surface,
                link_type: opp.submission_page ? 'submission_page' : opp.official_website ? 'official_website' : 'source_url' })}
            >
              {t('tf.open')}
            </a>
          )}
        </div>

        <div className="opp-feedback-row" role="group" aria-label={t('card.feedback.label')}>
          <span className="opp-feedback-kicker">{t('card.feedback.label')}</span>
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
          {toastKey && (
            <span className="opp-feedback-btn opp-applied-toast">
              {t(toastKey)}
            </span>
          )}
        </div>

      </div>
    </div>
  )
}
