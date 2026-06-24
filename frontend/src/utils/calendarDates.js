// Shared date helpers for the deadline calendars (Mochi discover view + Saffron
// seasonal calendar). Kept out of the component files so fast-refresh stays happy.

export function parseDeadline(str) {
  if (!str) return null
  const s = str.trim()
  if (/^(tbd|check|n\/a|unknown|no fixed|ongoing|rolling|open|twice|entry period)/i.test(s)) return null

  // ISO: 2026-06-27
  if (/^\d{4}-\d{2}-\d{2}/.test(s)) {
    const d = new Date(s.slice(0, 10) + 'T00:00:00')
    return isNaN(d.getTime()) ? null : d
  }
  // Japanese: 2026年06月06日
  const jpMatch = s.match(/(\d{4})年(\d{1,2})月(\d{1,2})日/)
  if (jpMatch) {
    const d = new Date(+jpMatch[1], +jpMatch[2] - 1, +jpMatch[3])
    return isNaN(d.getTime()) ? null : d
  }
  // English month-first: June 7, 2026
  const mdy = s.match(/([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})/)
  if (mdy) {
    const d = new Date(`${mdy[1]} ${mdy[2]}, ${mdy[3]}`)
    return isNaN(d.getTime()) ? null : d
  }
  // Day-month-year: 19th December 2025
  const dmy = s.match(/(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)\s+(\d{4})/)
  if (dmy) {
    const d = new Date(`${dmy[2]} ${dmy[1]}, ${dmy[3]}`)
    return isNaN(d.getTime()) ? null : d
  }
  return null
}

// Local YYYY-MM-DD (avoid toISOString's UTC shift).
export const keyOf = (d) =>
  `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
