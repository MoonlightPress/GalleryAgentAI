// Law #2 of v2: no naked numbers. Scores become fit-words backed by evidence.

export function fitLevel(score) {
  const s = parseFloat(score) || 0
  if (s >= 8.5) return 'strong'
  if (s >= 7)   return 'good'
  if (s >= 5)   return 'worth'
  return 'quiet'
}

// Evidence chips derived from verifiable fields only (evidence > prediction).
export function evidenceChips(opp) {
  const chips = []
  if (opp.deadline && !opp.deadline_past && opp.checklist?.some(
    c => c.label === 'Deadline' && c.status === 'ready')) chips.push('deadline')
  if (opp.contact && String(opp.contact).includes('@')) chips.push('contact')
  if (opp.submission_page) chips.push('link')
  if (opp.email_en || opp.email_ja || opp.email_zh) chips.push('draft')
  return chips
}

// Venue-appropriate email language, mirroring api.py's locale rule.
export function emailForVenue(opp, lang) {
  const city = (opp.city || '').toLowerCase()
  const country = (opp.country || '').toLowerCase()
  if (city.includes('tokyo') || country.includes('japan')) return opp.email_ja || opp.email_en
  if (city.includes('beijing') || country.includes('china')) return opp.email_zh || opp.email_en
  // otherwise prefer the artist's UI language if a draft exists, else English
  return opp[`email_${lang}`] || opp.email_en
}
