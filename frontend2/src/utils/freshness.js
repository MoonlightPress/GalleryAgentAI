const DAY_MS = 24 * 60 * 60 * 1000

export function formatFreshness(value, now = new Date()) {
  if (!value) return null
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return null

  const today = startOfDay(now)
  const updated = startOfDay(date)
  const diff = Math.round((today - updated) / DAY_MS)

  if (diff <= 0) return 'today'
  if (diff === 1) return 'yesterday'
  if (diff <= 6) return `${diff} days ago`

  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

function startOfDay(date) {
  return Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate())
}
