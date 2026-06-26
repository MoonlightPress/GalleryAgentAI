// Module-level GET cache. Survives component unmount/remount (page switches), so
// a page renders its last-known data INSTANTLY instead of flashing a loading
// state, then revalidates in the background and replaces if anything changed
// (Scott: "just cache and replace if something changes"). Cleared on a full page
// reload, which is the right time to drop stale shapes after a deploy.
const _cache = new Map()
export const getCache = (url) => _cache.get(url)
export const setCache = (url, val) => { _cache.set(url, val) }
