// Shared localization helpers — one place so no component falls through to raw
// English in the Chinese view.
//
// Background: each component used to carry its own `loc(field)` accessor that
// returned `opp[field]` (the English source) whenever a `_zh` was missing. On a
// zh-first dashboard that leaked English ("Twice-yearly (spring/autumn) — watch
// @mo…", "Unknown", "Check source"). These helpers fix that centrally:
//   1. Known sentinel values ("Unknown", "TBD", "Check source", …) route through
//      i18n so they read in the active language.
//   2. A free-text English value with no `_zh` is SUPPRESSED in a non-English
//      view (returns '') rather than echoed — the caller hides the line. The
//      pipeline's translation layer fills `_zh`; until it does, calm-empty beats
//      an English leak.
//   3. Internal placeholders ("Check source", "N/A", …) never reach the screen.

// Sentinel English values that have a clean i18n equivalent. Compared
// case-insensitively after trimming. Keys resolve through the bound t().
const SENTINEL_I18N = {
  'unknown':       'loc.unknown',
  'tbd':           'loc.unknown',
  'n/a':           'loc.unknown',
  'na':            'loc.unknown',
  'none':          'loc.unknown',
  'check source':  'loc.verify',
  'check site':    'loc.verify',
  'check':         'loc.verify',
  'to be confirmed': 'loc.unknown',
  'rolling':       'loc.rolling',
  'ongoing':       'loc.rolling',
  'open':          'loc.rolling',
  'no fixed deadline': 'loc.rolling',
}

// Does a string look like plain English free text (Latin-heavy, no CJK)?
// Used to decide whether a no-`_zh` value would leak English into a zh view.
// Hiragana, Katakana, CJK Unified Ideographs (+ Ext-A), compatibility ideographs,
// CJK symbols/punctuation, and fullwidth/halfwidth forms. Unicode-escaped so the
// source stays ASCII (no irregular-whitespace lint from a literal range).
const CJK_RE = /[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3000-\u303f\uff00-\uffef]/
const LATIN_RE = /[A-Za-z]/

export function isEnglishText(s) {
  if (!s) return false
  return LATIN_RE.test(s) && !CJK_RE.test(s)
}

// Map a sentinel value to its i18n key, or null if it isn't a sentinel.
function sentinelKey(value) {
  if (value == null) return null
  return SENTINEL_I18N[String(value).trim().toLowerCase()] || null
}

// locF(opp, field, lang, t) — the hardened field accessor.
//   - returns `field_zh` / `field_ja` when present (the localized data)
//   - routes a sentinel English value through i18n
//   - in a non-English view, suppresses a no-translation English free-text value
//     ('' → caller hides the line) instead of echoing English
//   - English view always shows the source value
// `t` is the bound translator (LanguageContext). It's optional; without it,
// sentinels are still suppressed rather than leaked in non-English views.
export function locF(opp, field, lang, t) {
  if (!opp) return ''
  const localized = lang !== 'en' ? opp[`${field}_${lang}`] : (opp[`${field}_en`] ?? opp[field])
  const raw = opp[field]
  const value = localized != null && localized !== '' ? localized : raw

  if (value == null || value === '') return ''

  // Sentinel routing happens regardless of language so "Unknown" never shows.
  const sk = sentinelKey(value)
  if (sk) return t ? t(sk) : ''

  if (lang === 'en') return value

  // We have a localized value (had a `_${lang}`)? Trust it.
  if (localized != null && localized !== '') return localized

  // Only a raw (source) value survives. If it reads as English in a zh/ja view,
  // suppress it rather than leak English. If it already contains CJK (e.g. a
  // Japanese venue note in the ja view, or proper-noun-heavy mixed text), keep it.
  return isEnglishText(value) ? '' : value
}

// ── Deadlines ───────────────────────────────────────────────────────────────

const EN_MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']
const JA_WEEKDAYS = ['日','月','火','水','木','金','土']

// Parse the messy stored deadline strings into a Date, or null when there's no
// real single date (rolling / TBD / unparseable). Mirrors the parser that lived
// in OppDetailPanel so there's one implementation.
export function parseDeadlineDate(str) {
  if (!str) return null
  const s = String(str).trim()
  if (/^(tbd|check|n\/a|na|unknown|none|no fixed|ongoing|rolling|open|twice|entry period|to be)/i.test(s)) return null
  if (/^\d{4}-\d{2}-\d{2}/.test(s)) {
    const d = new Date(s.slice(0, 10) + 'T00:00:00')
    return isNaN(d.getTime()) ? null : d
  }
  const jp = s.match(/(\d{4})年(\d{1,2})月(\d{1,2})日/)
  if (jp) { const d = new Date(+jp[1], +jp[2] - 1, +jp[3]); return isNaN(d.getTime()) ? null : d }
  const mdy = s.match(/([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})/)
  if (mdy) { const d = new Date(`${mdy[1]} ${mdy[2]}, ${mdy[3]}`); return isNaN(d.getTime()) ? null : d }
  const dmy = s.match(/(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)\s+(\d{4})/)
  if (dmy) { const d = new Date(`${dmy[2]} ${dmy[1]}, ${dmy[3]}`); return isNaN(d.getTime()) ? null : d }
  return null
}

// Format a parseable deadline in the active language; return the trimmed source
// when it isn't a single parseable date (e.g. "rolling").
export function formatDeadline(str, lang) {
  const d = parseDeadlineDate(str)
  if (!d) return str ? String(str).trim() : str
  if (lang === 'zh') return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
  if (lang === 'ja') return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日（${JA_WEEKDAYS[d.getDay()]}）`
  return `${EN_MONTHS[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`
}

// localizeDeadline(opp, lang, t) — the display string for a deadline:
//   - prefers `deadline_zh` / `deadline_ja` when present
//   - else formats the parseable `deadline`
//   - routes sentinels through i18n; never echoes a raw English placeholder
export function localizeDeadline(opp, lang, t) {
  if (!opp) return ''
  const pre = lang !== 'en' ? opp[`deadline_${lang}`] : null
  const source = pre != null && pre !== '' ? pre : opp.deadline
  if (source == null || source === '') return ''
  const sk = sentinelKey(source)
  if (sk) return t ? t(sk) : ''
  // If a localized deadline string was supplied, trust it as-is.
  if (pre != null && pre !== '') return pre
  const d = parseDeadlineDate(source)
  if (d) return formatDeadline(source, lang)
  // Unparseable free text: don't leak English into a zh/ja view.
  if (lang !== 'en' && isEnglishText(source)) return t ? t('loc.verify') : ''
  return String(source).trim()
}

// Whole days from today until the deadline (negative = past). null when there's
// no real date.
export function daysUntilDeadline(str) {
  const d = parseDeadlineDate(str)
  if (!d) return null
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const target = new Date(d)
  target.setHours(0, 0, 0, 0)
  return Math.round((target - today) / 86400000)
}

// Urgent = a real deadline within `withinDays` days from today (and not past).
export function isUrgentDeadline(str, withinDays = 7) {
  const days = daysUntilDeadline(str)
  return days != null && days >= 0 && days <= withinDays
}
