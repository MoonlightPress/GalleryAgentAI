import { useState, useEffect, useRef, Component } from 'react'
import './PeppercornPage.css'
import { peppercornHero } from '../utils/heroImages'
import { getCache, setCache } from '../utils/apiCache'
import { useLanguage } from '../i18n/LanguageContext'
import { tfb } from '../i18n/translations'
import { track } from '../utils/track'

// ── Section error boundary ────────────────────────────────────────────────
// Defense-in-depth: a throw inside one section must NOT white-screen the whole
// dashboard. The real fixes live in each section; this just contains the blast
// radius to a single card if anything else ever throws during render.
class SectionErrorBoundary extends Component {
  constructor(props) { super(props); this.state = { error: null } }
  static getDerivedStateFromError(error) { return { error } }
  render() {
    if (this.state.error) {
      return (
        <section className="pp-section pp-section--error">
          <p className="pp-section-note">{this.props.fallback || 'This section hit a snag and was hidden so the rest of the page keeps working.'}</p>
        </section>
      )
    }
    return this.props.children
  }
}

// ── Carousel card ─────────────────────────────────────────────────────────

function CarouselCard({ card, isActive, onClick }) {
  return (
    <div
      className={`pp-card${isActive ? ' pp-card--active' : ''}${!card.sectionId ? ' pp-card--passive' : ''}`}
      onClick={() => onClick(card)}
    >
      <div className="pp-card-name">{card.name}</div>
      {card.current ? (
        <div className="pp-card-values">
          <span className="pp-card-current">{card.current}</span>
          {card.next && (
            <>
              <span className="pp-card-sep"> / </span>
              <span className="pp-card-next">{card.next}</span>
            </>
          )}
        </div>
      ) : (
        <div className="pp-card-cta">{card.cta}</div>
      )}
      <div className="pp-card-desc">{card.desc}</div>
    </div>
  )
}

// ── Section shell (open/close controlled by parent) ───────────────────────

// Small painted watercolor accent per section (reuses the existing /icons set),
// keyed by section id, so the informational sections get a little warmth.
const PP_ICON_BASE = `${import.meta.env.BASE_URL}icons/`
const SECTION_ICON = {
  'artist-statement': 'ic_editorial',
  'career-goals':     'ic_award',
  'submission-log':   'ic_books',
  'exhibition-log':   'ic_gallery',
  'venue-log':        'ic_cafe',
  'contacts':         'ic_people',
}

function SectionShell({ id, title, subtitle, synopsis, isOpen, onToggle, sectionRef, children }) {
  const icon = SECTION_ICON[id]
  return (
    <section
      id={id}
      ref={sectionRef}
      className={`pp-section${isOpen ? '' : ' pp-section--closed'}`}
    >
      <button className="pp-toggle" onClick={onToggle}>
        <div className="pp-toggle-left">
          <div className="pp-toggle-text">
            <h2 className="pp-title">{title}</h2>
            {isOpen
              ? (subtitle && <p className="pp-subtitle">{subtitle}</p>)
              : ((synopsis || subtitle) && <p className="pp-synopsis">{synopsis || subtitle}</p>)}
          </div>
        </div>
        <span className={`pp-chevron${isOpen ? ' pp-chevron--open' : ''}`}>▾</span>
      </button>
      {isOpen && <div className="pp-body">{children}</div>}
    </section>
  )
}

function SaveBtn({ onSave, saved }) {
  const { t } = useLanguage()
  return (
    <button className={`pp-save${saved ? ' pp-save--done' : ''}`} onClick={onSave}>
      {saved ? t('pp.saved.done') : t('pp.save')}
    </button>
  )
}

function useSaved() {
  const [saved, setSaved] = useState(false)
  function flash() { setSaved(true); setTimeout(() => setSaved(false), 2200) }
  return [saved, flash]
}

// ── Instagram / Social strategy section ──────────────────────────────────

// ── Artist statement section ──────────────────────────────────────────────

function StatementExample() {
  const [show, setShow] = useState(false)
  const { t } = useLanguage()
  return (
    <div className="pp-stmt-example">
      <button className="pp-example-toggle" onClick={() => setShow(s => !s)}>
        {show ? t('pp.exToggle.hide') : t('pp.exToggle.show')}
      </button>
      {show && (
        <div className="pp-example-body">
          <div className="pp-example-col">
            <div className="pp-example-label">{t('pp.ex.generic')}</div>
            <p className="pp-example-text pp-example-text--generic">
              {t('pp.ex.generic.text')}
            </p>
          </div>
          <div className="pp-example-vs">→</div>
          <div className="pp-example-col">
            <div className="pp-example-label">{t('pp.ex.specific')}</div>
            <p className="pp-example-text pp-example-text--specific">
              {t('pp.ex.specific.text')}
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

function ArtistStatementSection({ data, onSave, isOpen, onToggle, sectionRef }) {
  const [text, setText] = useState(data || '')
  const [saved, flash] = useSaved()
  const { t } = useLanguage()
  // eslint-disable-next-line react-hooks/set-state-in-effect -- sync async-loaded data into editable local state
  useEffect(() => { setText(data || '') }, [data])

  return (
    <SectionShell
      id="artist-statement"
      sectionRef={sectionRef}
      title={t('pp.sec.statement')}
      subtitle={t('pp.sub.statement')}
      isOpen={isOpen}
      onToggle={onToggle}
    >
      <p className="pp-section-note">{t('pp.stmt.note')}</p>
      <StatementExample />
      <textarea
        className="pp-statement"
        value={text}
        onChange={e => setText(e.target.value)}
        placeholder={t('pp.stmt.placeholder')}
        rows={7}
      />
      <SaveBtn saved={saved} onSave={() => { onSave(text); flash() }} />
    </SectionShell>
  )
}

// ── Saffron's questions section ───────────────────────────────────────────

// Static keys for logic (answeredCount, ordering) — language-independent
const QUESTION_KEYS = [
  'posting_frequency',
  'audience_geography',
  'has_sold_work',
  'new_publication_planned',
  'has_artist_statement',
  'tide_china_contact',
  'second_exhibition_planned',
  'price_points',
]

function buildQuestions(t) {
  return QUESTION_KEYS.map((key, i) => ({
    key,
    text: t(`pp.q.${i}.text`),
    why:  t(`pp.q.${i}.why`),
    options: [0, 1, 2, 3].map(j => t(`pp.q.${i}.opt.${j}`)),
  }))
}

// Legacy seed tokens that predate the current free-text/option answer flow. The
// canonical schema (api.py) seeds every saffron answer to null; these stale
// values (a bare boolean `true` for has_artist_statement, a slug "daily" for
// posting_frequency) leaked in from an older format and are NOT real answers she
// gave. Treat them as unanswered so they don't show as completed.
const LEGACY_SEED_ANSWERS = new Set(['daily'])

// A real answer is a non-empty trimmed STRING produced via the answer UI — never
// a boolean/number/object and never a known legacy seed. This is the single
// source of truth for "answered": it drives the completed count, the done-list,
// and (critically) keeps non-string values out of the draft editor, where
// `.trim()` on a boolean would throw and white-screen the whole page.
function isAnswered(v) {
  return typeof v === 'string' && v.trim() !== '' && !LEGACY_SEED_ANSWERS.has(v.trim())
}

// Coerce any stored value into a safe string for the editable draft. Guards the
// render path: a stale boolean/number can never reach `<textarea>`/`.trim()`.
function draftFrom(v) {
  return typeof v === 'string' ? v : ''
}

function SaffronQuestionsSection({ data, onSave, isOpen, onToggle, sectionRef }) {
  const [answers, setAnswers] = useState(data || {})
  const { t } = useLanguage()
  // eslint-disable-next-line react-hooks/set-state-in-effect -- sync async-loaded data into editable local state
  useEffect(() => { setAnswers(data || {}) }, [data])

  const QUESTIONS = buildQuestions(t)

  const answeredCount    = QUESTION_KEYS.filter(k => isAnswered(answers[k])).length
  const allAnswered      = answeredCount === QUESTION_KEYS.length
  const firstUnanswered  = QUESTIONS.findIndex(q => !isAnswered(answers[q.key]))
  const startIdx         = firstUnanswered === -1 ? 0 : firstUnanswered
  const [activeIdx, setActiveIdx] = useState(startIdx)
  const [draft,     setDraft]     = useState(draftFrom(answers[QUESTIONS[startIdx]?.key]))

  const currentQ = QUESTIONS[activeIdx]

  function selectQ(idx) { setActiveIdx(idx); setDraft(draftFrom(answers[QUESTIONS[idx].key])) }

  function saveAnswer() {
    if (!draft.trim()) return
    const next = { ...answers, [currentQ.key]: draft.trim() }
    setAnswers(next)
    onSave(next)
    const nextUnanswered = QUESTIONS.findIndex((q, i) => i > activeIdx && !isAnswered(next[q.key]))
    if (nextUnanswered !== -1) { setActiveIdx(nextUnanswered); setDraft('') }
  }

  function clearAnswer(key) { const next = { ...answers, [key]: null }; setAnswers(next); onSave(next) }
  function skipQ() {
    const next = QUESTIONS.findIndex((q, i) => i > activeIdx && !isAnswered(answers[q.key]))
    if (next !== -1) { setActiveIdx(next); setDraft(draftFrom(answers[QUESTIONS[next].key])) }
  }

  const remaining = QUESTIONS.length - answeredCount
  const subtitle = allAnswered
    ? t('pp.sub.saffronQs.done')
    : t('pp.sub.saffronQs.rem', { n: remaining, s: remaining !== 1 ? 's' : '' })

  return (
    <SectionShell
      id="saffron-questions"
      sectionRef={sectionRef}
      title={t('pp.sec.saffronQs')}
      synopsis={t('pp.syn.saffronQs')}
      subtitle={subtitle}
      isOpen={isOpen}
      onToggle={onToggle}
    >
      {allAnswered ? (
        <p className="pp-section-note pp-section-note--gentle">
          {t('pp.sub.saffronQs.done')}
        </p>
      ) : (
        <>
          <div className="pp-q-dots">
            {QUESTIONS.map((q, i) => (
              <button
                key={q.key}
                className={['pp-q-dot', isAnswered(answers[q.key]) ? 'pp-q-dot--done' : '', i === activeIdx ? 'pp-q-dot--active' : ''].join(' ').trim()}
                onClick={() => selectQ(i)}
                title={q.text}
              />
            ))}
            <span className="pp-q-count">{answeredCount} / {QUESTIONS.length}</span>
          </div>

          <div className="pp-q-card">
            <div className="pp-q-num">{t('pp.question', { n: activeIdx + 1 })}</div>
            <p className="pp-q-text">{currentQ.text}</p>
            <p className="pp-q-why">{currentQ.why}</p>
            {currentQ.options && (
              <div className="pp-q-options">
                {currentQ.options.map((opt, i) => (
                  <button key={i} className="pp-q-option" onClick={() => setDraft(opt)}>{opt}</button>
                ))}
              </div>
            )}
            <textarea
              className="pp-q-input"
              value={draft}
              onChange={e => setDraft(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && e.metaKey && saveAnswer()}
              placeholder={t('pp.q.input.placeholder')}
              rows={3}
            />
            <div className="pp-q-actions">
              <button className="pp-save pp-save--answer" onClick={saveAnswer} disabled={!draft.trim()}>
                {t('pp.saveAnswer')}
              </button>
              {!isAnswered(answers[currentQ.key]) && (
                <button className="pp-skip" onClick={skipQ}>{t('pp.comeBack')}</button>
              )}
              {isAnswered(answers[currentQ.key]) && (
                <button className="pp-skip" onClick={() => clearAnswer(currentQ.key)}>{t('pp.clearAnswer')}</button>
              )}
            </div>
          </div>
        </>
      )}

      {answeredCount > 0 && (
        <div className="pp-q-done-list">
          <div className="pp-block-label">{t('pp.answered', { n: answeredCount })}</div>
          {QUESTIONS.filter(q => isAnswered(answers[q.key])).map(q => (
            <div key={q.key} className="pp-q-done-row" onClick={() => selectQ(QUESTIONS.indexOf(q))}>
              <span className="pp-q-done-check">✓</span>
              <div className="pp-q-done-body">
                <div className="pp-q-done-q">{q.text}</div>
                <div className="pp-q-done-a">{draftFrom(answers[q.key])}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </SectionShell>
  )
}

// ── Career goals section ──────────────────────────────────────────────────

const GOAL_PLACEHOLDER_KEYS = [
  'pp.goal.ph.0',
  'pp.goal.ph.1',
  'pp.goal.ph.2',
  'pp.goal.ph.3',
  'pp.goal.ph.4',
]

function CareerGoalsSection({ data, onSave, isOpen, onToggle, sectionRef }) {
  const [goals,  setGoals]  = useState(data || [])
  const [input,  setInput]  = useState('')
  const [, flash]           = useSaved()
  const [phIdx]             = useState(() => Math.floor(Math.random() * GOAL_PLACEHOLDER_KEYS.length))
  const [shownFirstNote, setShownFirstNote] = useState((data || []).length > 0)
  const { t, lang } = useLanguage()
  // Display localized seed text (state keeps the full goal objects, incl. _zh/_ja).
  const goalText = g => (lang === 'zh' && g.text_zh) || (lang === 'ja' && g.text_ja) || g.text
  // eslint-disable-next-line react-hooks/set-state-in-effect -- sync async-loaded data into editable local state
  useEffect(() => { setGoals(data || []) }, [data])

  function addGoal() {
    const trimmed = input.trim()
    if (!trimmed) return
    const isFirst = goals.length === 0
    const next = [...goals, { id: Date.now(), text: trimmed, done: false }]
    setGoals(next); setInput('')
    if (isFirst) setShownFirstNote(true)
    onSave(next); flash()
    track({ type: 'action', action: 'goal_add', name: trimmed })
  }
  function removeGoal(id) { const n = goals.filter(g => g.id !== id); setGoals(n); onSave(n) }
  function toggleDone(id) {
    const n = goals.map(g => g.id === id ? { ...g, done: !g.done } : g)
    setGoals(n); onSave(n)
  }

  const active = goals.filter(g => !g.done)
  const done   = goals.filter(g =>  g.done)

  return (
    <SectionShell
      id="career-goals"
      sectionRef={sectionRef}
      title={t('pp.sec.goals')}
      subtitle={t('pp.sub.goals')}
      isOpen={isOpen}
      onToggle={onToggle}
    >
      {goals.length === 0 && (
        <p className="pp-section-note">{t('pp.goals.empty')}</p>
      )}

      {active.length > 0 && (
        <div className="pp-goal-list">
          {active.map(g => (
            <div key={g.id} className="pp-goal-row">
              <button className="pp-goal-toggle" onClick={() => toggleDone(g.id)} title={t('pp.goal.markDone')} aria-label={t('pp.goal.markDone')} />
              <span className="pp-goal-text">{goalText(g)}</span>
              <button className="pp-goal-remove" onClick={() => removeGoal(g.id)} title={t('pp.goal.remove')}>×</button>
            </div>
          ))}
        </div>
      )}

      <div className="pp-goal-add">
        <input
          className="pp-goal-input"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && addGoal()}
          placeholder={t(GOAL_PLACEHOLDER_KEYS[phIdx]) + '…'}
        />
        <button className="pp-add-btn" onClick={addGoal}>{t('pp.add')}</button>
      </div>

      {shownFirstNote && goals.length === 1 && (
        <p className="pp-first-goal-note">{t('pp.goals.firstNote')}</p>
      )}

      {done.length > 0 && (
        <div className="pp-goal-list pp-goal-list--done">
          {done.map(g => (
            <div key={g.id} className="pp-goal-row pp-goal-row--done">
              <button className="pp-goal-toggle" onClick={() => toggleDone(g.id)} title={t('pp.goal.reopen')}>✓</button>
              <span className="pp-goal-text">{goalText(g)}</span>
              <button className="pp-goal-remove" onClick={() => removeGoal(g.id)} title={t('pp.goal.remove')}>×</button>
            </div>
          ))}
        </div>
      )}
    </SectionShell>
  )
}

// ── Preferences section ───────────────────────────────────────────────────

const TIER_NS     = [1, 2, 3, 4]
const TRACK_IDS   = ['publication', 'gallery', 'hybrid']
const AVOID_IDS   = ['photography_calls', 'high_fees', 'international_travel', 'digital_only', 'large_group']
const GEO_IDS     = ['tokyo', 'japan', 'beijing', 'international']
const FEE_IDS     = ['free', 'low', 'medium', 'any']
const SURFACE_IDS = ['zines_books', 'gallery_shows', 'residencies', 'cafes_bookshops', 'art_fairs']

function PreferencesSection({ data, onSave, isOpen, onToggle, sectionRef }) {
  const { t } = useLanguage()
  const pri  = (data || {}).priorities  || {}
  const pref = (data || {}).preferences || {}

  const TIERS = TIER_NS.map(n => ({ n, label: t(`pp.tier.${n}.label`), desc: t(`pp.tier.${n}.desc`) }))
  const TRACKS = TRACK_IDS.map(id => ({ id, label: t(`pp.track.${id}.label`), desc: t(`pp.track.${id}.desc`) }))
  const AVOID_OPTIONS = AVOID_IDS.map(id => ({ id, label: t(`pp.avoid.${id}`) }))
  const GEO_OPTIONS = GEO_IDS.map(id => ({ id, label: t(`pp.geo.${id}.label`), desc: t(`pp.geo.${id}.desc`) }))
  const FEE_OPTIONS = FEE_IDS.map(id => ({ id, label: t(`pp.fee.${id}`) }))
  const SURFACE_OPTIONS = SURFACE_IDS.map(id => ({ id, label: t(`pp.surface.${id}`) }))

  const [tiers, setTiers] = useState(pri.active_tiers   || [1, 2])
  const [track, setTrack] = useState(pri.primary_track   || 'hybrid')
  const [avoid, setAvoid] = useState(pri.avoid           || [])
  const [geo,   setGeo]   = useState(pref.geo_focus      || ['tokyo', 'international'])
  const [fee,   setFee]   = useState(pref.fee_tolerance  || 'low')
  const [more,  setMore]  = useState(pref.surface_more   || ['zines_books'])
  const [less,  setLess]  = useState(pref.surface_less   || [])
  const [saved, flash]    = useSaved()

  /* eslint-disable react-hooks/set-state-in-effect -- sync async-loaded data into editable local state */
  useEffect(() => {
    const p  = (data || {}).priorities  || {}
    const pr = (data || {}).preferences || {}
    setTiers(p.active_tiers  || [1, 2])
    setTrack(p.primary_track || 'hybrid')
    setAvoid(p.avoid         || [])
    setGeo(pr.geo_focus      || ['tokyo', 'international'])
    setFee(pr.fee_tolerance  || 'low')
    setMore(pr.surface_more  || ['zines_books'])
    setLess(pr.surface_less  || [])
  }, [data])
  /* eslint-enable react-hooks/set-state-in-effect */

  const toggleTier = n   => setTiers(ts => ts.includes(n) ? ts.filter(tier => tier !== n) : [...ts, n].sort())
  const toggleAvoid = id => setAvoid(av => av.includes(id) ? av.filter(a => a !== id) : [...av, id])
  const toggleGeo   = id => setGeo(gs => gs.includes(id) ? gs.filter(g => g !== id) : [...gs, id])
  const toggleMore  = id => { setMore(ms => ms.includes(id) ? ms.filter(m => m !== id) : [...ms, id]); setLess(ls => ls.filter(l => l !== id)) }
  const toggleLess  = id => { setLess(ls => ls.includes(id) ? ls.filter(l => l !== id) : [...ls, id]); setMore(ms => ms.filter(m => m !== id)) }

  function handleSave() {
    onSave({ priorities: { active_tiers: tiers, primary_track: track, avoid }, preferences: { geo_focus: geo, fee_tolerance: fee, surface_more: more, surface_less: less } })
    flash()
  }

  return (
    <SectionShell
      id="preferences"
      sectionRef={sectionRef}
      title={t('pp.sec.preferences')}
      subtitle={t('pp.sub.preferences')}
      isOpen={isOpen}
      onToggle={onToggle}
    >
      <p className="pp-section-note">{t('pp.prefs.note')}</p>

      <div className="pp-group">
        <div className="pp-group-label">{t('pp.group.activeTiers')}</div>
        <p className="pp-group-hint">{t('pp.group.tiersHint')}</p>
        {TIERS.map(tier => (
          <label key={tier.n} className="pp-check-row">
            <input type="checkbox" className="pp-check" checked={tiers.includes(tier.n)} onChange={() => toggleTier(tier.n)} />
            <span className="pp-check-label"><strong>{tier.label}</strong><span className="pp-check-desc">{tier.desc}</span></span>
          </label>
        ))}
      </div>

      <div className="pp-group">
        <div className="pp-group-label">{t('pp.group.primaryTrack')}</div>
        {TRACKS.map(tr => (
          <label key={tr.id} className="pp-radio-row">
            <input type="radio" className="pp-radio" name="pp-track" value={tr.id} checked={track === tr.id} onChange={() => setTrack(tr.id)} />
            <span className="pp-check-label"><strong>{tr.label}</strong><span className="pp-check-desc">{tr.desc}</span></span>
          </label>
        ))}
      </div>

      <div className="pp-group">
        <div className="pp-group-label">{t('pp.group.avoid')}</div>
        {AVOID_OPTIONS.map(opt => (
          <label key={opt.id} className="pp-check-row">
            <input type="checkbox" className="pp-check" checked={avoid.includes(opt.id)} onChange={() => toggleAvoid(opt.id)} />
            <span className="pp-check-label">{opt.label}</span>
          </label>
        ))}
      </div>

      <div className="pp-group">
        <div className="pp-group-label">{t('pp.group.geoFocus')}</div>
        {GEO_OPTIONS.map(opt => (
          <label key={opt.id} className="pp-check-row">
            <input type="checkbox" className="pp-check" checked={geo.includes(opt.id)} onChange={() => toggleGeo(opt.id)} />
            <span className="pp-check-label"><strong>{opt.label}</strong>{opt.desc && <span className="pp-check-desc">{opt.desc}</span>}</span>
          </label>
        ))}
      </div>

      <div className="pp-group">
        <div className="pp-group-label">{t('pp.group.feeTolerance')}</div>
        {FEE_OPTIONS.map(opt => (
          <label key={opt.id} className="pp-radio-row">
            <input type="radio" className="pp-radio" name="pp-fee" value={opt.id} checked={fee === opt.id} onChange={() => setFee(opt.id)} />
            <span className="pp-check-label">{opt.label}</span>
          </label>
        ))}
      </div>

      <div className="pp-group">
        <div className="pp-group-label">{t('pp.group.catWeighting')}</div>
        <p className="pp-group-hint">{t('pp.group.catHint')}</p>
        <div className="pp-surface-grid">
          <div className="pp-surface-header">
            <span />
            <span className="pp-surface-col-label">{t('pp.group.more')}</span>
            <span className="pp-surface-col-label">{t('pp.group.less')}</span>
          </div>
          {SURFACE_OPTIONS.map(opt => (
            <div key={opt.id} className="pp-surface-row">
              <span className="pp-surface-name">{opt.label}</span>
              <input type="checkbox" className="pp-check pp-check--more" checked={more.includes(opt.id)} onChange={() => toggleMore(opt.id)} />
              <input type="checkbox" className="pp-check pp-check--less" checked={less.includes(opt.id)} onChange={() => toggleLess(opt.id)} />
            </div>
          ))}
        </div>
      </div>

      <SaveBtn saved={saved} onSave={handleSave} />
    </SectionShell>
  )
}

// ── Submission log section ────────────────────────────────────────────────

const OUTCOME_OPTIONS = [
  { value: 'pending' },
  { value: 'accepted' },
  { value: 'rejected' },
  { value: 'waitlisted' },
  { value: 'withdrawn' },
]

// Sub-navigation for a long log list: "All" + one chip per value present, with
// counts. Reuses the CRM filter-tab styling so every log reads the same, and the
// chips auto-hide when there's nothing to navigate (Scott, 2026-06-26: the long
// lists need sub-navigation, not one giant scroll to wade through).
const LOG_FILTER_ALL = { en: 'All', zh: '全部', ja: 'すべて' }
function LogFilterTabs({ rows, field, labelFor, active, onChange, lang }) {
  const present = []
  const counts = {}
  for (const r of rows) {
    const v = r[field]
    if (v == null || v === '') continue
    if (!(v in counts)) { counts[v] = 0; present.push(v) }
    counts[v]++
  }
  if (present.length <= 1) return null
  return (
    <div className="crm-filter-tabs">
      <button
        className={`crm-filter-tab${active === 'all' ? ' crm-filter-tab--active' : ''}`}
        onClick={() => onChange('all')}
      >
        {(LOG_FILTER_ALL[lang] || LOG_FILTER_ALL.en)} ({rows.length})
      </button>
      {present.map(v => (
        <button
          key={v}
          className={`crm-filter-tab${active === v ? ' crm-filter-tab--active' : ''}`}
          onClick={() => onChange(v)}
        >
          {labelFor(v)} ({counts[v]})
        </button>
      ))}
    </div>
  )
}

function SubmissionLogSection({ isOpen, onToggle, sectionRef }) {
  const { t, lang } = useLanguage()
  const [submissions, setSubmissions] = useState([])
  const [filter, setFilter] = useState('all')
  const [form, setForm] = useState({ date: '', venue: '', what: '', outcome: 'pending', notes: '' })
  const [saving, setSaving] = useState(false)
  const [saved, flash] = useSaved()

  useEffect(() => {
    fetch('/api/submissions')
      .then(r => r.ok ? r.json() : [])
      .then(data => setSubmissions(Array.isArray(data) ? data : []))
      .catch(() => {})
  }, [])

  function setField(k, v) { setForm(f => ({ ...f, [k]: v })) }

  async function submitEntry() {
    if (!form.venue.trim() || !form.what.trim()) return
    setSaving(true)
    try {
      const r = await fetch('/api/submissions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form, date: form.date || new Date().toISOString().slice(0, 10) }),
      })
      if (r.ok) {
        const updated = await fetch('/api/submissions').then(r2 => r2.json())
        setSubmissions(Array.isArray(updated) ? updated : [])
        setForm({ date: '', venue: '', what: '', outcome: 'pending', notes: '' })
        flash()
      }
    } finally {
      setSaving(false)
    }
  }

  const OUTCOME_COLORS = {
    accepted:   { bg: '#f0fbee', border: '#8fc98a', text: '#2e6626' },
    rejected:   { bg: '#fef5f5', border: '#e8b0b0', text: '#8b2a2a' },
    waitlisted: { bg: '#fffbef', border: '#e8d890', text: '#7a6010' },
    withdrawn:  { bg: '#f5f5f5', border: '#ccc',    text: '#555' },
    pending:    { bg: '#f5f8ff', border: '#b0c4e8', text: '#2a4080' },
  }

  const sorted = [...submissions].sort((a, b) => (b.date || '').localeCompare(a.date || ''))
  const visible = filter === 'all' ? sorted : sorted.filter(s => s.outcome === filter)

  return (
    <SectionShell
      id="submission-log"
      sectionRef={sectionRef}
      title={t('pp.sec.sublog')}
      synopsis={t('pp.syn.sublog')}
      subtitle={submissions.length === 0 ? t('pp.sub.sublog.empty') : t('pp.sub.sublog.count', { n: submissions.length, s: submissions.length !== 1 ? 's' : '' })}
      isOpen={isOpen}
      onToggle={onToggle}
    >
      <p className="pp-section-note">{t('pp.sublog.note')}</p>

      <div className="pp-sub-form">
        <div className="pp-sub-form-row">
          <div className="pp-sub-field">
            <label className="pp-sub-label">{t('pp.sublog.date')}</label>
            <input
              type="date"
              className="pp-sub-input"
              value={form.date}
              onChange={e => setField('date', e.target.value)}
            />
          </div>
          <div className="pp-sub-field pp-sub-field--wide">
            <label className="pp-sub-label">{t('pp.sublog.venue')}</label>
            <input
              type="text"
              className="pp-sub-input"
              value={form.venue}
              onChange={e => setField('venue', e.target.value)}
              placeholder={t('pp.sublog.ph.venue')}
            />
          </div>
          <div className="pp-sub-field">
            <label className="pp-sub-label">{t('pp.sublog.outcome')}</label>
            <select className="pp-sub-select" value={form.outcome} onChange={e => setField('outcome', e.target.value)}>
              {OUTCOME_OPTIONS.map(o => <option key={o.value} value={o.value}>{t('pp.outcome.' + o.value)}</option>)}
            </select>
          </div>
        </div>
        <div className="pp-sub-field">
          <label className="pp-sub-label">{t('pp.sublog.what')}</label>
          <input
            type="text"
            className="pp-sub-input"
            value={form.what}
            onChange={e => setField('what', e.target.value)}
            placeholder={t('pp.sublog.ph.what')}
          />
        </div>
        <div className="pp-sub-field">
          <label className="pp-sub-label">{t('pp.sublog.notes')}</label>
          <input
            type="text"
            className="pp-sub-input"
            value={form.notes}
            onChange={e => setField('notes', e.target.value)}
            placeholder={t('pp.sublog.ph.notes')}
          />
        </div>
        <button
          className={`pp-save${saved ? ' pp-save--done' : ''}`}
          onClick={submitEntry}
          disabled={saving || !form.venue.trim() || !form.what.trim()}
        >
          {saved ? t('pp.sublog.btn.done') : t('pp.sublog.btn')}
        </button>
      </div>

      <LogFilterTabs rows={sorted} field="outcome" labelFor={v => tfb(t, 'pp.outcome.' + v, v)} active={filter} onChange={setFilter} lang={lang} />
      {visible.length > 0 && (
        <div className="pp-sub-list">
          {visible.map(s => {
            const colors = OUTCOME_COLORS[s.outcome] || OUTCOME_COLORS.pending
            return (
              <div key={s.id || s.date + s.venue} className="pp-sub-row" style={{ borderLeft: `3px solid ${colors.border}` }}>
                <div className="pp-sub-row-header">
                  <span className="pp-sub-venue">{s.venue}</span>
                  <span className="pp-sub-outcome" style={{ background: colors.bg, color: colors.text, border: `1px solid ${colors.border}` }}>
                    {tfb(t, 'pp.outcome.' + s.outcome, s.outcome)}
                  </span>
                  {s.date && <span className="pp-sub-date">{s.date}</span>}
                </div>
                <div className="pp-sub-what">{s.what}</div>
                {s.notes && <div className="pp-sub-notes">{s.notes}</div>}
              </div>
            )
          })}
        </div>
      )}
    </SectionShell>
  )
}

// ── Exhibition log section ────────────────────────────────────────────────

const SHOW_TYPE_OPTIONS = [
  { value: 'group' },
  { value: 'solo' },
  { value: 'fair' },
  { value: 'residency_show' },
]

const SHOW_OUTCOME_OPTIONS = [
  { value: 'shown' },
  { value: 'planned' },
  { value: 'cancelled' },
]

const SHOW_OUTCOME_COLORS = {
  shown:     { bg: '#f0fbee', border: '#8fc98a', text: '#2e6626' },
  planned:   { bg: '#f5f8ff', border: '#b0c4e8', text: '#2a4080' },
  cancelled: { bg: '#f5f5f5', border: '#ccc',    text: '#555' },
}

function ExhibitionLogSection({ isOpen, onToggle, sectionRef, liveGroupShows, onCountsChanged }) {
  const { t, lang } = useLanguage()
  const [shows, setShows] = useState([])
  const [filter, setFilter] = useState('all')
  const [form, setForm] = useState({ date: '', name: '', venue: '', type: 'group', outcome: 'shown', notes: '' })
  const [saving, setSaving] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [saved, flash] = useSaved()

  useEffect(() => {
    fetch('/api/exhibition_log')
      .then(r => r.ok ? r.json() : [])
      .then(d => setShows(Array.isArray(d) ? d : []))
      .catch(() => {})
  }, [])

  function setField(k, v) { setForm(f => ({ ...f, [k]: v })) }

  function resetForm() {
    setForm({ date: '', name: '', venue: '', type: 'group', outcome: 'shown', notes: '' })
    setEditingId(null)
  }

  function startEdit(s) {
    setForm({
      date: s.date || '', name: s.name || '', venue: s.venue || '',
      type: s.type || 'group', outcome: s.outcome || 'shown', notes: s.notes || '',
    })
    setEditingId(s.id)
  }

  async function submitShow() {
    if (!form.name.trim() && !form.venue.trim()) return
    const wasEditing = !!editingId
    setSaving(true)
    try {
      // PATCH an existing entry when editing, POST a new one otherwise.
      const url = editingId ? `/api/exhibition_log/${editingId}` : '/api/exhibition_log'
      const r = await fetch(url, {
        method: editingId ? 'PATCH' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form }),
      })
      if (r.ok) {
        const updated = await fetch('/api/exhibition_log').then(r2 => r2.json())
        setShows(Array.isArray(updated) ? updated : [])
        resetForm()
        flash()
        onCountsChanged?.()  // refresh the canonical group-show count (shared with Saffron)
        track({ type: 'action', action: wasEditing ? 'exhibition_log_edit' : 'exhibition_log_add', name: form.name || form.venue })
      }
    } finally {
      setSaving(false)
    }
  }

  async function deleteShow(id) {
    try {
      const r = await fetch(`/api/exhibition_log/${id}`, { method: 'DELETE' })
      // Only drop it from the UI if the server actually deleted it — otherwise
      // it reappears on reload and the user thinks the delete worked.
      if (r.ok) { setShows(prev => prev.filter(s => s.id !== id)); onCountsChanged?.() }
    } catch { /* leave the row in place on network failure */ }
  }

  const sorted = [...shows].sort((a, b) => (b.date || '').localeCompare(a.date || ''))
  const visible = filter === 'all' ? sorted : sorted.filter(s => s.type === filter)
  // T0.6 — show THE canonical app-wide group-show count (the same number Saffron
  // uses), supplied by the server via /api/peppercorn live_counts. Never recompute
  // it locally (that diverged from Saffron the moment a show was logged). Fall back
  // to the logged-only count only if the canonical value hasn't loaded yet.
  const total = (typeof liveGroupShows === 'number')
    ? liveGroupShows
    : 1 + shows.filter(s => s.type === 'group').length

  return (
    <SectionShell
      id="exhibition-log"
      sectionRef={sectionRef}
      title={t('pp.sec.exlog')}
      synopsis={t('pp.syn.exlog')}
      subtitle={shows.length === 0 && total <= 1 ? t('pp.sub.exlog.empty') : t('pp.sub.exlog.count', { n: total })}
      isOpen={isOpen}
      onToggle={onToggle}
    >
      <p className="pp-section-note">{t('pp.exlog.note')}</p>

      <div className="pp-sub-form">
        <div className="pp-sub-form-row">
          <div className="pp-sub-field">
            <label className="pp-sub-label">{t('pp.exlog.date')}</label>
            <input
              type="month"
              className="pp-sub-input"
              value={form.date}
              onChange={e => setField('date', e.target.value)}
            />
          </div>
          <div className="pp-sub-field pp-sub-field--wide">
            <label className="pp-sub-label">{t('pp.exlog.name')}</label>
            <input
              type="text"
              className="pp-sub-input"
              value={form.name}
              onChange={e => setField('name', e.target.value)}
              placeholder={t('pp.exlog.ph.name')}
            />
          </div>
          <div className="pp-sub-field">
            <label className="pp-sub-label">{t('pp.exlog.type')}</label>
            <select className="pp-sub-select" value={form.type} onChange={e => setField('type', e.target.value)}>
              {SHOW_TYPE_OPTIONS.map(o => <option key={o.value} value={o.value}>{t('pp.showType.' + o.value)}</option>)}
            </select>
          </div>
          <div className="pp-sub-field">
            <label className="pp-sub-label">{t('pp.exlog.outcome')}</label>
            <select className="pp-sub-select" value={form.outcome} onChange={e => setField('outcome', e.target.value)}>
              {SHOW_OUTCOME_OPTIONS.map(o => <option key={o.value} value={o.value}>{t('pp.showOutcome.' + o.value)}</option>)}
            </select>
          </div>
        </div>
        <div className="pp-sub-field">
          <label className="pp-sub-label">{t('pp.exlog.venue')}</label>
          <input
            type="text"
            className="pp-sub-input"
            value={form.venue}
            onChange={e => setField('venue', e.target.value)}
            placeholder={t('pp.exlog.ph.venue')}
          />
        </div>
        <div className="pp-sub-field">
          <label className="pp-sub-label">{t('pp.exlog.notes')}</label>
          <input
            type="text"
            className="pp-sub-input"
            value={form.notes}
            onChange={e => setField('notes', e.target.value)}
            placeholder={t('pp.exlog.ph.notes')}
          />
        </div>
        <div className="pp-sub-form-actions">
          <button
            className={`pp-save${saved ? ' pp-save--done' : ''}`}
            onClick={submitShow}
            disabled={saving || (!form.name.trim() && !form.venue.trim())}
          >
            {saved ? t('pp.exlog.btn.done') : editingId ? t('pp.exlog.btn.update') : t('pp.exlog.btn')}
          </button>
          {editingId && (
            <button className="pp-sub-cancel" onClick={resetForm} disabled={saving}>
              {t('pp.exlog.cancel')}
            </button>
          )}
        </div>
      </div>

      <LogFilterTabs rows={[{ type: 'group' }, ...sorted]} field="type" labelFor={v => tfb(t, 'pp.showType.' + v, v)} active={filter} onChange={setFilter} lang={lang} />
      <div className="pp-sub-list">
        {/* The pinned first Japan exhibition (always a group show). */}
        {(filter === 'all' || filter === 'group') && (
        <div className="pp-sub-row pp-sub-row--system" style={{ borderLeft: '3px solid #8fc98a' }}>
          <div className="pp-sub-row-header">
            <span className="pp-sub-venue">Tide from China Part 1</span>
            <span className="pp-sub-outcome" style={{ background: '#f0fbee', color: '#2e6626', border: '1px solid #8fc98a' }}>
              {t('pp.showOutcome.shown')}
            </span>
            <span className="pp-sub-date">2023-02</span>
          </div>
          <div className="pp-sub-what">ACG_Labo, Harajuku, Tokyo · {t('pp.showType.group')}</div>
          <div className="pp-sub-notes">{t('pp.exlog.systemEntry')}</div>
        </div>
        )}

        {visible.map(s => {
          const colors = SHOW_OUTCOME_COLORS[s.outcome] || SHOW_OUTCOME_COLORS.shown
          return (
            <div key={s.id} className="pp-sub-row" style={{ borderLeft: `3px solid ${colors.border}` }}>
              <div className="pp-sub-row-header">
                <span className="pp-sub-venue">{s.name || s.venue}</span>
                <span className="pp-sub-outcome" style={{ background: colors.bg, color: colors.text, border: `1px solid ${colors.border}` }}>
                  {s.outcome ? t('pp.showOutcome.' + s.outcome) : ''}
                </span>
                {s.date && <span className="pp-sub-date">{s.date}</span>}
                <button className="pp-edit-btn" onClick={() => startEdit(s)} title={t('pp.exlog.edit')}>✎</button>
                <button className="pp-edit-btn" onClick={() => deleteShow(s.id)} title={t('pp.exlog.delete')}>×</button>
              </div>
              {s.venue && s.name && <div className="pp-sub-what">{s.venue} · {tfb(t, 'pp.showType.' + s.type, s.type)}</div>}
              {s.notes && <div className="pp-sub-notes">{s.notes}</div>}
            </div>
          )
        })}
      </div>
    </SectionShell>
  )
}

// ── Venue / CRM log section ───────────────────────────────────────────────

const VENUE_STATUS_OPTIONS = [
  { value: 'cold' },
  { value: 'researching' },
  { value: 'in_contact' },
  { value: 'submitted' },
  { value: 'ongoing' },
  { value: 'rejected' },
]

const VENUE_TYPE_OPTIONS = [
  { value: 'gallery' },
  { value: 'cafe_gallery' },
  { value: 'bookshop' },
  { value: 'zine_shop' },
  { value: 'artist_space' },
  { value: 'fair' },
  { value: 'institution' },
  { value: 'residency' },
  { value: 'other' },
]

const STATUS_COLORS = {
  cold:       { bg: '#f5f5f5', border: '#ccc',    text: '#555' },
  researching:{ bg: '#fdf5e8', border: '#e8c878', text: '#7a5010' },
  in_contact: { bg: '#f0f6ff', border: '#90aee0', text: '#1a3a80' },
  submitted:  { bg: '#fff8ef', border: '#e8b870', text: '#804a10' },
  ongoing:    { bg: '#f0fbee', border: '#8fc98a', text: '#2e6626' },
  rejected:   { bg: '#fef5f5', border: '#e8b0b0', text: '#8b2a2a' },
}

function VenueContactCard({ contact: c, onUpdate }) {
  const { t, lang } = useLanguage()
  const loc = (obj, f) => (obj && ((lang === 'zh' && obj[f + '_zh']) || (lang === 'ja' && obj[f + '_ja']) || obj[f])) || ''
  const [editing, setEditing] = useState(false)
  const [editStatus, setEditStatus] = useState(c.status || 'cold')
  const [editNotes, setEditNotes] = useState(c.notes || '')
  const [editLastContacted, setEditLastContacted] = useState(c.last_contacted || '')
  const [saving, setSaving] = useState(false)

  const colors = STATUS_COLORS[c.status] || STATUS_COLORS.cold

  async function saveEdit() {
    setSaving(true)
    try {
      const r = await fetch('/api/contacts/update', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: c.name,
          status: editStatus,
          notes: editNotes,
          last_contacted: editLastContacted,
        }),
      })
      if (r.ok) {
        const res = await r.json()
        onUpdate(res.contact)
        setEditing(false)
      }
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="pp-sub-row" style={{ borderLeft: `3px solid ${colors.border}` }}>
      <div className="pp-sub-row-header">
        <span className="pp-sub-venue">{c.name}</span>
        <span className="pp-sub-outcome" style={{ background: colors.bg, color: colors.text, border: `1px solid ${colors.border}` }}>
          {tfb(t, 'pp.venuelog.status.' + c.status, c.status)}
        </span>
        {c.city && <span className="pp-sub-date">{c.city}</span>}
        {c.last_contacted && <span className="pp-sub-date">{t('pp.crm.contactedOn', { date: c.last_contacted })}</span>}
        {!editing && (
          <button className="pp-edit-btn" onClick={() => { setEditing(true); setEditStatus(c.status || 'cold'); setEditNotes(c.notes || ''); setEditLastContacted(c.last_contacted || '') }}>
            {t('pp.crm.edit')}
          </button>
        )}
      </div>
      {c.type && !editing && <div className="pp-sub-what">{tfb(t, 'pp.venueType.' + c.type, c.type)}</div>}
      {c.notes && !editing && <div className="pp-sub-notes">{loc(c, 'notes')}</div>}

      {editing && (
        <div className="pp-inline-edit">
          <div className="pp-sub-form-row">
            <div className="pp-sub-field">
              <label className="pp-sub-label">{t('pp.crm.status')}</label>
              <select className="pp-sub-select" value={editStatus} onChange={e => setEditStatus(e.target.value)}>
                {VENUE_STATUS_OPTIONS.map(o => (
                  <option key={o.value} value={o.value}>{tfb(t, 'pp.venuelog.status.' + o.value, o.value)}</option>
                ))}
              </select>
            </div>
            <div className="pp-sub-field">
              <label className="pp-sub-label">{t('pp.crm.lastContacted')}</label>
              <input type="date" className="pp-sub-input" value={editLastContacted} onChange={e => setEditLastContacted(e.target.value)} />
            </div>
          </div>
          <div className="pp-sub-field">
            <label className="pp-sub-label">{t('pp.crm.notes')}</label>
            <input type="text" className="pp-sub-input" value={editNotes} onChange={e => setEditNotes(e.target.value)} />
          </div>
          <div className="pp-q-actions">
            <button className="pp-save" onClick={saveEdit} disabled={saving}>{t('pp.crm.save')}</button>
            <button className="pp-skip" onClick={() => setEditing(false)}>{t('pp.crm.cancel')}</button>
          </div>
        </div>
      )}
    </div>
  )
}

function VenueLogSection({ isOpen, onToggle, sectionRef }) {
  const { t, lang } = useLanguage()
  const [contacts, setContacts] = useState([])
  const [filter, setFilter] = useState('all')
  const [form, setForm] = useState({ name: '', type: 'gallery', city: 'Tokyo', last_visited: '', last_contacted: '', status: 'cold', notes: '' })
  const [saving, setSaving] = useState(false)
  const [saved, flash] = useSaved()

  useEffect(() => {
    fetch('/api/contacts')
      .then(r => r.ok ? r.json() : [])
      .then(data => setContacts(Array.isArray(data) ? data : []))
      .catch(() => {})
  }, [])

  function setField(k, v) { setForm(f => ({ ...f, [k]: v })) }

  async function submitContact() {
    if (!form.name.trim()) return
    setSaving(true)
    try {
      const r = await fetch('/api/contacts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      if (r.ok) {
        const updated = await fetch('/api/contacts').then(r2 => r2.json())
        setContacts(Array.isArray(updated) ? updated : [])
        setForm({ name: '', type: 'gallery', city: 'Tokyo', last_visited: '', last_contacted: '', status: 'cold', notes: '' })
        flash()
      }
    } finally {
      setSaving(false)
    }
  }

  const sorted = [...contacts].sort((a, b) => (b.last_visited || b.logged_at || '').localeCompare(a.last_visited || a.logged_at || ''))
  const visible = filter === 'all' ? sorted : sorted.filter(c => c.status === filter)

  return (
    <SectionShell
      id="venue-log"
      sectionRef={sectionRef}
      title={t('pp.sec.venuelog')}
      synopsis={t('pp.syn.venuelog')}
      subtitle={contacts.length === 0 ? t('pp.sub.venuelog.empty') : t('pp.sub.venuelog.count', { n: contacts.length, s: contacts.length !== 1 ? 's' : '' })}
      isOpen={isOpen}
      onToggle={onToggle}
    >
      <p className="pp-section-note">{t('pp.venuelog.note')}</p>

      <div className="pp-sub-form">
        <div className="pp-sub-form-row">
          <div className="pp-sub-field pp-sub-field--wide">
            <label className="pp-sub-label">{t('pp.venuelog.name')}</label>
            <input
              type="text"
              className="pp-sub-input"
              value={form.name}
              onChange={e => setField('name', e.target.value)}
              placeholder={t('pp.venuelog.ph.name')}
            />
          </div>
          <div className="pp-sub-field">
            <label className="pp-sub-label">{t('pp.venuelog.type')}</label>
            <select className="pp-sub-select" value={form.type} onChange={e => setField('type', e.target.value)}>
              {VENUE_TYPE_OPTIONS.map(o => <option key={o.value} value={o.value}>{t('pp.venueType.' + o.value)}</option>)}
            </select>
          </div>
        </div>
        <div className="pp-sub-form-row">
          <div className="pp-sub-field">
            <label className="pp-sub-label">{t('pp.venuelog.city')}</label>
            <input
              type="text"
              className="pp-sub-input"
              value={form.city}
              onChange={e => setField('city', e.target.value)}
              placeholder="Tokyo"
            />
          </div>
          <div className="pp-sub-field">
            <label className="pp-sub-label">{t('pp.venuelog.lastVisited')}</label>
            <input
              type="date"
              className="pp-sub-input"
              value={form.last_visited}
              onChange={e => setField('last_visited', e.target.value)}
            />
          </div>
          <div className="pp-sub-field">
            <label className="pp-sub-label">{t('pp.venuelog.lastContacted')}</label>
            <input
              type="date"
              className="pp-sub-input"
              value={form.last_contacted}
              onChange={e => setField('last_contacted', e.target.value)}
            />
          </div>
          <div className="pp-sub-field">
            <label className="pp-sub-label">{t('pp.venuelog.status')}</label>
            <select className="pp-sub-select" value={form.status} onChange={e => setField('status', e.target.value)}>
              {VENUE_STATUS_OPTIONS.map(o => <option key={o.value} value={o.value}>{t('pp.venuelog.status.' + o.value)}</option>)}
            </select>
          </div>
        </div>
        <div className="pp-sub-field">
          <label className="pp-sub-label">{t('pp.venuelog.notes')}</label>
          <input
            type="text"
            className="pp-sub-input"
            value={form.notes}
            onChange={e => setField('notes', e.target.value)}
            placeholder={t('pp.venuelog.ph.notes')}
          />
        </div>
        <button
          className={`pp-save${saved ? ' pp-save--done' : ''}`}
          onClick={submitContact}
          disabled={saving || !form.name.trim()}
        >
          {saved ? t('pp.venuelog.btn.done') : t('pp.venuelog.btn')}
        </button>
      </div>

      <LogFilterTabs rows={sorted} field="status" labelFor={v => tfb(t, 'pp.venuelog.status.' + v, v)} active={filter} onChange={setFilter} lang={lang} />
      {visible.length > 0 && (
        <div className="pp-sub-list">
          {visible.map((c, i) => (
            <VenueContactCard
              key={c.logged_at || i}
              contact={c}
              onUpdate={updated => {
                setContacts(prev => prev.map(x => (x.name === updated.name ? updated : x)))
              }}
            />
          ))}
        </div>
      )}
    </SectionShell>
  )
}

// ── CRM Contacts section ──────────────────────────────────────────────────

const CRM_STATUS_META = {
  ready_to_review: { label: 'Ready to reach out', bg: '#fdf5e8', border: '#e8c878', text: '#7a5010' },
  contacted:       { label: 'Contacted',           bg: '#f0f6ff', border: '#90aee0', text: '#1a3a80' },
  responded:       { label: 'Responded',           bg: '#f0fbee', border: '#8fc98a', text: '#2e6626' },
  relationship:    { label: 'Relationship',        bg: '#fdfbe8', border: '#c8b040', text: '#5a4000' },
  not_a_fit:       { label: 'Not a fit',           bg: '#f5f5f5', border: '#ccc',    text: '#555'    },
  // existing statuses from pipeline data
  cold:            { label: 'Not yet approached',  bg: '#f5f5f5', border: '#ccc',    text: '#555'    },
  researching:     { label: 'Researching',         bg: '#fdf5e8', border: '#e8c878', text: '#7a5010' },
  in_contact:      { label: 'In contact',          bg: '#f0f6ff', border: '#90aee0', text: '#1a3a80' },
  submitted:       { label: 'Submitted',           bg: '#fff8ef', border: '#e8b870', text: '#804a10' },
  ongoing:         { label: 'Ongoing',             bg: '#f0fbee', border: '#8fc98a', text: '#2e6626' },
  rejected:        { label: 'Rejected',            bg: '#fef5f5', border: '#e8b0b0', text: '#8b2a2a' },
}

const CRM_FILTER_TAB_IDS = ['all', 'active', 'research', 'cold']

function crmStatusMeta(status) {
  return CRM_STATUS_META[status] || { label: status, bg: '#f5f5f5', border: '#ccc', text: '#555' }
}

const CRM_TYPE_LABELS = {
  gallery: 'Gallery', gallery_small: 'Gallery', artist_space: 'Artist Space',
  cafe_gallery: 'Café Gallery', cafe: 'Café',
  bookstore_gallery: 'Bookstore Gallery', bookshop: 'Bookshop', bookstore: 'Bookshop',
  zine_shop: 'Zine Shop', fair: 'Art Fair', zine_fair: 'Zine Fair',
  press_target: 'Press', magazine: 'Magazine', publication: 'Publication',
  book_publisher: 'Publisher', institutional: 'Institution', open_call: 'Open Call',
}

function CrmContactCard({ contact: c, onUpdate }) {
  const [expanded, setExpanded] = useState(false)
  const [loading, setLoading] = useState(false)
  const [noteDraft, setNoteDraft] = useState(c.personal_note || '')
  const { t, lang } = useLanguage()
  // Show the contact_translation_engine's _zh/_ja prose, not the English base.
  const loc = (obj, f) => (obj && ((lang === 'zh' && obj[f + '_zh']) || (lang === 'ja' && obj[f + '_ja']) || obj[f])) || ''
  const meta = crmStatusMeta(c.status)

  const today = new Date().toISOString().slice(0, 10)

  async function patchContact(fields) {
    setLoading(true)
    try {
      const r = await fetch(`/api/contacts/${encodeURIComponent(c.name)}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(fields),
      })
      if (r.ok) {
        const res = await r.json()
        onUpdate(res.contact)
      }
    } finally {
      setLoading(false)
    }
  }

  function markContacted(e) {
    e.stopPropagation()
    patchContact({ status: 'contacted', last_contacted: today })
  }

  function markReplied(e) {
    e.stopPropagation()
    patchContact({ response_received: true, status: 'responded' })
  }

  const lastContactedLabel = c.last_contacted
    ? c.last_contacted.slice(0, 10)
    : t('pp.crm.neverContacted')

  const showMarkContacted = !['contacted','responded','relationship'].includes(c.status)
  const showGotReply = ['contacted','in_contact'].includes(c.status) && !c.response_received

  return (
    <div className="crm-card" onClick={() => setExpanded(x => !x)}>
      <div className="crm-card-header">
        <div className="crm-card-left">
          <span className="crm-card-name">{c.name}</span>
          {c.type && (
            <span className="crm-type-badge">
              {t(`pp.venueType.${c.type}`) !== `pp.venueType.${c.type}`
                ? t(`pp.venueType.${c.type}`)
                : (CRM_TYPE_LABELS[c.type] || c.type)}
            </span>
          )}
        </div>
        <div className="crm-card-right">
          <span
            className="crm-status-pill"
            style={{ background: meta.bg, color: meta.text, border: `1px solid ${meta.border}` }}
          >
            {t(`pp.crm.statusLabel.${c.status}`) !== `pp.crm.statusLabel.${c.status}`
              ? t(`pp.crm.statusLabel.${c.status}`)
              : meta.label}
          </span>
          {c.city && <span className="crm-city">{c.city}</span>}
          <span className="crm-last-contacted">{lastContactedLabel}</span>
        </div>
      </div>

      <div className="crm-card-actions" onClick={e => e.stopPropagation()}>
        {c.contact_email && (
          <a
            className="crm-email-link"
            href={`mailto:${c.contact_email}`}
            onClick={e => e.stopPropagation()}
          >
            {c.contact_email}
          </a>
        )}
        <a
          className="crm-lookup-link"
          href={`https://www.google.com/search?q=${encodeURIComponent(`${c.name} ${c.city || ''}`)}`}
          target="_blank"
          rel="noreferrer"
          onClick={e => e.stopPropagation()}
        >
          {t('pp.crm.lookUp')} ↗
        </a>
        {showMarkContacted && (
          <button className="crm-action-btn" disabled={loading} onClick={markContacted}>
            {t('pp.crm.markContacted')}
          </button>
        )}
        {showGotReply && (
          <button className="crm-action-btn crm-action-btn--reply" disabled={loading} onClick={markReplied}>
            {t('pp.crm.gotReply')}
          </button>
        )}
      </div>

      {expanded && (
        <div className="crm-card-expanded">
          {c.crm_analysis?.next_action && (
            <div className="crm-expanded-row crm-expanded-row--action">
              <span className="crm-expanded-label crm-expanded-label--action">{t('pp.crm.nextAction')}</span>
              <p className="crm-expanded-text crm-expanded-text--action">{loc(c.crm_analysis, 'next_action')}</p>
            </div>
          )}
          {c.why_relevant && (
            <div className="crm-expanded-row">
              <span className="crm-expanded-label">{t('pp.crm.whyRelevant')}</span>
              <p className="crm-expanded-text">{loc(c, 'why_relevant')}</p>
            </div>
          )}
          {c.crm_analysis?.risk_notes && (
            <div className="crm-expanded-row">
              <span className="crm-expanded-label">{t('pp.crm.watchOut')}</span>
              <p className="crm-expanded-text crm-expanded-text--risk">{loc(c.crm_analysis, 'risk_notes')}</p>
            </div>
          )}
          {c.notes && (
            <div className="crm-expanded-row">
              <span className="crm-expanded-label">{t('pp.crm.notes')}</span>
              <p className="crm-expanded-text">{loc(c, 'notes')}</p>
            </div>
          )}
          {(c.contact_page || c.official_website) && (
            <div className="crm-expanded-row">
              <a
                className="crm-page-link"
                href={c.contact_page || c.official_website}
                target="_blank"
                rel="noopener noreferrer"
                onClick={e => e.stopPropagation()}
              >
                {c.contact_page ? t('pp.crm.contactPage') : t('pp.crm.website')} ↗
              </a>
            </div>
          )}
          <div className="crm-expanded-row" onClick={e => e.stopPropagation()}>
            <span className="crm-expanded-label">{t('pp.crm.yourNotes')}</span>
            <textarea
              className="crm-note-input"
              value={noteDraft}
              onChange={e => setNoteDraft(e.target.value)}
              placeholder={t('pp.crm.yourNotesPlaceholder')}
              rows={2}
            />
            {noteDraft.trim() !== (c.personal_note || '') && (
              <button
                className="crm-action-btn crm-note-save"
                disabled={loading}
                onClick={() => patchContact({ personal_note: noteDraft.trim() })}
              >
                {t('pp.crm.saveNote')}
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

function ContactsSection({ isOpen, onToggle, sectionRef }) {
  const [contacts, setContacts] = useState([])
  const [filter, setFilter] = useState('all')
  const [loading, setLoading] = useState(true)
  const [showAdd, setShowAdd] = useState(false)
  const [newName, setNewName] = useState('')
  const [newNote, setNewNote] = useState('')
  const { t } = useLanguage()

  function load() {
    fetch('/api/contacts')
      .then(r => r.ok ? r.json() : [])
      .then(data => { setContacts(Array.isArray(data) ? data : []); setLoading(false) })
      .catch(() => setLoading(false))
  }
  // eslint-disable-next-line react-hooks/exhaustive-deps -- run once on mount
  useEffect(() => { load() }, [])

  function handleUpdate(updated) {
    setContacts(prev => prev.map(c => c.name === updated.name ? updated : c))
  }

  async function addContact() {
    const name = newName.trim()
    if (!name) return
    try {
      await fetch('/api/contacts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, status: 'researching', notes: newNote.trim() }),
      })
    } catch { /* no-op on network failure */ }
    setNewName(''); setNewNote(''); setShowAdd(false)
    load()
  }

  // Summary counts
  const readyCount   = contacts.filter(c => c.status === 'ready_to_review').length
  const activeCount  = contacts.filter(c => ['in_contact', 'sent_inquiry', 'contacted', 'responded'].includes(c.status)).length
  const researchCount = contacts.filter(c => c.status === 'researching').length

  const summaryParts = []
  if (readyCount)    summaryParts.push(t('pp.contacts.ready', { n: readyCount }))
  if (activeCount)   summaryParts.push(t('pp.contacts.active', { n: activeCount }))
  if (researchCount) summaryParts.push(t('pp.contacts.researching', { n: researchCount }))
  const subtitle = contacts.length === 0
    ? t('pp.contacts.empty')
    : t('pp.contacts.summary', { n: contacts.length, parts: summaryParts.join(', ') || t('pp.contacts.allCold') })

  const FILTER_STATUS_MAP = {
    all:      null,
    active:   ['in_contact', 'sent_inquiry', 'contacted', 'responded', 'ready_to_review'],
    research: ['researching'],
    cold:     ['cold'],
  }

  const filtered = filter === 'all'
    ? contacts
    : contacts.filter(c => (FILTER_STATUS_MAP[filter] || []).includes(c.status))

  return (
    <SectionShell
      id="contacts"
      sectionRef={sectionRef}
      title={t('pp.sec.contacts')}
      synopsis={t('pp.syn.contacts')}
      subtitle={subtitle}
      isOpen={isOpen}
      onToggle={onToggle}
    >
      <p className="pp-section-note">{t('pp.contacts.note')}</p>

      {/* Add someone she's met */}
      {showAdd ? (
        <div className="crm-add-form" onClick={e => e.stopPropagation()}>
          <input
            className="crm-add-input"
            value={newName}
            onChange={e => setNewName(e.target.value)}
            placeholder={t('pp.crm.addNamePlaceholder')}
            autoFocus
          />
          <input
            className="crm-add-input"
            value={newNote}
            onChange={e => setNewNote(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && addContact()}
            placeholder={t('pp.crm.addNotePlaceholder')}
          />
          <button className="crm-action-btn" onClick={addContact} disabled={!newName.trim()}>{t('pp.crm.addSave')}</button>
          <button className="crm-add-cancel" onClick={() => { setShowAdd(false); setNewName(''); setNewNote('') }}>{t('pp.crm.addCancel')}</button>
        </div>
      ) : (
        <button className="crm-add-toggle" onClick={() => setShowAdd(true)}>{t('pp.crm.addSomeone')}</button>
      )}

      {/* Summary bar */}
      {contacts.length > 0 && (
        <div className="crm-summary-bar">
          <span className="crm-summary-text">{subtitle}</span>
        </div>
      )}

      {/* Filter tabs */}
      <div className="crm-filter-tabs">
        {CRM_FILTER_TAB_IDS.map(id => (
          <button
            key={id}
            className={`crm-filter-tab${filter === id ? ' crm-filter-tab--active' : ''}`}
            onClick={() => setFilter(id)}
          >
            {t('pp.contacts.filter.' + id)}
          </button>
        ))}
      </div>

      {loading && <p className="pp-section-note">{t('pp.contacts.loading')}</p>}

      {!loading && filtered.length === 0 && (
        <p className="pp-section-note">
          {filter === 'all'
            ? t('pp.contacts.emptyAll')
            : t('pp.contacts.emptyFilter')}
        </p>
      )}

      {!loading && filtered.length > 0 && (
        <div className="crm-list">
          {filtered.map((c, i) => (
            <CrmContactCard
              key={c.name || i}
              contact={c}
              onUpdate={handleUpdate}
            />
          ))}
        </div>
      )}
    </SectionShell>
  )
}

// ── Career event quick-log ────────────────────────────────────────────────

const EVENT_TYPES = [
  { type: 'accepted',     icon: '✓' },
  { type: 'rejected',     icon: '✗' },
  { type: 'conversation', icon: '💬' },
  { type: 'visited',      icon: '👁' },
  { type: 'sold',         icon: '¥' },
  { type: 'featured',     icon: '★' },
]

function CareerEventWidget() {
  const { t } = useLanguage()
  const [editType,  setEditType]  = useState(null)
  const [editId,    setEditId]    = useState(null)
  const [noteDraft, setNoteDraft] = useState('')
  const [flashType, setFlashType] = useState(null)

  // One tap logs straight into the knowledge base — nothing stays on screen.
  // An optional, transient detail field follows (which venue? how much?).
  async function logEvent(type) {
    setFlashType(type)
    setTimeout(() => setFlashType(f => (f === type ? null : f)), 1800)
    try {
      const r = await fetch('/api/career_events', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, note: '' }),
      })
      const d = await r.json().catch(() => null)
      if (d?.entry?.id) { setEditType(type); setEditId(d.entry.id); setNoteDraft('') }
    } catch { /* no-op on network failure */ }
  }

  async function saveNote() {
    const note = noteDraft.trim()
    const id = editId
    setEditType(null); setEditId(null); setNoteDraft('')
    if (!note || !id) return
    try {
      await fetch(`/api/career_events/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ note }),
      })
    } catch { /* no-op on network failure */ }
  }

  return (
    <div className="pp-event-widget">
      <div className="pp-event-prompt">{t('pp.event.prompt')}</div>
      <div className="pp-event-buttons">
        {EVENT_TYPES.map(({ type, icon }) => (
          <button
            key={type}
            className={`pp-event-btn${flashType === type ? ' pp-event-btn--logged' : ''}`}
            onClick={() => logEvent(type)}
            title={t(`pp.event.type.${type}`)}
          >
            <span className="pp-event-icon">{flashType === type ? '✓' : icon}</span>
            <span className="pp-event-label">{t(`pp.event.type.${type}`)}</span>
          </button>
        ))}
      </div>

      {flashType && (
        <div className="pp-event-confirm">✓ {t('pp.event.logged')}</div>
      )}

      {editType && (
        <div className="pp-event-detail">
          <input
            className="pp-event-detail-input"
            value={noteDraft}
            onChange={e => setNoteDraft(e.target.value)}
            onKeyDown={e => {
              if (e.key === 'Enter') saveNote()
              if (e.key === 'Escape') { setEditType(null); setEditId(null); setNoteDraft('') }
            }}
            onBlur={saveNote}
            placeholder={t(`pp.event.detail.${editType}`)}
            autoFocus
          />
          <button className="pp-event-detail-save" onClick={saveNote}>{t('pp.event.save')}</button>
        </div>
      )}
    </div>
  )
}

function AccomplishmentBand() {
  const { t } = useLanguage()
  const [text,  setText]  = useState('')
  const [saved, setSaved] = useState(false)

  async function log() {
    const note = text.trim()
    if (!note) return
    setText(''); setSaved(true)
    setTimeout(() => setSaved(false), 2600)
    try {
      await fetch('/api/career_events', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'accomplishment', note }),
      })
    } catch { /* no-op on network failure */ }
  }

  return (
    <div className="pp-accomplish-band">
      <p className="pp-accomplish-preamble">{t('pp.goals.preamble')}</p>
      <span className="pp-accomplish-label">{t('pp.goals.accomplishLabel')}</span>
      <div className="pp-goal-add">
        <input
          className="pp-goal-input"
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && log()}
          placeholder={t('pp.goals.accomplishPlaceholder')}
        />
        <button className="pp-add-btn" onClick={log}>{t('pp.add')}</button>
      </div>
      {saved && <p className="pp-first-goal-note">{t('pp.goals.accomplishSaved')}</p>}
    </div>
  )
}

// ── Carousel data builders ────────────────────────────────────────────────

function buildCarouselCards(profile, t) {
  const answers      = profile.saffron_answers || {}
  const answeredCount= QUESTION_KEYS.filter(k => isAnswered(answers[k])).length
  const goalsCount   = (profile.goals || []).filter(g => !g.done).length
  const hasText      = (profile.artist_statement || '').length > 30

  const qsDesc = answeredCount === 0 ? t('pp.carousel.qs.desc.0')
    : answeredCount < 4  ? t('pp.carousel.qs.desc.building', { n: answeredCount })
    : answeredCount < 8  ? t('pp.carousel.qs.desc.partial')
    :                      t('pp.carousel.qs.desc.done')

  const cards = [
    {
      id: 'stmt',
      sectionId: 'artist-statement',
      name: t('pp.carousel.stmt.name'),
      current: hasText ? t('pp.carousel.stmt.current.draft') : t('pp.carousel.stmt.current.none'),
      next: t('pp.carousel.stmt.next'),
      ratio: hasText ? 0.5 : 0,
      desc: t('pp.carousel.stmt.desc'),
    },
    {
      id: 'qs',
      sectionId: 'saffron-questions',
      name: t('pp.carousel.qs.name'),
      // No goalpost: a gentle count, never "x/8" (a quota she could feel behind on).
      current: answeredCount > 0 ? String(answeredCount) : null,
      cta: answeredCount > 0 ? null : t('pp.carousel.qs.cta'),
      desc: qsDesc,
    },
    {
      id: 'goals',
      sectionId: 'career-goals',
      name: t('pp.carousel.goals.name'),
      // No goalpost: a gentle count, never "x/3".
      current: goalsCount > 0 ? String(goalsCount) : null,
      cta: goalsCount > 0 ? null : t('pp.carousel.goals.cta'),
      desc: goalsCount === 0 ? t('pp.carousel.goals.desc.empty') : t('pp.carousel.goals.desc.has'),
    },
    {
      id: 'acc',
      sectionId: 'career-goals',
      name: t('pp.carousel.acc.name'),
      cta:  t('pp.carousel.acc.cta'),
      desc: t('pp.carousel.acc.desc'),
    },
    {
      id: 'prefs',
      sectionId: 'preferences',
      name: t('pp.carousel.prefs.name'),
      cta:  t('pp.carousel.prefs.cta'),
      desc: t('pp.carousel.prefs.desc'),
    },
  ]

  // Fixed order — a short to-do list of things she can give Peppercorn.
  const order = ['qs', 'stmt', 'goals', 'acc', 'prefs']
  return order.map(id => cards.find(c => c.id === id)).filter(Boolean)
}

// Section order (Scott, 2026-06-26): the artist statement first, then the
// profile-building INPUTS she actually shapes her profile with — preferences,
// goals, and the questions/notes — kept right under the statement so they're
// never buried. Only THEN the long record/log forms (exhibitions, submissions,
// venues, contacts), which are reference lists she dips into, not the wall she
// has to wade through first. (The old score-sort dropped preferences below all
// four long logs, so she'd never scroll to it.)
function computeSectionOrder() {
  return [
    'artist-statement',
    'preferences',
    'career-goals',
    'saffron-questions',
    'exhibition-log',
    'submission-log',
    'venue-log',
    'contacts',
  ]
}

// ── Dismissal insight banner ──────────────────────────────────────────────

function DismissalInsightBanner() {
  const { t } = useLanguage()
  const [insights, setInsights] = useState(null)
  const [dismissed, setDismissed] = useState(false)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    fetch('/api/feedback/insights')
      .then(r => r.ok ? r.json() : null)
      .then(d => setInsights(d))
      .catch(() => {})
  }, [])

  if (!insights || dismissed || saved) return null
  const entries = Object.entries(insights.dismissals || {})
  if (entries.length === 0) return null

  // Pick the category with most dismissals
  const [topCategory, topCount] = entries.sort((a, b) => b[1] - a[1])[0]

  // Human-readable category name — use translation key, fall back to slug
  const categoryLabel = t(`cat.${topCategory}`) !== `cat.${topCategory}`
    ? t(`cat.${topCategory}`)
    : topCategory.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())

  async function suppress() {
    await fetch('/api/feedback/suppress-category', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category: topCategory }),
    })
    setSaved(true)
  }

  return (
    <div className="pp-dismissal-insight">
      <span className="pp-dismissal-icon">🐭</span>
      <div className="pp-dismissal-body">
        <span className="pp-dismissal-text">
          {t('pp.dismissal.text', { n: topCount, cat: categoryLabel })}
        </span>
        <div className="pp-dismissal-actions">
          <button className="pp-dismissal-confirm" onClick={suppress}>
            {t('pp.dismissal.confirm')}
          </button>
          <button className="pp-dismissal-skip" onClick={() => setDismissed(true)}>
            {t('pp.dismissal.skip')}
          </button>
        </div>
      </div>
    </div>
  )
}

function PeppercornIntro() {
  const { t } = useLanguage()
  const [dismissed, setDismissed] = useState(() => {
    try { return localStorage.getItem('pp_intro_dismissed') === '1' } catch { return false }
  })
  if (dismissed) return null
  function close() {
    setDismissed(true)
    try { localStorage.setItem('pp_intro_dismissed', '1') } catch { /* localStorage unavailable */ }
  }
  return (
    <div className="pp-intro">
      <button className="pp-intro-close" onClick={close} title={t('pp.intro.dismiss')}>×</button>
      <p className="pp-intro-text">{t('pp.intro.body')}</p>
    </div>
  )
}

// ── Page root ──────────────────────────────────────────────────────────────

export default function PeppercornPage({ nav }) {
  const [profile,     setProfile]     = useState(() => getCache('/api/peppercorn') ?? null)
  const [statusMsg,   setStatusMsg]   = useState('')
  const [isSaved,     setIsSaved]     = useState(false)
  const [fetchError,  setFetchError]  = useState(null)
  const [openSections,setOpenSections]= useState(new Set(['artist-statement']))
  const [activeCard,  setActiveCard]  = useState(null)
  const { t, lang } = useLanguage()

  const sectionRefs   = useRef({})
  const carouselCards = profile ? buildCarouselCards(profile, t) : []
  const sectionOrder  = profile ? computeSectionOrder(profile) : []
  // Localized seed statement (English base + _zh/_ja siblings) so it never shows
  // English in 中文/日本語 mode. Edits overwrite all three (see onSave below).
  const localizedStatement = profile
    ? ((lang === 'zh' && profile.artist_statement_zh) ||
       (lang === 'ja' && profile.artist_statement_ja) ||
       profile.artist_statement)
    : undefined

  useEffect(() => {
    fetch('/api/peppercorn')
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json() })
      .then(p => { setCache('/api/peppercorn', p); setProfile(p); setOpenSections(new Set(['artist-statement'])) })
      .catch(e => setFetchError(e.message))
  }, [])

  // Track active card via IntersectionObserver
  const sectionOrderKey = sectionOrder.join(',')
  useEffect(() => {
    if (!profile) return
    const obs = new IntersectionObserver(
      entries => {
        entries.forEach(e => { if (e.isIntersecting) setActiveCard(e.target.id) })
      },
      { rootMargin: '-15% 0px -65% 0px' }
    )
    Object.values(sectionRefs.current).forEach(el => { if (el) obs.observe(el) })
    return () => obs.disconnect()
  }, [profile, sectionOrderKey])

  async function saveSection(updates) {
    const next = { ...profile, ...updates }
    setProfile(next)
    setStatusMsg(t('pp.saving'))
    setIsSaved(false)
    try {
      // Strip server-derived fields (e.g. live_counts, injected by GET) so they
      // are never persisted back into peppercorn_profile.json (T4.2). The server
      // strips them too, but not sending them keeps the payload honest.
      const { live_counts: _drop, ...toSave } = next
      void _drop
      const r = await fetch('/api/peppercorn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(toSave),
      })
      if (!r.ok) throw new Error(r.status)
      // The backend reports regen_started when a statement edit kicked off a
      // background draft refresh — tell her it's updating so the wait reads as
      // progress, not a no-op.
      let updating = false
      try { updating = !!(await r.json())?.regen_started } catch { /* ignore */ }
      setStatusMsg(updating ? t('pp.draftsUpdating') : t('pp.saved'))
      setIsSaved(true)
      const _keys = Object.keys(updates || {})
      track({
        type: 'action',
        action: (_keys.length === 1 && _keys[0] === 'saffron_answers') ? 'saffron_answer' : 'profile_save',
      })
      setTimeout(() => { setStatusMsg(''); setIsSaved(false) }, updating ? 5000 : 2000)
    } catch {
      setStatusMsg(t('pp.saveError'))
      setTimeout(() => setStatusMsg(''), 3000)
    }
  }

  // T0.6 — after she logs/deletes a show, pull the fresh canonical group-show
  // count (the same number Saffron shows) without disturbing her editable fields.
  async function refreshLiveCounts() {
    try {
      const r = await fetch('/api/peppercorn')
      if (!r.ok) return
      const p = await r.json()
      if (p?.live_counts) setProfile(prev => (prev ? { ...prev, live_counts: p.live_counts } : prev))
    } catch { /* leave the count as-is on network failure */ }
  }

  function handleCardClick(card) {
    if (!card.sectionId) return
    setActiveCard(card.id)
    setOpenSections(prev => new Set([...prev, card.sectionId]))
    setTimeout(() => {
      const el = sectionRefs.current[card.sectionId]
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }, 40)
  }

  function toggleSection(id) {
    setOpenSections(prev => {
      const next = new Set(prev)
      const opening = !next.has(id)
      opening ? next.add(id) : next.delete(id)
      if (opening) track({ type: 'nav', page: 'refine', section: id })
      return next
    })
  }

  function setSectionRef(id) {
    // eslint-disable-next-line react-hooks/refs -- callback ref: assignment runs on attach, not during render
    return el => { sectionRefs.current[id] = el }
  }

  const SECTION_COMPONENTS = {
    'artist-statement': (
      <ArtistStatementSection
        key="artist-statement"
        data={localizedStatement}
        // Her statement is ONE canonical field (T4.2). Save it once; the server
        // drops any stale localized siblings so the next render falls back to the
        // canonical text until a real translation is produced — it never shows an
        // out-of-date zh/ja copy that silently drifted from her edit.
        onSave={v => saveSection({ artist_statement: v, artist_statement_zh: null, artist_statement_ja: null })}
        isOpen={openSections.has('artist-statement')}
        onToggle={() => toggleSection('artist-statement')}
        sectionRef={setSectionRef('artist-statement')}
      />
    ),
    'saffron-questions': (
      <SectionErrorBoundary key="saffron-questions" fallback={tfb(t, 'pp.sectionError', 'This section hit a snag and was hidden so the rest of the page keeps working.')}>
        <SaffronQuestionsSection
          data={profile?.saffron_answers}
          onSave={v => saveSection({ saffron_answers: v })}
          isOpen={openSections.has('saffron-questions')}
          onToggle={() => toggleSection('saffron-questions')}
          sectionRef={setSectionRef('saffron-questions')}
        />
      </SectionErrorBoundary>
    ),
    'career-goals': (
      <CareerGoalsSection
        key="career-goals"
        data={profile?.goals}
        onSave={v => saveSection({ goals: v })}
        isOpen={openSections.has('career-goals')}
        onToggle={() => toggleSection('career-goals')}
        sectionRef={setSectionRef('career-goals')}
      />
    ),
    'preferences': (
      <PreferencesSection
        key="preferences"
        data={{ priorities: profile?.priorities, preferences: profile?.preferences }}
        onSave={v => saveSection(v)}
        isOpen={openSections.has('preferences')}
        onToggle={() => toggleSection('preferences')}
        sectionRef={setSectionRef('preferences')}
      />
    ),
    'exhibition-log': (
      <ExhibitionLogSection
        key="exhibition-log"
        liveGroupShows={profile?.live_counts?.group_shows}
        onCountsChanged={refreshLiveCounts}
        isOpen={openSections.has('exhibition-log')}
        onToggle={() => toggleSection('exhibition-log')}
        sectionRef={setSectionRef('exhibition-log')}
      />
    ),
    'submission-log': (
      <SubmissionLogSection
        key="submission-log"
        isOpen={openSections.has('submission-log')}
        onToggle={() => toggleSection('submission-log')}
        sectionRef={setSectionRef('submission-log')}
      />
    ),
    'venue-log': (
      <VenueLogSection
        key="venue-log"
        isOpen={openSections.has('venue-log')}
        onToggle={() => toggleSection('venue-log')}
        sectionRef={setSectionRef('venue-log')}
      />
    ),
    'contacts': (
      <ContactsSection
        key="contacts"
        isOpen={openSections.has('contacts')}
        onToggle={() => toggleSection('contacts')}
        sectionRef={setSectionRef('contacts')}
      />
    ),
  }

  return (
    <div className="peppercorn-page">

      {/* Ambient mouse illustration */}
      <div className="pp-mouse-ambient">
        <img src={peppercornHero} alt="Peppercorn" className="pp-mouse-img" />
      </div>

      {nav}

      {/* Status bar */}
      {statusMsg && (
        <div className={`pp-status-bar${isSaved ? ' pp-status-bar--saved' : ''}`}>
          {statusMsg}
        </div>
      )}

      {!profile && !fetchError && <div className="pp-loading">{t('pp.loading')}</div>}
      {fetchError && <div className="pp-loading">{t('pp.loadError')}</div>}

      {profile && (
        <>
          <PeppercornIntro />

          <div className="pp-content">
            <DismissalInsightBanner />
          </div>

          {/* Carousel — a short to-do list of things Peppercorn could use */}
          <div className="pp-carousel-wrap">
            <div className="pp-carousel">
              {carouselCards.map(card => {
                const isActive = activeCard === card.id ||
                  (card.sectionId && activeCard === card.sectionId)
                return (
                  <CarouselCard
                    key={card.id}
                    card={card}
                    isActive={isActive}
                    onClick={handleCardClick}
                  />
                )
              })}
            </div>
          </div>

          {/* Accomplishment band — between the to-do notes and the sections */}
          <div className="pp-content">
            <AccomplishmentBand />
          </div>

          {/* Sections in dynamic order */}
          <div className="pp-content">
            {sectionOrder.map(id => SECTION_COMPONENTS[id])}
          </div>
        </>
      )}
    </div>
  )
}
