// Painted per-category icons (ported from v1 OppCard.jsx CAT_ICON, extended to
// cover every category the live API actually serves — no identical-icon flood).
const ICONS = '/assets/icons/'

export const CAT_ICON = {
  // ── Galleries & spaces ─────────────────────────────────────────────
  gallery:                        ICONS + 'icon_gallery.png',
  gallery_small:                  ICONS + 'icon_gallery_small.png',
  gallery_event:                  ICONS + 'icon_studio.png',
  artist_space:                   ICONS + 'icon_artist_space.png',
  event_space:                    ICONS + 'icon_studio.png',
  // ── Cafés & bookshops ──────────────────────────────────────────────
  cafe_gallery:                   ICONS + 'icon_cafe_gallery.png',
  bookstore_gallery:              ICONS + 'icon_reading_nook.png',
  bookstore_event:                ICONS + 'icon_bookstore.png',
  // ── Zines, books & publishing ──────────────────────────────────────
  zine_print:                     ICONS + 'icon_zines.png',
  book_publishing:                ICONS + 'icon_zines.png',
  global_artist_book_platform:    ICONS + 'icon_bookstore.png',
  global_art_book_fair:           ICONS + 'icon_fair.png',
  global_book_arts:               ICONS + 'icon_zines.png',
  zine_shop_consignment:          ICONS + 'icon_bookstore.png',
  group_publication_open_call:    ICONS + 'icon_submission.png',
  global_photobook:               ICONS + 'icon_submission.png',
  editorial_illustration:         ICONS + 'icon_submission.png',
  magazine_call:                  ICONS + 'icon_submission.png',
  book_cover_call:                ICONS + 'icon_submission.png',
  // ── Fairs & markets ────────────────────────────────────────────────
  fair_popup:                     ICONS + 'icon_fair.png',
  zine_fair_booth:                ICONS + 'icon_fair.png',
  market_event:                   ICONS + 'icon_art_market.png',
  // ── Open calls ─────────────────────────────────────────────────────
  institutional:                  ICONS + 'icon_open_call.png',
  global_open_call:               ICONS + 'icon_open_call.png',
  global_watercolor_open_call:    ICONS + 'icon_open_call.png',
  japan_watercolor_open_call:     ICONS + 'icon_open_call.png',
  japan_watercolor_institution:   ICONS + 'icon_open_call.png',
  photo_open_call:                ICONS + 'icon_open_call.png',
  open_call_index:                ICONS + 'icon_open_call.png',
  // ── Competitions & awards ──────────────────────────────────────────
  competition_award:              ICONS + 'icon_prize.png',
  illustration_prize:             ICONS + 'icon_prize.png',
  watercolor_competition:         ICONS + 'icon_prize.png',
  emerging_artist_award:          ICONS + 'icon_prize.png',
  // ── Grants, residencies & fellowships ──────────────────────────────
  grant:                          ICONS + 'icon_residency_intl.png',
  residency:                      ICONS + 'icon_residency.png',
  global_residency:               ICONS + 'icon_residency_intl.png',
  global_grant_fellowship:        ICONS + 'icon_residency_intl.png',
  residency_beijing:              ICONS + 'icon_residency.png',
  // ── Press ──────────────────────────────────────────────────────────
  press_target:                   ICONS + 'icon_research.png',
}

export const DEFAULT_ICON = ICONS + 'icon_open_call.png'

export function catIcon(category) {
  return CAT_ICON[category] || DEFAULT_ICON
}
