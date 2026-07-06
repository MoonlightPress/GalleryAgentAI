// Pure helpers backing the "Mochi found something new" banner. The is_new flag
// itself (from /api/opportunities) is stateless and identical on every device;
// only the banner's dismissal is per-device, tracked here.
//
// The banner HEADLINE deliberately counts fewer things than carry the per-card
// "New" badge. A pipeline run can add 100+ opportunities at once; announcing
// "found 103 new things" is just "the pipeline ran" and earns an eye-roll. So
// the banner counts only ones worth stopping for — newly added, still open, and
// a genuinely ready/good-fit pick. The passive per-card badge (OppCard reads
// opp.is_new directly) still shows on everything recent.

export function isBannerWorthy(opp) {
  return !!(
    opp &&
    opp.is_new &&
    !opp.deadline_past &&
    opp.actionability_status === 'ready'
  )
}

// Ids of the banner-worthy opportunities, across all sections.
export function bannerWorthyIds(sections) {
  const ids = new Set()
  for (const items of Object.values(sections || {})) {
    for (const opp of items || []) {
      if (isBannerWorthy(opp) && opp.id) ids.add(opp.id)
    }
  }
  return ids
}

// How many banner-worthy ids haven't been dismissed yet.
export function countUndismissed(sections, dismissedIds) {
  const dismissed = dismissedIds || new Set()
  let count = 0
  for (const id of bannerWorthyIds(sections)) {
    if (!dismissed.has(id)) count++
  }
  return count
}

// Drop dismissed ids that are no longer banner-worthy (aged out, closed, or
// gone from the feed) — keeps localStorage small and self-cleaning.
export function pruneDismissed(sections, dismissedIds) {
  const current = bannerWorthyIds(sections)
  const pruned = new Set()
  for (const id of (dismissedIds || [])) {
    if (current.has(id)) pruned.add(id)
  }
  return pruned
}
