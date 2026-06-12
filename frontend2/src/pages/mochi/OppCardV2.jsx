// Hunt Board card v2 — painted icon, fit word with evidence, full sentences
// (CSS clamp only), action row, always-visible feedback, in-place expansion.
import { useState } from 'react'
import { loc } from '../../utils/api'
import { useLanguage } from '../../i18n/LanguageContext'
import { catIcon } from './catIcons'
import { ActionRow, DeadlineBit, DetailBody, FeedbackRow, FitBadge } from './cardParts'

function orgDiffers(opp) {
  const name = (opp.name || '').toLowerCase()
  const org = (opp.organization || '').trim()
  if (!org) return false
  const orgLow = org.toLowerCase()
  return orgLow !== name && !name.includes(orgLow)
}

export default function OppCardV2({ opp, isOpen, onDetails, onRemove, showToast, muted }) {
  const { t, lang } = useLanguage()
  const [fading, setFading] = useState(false)
  const summary = loc(opp, 'summary', lang)
  const why = loc(opp, 'why_card', lang) || loc(opp, 'why_it_fits', lang)
  const catKey = `cat.${opp.category}`
  const catLabel = opp.category ? (t(catKey) === catKey ? opp.category : t(catKey)) : ''

  function handleRemove(id) {
    // gentle fade before the card leaves the grid
    setFading(true)
    setTimeout(() => onRemove && onRemove(id), 450)
  }

  return (
    <article
      className={`card card--hover mv2-card${isOpen ? ' mv2-card--open' : ''}${fading ? ' mv2-card--fading' : ''}${muted ? ' mv2-card--muted' : ''}`}
    >
      <header className="mv2-card-head">
        <img className="mv2-card-icon" src={catIcon(opp.category)} alt="" />
        <div className="mv2-card-headtext">
          <h3 className="h-card mv2-card-name">{loc(opp, 'name', lang)}</h3>
          {orgDiffers(opp) && <div className="mv2-card-org">{opp.organization}</div>}
        </div>
        <FitBadge opp={opp} />
      </header>

      <div className="mv2-card-pills">
        {catLabel && <span className="pill">{catLabel}</span>}
        {opp.city && <span className="pill pill--loc">{opp.city}</span>}
        <DeadlineBit opp={opp} />
      </div>

      {summary && <p className="mv2-card-summary clamp-3">{summary}</p>}
      {why && <p className="mv2-card-why voice clamp-2">{why}</p>}

      <ActionRow opp={opp} isOpen={isOpen} onDetails={onDetails} showToast={showToast} />

      {isOpen && <DetailBody opp={opp} showToast={showToast} />}

      <footer className="mv2-card-foot">
        <FeedbackRow opp={opp} onRemove={handleRemove} showToast={showToast} />
      </footer>
    </article>
  )
}
