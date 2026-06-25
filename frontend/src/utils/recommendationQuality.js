const PREFERRED_MEDIA = new Set(['watercolor', 'book_arts', 'illustration', 'painting'])
const STRONG_SECTIONS = new Set(['immediate_best_moves', 'open_calls', 'zines_and_print', 'relationship_targets'])
const RELATIONSHIP_CATEGORIES = new Set(['gallery', 'cafe_gallery', 'artist_space', 'bookstore_gallery', 'gallery_event'])

export function enrichOpportunity(opp, sectionKey = '', feedback = {}) {
  const checks = checklistMap(opp)
  const reviewLabels = []
  const reasons = []
  let sortScore = numeric(opp.overall_score ?? opp.score)
  const backendActionability = backendRecommendation(opp)

  if (sectionKey === 'immediate_best_moves') sortScore += 7
  if (sectionKey === 'watch_list') sortScore -= 2

  if (opp.deadline_past || opp.closed_this_cycle) {
    sortScore -= 18
    reviewLabels.push('Timing needs review')
  }

  if (PREFERRED_MEDIA.has(opp.native_medium)) {
    sortScore += 5
    reasons.push(mediaReason(opp.native_medium))
  } else if (opp.native_medium === 'photography') {
    sortScore -= 6
    reviewLabels.push('Medium fit is weaker')
  }

  applyChecklistSignal(checks, 'Submission path', {
    ready: () => {
      sortScore += 5
      reasons.push('Submission path is clear')
    },
    review: () => {
      sortScore -= 5
      reviewLabels.push('Find submission path')
    },
  })

  applyChecklistSignal(checks, 'Deadline', {
    ready: () => {
      sortScore += 3
      reasons.push('Deadline is checked')
    },
    review: () => {
      if (!isEvergreen(opp)) {
        sortScore -= 3
        reviewLabels.push('Confirm deadline')
      }
    },
  })

  applyChecklistSignal(checks, 'Entry fee', {
    ready: item => {
      sortScore += feeLooksFree(item?.note) ? 3 : 1
      reasons.push(feeLooksFree(item?.note) ? 'No entry fee found' : 'Fee is known')
    },
    review: () => {
      sortScore -= 2
      reviewLabels.push('Verify fee')
    },
  })

  if (isLocalFit(opp)) {
    sortScore += 2
    reasons.push('Local or Japan-friendly')
  }

  if (RELATIONSHIP_CATEGORIES.has(opp.category)) {
    sortScore += 1
    reasons.push('Good relationship target')
  }

  if (opp.student_call) {
    sortScore -= 8
    reviewLabels.push('Eligibility may not fit')
  }

  if (feedback.followedIds?.has(opp.id)) {
    sortScore += 8
    reasons.unshift('You marked this worth watching')
  }

  if (feedback.maybeIds?.has(opp.id)) {
    // "Maybe later" = not now — push it BACK (but not hidden like not_for_me).
    sortScore -= 6
    reviewLabels.push('Saved for later')
  }

  if (feedback.hiddenIds?.has(opp.id)) {
    sortScore -= 100
    reviewLabels.push('Hidden by feedback')
  }

  if (feedback.hiddenCategories?.has(opp.category)) {
    sortScore -= 8
    reviewLabels.push('Similar items were marked not for me')
  }

  if (backendActionability.status === 'check_before_acting') sortScore -= 3
  if (backendActionability.status === 'review') sortScore -= 8
  if (backendActionability.status === 'closed_or_stale') sortScore -= 40

  const uniqueReasons = unique(backendActionability.reasons.length ? backendActionability.reasons : reasons).slice(0, 3)
  const uniqueReviewLabels = unique(backendActionability.flags.length ? backendActionability.flags : reviewLabels).slice(0, 3)
  const readiness = backendActionability.status
    ? (backendActionability.status === 'ready' ? 'ready' : 'review')
    : (uniqueReviewLabels.length || sortScore < 8 ? 'review' : 'ready')

  return {
    ...opp,
    recommendation: {
      readiness,
      actionabilityStatus: backendActionability.status || readiness,
      reasons: uniqueReasons,
      reviewLabels: uniqueReviewLabels,
      reasonLine: buildReasonLine(uniqueReasons, uniqueReviewLabels),
      sourceSection: sectionKey,
      sortScore,
    },
  }
}

export function rankOpportunities(items, sectionKey = '', feedback = {}) {
  return items
    .map(opp => enrichOpportunity(opp, sectionKey, feedback))
    .sort((a, b) => b.recommendation.sortScore - a.recommendation.sortScore)
}

export function strongestPicks(sections, limit = 5, feedback = {}) {
  return Object.entries(sections || {})
    .filter(([sectionKey]) => STRONG_SECTIONS.has(sectionKey))
    .flatMap(([sectionKey, items]) => rankOpportunities(items || [], sectionKey, feedback))
    .filter(opp => opp.recommendation.readiness === 'ready')
    .sort((a, b) => b.recommendation.sortScore - a.recommendation.sortScore)
    .slice(0, limit)
}

export function feedbackSignalsFromActions(actions = {}) {
  const hiddenIds = new Set()
  const followedIds = new Set()
  const maybeIds = new Set()
  const hiddenCategories = new Set()

  Object.values(actions).forEach(entry => {
    if (!entry?.action) return
    if (entry.action === 'not_for_me') {
      hiddenIds.add(entry.id)
      if (entry.category) hiddenCategories.add(entry.category)
    }
    if (entry.action === 'follow') followedIds.add(entry.id)
    if (entry.action === 'maybe_later') maybeIds.add(entry.id)
  })

  return { hiddenIds, followedIds, maybeIds, hiddenCategories }
}

function checklistMap(opp) {
  return new Map((opp.checklist || []).map(item => [item.label, item]))
}

function applyChecklistSignal(checks, label, handlers) {
  const item = checks.get(label)
  if (!item) {
    handlers.review?.(item)
    return
  }
  if (item.status === 'ready') handlers.ready?.(item)
  else handlers.review?.(item)
}

function buildReasonLine(reasons, reviewLabels) {
  if (reasons.length) return reasons.join(' · ')
  if (reviewLabels.length) return `Needs a quick check: ${reviewLabels.map(humanizeFlag).join(' · ')}`
  return 'Mochi needs one more look before recommending this strongly.'
}

function backendRecommendation(opp) {
  return {
    status: opp.actionability_status || null,
    flags: Array.isArray(opp.review_flags) ? opp.review_flags : [],
    reasons: Array.isArray(opp.recommendation_reasons) ? opp.recommendation_reasons : [],
  }
}

function mediaReason(nativeMedium) {
  if (nativeMedium === 'watercolor') return 'Matches her watercolor practice'
  if (nativeMedium === 'book_arts') return 'Fits artist books or printed work'
  if (nativeMedium === 'illustration') return 'Fits illustration-forward work'
  return 'Matches her current body of work'
}

function isLocalFit(opp) {
  const city = String(opp.city || '').toLowerCase()
  const country = String(opp.country || '').toLowerCase()
  return city.includes('tokyo') || country.includes('japan')
}

function isEvergreen(opp) {
  return RELATIONSHIP_CATEGORIES.has(opp.category) || !opp.deadline
}

function feeLooksFree(note = '') {
  const text = String(note).toLowerCase()
  return text.includes('free') || text.includes('¥0') || text === '0'
}

function numeric(value) {
  const n = Number(value)
  return Number.isFinite(n) ? n : 0
}

function unique(values) {
  return [...new Set(values.filter(Boolean))]
}

function humanizeFlag(flag) {
  return String(flag).replaceAll('_', ' ')
}
