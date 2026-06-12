// Law #1 of v2: never show a dead date as a live action.
// Mirrors api.py's _parse_deadline_date / _deadline_past so the UI is safe even
// when the backend serves stale entries (known gap: /api/today quick_win fallback
// and stretch_goal slots are ungated — see reports/ux_pass_2026-06/05_API_AUDIT.md).

const PLACEHOLDERS = /^(tbd|check|n\/a|unknown|none|varies|see website|no fixed|ongoing|rolling|open|未定|随時|要確認|待定)/i

const MONTHS = {
  jan: 0, feb: 1, mar: 2, apr: 3, may: 4, jun: 5,
  jul: 6, aug: 7, sep: 8, oct: 9, nov: 10, dec: 11,
}

export function parseDeadline(str) {
  if (!str) return null
  const s = String(str).trim()
  if (!s || PLACEHOLDERS.test(s)) return null

  let m = s.match(/(\d{4})-(\d{2})-(\d{2})/)
  if (m) return new Date(+m[1], +m[2] - 1, +m[3])

  m = s.match(/(\d{4})年(\d{1,2})月(\d{1,2})日/)
  if (m) return new Date(+m[1], +m[2] - 1, +m[3])

  m = s.match(/([A-Za-z]{3,})\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})/)
  if (m) {
    const mon = MONTHS[m[1].slice(0, 3).toLowerCase()]
    if (mon !== undefined) return new Date(+m[3], mon, +m[2])
  }

  m = s.match(/(\d{1,2})\s+([A-Za-z]{3,})\s+(\d{4})/)
  if (m) {
    const mon = MONTHS[m[2].slice(0, 3).toLowerCase()]
    if (mon !== undefined) return new Date(+m[3], mon, +m[1])
  }
  return null
}

// True when a parseable deadline is in the past (>1 day grace).
export function isPastDeadline(opp) {
  if (opp?.deadline_past) return true
  const d = parseDeadline(opp?.deadline)
  if (!d) return false
  return (Date.now() - d.getTime()) > 24 * 3600 * 1000
}

export function daysUntil(opp) {
  const d = parseDeadline(opp?.deadline)
  if (!d) return null
  return Math.ceil((d.getTime() - Date.now()) / (24 * 3600 * 1000))
}

const EN_MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December']
const JA_DAYS = ['日', '月', '火', '水', '木', '金', '土']

export function formatDeadline(str, lang) {
  const d = parseDeadline(str)
  if (!d) return str ? String(str).slice(0, 40) : ''
  if (lang === 'zh') return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
  if (lang === 'ja') return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日（${JA_DAYS[d.getDay()]}）`
  return `${EN_MONTHS[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`
}

// Partition a card list into { live, stale } per law #1.
export function splitStale(items) {
  const live = [], stale = []
  for (const it of items || []) (isPastDeadline(it) || it.closed_this_cycle ? stale : live).push(it)
  return { live, stale }
}
