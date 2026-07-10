// Foreground-time tracking for a single page.
//
// The naive version — "fire a leave whenever visibilitychange says hidden" —
// produced a log nobody could read. Safari (both iOS and macOS) churns the
// visibility state around app-switcher snapshots, tab close, and bfcache, so a
// hidden→visible→hidden cycle can complete in 200ms. Each cycle looked like a
// separate 1-3 second visit. In one week's log, 13 of her 22 recorded "sessions"
// were this artefact and 9 were real.
//
// Two rules fix it:
//   1. A hide is only a leave if it *lasts*. Wait out a short grace period; if
//      the page comes back inside it, nothing happened and nothing is reported.
//   2. Dwell is the sum of genuinely-foreground time. Hidden gaps are excluded,
//      so a tab left open overnight no longer reports a nine-hour read.
//
// `pagehide` is exempt from the grace: a closing tab has no future in which to
// come back, and a delayed beacon would never be sent.
//
// Known limitation: a macOS Safari window sitting behind another window still
// reports `visible`. Only tab-level attention is observable from here.

export const FLAP_GRACE_MS = 1200

// Below this much foreground time, the page was shown but not used. In her log
// every such window followed a long absence, lasted 1-4s, and contained no
// click and no network request: a phone waking with the tab still open, not a
// visit. Flagged rather than dropped, so the digest can exclude them without
// the raw log losing anything.
export const GLANCE_MS = 3000

export function createVisibilityTracker({
  emit,
  now = () => Date.now(),
  setTimer = setTimeout,
  clearTimer = clearTimeout,
  graceMs = FLAP_GRACE_MS,
}) {
  let visibleSince = now()
  let accumulated = 0        // foreground ms banked on this page so far
  let hiddenAt = null
  let pendingTimer = null
  let leaveEmitted = false

  function bankVisibleTime(at) {
    if (visibleSince != null) {
      accumulated += at - visibleSince
      visibleSince = null
    }
  }

  function cancelPending() {
    if (pendingTimer != null) {
      clearTimer(pendingTimer)
      pendingTimer = null
    }
  }

  function emitLeave(reason) {
    if (leaveEmitted) return
    leaveEmitted = true
    emit({ type: 'leave', reason, dwell_ms: accumulated, glance: accumulated < GLANCE_MS })
  }

  return {
    onHidden() {
      if (hiddenAt != null) return           // already hidden; ignore the repeat
      const at = now()
      hiddenAt = at
      bankVisibleTime(at)
      pendingTimer = setTimer(() => {
        pendingTimer = null
        emitLeave('hidden')
      }, graceMs)
    },

    onVisible() {
      const at = now()
      if (pendingTimer != null) {
        // Came back inside the grace window: a flap, not a visit boundary.
        cancelPending()
        hiddenAt = null
        visibleSince = at
        return
      }
      if (leaveEmitted) {
        emit({ type: 'return', away_ms: hiddenAt != null ? at - hiddenAt : 0 })
        leaveEmitted = false
        accumulated = 0
      }
      hiddenAt = null
      visibleSince = at
    },

    // The tab is going away for real — flush now, grace be damned.
    onPageHide() {
      cancelPending()
      bankVisibleTime(hiddenAt ?? now())
      emitLeave('pagehide')
    },

    onPageChange() {
      cancelPending()
      visibleSince = now()
      accumulated = 0
      hiddenAt = null
      leaveEmitted = false
    },
  }
}
