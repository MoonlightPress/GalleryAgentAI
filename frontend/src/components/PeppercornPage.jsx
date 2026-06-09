import { useState, useEffect, useRef } from 'react'
import './PeppercornPage.css'
import { peppercornHero } from '../utils/heroImages'
import { useLanguage } from '../i18n/LanguageContext'

// ── SVG progress arc ──────────────────────────────────────────────────────

function ArcProgress({ ratio, size = 52 }) {
  const r = size * 0.38
  const cx = size / 2
  const cy = size / 2
  const circ = 2 * Math.PI * r
  const pct = Math.min(1, Math.max(0, isNaN(ratio) ? 0 : ratio))
  const offset = circ * (1 - pct)
  return (
    <svg width={size} height={size}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#dce8cc" strokeWidth="3.5" />
      <circle
        cx={cx} cy={cy} r={r}
        fill="none"
        stroke="#6a8a5a"
        strokeWidth="3.5"
        strokeDasharray={`${circ}`}
        strokeDashoffset={`${offset}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
    </svg>
  )
}

// ── Carousel card ─────────────────────────────────────────────────────────

function CarouselCard({ card, isActive, onClick }) {
  return (
    <div
      className={`pp-card${isActive ? ' pp-card--active' : ''}${!card.sectionId ? ' pp-card--passive' : ''}`}
      onClick={() => onClick(card)}
    >
      <div className="pp-card-arc">
        <ArcProgress ratio={card.ratio} />
      </div>
      <div className="pp-card-name">{card.name}</div>
      <div className="pp-card-values">
        <span className="pp-card-current">{card.current}</span>
        <span className="pp-card-sep"> / </span>
        <span className="pp-card-next">{card.next}</span>
      </div>
      <div className="pp-card-desc">{card.desc}</div>
    </div>
  )
}

// ── Section shell (open/close controlled by parent) ───────────────────────

function SectionShell({ id, title, subtitle, isOpen, onToggle, sectionRef, children }) {
  return (
    <section
      id={id}
      ref={sectionRef}
      className={`pp-section${isOpen ? '' : ' pp-section--closed'}`}
    >
      <button className="pp-toggle" onClick={onToggle}>
        <div className="pp-toggle-text">
          <h2 className="pp-title">{title}</h2>
          {isOpen && subtitle && <p className="pp-subtitle">{subtitle}</p>}
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

function InstagramStrategySection({ isOpen, onToggle, sectionRef }) {
  const { t } = useLanguage()
  return (
    <SectionShell
      id="instagram-strategy"
      sectionRef={sectionRef}
      title={t('pp.sec.instagram')}
      subtitle={t('pp.sub.instagram')}
      isOpen={isOpen}
      onToggle={onToggle}
    >
      <div className="pp-analysis-grid">

        <div className="pp-platform-block">
          <div className="pp-platform-header">
            <span className="pp-platform-name">Instagram</span>
            <span className="pp-platform-handle">@gegyjiji</span>
            <span className="pp-platform-count">{t('pp.ig.count')}</span>
          </div>
          <p className="pp-analysis-note">{t('pp.ig.analysis.21k')}</p>
          <div className="pp-threshold-list">
            <div className="pp-threshold-row">
              <div className="pp-threshold-marker pp-threshold-marker--next">25k</div>
              <p className="pp-threshold-desc">{t('pp.ig.thresh.25k')}</p>
            </div>
            <div className="pp-threshold-row">
              <div className="pp-threshold-marker">50k</div>
              <p className="pp-threshold-desc">{t('pp.ig.thresh.50k')}</p>
            </div>
            <div className="pp-threshold-row">
              <div className="pp-threshold-marker">100k</div>
              <p className="pp-threshold-desc">{t('pp.ig.thresh.100k')}</p>
            </div>
          </div>
          <div className="pp-tactics-block">
            <div className="pp-block-label">{t('pp.ig.tactics.label')}</div>
            <ul className="pp-tactics-list">
              <li>{t('pp.ig.tactics.0')}</li>
              <li>{t('pp.ig.tactics.1')}</li>
              <li>{t('pp.ig.tactics.2')}</li>
              <li>{t('pp.ig.tactics.3')}</li>
            </ul>
          </div>
        </div>

        <div className="pp-platform-block">
          <div className="pp-platform-header">
            <span className="pp-platform-name">Twitter / X</span>
            <span className="pp-platform-handle">@GegYjiji</span>
            <span className="pp-platform-count">{t('pp.tw.count')}</span>
          </div>
          <p className="pp-analysis-note">{t('pp.tw.analysis')}</p>
          <div className="pp-threshold-list">
            <div className="pp-threshold-row">
              <div className="pp-threshold-marker pp-threshold-marker--next">100k</div>
              <p className="pp-threshold-desc">{t('pp.tw.thresh.100k')}</p>
            </div>
          </div>
          <div className="pp-insight-box">{t('pp.tw.insight')}</div>
          <div className="pp-gentle-questions">
            <div className="pp-block-label">{t('pp.tw.wondering.label')}</div>
            <ul className="pp-wondering-list">
              <li>{t('pp.tw.wondering.0')}</li>
              <li>{t('pp.tw.wondering.1')}</li>
              <li>{t('pp.tw.wondering.2')}</li>
            </ul>
          </div>
        </div>

      </div>
    </SectionShell>
  )
}

// ── Exhibition pathway section ────────────────────────────────────────────

function ExhibitionPathwaySection({ isOpen, onToggle, sectionRef }) {
  const { t } = useLanguage()
  return (
    <SectionShell
      id="exhibition-pathway"
      sectionRef={sectionRef}
      title={t('pp.sec.exhibition')}
      subtitle={t('pp.sub.exhibition')}
      isOpen={isOpen}
      onToggle={onToggle}
    >
      <div className="pp-pathway-grid">
        <div>
          <div className="pp-pathway-record">
            <div className="pp-pathway-show-title">Tide from China Part 1</div>
            <div className="pp-pathway-show-meta">{t('pp.shows.meta')}</div>
            <div className="pp-pathway-show-note">{t('pp.shows.record.label')}</div>
          </div>

          <div className="pp-threshold-list pp-threshold-list--shows">
            <div className="pp-threshold-row pp-threshold-row--done">
              <div className="pp-threshold-marker pp-threshold-marker--done">1 ✓</div>
              <p className="pp-threshold-desc">{t('pp.shows.thresh.1')}</p>
            </div>
            <div className="pp-threshold-row">
              <div className="pp-threshold-marker pp-threshold-marker--next">2</div>
              <p className="pp-threshold-desc">{t('pp.shows.thresh.2')}</p>
            </div>
            <div className="pp-threshold-row">
              <div className="pp-threshold-marker pp-threshold-marker--key">3</div>
              <p className="pp-threshold-desc">{t('pp.shows.thresh.3')}</p>
            </div>
            <div className="pp-threshold-row">
              <div className="pp-threshold-marker">5</div>
              <p className="pp-threshold-desc">{t('pp.shows.thresh.5')}</p>
            </div>
          </div>
        </div>

        <div>
          <div className="pp-next-targets">
            <div className="pp-block-label">{t('pp.shows.nextTargets')}</div>
            <div className="pp-target-row">
              <div className="pp-target-name">3331 Arts Chiyoda</div>
              <p className="pp-target-desc">{t('pp.shows.3331.desc')}</p>
            </div>
            <div className="pp-target-row">
              <div className="pp-target-name">Design Festa Gallery</div>
              <p className="pp-target-desc">{t('pp.shows.dfg.desc')}</p>
            </div>
            <div className="pp-target-row">
              <div className="pp-target-name">Gallery IYN</div>
              <p className="pp-target-desc">{t('pp.shows.iyn.desc')}</p>
            </div>
          </div>

          <p className="pp-timeline-note">{t('pp.shows.timeline')}</p>
        </div>
      </div>
    </SectionShell>
  )
}

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

function SaffronQuestionsSection({ data, onSave, isOpen, onToggle, sectionRef }) {
  const [answers, setAnswers] = useState(data || {})
  const { t } = useLanguage()
  useEffect(() => { setAnswers(data || {}) }, [data])

  const QUESTIONS = buildQuestions(t)

  const answeredCount    = QUESTION_KEYS.filter(k => answers[k]).length
  const allAnswered      = answeredCount === QUESTION_KEYS.length
  const firstUnanswered  = QUESTIONS.findIndex(q => !answers[q.key])
  const startIdx         = firstUnanswered === -1 ? 0 : firstUnanswered
  const [activeIdx, setActiveIdx] = useState(startIdx)
  const [draft,     setDraft]     = useState(answers[QUESTIONS[startIdx]?.key] || '')

  const currentQ = QUESTIONS[activeIdx]

  function selectQ(idx) { setActiveIdx(idx); setDraft(answers[QUESTIONS[idx].key] || '') }

  function saveAnswer() {
    if (!draft.trim()) return
    const next = { ...answers, [currentQ.key]: draft.trim() }
    setAnswers(next)
    onSave(next)
    const nextUnanswered = QUESTIONS.findIndex((q, i) => i > activeIdx && !next[q.key])
    if (nextUnanswered !== -1) { setActiveIdx(nextUnanswered); setDraft('') }
  }

  function clearAnswer(key) { const next = { ...answers, [key]: null }; setAnswers(next); onSave(next) }
  function skipQ() {
    const next = QUESTIONS.findIndex((q, i) => i > activeIdx && !answers[q.key])
    if (next !== -1) { setActiveIdx(next); setDraft(answers[QUESTIONS[next].key] || '') }
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
                className={['pp-q-dot', answers[q.key] ? 'pp-q-dot--done' : '', i === activeIdx ? 'pp-q-dot--active' : ''].join(' ').trim()}
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
              {!answers[currentQ.key] && (
                <button className="pp-skip" onClick={skipQ}>{t('pp.comeBack')}</button>
              )}
              {answers[currentQ.key] && (
                <button className="pp-skip" onClick={() => clearAnswer(currentQ.key)}>{t('pp.clearAnswer')}</button>
              )}
            </div>
          </div>
        </>
      )}

      {answeredCount > 0 && (
        <div className="pp-q-done-list">
          <div className="pp-block-label">{t('pp.answered', { n: answeredCount })}</div>
          {QUESTIONS.filter(q => answers[q.key]).map(q => (
            <div key={q.key} className="pp-q-done-row" onClick={() => selectQ(QUESTIONS.indexOf(q))}>
              <span className="pp-q-done-check">✓</span>
              <div className="pp-q-done-body">
                <div className="pp-q-done-q">{q.text}</div>
                <div className="pp-q-done-a">{answers[q.key]}</div>
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
  const [saved,  flash]     = useSaved()
  const [phIdx]             = useState(() => Math.floor(Math.random() * GOAL_PLACEHOLDER_KEYS.length))
  const [shownFirstNote, setShownFirstNote] = useState((data || []).length > 0)
  const { t } = useLanguage()
  useEffect(() => { setGoals(data || []) }, [data])

  function addGoal() {
    const t = input.trim()
    if (!t) return
    const isFirst = goals.length === 0
    const next = [...goals, { id: Date.now(), text: t, done: false }]
    setGoals(next); setInput('')
    if (isFirst) setShownFirstNote(true)
    onSave(next); flash()
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
              <button className="pp-goal-toggle" onClick={() => toggleDone(g.id)} title={t('pp.goal.markDone')}>○</button>
              <span className="pp-goal-text">{g.text}</span>
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
              <span className="pp-goal-text">{g.text}</span>
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

  const toggleTier = n   => setTiers(ts => ts.includes(n) ? ts.filter(t => t !== n) : [...ts, n].sort())
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
        {TIERS.map(t => (
          <label key={t.n} className="pp-check-row">
            <input type="checkbox" className="pp-check" checked={tiers.includes(t.n)} onChange={() => toggleTier(t.n)} />
            <span className="pp-check-label"><strong>{t.label}</strong><span className="pp-check-desc">{t.desc}</span></span>
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

function SubmissionLogSection({ isOpen, onToggle, sectionRef }) {
  const { t } = useLanguage()
  const [submissions, setSubmissions] = useState([])
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

  return (
    <SectionShell
      id="submission-log"
      sectionRef={sectionRef}
      title={t('pp.sec.sublog')}
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

      {sorted.length > 0 && (
        <div className="pp-sub-list">
          {sorted.map(s => {
            const colors = OUTCOME_COLORS[s.outcome] || OUTCOME_COLORS.pending
            return (
              <div key={s.id || s.date + s.venue} className="pp-sub-row" style={{ borderLeft: `3px solid ${colors.border}` }}>
                <div className="pp-sub-row-header">
                  <span className="pp-sub-venue">{s.venue}</span>
                  <span className="pp-sub-outcome" style={{ background: colors.bg, color: colors.text, border: `1px solid ${colors.border}` }}>
                    {t('pp.outcome.' + s.outcome) || s.outcome}
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

function ExhibitionLogSection({ isOpen, onToggle, sectionRef }) {
  const { t } = useLanguage()
  const [shows, setShows] = useState([])
  const [form, setForm] = useState({ date: '', name: '', venue: '', type: 'group', outcome: 'shown', notes: '' })
  const [saving, setSaving] = useState(false)
  const [saved, flash] = useSaved()

  useEffect(() => {
    fetch('/api/exhibition_log')
      .then(r => r.ok ? r.json() : [])
      .then(d => setShows(Array.isArray(d) ? d : []))
      .catch(() => {})
  }, [])

  function setField(k, v) { setForm(f => ({ ...f, [k]: v })) }

  async function submitShow() {
    if (!form.name.trim() && !form.venue.trim()) return
    setSaving(true)
    try {
      const r = await fetch('/api/exhibition_log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form }),
      })
      if (r.ok) {
        const updated = await fetch('/api/exhibition_log').then(r2 => r2.json())
        setShows(Array.isArray(updated) ? updated : [])
        setForm({ date: '', name: '', venue: '', type: 'group', outcome: 'shown', notes: '' })
        flash()
      }
    } finally {
      setSaving(false)
    }
  }

  async function deleteShow(id) {
    await fetch(`/api/exhibition_log/${id}`, { method: 'DELETE' })
    setShows(prev => prev.filter(s => s.id !== id))
  }

  const sorted = [...shows].sort((a, b) => (b.date || '').localeCompare(a.date || ''))
  const groupCount = shows.filter(s => s.type === 'group').length
  const total = 1 + groupCount  // 1 hardcoded + logged

  return (
    <SectionShell
      id="exhibition-log"
      sectionRef={sectionRef}
      title={t('pp.sec.exlog')}
      subtitle={shows.length === 0 ? t('pp.sub.exlog.empty') : t('pp.sub.exlog.count', { n: total })}
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
        <button
          className={`pp-save${saved ? ' pp-save--done' : ''}`}
          onClick={submitShow}
          disabled={saving || (!form.name.trim() && !form.venue.trim())}
        >
          {saved ? t('pp.exlog.btn.done') : t('pp.exlog.btn')}
        </button>
      </div>

      {/* Hardcoded confirmed show */}
      <div className="pp-sub-list">
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

        {sorted.map(s => {
          const colors = SHOW_OUTCOME_COLORS[s.outcome] || SHOW_OUTCOME_COLORS.shown
          return (
            <div key={s.id} className="pp-sub-row" style={{ borderLeft: `3px solid ${colors.border}` }}>
              <div className="pp-sub-row-header">
                <span className="pp-sub-venue">{s.name || s.venue}</span>
                <span className="pp-sub-outcome" style={{ background: colors.bg, color: colors.text, border: `1px solid ${colors.border}` }}>
                  {t('pp.showOutcome.' + s.outcome) || s.outcome}
                </span>
                {s.date && <span className="pp-sub-date">{s.date}</span>}
                <button className="pp-edit-btn" onClick={() => deleteShow(s.id)} title={t('pp.exlog.delete')}>×</button>
              </div>
              {s.venue && s.name && <div className="pp-sub-what">{s.venue} · {t('pp.showType.' + s.type) || s.type}</div>}
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
  const { t } = useLanguage()
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
          {t('pp.venuelog.status.' + c.status) || c.status}
        </span>
        {c.city && <span className="pp-sub-date">{c.city}</span>}
        {c.last_contacted && <span className="pp-sub-date">{t('pp.crm.contactedOn', { date: c.last_contacted })}</span>}
        {!editing && (
          <button className="pp-edit-btn" onClick={() => { setEditing(true); setEditStatus(c.status || 'cold'); setEditNotes(c.notes || ''); setEditLastContacted(c.last_contacted || '') }}>
            {t('pp.crm.edit')}
          </button>
        )}
      </div>
      {c.type && !editing && <div className="pp-sub-what">{t('pp.venueType.' + c.type) || c.type}</div>}
      {c.notes && !editing && <div className="pp-sub-notes">{c.notes}</div>}

      {editing && (
        <div className="pp-inline-edit">
          <div className="pp-sub-form-row">
            <div className="pp-sub-field">
              <label className="pp-sub-label">{t('pp.crm.status')}</label>
              <select className="pp-sub-select" value={editStatus} onChange={e => setEditStatus(e.target.value)}>
                {VENUE_STATUS_OPTIONS.map(o => (
                  <option key={o.value} value={o.value}>{t('pp.venuelog.status.' + o.value) || o.value}</option>
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
  const { t } = useLanguage()
  const [contacts, setContacts] = useState([])
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

  return (
    <SectionShell
      id="venue-log"
      sectionRef={sectionRef}
      title={t('pp.sec.venuelog')}
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

      {sorted.length > 0 && (
        <div className="pp-sub-list">
          {sorted.map((c, i) => (
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

const CRM_FILTER_TABS = [
  { id: 'all',           label: 'All' },
  { id: 'ready',         label: 'Ready' },
  { id: 'active',        label: 'Active' },
  { id: 'relationship',  label: 'Relationships' },
]

function crmStatusMeta(status) {
  return CRM_STATUS_META[status] || { label: status, bg: '#f5f5f5', border: '#ccc', text: '#555' }
}

function CrmContactCard({ contact: c, onUpdate }) {
  const [expanded, setExpanded] = useState(false)
  const [loading, setLoading] = useState(false)
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
    : 'Never contacted'

  const showMarkContacted = !['contacted','responded','relationship'].includes(c.status)
  const showGotReply = ['contacted','in_contact'].includes(c.status) && !c.response_received

  return (
    <div className="crm-card" onClick={() => setExpanded(x => !x)}>
      <div className="crm-card-header">
        <div className="crm-card-left">
          <span className="crm-card-name">{c.name}</span>
          {c.type && (
            <span className="crm-type-badge">{c.type}</span>
          )}
        </div>
        <div className="crm-card-right">
          <span
            className="crm-status-pill"
            style={{ background: meta.bg, color: meta.text, border: `1px solid ${meta.border}` }}
          >
            {meta.label}
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
        {showMarkContacted && (
          <button className="crm-action-btn" disabled={loading} onClick={markContacted}>
            Mark contacted
          </button>
        )}
        {showGotReply && (
          <button className="crm-action-btn crm-action-btn--reply" disabled={loading} onClick={markReplied}>
            Got reply
          </button>
        )}
      </div>

      {expanded && (
        <div className="crm-card-expanded">
          {c.crm_analysis?.next_action && (
            <div className="crm-expanded-row crm-expanded-row--action">
              <span className="crm-expanded-label crm-expanded-label--action">Next action</span>
              <p className="crm-expanded-text crm-expanded-text--action">{c.crm_analysis.next_action}</p>
            </div>
          )}
          {c.why_relevant && (
            <div className="crm-expanded-row">
              <span className="crm-expanded-label">Why relevant</span>
              <p className="crm-expanded-text">{c.why_relevant}</p>
            </div>
          )}
          {c.crm_analysis?.risk_notes && (
            <div className="crm-expanded-row">
              <span className="crm-expanded-label">Watch out</span>
              <p className="crm-expanded-text crm-expanded-text--risk">{c.crm_analysis.risk_notes}</p>
            </div>
          )}
          {c.notes && (
            <div className="crm-expanded-row">
              <span className="crm-expanded-label">Notes</span>
              <p className="crm-expanded-text">{c.notes}</p>
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
                {c.contact_page ? 'Contact page' : 'Website'} ↗
              </a>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function ContactsSection({ isOpen, onToggle, sectionRef }) {
  const [contacts, setContacts] = useState([])
  const [filter, setFilter] = useState('all')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/contacts')
      .then(r => r.ok ? r.json() : [])
      .then(data => { setContacts(Array.isArray(data) ? data : []); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  function handleUpdate(updated) {
    setContacts(prev => prev.map(c => c.name === updated.name ? updated : c))
  }

  // Summary counts
  const readyCount   = contacts.filter(c => ['ready_to_review', 'researching'].includes(c.status)).length
  const activeCount  = contacts.filter(c => ['contacted', 'in_contact', 'responded', 'submitted'].includes(c.status)).length
  const relCount     = contacts.filter(c => c.status === 'relationship' || c.status === 'ongoing').length

  const summaryParts = []
  if (readyCount)  summaryParts.push(`${readyCount} ready to reach out`)
  if (activeCount) summaryParts.push(`${activeCount} active`)
  if (relCount)    summaryParts.push(`${relCount} relationship${relCount !== 1 ? 's' : ''}`)
  const subtitle = contacts.length === 0
    ? 'No contacts yet'
    : `${contacts.length} contacts — ${summaryParts.join(', ') || 'no active threads'}`

  const FILTER_STATUS_MAP = {
    all:          null,
    ready:        ['ready_to_review', 'researching', 'cold'],
    active:       ['contacted', 'in_contact', 'responded', 'submitted'],
    relationship: ['relationship', 'ongoing'],
  }

  const filtered = filter === 'all'
    ? contacts
    : contacts.filter(c => (FILTER_STATUS_MAP[filter] || []).includes(c.status))

  return (
    <SectionShell
      id="contacts"
      sectionRef={sectionRef}
      title="Contacts"
      subtitle={subtitle}
      isOpen={isOpen}
      onToggle={onToggle}
    >
      <p className="pp-section-note">
        Venues and people worth cultivating. Tap a card to see notes. Use the quick buttons to track outreach.
      </p>

      {/* Summary bar */}
      {contacts.length > 0 && (
        <div className="crm-summary-bar">
          <span className="crm-summary-text">{subtitle}</span>
        </div>
      )}

      {/* Filter tabs */}
      <div className="crm-filter-tabs">
        {CRM_FILTER_TABS.map(tab => (
          <button
            key={tab.id}
            className={`crm-filter-tab${filter === tab.id ? ' crm-filter-tab--active' : ''}`}
            onClick={() => setFilter(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {loading && <p className="pp-section-note">Loading contacts…</p>}

      {!loading && filtered.length === 0 && (
        <p className="pp-section-note">
          {filter === 'all'
            ? 'No contacts in the system yet. The pipeline adds contacts as it discovers venues.'
            : `No contacts in this category.`}
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

const EVENT_COLORS = {
  accepted:     { bg: '#f0fbee', border: '#8fc98a', text: '#2e6626' },
  rejected:     { bg: '#fef5f5', border: '#e8b0b0', text: '#8b2a2a' },
  conversation: { bg: '#f0f6ff', border: '#90aee0', text: '#1a3a80' },
  visited:      { bg: '#fdf8f0', border: '#e0cba0', text: '#7a5010' },
  sold:         { bg: '#f6fdf0', border: '#a8d890', text: '#3a6020' },
  featured:     { bg: '#fffbef', border: '#e8d890', text: '#7a6010' },
}

function CareerEventWidget() {
  const { t } = useLanguage()
  const [events, setEvents] = useState([])
  const [noteType, setNoteType] = useState(null)
  const [note, setNote] = useState('')
  const [flash, setFlash] = useState(false)

  useEffect(() => {
    fetch('/api/career_events')
      .then(r => r.ok ? r.json() : [])
      .then(d => setEvents(Array.isArray(d) ? d.slice(0, 5) : []))
      .catch(() => {})
  }, [flash])

  async function logEvent(type) {
    if (noteType === type && note.trim() === '') {
      // second tap on same type without note — just submit
    } else if (noteType !== type) {
      setNoteType(type)
      setNote('')
      return
    }
    await fetch('/api/career_events', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type, note: note.trim() }),
    })
    setNoteType(null)
    setNote('')
    setFlash(f => !f)
  }

  async function quickLog(type) {
    // Single tap logs immediately (no note required)
    await fetch('/api/career_events', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type, note: '' }),
    })
    setNoteType(null)
    setNote('')
    setFlash(f => !f)
  }

  return (
    <div className="pp-event-widget">
      <div className="pp-event-prompt">{t('pp.event.prompt')}</div>
      <div className="pp-event-buttons">
        {EVENT_TYPES.map(({ type, icon }) => {
          const colors = EVENT_COLORS[type] || {}
          const isActive = noteType === type
          return (
            <button
              key={type}
              className={`pp-event-btn${isActive ? ' pp-event-btn--active' : ''}`}
              style={isActive ? { background: colors.bg, borderColor: colors.border, color: colors.text } : {}}
              onClick={() => {
                if (isActive) {
                  logEvent(type)
                } else {
                  setNoteType(type)
                  setNote('')
                }
              }}
              title={t(`pp.event.type.${type}`)}
            >
              <span className="pp-event-icon">{icon}</span>
              <span className="pp-event-label">{t(`pp.event.type.${type}`)}</span>
            </button>
          )
        })}
      </div>

      {noteType && (
        <div className="pp-event-note-row">
          <input
            className="pp-sub-input pp-event-note-input"
            value={note}
            onChange={e => setNote(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter') logEvent(noteType) }}
            placeholder={t('pp.event.note.placeholder')}
            autoFocus
          />
          <button className="pp-save pp-event-log-btn" onClick={() => logEvent(noteType)}>
            {t('pp.event.log')}
          </button>
          <button className="pp-skip" onClick={() => { setNoteType(null); setNote('') }}>
            {t('pp.event.cancel')}
          </button>
        </div>
      )}

      {events.length > 0 && (
        <div className="pp-event-recent">
          {events.map((ev, i) => {
            const colors = EVENT_COLORS[ev.type] || EVENT_COLORS.conversation
            const evType = EVENT_TYPES.find(e => e.type === ev.type)
            return (
              <div key={ev.id || i} className="pp-event-recent-row">
                <span className="pp-event-recent-icon" style={{ color: colors.text }}>{evType?.icon || '•'}</span>
                <span className="pp-event-recent-type" style={{ color: colors.text }}>{t(`pp.event.type.${ev.type}`)}</span>
                {ev.note && <span className="pp-event-recent-note">{ev.note}</span>}
                <span className="pp-event-recent-date">{ev.date}</span>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

// ── Carousel data builders ────────────────────────────────────────────────

function buildCarouselCards(profile, t) {
  const answers      = profile.saffron_answers || {}
  const answeredCount= QUESTION_KEYS.filter(k => answers[k]).length
  const goalsCount   = (profile.goals || []).filter(g => !g.done).length
  const hasText      = (profile.artist_statement || '').length > 30

  const qsDesc = answeredCount === 0 ? t('pp.carousel.qs.desc.0')
    : answeredCount < 4  ? t('pp.carousel.qs.desc.building', { n: answeredCount })
    : answeredCount < 8  ? t('pp.carousel.qs.desc.partial')
    :                      t('pp.carousel.qs.desc.done')

  const cards = [
    {
      id: 'tw',
      sectionId: 'instagram-strategy',
      name: t('pp.carousel.tw.name'),
      current: '~90k',
      next: '100k',
      ratio: 90 / 100,
      desc: t('pp.carousel.tw.desc'),
    },
    {
      id: 'ig',
      sectionId: 'instagram-strategy',
      name: t('pp.carousel.ig.name'),
      current: '21k',
      next: '25k',
      ratio: 21 / 25,
      desc: t('pp.carousel.ig.desc'),
    },
    {
      id: 'pub',
      sectionId: null,
      name: t('pp.carousel.pub.name'),
      current: '2',
      next: '3',
      ratio: 2 / 3,
      desc: t('pp.carousel.pub.desc'),
    },
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
      id: 'shows',
      sectionId: 'exhibition-pathway',
      name: t('pp.carousel.shows.name'),
      current: '1',
      next: '3',
      ratio: 1 / 3,
      desc: t('pp.carousel.shows.desc'),
    },
    {
      id: 'qs',
      sectionId: 'saffron-questions',
      name: t('pp.carousel.qs.name'),
      current: `${answeredCount}/8`,
      next: '8/8',
      ratio: answeredCount / 8,
      desc: qsDesc,
    },
    {
      id: 'goals',
      sectionId: 'career-goals',
      name: t('pp.carousel.goals.name'),
      current: String(goalsCount),
      next: goalsCount < 1 ? '1' : '3',
      ratio: goalsCount === 0 ? 0 : Math.min(goalsCount / 3, 1),
      desc: goalsCount === 0 ? t('pp.carousel.goals.desc.empty') : t('pp.carousel.goals.desc.has'),
    },
  ]

  const tw   = cards.find(c => c.id === 'tw')
  const qs   = cards.find(c => c.id === 'qs')
  const rest = cards.filter(c => c.id !== 'tw' && c.id !== 'qs').sort((a, b) => b.ratio - a.ratio)
  return [tw, qs, ...rest].filter(Boolean)
}

function computeSectionOrder(profile) {
  const answers      = profile.saffron_answers || {}
  const answeredCount= QUESTION_KEYS.filter(k => answers[k]).length
  const goalsCount   = (profile.goals || []).length
  const hasText      = (profile.artist_statement || '').length > 30

  const scores = {
    'instagram-strategy': 0.80,
    'artist-statement':   hasText ? 0.50 : 0.05,
    'exhibition-pathway': 0.40,
    'exhibition-log':     0.38,
    'submission-log':     0.35,
    'contacts':           0.34,
    'venue-log':          0.30,
    'preferences':        0.20,
    'career-goals':       Math.min(goalsCount / 3, 0.75),
    'saffron-questions':  answeredCount / 8,
  }

  return Object.entries(scores)
    .sort((a, b) => b[1] - a[1])
    .map(([id]) => id)
}

// ── Dismissal insight banner ──────────────────────────────────────────────

function DismissalInsightBanner() {
  const { t, lang } = useLanguage()
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

// ── Page root ──────────────────────────────────────────────────────────────

export default function PeppercornPage({ nav }) {
  const [profile,     setProfile]     = useState(null)
  const [statusMsg,   setStatusMsg]   = useState('')
  const [isSaved,     setIsSaved]     = useState(false)
  const [fetchError,  setFetchError]  = useState(null)
  const [openSections,setOpenSections]= useState(new Set(['instagram-strategy']))
  const [activeCard,  setActiveCard]  = useState(null)
  const { t } = useLanguage()

  const sectionRefs   = useRef({})
  const carouselCards = profile ? buildCarouselCards(profile, t) : []
  const sectionOrder  = profile ? computeSectionOrder(profile) : []

  useEffect(() => {
    fetch('/api/peppercorn')
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json() })
      .then(p => { setProfile(p); setOpenSections(new Set(['instagram-strategy'])) })
      .catch(e => setFetchError(e.message))
  }, [])

  // Track active card via IntersectionObserver
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
  }, [profile, sectionOrder.join(',')])

  async function saveSection(updates) {
    const next = { ...profile, ...updates }
    setProfile(next)
    setStatusMsg(t('pp.saving'))
    setIsSaved(false)
    try {
      const r = await fetch('/api/peppercorn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(next),
      })
      if (!r.ok) throw new Error(r.status)
      setStatusMsg(t('pp.saved'))
      setIsSaved(true)
      setTimeout(() => { setStatusMsg(''); setIsSaved(false) }, 2000)
    } catch {
      setStatusMsg(t('pp.saveError'))
      setTimeout(() => setStatusMsg(''), 3000)
    }
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
      next.has(id) ? next.delete(id) : next.add(id)
      return next
    })
  }

  function setSectionRef(id) {
    return el => { sectionRefs.current[id] = el }
  }

  const SECTION_COMPONENTS = {
    'instagram-strategy': (
      <InstagramStrategySection
        key="instagram-strategy"
        isOpen={openSections.has('instagram-strategy')}
        onToggle={() => toggleSection('instagram-strategy')}
        sectionRef={setSectionRef('instagram-strategy')}
      />
    ),
    'exhibition-pathway': (
      <ExhibitionPathwaySection
        key="exhibition-pathway"
        isOpen={openSections.has('exhibition-pathway')}
        onToggle={() => toggleSection('exhibition-pathway')}
        sectionRef={setSectionRef('exhibition-pathway')}
      />
    ),
    'artist-statement': (
      <ArtistStatementSection
        key="artist-statement"
        data={profile?.artist_statement}
        onSave={v => saveSection({ artist_statement: v })}
        isOpen={openSections.has('artist-statement')}
        onToggle={() => toggleSection('artist-statement')}
        sectionRef={setSectionRef('artist-statement')}
      />
    ),
    'saffron-questions': (
      <SaffronQuestionsSection
        key="saffron-questions"
        data={profile?.saffron_answers}
        onSave={v => saveSection({ saffron_answers: v })}
        isOpen={openSections.has('saffron-questions')}
        onToggle={() => toggleSection('saffron-questions')}
        sectionRef={setSectionRef('saffron-questions')}
      />
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
      {fetchError && <div className="pp-loading">{t('sf.error')}</div>}

      {profile && (
        <>
          {/* Career event quick-log */}
          <div className="pp-content">
            <CareerEventWidget />
            <DismissalInsightBanner />
          </div>

          {/* Carousel */}
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

          {/* Sections in dynamic order */}
          <div className="pp-content">
            {sectionOrder.map(id => SECTION_COMPONENTS[id])}
          </div>
        </>
      )}
    </div>
  )
}
