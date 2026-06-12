// Small shared pieces for the Peppercorn page.
import { useState } from 'react'

// Warm outcome language — atelier tokens only (classes in peppercorn.css).
const TONE_BY_STATUS = {
  // submissions
  accepted: 'leaf', rejected: 'rose', pending: 'gold', waitlisted: 'parchment', withdrawn: 'muted',
  // exhibitions
  shown: 'leaf', planned: 'gold', cancelled: 'muted',
  // contacts / CRM
  ready_to_review: 'gold', contacted: 'gold', sent_inquiry: 'gold', in_contact: 'gold',
  submitted: 'gold', researching: 'parchment', responded: 'leaf', ongoing: 'leaf',
  relationship: 'leaf', not_a_fit: 'muted', cold: 'muted',
  // career events
  conversation: 'gold', visited: 'parchment', sold: 'leaf', featured: 'gold',
}

export function tone(status) {
  return TONE_BY_STATUS[status] || 'parchment'
}

export function OutcomeChip({ status, label }) {
  return <span className={`pep-chip pep-chip--${tone(status)}`}>{label}</span>
}

// Brief "saved ✓" flash on a button.
export function useSaved() {
  const [saved, setSaved] = useState(false)
  function flash() { setSaved(true); setTimeout(() => setSaved(false), 2200) }
  return [saved, flash]
}

export function Field({ label, children, wide }) {
  return (
    <div className={`pep-field${wide ? ' pep-field--wide' : ''}`}>
      <label className="pep-label tiny">{label}</label>
      {children}
    </div>
  )
}
