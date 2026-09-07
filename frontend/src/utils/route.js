// Hash routing — so a link can point at a companion, not just at the app.
//
// Hash rather than path because the built app is served under /mochi/ by nginx
// with no SPA rewrite: a path router would 404 on refresh or on any link she
// opens cold. The hash never reaches the server, so /mochi/#observe is still a
// request for /mochi/index.html and always resolves.
//
// Shape: #<page> or #<page>/<tab>, e.g. #observe, #observe/calendar.
// Anything unrecognised degrades to discover rather than erroring — a stale or
// mistyped link should land her somewhere useful, never on a blank screen.

// 'observe2' is the Saffron restructure prototype. It is deliberately NOT in
// the nav — the only way in is typing the hash (or /mochi2, which nginx
// redirects here), so she cannot land on it by accident while it is being
// worked on. Remove it from this list to retire the prototype.
export const PAGES = ['discover', 'observe', 'observe2', 'refine']

// Saffron's sub-tabs, in the order SaffronPage renders them. Only 'observe'
// carries a tab today; the others ignore the second segment.
export const SAFFRON_TABS = ['strategy', 'profile', 'calendar', 'relationships', 'money']

export const DEFAULT_ROUTE = { page: 'discover', tab: null }

/**
 * Read a location hash into { page, tab }.
 * Tolerates: no hash, '#', a leading '#/', trailing slashes, mixed case,
 * unknown pages, and unknown tabs (dropped, page kept).
 */
export function parseHash(hash) {
  if (typeof hash !== 'string') return { ...DEFAULT_ROUTE }
  const raw = hash.trim().replace(/^#/, '').replace(/^\/+/, '').replace(/\/+$/, '').trim()
  if (!raw) return { ...DEFAULT_ROUTE }

  const [rawPage, rawTab] = raw.split('/')
  const page = PAGES.includes(rawPage.toLowerCase()) ? rawPage.toLowerCase() : null
  if (!page) return { ...DEFAULT_ROUTE }

  const tab = rawTab && page === 'observe' && SAFFRON_TABS.includes(rawTab.toLowerCase())
    ? rawTab.toLowerCase()
    : null
  return { page, tab }
}

/**
 * Build the hash for a route. Discover with no tab is the app's front door, so
 * it gets the bare '#discover' rather than an empty hash — an empty hash would
 * leave whatever hash was there before in the address bar.
 */
export function formatHash(page, tab) {
  const p = PAGES.includes(page) ? page : 'discover'
  const okTab = tab && p === 'observe' && SAFFRON_TABS.includes(tab)
  return `#${p}${okTab ? `/${tab}` : ''}`
}

/** True when two routes are the same page+tab (used to avoid pointless history entries). */
export function sameRoute(a, b) {
  return !!a && !!b && a.page === b.page && (a.tab || null) === (b.tab || null)
}
