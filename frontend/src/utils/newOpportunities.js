// Pure helpers backing the "Mochi found something new" banner. The is_new
// flag itself (from /api/opportunities) is stateless and identical on every
// device; only the banner's dismissal is per-device, tracked here.

// Every opportunity id currently flagged is_new, across all sections.
export function allNewIds(sections) {
  const ids = new Set()
  for (const items of Object.values(sections || {})) {
    for (const opp of items || []) {
      if (opp && opp.is_new && opp.id) ids.add(opp.id)
    }
  }
  return ids
}

// How many new ids haven't been dismissed yet.
export function countUndismissed(sections, dismissedIds) {
  const dismissed = dismissedIds || new Set()
  let count = 0
  for (const id of allNewIds(sections)) {
    if (!dismissed.has(id)) count++
  }
  return count
}

// Drop dismissed ids that are no longer actually new (aged out of the
// window, or gone from the feed) - keeps localStorage small and
// self-cleaning instead of growing forever.
export function pruneDismissed(sections, dismissedIds) {
  const current = allNewIds(sections)
  const pruned = new Set()
  for (const id of (dismissedIds || [])) {
    if (current.has(id)) pruned.add(id)
  }
  return pruned
}
