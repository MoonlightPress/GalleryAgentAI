// Today's Focus card — one of exactly three. Carries the deadline guard:
// a stale slot never shows its date as the action date (law #1).
import { loc } from '../../utils/api'
import { useLanguage } from '../../i18n/LanguageContext'
import { useLocalT } from '../../i18n/local'
import { strings } from './strings'
import { catIcon } from './catIcons'
import { ActionRow, DeadlineBit, DetailBody, VerifiedChips } from './cardParts'

// role → label/time keys (global tf.* dictionary) + warm accent token.
// Stretch accent is plum — never blue (spec §Page 1).
const ROLES = {
  quick_win:    { label: 'tf.role.quickWin',    time: 'tf.time.min5',    accent: 'var(--leaf-deep)', wash: 'var(--leaf-faint)' },
  high_impact:  { label: 'tf.role.highImpact',  time: 'tf.time.min3060', accent: 'var(--gold-deep)', wash: 'var(--gold-faint)' },
  stretch_goal: { label: 'tf.role.stretchGoal', time: 'tf.time.longer',  accent: 'var(--plum)',      wash: 'var(--plum-faint)' },
}

export default function FocusCard({ card, role, isOpen, onDetails, showToast }) {
  const { t, lang } = useLanguage()
  const t2 = useLocalT(strings)
  if (!card) return null
  const cfg = ROLES[role] || ROLES.high_impact
  const summary = loc(card, 'summary', lang)
  const why = loc(card, 'why_card', lang) || loc(card, 'why_it_fits', lang)
  // Follow-up nudges (overdue application / stale contact) wear their own label
  const isFollowup = card.submission_followup || card.crm_followup

  return (
    <article
      className={`card mv2-focus${isOpen ? ' mv2-card--open mv2-focus--open' : ''}`}
      style={{ '--fc-accent': cfg.accent, '--fc-wash': cfg.wash }}
    >
      <div className="mv2-focus-role">
        <span className="mv2-focus-dot" aria-hidden="true" />
        <span className="mv2-focus-label">{isFollowup ? t2('v2.mochi.focus.followup') : t(cfg.label)}</span>
        <span className="mv2-focus-time">{t(cfg.time)}</span>
      </div>

      <header className="mv2-card-head">
        <img className="mv2-card-icon" src={catIcon(card.category)} alt="" />
        <h3 className="h-card mv2-card-name">{loc(card, 'name', lang)}</h3>
      </header>

      <div className="mv2-card-pills">
        {card.city && (
          <span className="pill pill--loc">
            {card.city}{card.country && card.country !== card.city ? ` · ${card.country}` : ''}
          </span>
        )}
        {/* DeadlineBit renders the caution chip for stale items — never the dead date */}
        <DeadlineBit opp={card} />
      </div>

      {summary && <p className="mv2-card-summary clamp-3">{summary}</p>}
      {why && <p className="mv2-card-why voice clamp-2">{why}</p>}

      <div className="mv2-focus-chips"><VerifiedChips opp={card} /></div>

      <ActionRow opp={card} isOpen={isOpen} onDetails={onDetails} showToast={showToast} />

      {isOpen && <DetailBody opp={card} showToast={showToast} />}
    </article>
  )
}
