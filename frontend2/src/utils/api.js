// Thin fetch helpers — every page consumes the same endpoints as v1.

async function getJSON(url) {
  const r = await fetch(url)
  if (!r.ok) throw new Error(`${url} → ${r.status}`)
  return r.json()
}

async function sendJSON(url, body, method = 'POST') {
  const r = await fetch(url, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!r.ok) throw new Error(`${url} → ${r.status}`)
  return r.json()
}

export const api = {
  opportunities: () => getJSON('/api/opportunities'),
  today:         () => getJSON('/api/today'),
  saffron:       () => getJSON('/api/saffron'),
  careerStrategy:() => getJSON('/api/career_strategy'),
  peppercorn:    () => getJSON('/api/peppercorn'),
  savePeppercorn:(d) => sendJSON('/api/peppercorn', d),
  submissions:   () => getJSON('/api/submissions'),
  addSubmission: (d) => sendJSON('/api/submissions', d),
  contacts:      () => getJSON('/api/contacts'),
  addContact:    (d) => sendJSON('/api/contacts', d),
  patchContact:  (name, d) => sendJSON(`/api/contacts/${encodeURIComponent(name)}`, d, 'PATCH'),
  exhibitions:   () => getJSON('/api/exhibition_log'),
  addExhibition: (d) => sendJSON('/api/exhibition_log', d),
  careerEvents:  () => getJSON('/api/career_events'),
  addCareerEvent:(d) => sendJSON('/api/career_events', d),
  feedback:      (d) => sendJSON('/api/feedback', d),
  feedbackInsights: () => getJSON('/api/feedback/insights'),
  suppressCategory: (category) => sendJSON('/api/feedback/suppress-category', { category }),
}

// Localized field accessor shared by all pages: loc(opp, 'summary', lang)
export function loc(obj, field, lang) {
  if (!obj) return ''
  if (lang === 'zh' && obj[field + '_zh']) return obj[field + '_zh']
  if (lang === 'ja' && obj[field + '_ja']) return obj[field + '_ja']
  return obj[field] || ''
}

export async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch {
    // fallback for non-secure contexts
    const ta = document.createElement('textarea')
    ta.value = text
    document.body.appendChild(ta)
    ta.select()
    const ok = document.execCommand('copy')
    document.body.removeChild(ta)
    return ok
  }
}
