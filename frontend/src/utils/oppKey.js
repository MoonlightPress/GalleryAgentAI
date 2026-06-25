// One stable identifier for an opportunity, used everywhere a card needs to be
// keyed: feedback POST, localStorage persistence, and suppression.
//
// The reviewer flagged a real inconsistency: feedback POSTed under
// `opp.title || opp.name || opp.id` while suppression called `onSuppressed(opp.id)`.
// When those differ, a "not for me" could persist under one key and re-appear
// under another on reload. This collapses everything onto one key.
//
// The served `id` is the backend's canonical opp id (api.py `_opp_id`, an md5
// hash). The app's `hiddenIds`/suppression set and the server's own suppressed
// list both key on this hash — so `id` is the one correct key. We fall back to
// title/name only for the rare card built without an id (e.g. CRM follow-up
// cards). Always a string.
export function oppKey(opp) {
  if (!opp) return ''
  return String(opp.id || opp.title || opp.name || '')
}
