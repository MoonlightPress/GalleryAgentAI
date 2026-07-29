// "New to her" tracking for the banner + card badges. Per-device, and — unlike a
// fixed time window — it survives any length of absence: an opportunity stays
// "new" until she actually returns and sees it, then clears on her NEXT visit.
//
// Model: a per-device "seen" set of opp-ids (localStorage). "New to her" = served
// now, not yet seen. On the first ever load we seed the seen-set with everything
// EXCEPT the current server-"new" batch, so a returning user sees the recent
// batch but isn't flooded with the entire catalog. After that it's pure
// set-difference — no time gate. She sees new things her whole visit; on
// session end (or dismiss) they're marked seen and are gone next visit.

const SEEN_KEY = 'mochi_seen_opps'
const SEEDED_KEY = 'mochi_new_seeded'

// ── Pure helpers (no storage) ────────────────────────────────────────────────

export function collectIds(sections, pred) {
  const out = new Set()
  for (const items of Object.values(sections || {})) {
    for (const o of items || []) {
      if (o && o.id && (!pred || pred(o))) out.add(o.id)
    }
  }
  return out
}

// First-load seed: all served ids EXCEPT the current server-is_new batch.
export function initialSeen(sections) {
  const serverNew = collectIds(sections, o => o.is_new)
  const seen = new Set()
  for (const id of collectIds(sections)) if (!serverNew.has(id)) seen.add(id)
  return seen
}

// New to this device = served now, not in the seen set.
export function freshIds(sections, seen) {
  const s = seen || new Set()
  const fresh = new Set()
  for (const id of collectIds(sections)) if (!s.has(id)) fresh.add(id)
  return fresh
}

// Banner headline is stricter than the badge: still open AND a ready pick.
export function isBannerWorthy(opp) {
  return !!(opp && !opp.deadline_past && opp.actionability_status === 'ready')
}

// How many fresh-to-her opps are also banner-worthy. The watch list is
// excluded: passed recurring entries land there with deadline cleared and
// past reset for display, so they'd pass isBannerWorthy while being
// next-edition reminders she cannot act on — they inflated the banner count.
export function bannerCount(sections, fresh) {
  let n = 0
  for (const [key, items] of Object.entries(sections || {})) {
    if (key === 'watch_list') continue
    for (const o of items || []) {
      if (o && o.id && fresh.has(o.id) && isBannerWorthy(o)) n++
    }
  }
  return n
}

// ── localStorage orchestration ───────────────────────────────────────────────

function readSeen() {
  try {
    const raw = localStorage.getItem(SEEN_KEY)
    return raw ? new Set(JSON.parse(raw)) : new Set()
  } catch { return new Set() }
}

function writeSeen(s) {
  try { localStorage.setItem(SEEN_KEY, JSON.stringify([...s])) } catch { /* best-effort */ }
}

let _fresh = null   // per-session cache so banner + every card agree

// Compute (and cache for the session) the fresh-to-her set, seeding on the first
// ever load. Returns empty until real data arrives — never seeds on an empty
// payload (which would permanently mark the seed done with nothing seen).
export function freshToHer(sections) {
  if (_fresh) return _fresh
  const all = collectIds(sections)
  if (all.size === 0) return new Set()
  let seen = readSeen()
  try {
    if (localStorage.getItem(SEEDED_KEY) !== '1') {
      seen = initialSeen(sections)
      writeSeen(seen)
      localStorage.setItem(SEEDED_KEY, '1')
    }
  } catch { /* best-effort — no seeding, treat all as fresh */ }
  _fresh = freshIds(sections, seen)
  return _fresh
}

export function isFresh(id) {
  return !!(_fresh && _fresh.has(id))
}

// Mark the current fresh set as seen so it clears next visit. Called on session
// end (pagehide) and on manual dismiss. Also empties the session cache so a
// dismissed/left banner doesn't reappear on in-session re-navigation.
export function markFreshSeen() {
  if (!_fresh || _fresh.size === 0) return
  const seen = readSeen()
  for (const id of _fresh) seen.add(id)
  writeSeen(seen)
  _fresh = new Set()
}

// Test-only: reset the session cache between cases.
export function _resetForTest() { _fresh = null }
