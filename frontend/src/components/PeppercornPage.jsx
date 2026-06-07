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
              "I am an artist working with watercolor, exploring themes of memory and urban space."
            </p>
          </div>
          <div className="pp-example-vs">→</div>
          <div className="pp-example-col">
            <div className="pp-example-label">{t('pp.ex.specific')}</div>
            <p className="pp-example-text pp-example-text--specific">
              "My paintings are slow observations of urban places between moments — the alley
              before anyone arrives, the café after everyone has left. I work in watercolor because
              it captures what memory does to architecture: softened edges, color that breathes,
              forms that are almost but not quite precise."
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

const GOAL_PLACEHOLDERS = [
  'Table at Tokyo Art Book Fair',
  'First solo show before 30',
  "Get featured in It's Nice That",
  'Collaborate with a Tokyo bookshop',
  'Sell 20 prints in a single month',
]

function CareerGoalsSection({ data, onSave, isOpen, onToggle, sectionRef }) {
  const [goals,  setGoals]  = useState(data || [])
  const [input,  setInput]  = useState('')
  const [saved,  flash]     = useSaved()
  const [phIdx]             = useState(() => Math.floor(Math.random() * GOAL_PLACEHOLDERS.length))
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
              <button className="pp-goal-toggle" onClick={() => toggleDone(g.id)} title="Mark complete">○</button>
              <span className="pp-goal-text">{g.text}</span>
              <button className="pp-goal-remove" onClick={() => removeGoal(g.id)} title="Remove">×</button>
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
          placeholder={GOAL_PLACEHOLDERS[phIdx] + '…'}
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
              <button className="pp-goal-toggle" onClick={() => toggleDone(g.id)} title="Reopen">✓</button>
              <span className="pp-goal-text">{g.text}</span>
              <button className="pp-goal-remove" onClick={() => removeGoal(g.id)} title="Remove">×</button>
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
  { value: 'pending',    label: 'Pending' },
  { value: 'accepted',   label: 'Accepted ✓' },
  { value: 'rejected',   label: 'Rejected' },
  { value: 'waitlisted', label: 'Waitlisted' },
  { value: 'withdrawn',  label: 'Withdrawn' },
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
      title="Submission Log"
      subtitle={submissions.length === 0 ? 'No submissions logged yet' : `${submissions.length} submission${submissions.length !== 1 ? 's' : ''} on record`}
      isOpen={isOpen}
      onToggle={onToggle}
    >
      <p className="pp-section-note">Keep a record of what you've submitted and what happened. The system uses this to avoid recommending the same venue twice.</p>

      <div className="pp-sub-form">
        <div className="pp-sub-form-row">
          <div className="pp-sub-field">
            <label className="pp-sub-label">Date</label>
            <input
              type="date"
              className="pp-sub-input"
              value={form.date}
              onChange={e => setField('date', e.target.value)}
            />
          </div>
          <div className="pp-sub-field pp-sub-field--wide">
            <label className="pp-sub-label">Venue or opportunity</label>
            <input
              type="text"
              className="pp-sub-input"
              value={form.venue}
              onChange={e => setField('venue', e.target.value)}
              placeholder="Gallery name, open call, fair…"
            />
          </div>
          <div className="pp-sub-field">
            <label className="pp-sub-label">Outcome</label>
            <select className="pp-sub-select" value={form.outcome} onChange={e => setField('outcome', e.target.value)}>
              {OUTCOME_OPTIONS.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
            </select>
          </div>
        </div>
        <div className="pp-sub-field">
          <label className="pp-sub-label">What was submitted</label>
          <input
            type="text"
            className="pp-sub-input"
            value={form.what}
            onChange={e => setField('what', e.target.value)}
            placeholder="Urban Watercolors series, 5 works / artist book proposal / residency application…"
          />
        </div>
        <div className="pp-sub-field">
          <label className="pp-sub-label">Notes (optional)</label>
          <input
            type="text"
            className="pp-sub-input"
            value={form.notes}
            onChange={e => setField('notes', e.target.value)}
            placeholder="Follow-up needed, referral from…"
          />
        </div>
        <button
          className={`pp-save${saved ? ' pp-save--done' : ''}`}
          onClick={submitEntry}
          disabled={saving || !form.venue.trim() || !form.what.trim()}
        >
          {saved ? 'Logged ✓' : 'Log submission'}
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
                    {OUTCOME_OPTIONS.find(o => o.value === s.outcome)?.label || s.outcome}
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
    'submission-log':     0.35,
    'preferences':        0.20,
    'career-goals':       Math.min(goalsCount / 3, 0.75),
    'saffron-questions':  answeredCount / 8,
  }

  return Object.entries(scores)
    .sort((a, b) => b[1] - a[1])
    .map(([id]) => id)
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
    'submission-log': (
      <SubmissionLogSection
        key="submission-log"
        isOpen={openSections.has('submission-log')}
        onToggle={() => toggleSection('submission-log')}
        sectionRef={setSectionRef('submission-log')}
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
