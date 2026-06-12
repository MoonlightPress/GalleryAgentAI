// Shared card pieces for the Mochi page: fit badge + evidence popover,
// verified chips, deadline bit (law #1 guard), action row, feedback row,
// and the in-place detail body.
import { useState, useRef, useEffect } from 'react'
import { api, loc, copyText } from '../../utils/api'
import { isPastDeadline, daysUntil, formatDeadline } from '../../utils/deadlines'
import { fitLevel, evidenceChips, emailForVenue } from '../../utils/fitWords'
import { useLanguage } from '../../i18n/LanguageContext'
import { useLocalT } from '../../i18n/local'
import { strings } from './strings'

// ── Feedback (exactly v1 OppCard.jsx shape) ─────────────────────────────────
export const FEEDBACK_IDS = [
  { id: 'follow',      key: 'card.feedback.follow',   glyph: '★' },
  { id: 'applied',     key: 'card.feedback.applied',  glyph: '✓' },
  { id: 'maybe_later', key: 'card.feedback.maybe',    glyph: '◷' },
  { id: 'not_for_me',  key: 'card.feedback.notForMe', glyph: '✕' },
]

export async function saveFeedback(opp, action) {
  try {
    await api.feedback({
      opp_id:      opp.title || opp.name || opp.id,
      action,
      opp_name:    opp.name  || opp.title || '',
      opp_title:   opp.title || opp.name  || '',
      opp_website: opp.official_website   || '',
    })
  } catch {
    // best-effort — never block the UI on feedback
  }
}

export function FeedbackRow({ opp, onRemove, showToast }) {
  const { t } = useLanguage()
  const [picked, setPicked] = useState(null)

  async function handle(id) {
    const next = picked === id ? null : id
    setPicked(next)
    if (!next) return
    await saveFeedback(opp, next)
    if (next === 'applied') showToast(t('card.toast.logged'))
    if (next === 'not_for_me' && onRemove) onRemove(opp.id)
  }

  return (
    <div className="mv2-feedback" role="group" aria-label="feedback">
      {FEEDBACK_IDS.map(a => (
        <button
          key={a.id}
          className={`mv2-feedback-btn${picked === a.id ? ' mv2-feedback-btn--on' : ''}`}
          onClick={() => handle(a.id)}
          title={t(a.key)}
        >
          <span aria-hidden="true">{a.glyph}</span>
          <span className="mv2-feedback-label">{t(a.key)}</span>
        </button>
      ))}
    </div>
  )
}

// ── Fit word + evidence popover (law #2: no naked numbers) ──────────────────
export function FitBadge({ opp }) {
  const { lang } = useLanguage()
  const t2 = useLocalT(strings)
  const [open, setOpen] = useState(false)
  const ref = useRef(null)
  const level = fitLevel(opp.score || opp.overall_score)
  const chips = evidenceChips(opp)
  const bullets = loc(opp, 'bullets', lang) || []

  useEffect(() => {
    if (!open) return
    function away(e) { if (ref.current && !ref.current.contains(e.target)) setOpen(false) }
    document.addEventListener('mousedown', away)
    return () => document.removeEventListener('mousedown', away)
  }, [open])

  return (
    <span className="mv2-fit-wrap" ref={ref}
      onMouseEnter={() => setOpen(true)} onMouseLeave={() => setOpen(false)}>
      <button
        type="button"
        className={`fit fit--${level} mv2-fit-btn`}
        aria-expanded={open}
        onClick={() => setOpen(v => !v)}
      >
        {t2(`v2.mochi.fit.${level}`)}
      </button>
      {open && (bullets.length > 0 || chips.length > 0) && (
        <span className="mv2-evidence" role="tooltip">
          <span className="mv2-evidence-title">{t2('v2.mochi.evidence.title')}</span>
          {bullets.length > 0 && (
            <ul className="mv2-evidence-list">
              {bullets.map((b, i) => <li key={i}>{b}</li>)}
            </ul>
          )}
          {chips.length > 0 && <VerifiedChips opp={opp} chips={chips} />}
        </span>
      )}
    </span>
  )
}

export function VerifiedChips({ opp, chips }) {
  const t2 = useLocalT(strings)
  const list = chips || evidenceChips(opp)
  if (!list.length) return null
  return (
    <span className="mv2-chips">
      {list.map(c => (
        <span key={c} className="chip-verified">{t2(`v2.mochi.chip.${c}`)}</span>
      ))}
    </span>
  )
}

// ── Deadline bit — law #1: never render a dead date as a live action ────────
export function DeadlineBit({ opp }) {
  const { t, lang } = useLanguage()
  const t2 = useLocalT(strings)

  if (isPastDeadline(opp) || opp.closed_this_cycle) {
    return <span className="chip-caution">{t2('v2.mochi.focus.recheck')}</span>
  }
  const days = daysUntil(opp)
  if (days === null) return null
  const label = formatDeadline(opp.deadline, lang)
  const urgency = days <= 3 ? ' mv2-deadline--urgent' : days <= 7 ? ' mv2-deadline--soon' : ''
  return (
    <span className={`pill mv2-deadline${urgency}`}>
      {label}
      {days >= 0 && days <= 14 && (
        <span className="mv2-deadline-days">
          {days === 0 ? t('cal.today') : days === 1 ? t('cal.tomorrow') : t('cal.daysLeft', { n: days })}
        </span>
      )}
    </span>
  )
}

// ── Action row: Copy email (THE button) / Open page / Details ───────────────
export function ActionRow({ opp, isOpen, onDetails, showToast }) {
  const { t, lang } = useLanguage()
  const t2 = useLocalT(strings)
  const draft = emailForVenue(opp, lang)
  const page = opp.submission_page || opp.official_website

  async function handleCopy() {
    const ok = await copyText(draft)
    if (ok) showToast(t2('v2.mochi.act.copied'))
  }

  return (
    <div className="mv2-actions">
      {draft && (
        <button className="btn-warm" onClick={handleCopy}>{t2('v2.mochi.act.copyEmail')}</button>
      )}
      {page && (
        <a className="btn-quiet mv2-open" href={page} target="_blank" rel="noreferrer">
          {t2('v2.mochi.act.openPage')}
        </a>
      )}
      <button className={`btn-quiet${isOpen ? ' btn-quiet--active' : ''}`} onClick={onDetails}>
        {isOpen ? t('card.close') : t('card.details')}
      </button>
    </div>
  )
}

// ── In-place detail body (rendered inside the expanded card) ────────────────
const EMAIL_TABS = [['ja', '日本語'], ['zh', '中文'], ['en', 'English']]

function defaultEmailTab(opp, lang) {
  const city = (opp.city || '').toLowerCase()
  const country = (opp.country || '').toLowerCase()
  if ((city.includes('tokyo') || country.includes('japan')) && opp.email_ja) return 'ja'
  if ((city.includes('beijing') || country.includes('china')) && opp.email_zh) return 'zh'
  if (opp[`email_${lang}`]) return lang
  return 'en'
}

export function DetailBody({ opp, showToast }) {
  const { t, lang } = useLanguage()
  const t2 = useLocalT(strings)
  const [tab, setTab] = useState(() => defaultEmailTab(opp, lang))
  const bullets = loc(opp, 'bullets', lang) || []
  const warning = loc(opp, 'soft_warning', lang)
  const nextAction = lang === 'en' ? opp.next_action : (opp[`next_action_${lang}`] || opp.next_action)
  const draft = opp[`email_${tab}`]

  async function copyDraft() {
    const ok = await copyText(draft)
    if (ok) showToast(t2('v2.mochi.act.copied'))
  }

  return (
    <div className="mv2-detail">
      <div className="mv2-detail-left">
        {opp.checklist?.length > 0 && (
          <div className="mv2-detail-block">
            <div className="mv2-detail-label">{t('detail.label.checklist')}</div>
            <ul className="mv2-checklist">
              {opp.checklist.map((item, i) => {
                const label = (lang === 'zh' && item.label_zh) ? item.label_zh
                            : (lang === 'ja' && item.label_ja) ? item.label_ja : item.label
                const note  = (lang === 'zh' && item.note_zh)  ? item.note_zh
                            : (lang === 'ja' && item.note_ja)  ? item.note_ja : item.note
                return (
                  <li key={i} className={`mv2-check mv2-check--${item.status || 'unknown'}`}>
                    <span className="mv2-check-mark" aria-hidden="true">
                      {item.status === 'ready' ? '✓' : item.status === 'missing' ? '✗' : '○'}
                    </span>
                    <span><strong>{label}</strong>{note ? <span className="mv2-check-note"> — {note}</span> : null}</span>
                  </li>
                )
              })}
            </ul>
          </div>
        )}

        {bullets.length > 0 && (
          <div className="mv2-detail-block">
            <div className="mv2-detail-label">{t('detail.label.keyPoints')}</div>
            <ul className="mv2-bullets">
              {bullets.map((b, i) => <li key={i}>{b}</li>)}
            </ul>
          </div>
        )}

        {nextAction && (
          <div className="mv2-detail-block">
            <div className="mv2-detail-label">{t('detail.label.howApply')}</div>
            <p>{nextAction}</p>
          </div>
        )}

        {warning && (
          <div className="mv2-detail-block">
            <span className="chip-caution mv2-warning">{warning}</span>
          </div>
        )}
      </div>

      <div className="mv2-detail-right">
        <div className="mv2-email-head">
          <span className="mv2-detail-label">{t('detail.label.emailDraft')}</span>
          <span className="mv2-email-tabs">
            {EMAIL_TABS.map(([key, label]) => (
              <button
                key={key}
                className={`mv2-email-tab${tab === key ? ' mv2-email-tab--on' : ''}`}
                onClick={() => setTab(key)}
              >
                {label}
              </button>
            ))}
          </span>
        </div>
        {draft ? (
          <>
            <pre className="mv2-email-body">{draft}</pre>
            <button className="btn-warm mv2-email-copy" onClick={copyDraft}>
              {t('detail.copyDraft')}
            </button>
          </>
        ) : (
          <p className="mv2-email-empty">{t('detail.email.empty')}</p>
        )}
      </div>
    </div>
  )
}
