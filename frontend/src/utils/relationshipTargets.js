// Pure display logic for Mochi's "people to reach out to" view.
// The /api/contacts endpoint already sorts by status; here we order by how
// strong a relationship target each contact is, and note how to reach them.

const PRIORITY_RANK = { high: 0, medium: 1, low: 2 }

function priorityOf(contact) {
  const p =
    (contact.crm_analysis && contact.crm_analysis.priority) ||
    contact.priority ||
    ''
  return PRIORITY_RANK[String(p).toLowerCase()] ?? 3
}

// How the artist can reach this contact, best channel first.
export function reachVia(contact = {}) {
  if (contact.contact_email) return 'email'
  if (contact.official_website || contact.contact_page || contact.submission_page) {
    return 'website'
  }
  return 'none'
}

// Sort by priority (high first), stable within equal priority, annotate reachVia,
// and optionally cap the list. Safe on null/undefined input.
export function prepareRelationshipTargets(contacts, { limit } = {}) {
  if (!Array.isArray(contacts)) return []
  const ranked = contacts
    .map((c, i) => ({ c, i, rank: priorityOf(c) }))
    .sort((a, b) => a.rank - b.rank || a.i - b.i)
    .map(({ c }) => ({ ...c, reachVia: reachVia(c) }))
  return typeof limit === 'number' ? ranked.slice(0, limit) : ranked
}
