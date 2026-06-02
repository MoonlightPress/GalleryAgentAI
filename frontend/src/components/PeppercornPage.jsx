import { useState, useEffect, useRef } from 'react'
import './PeppercornPage.css'
import { peppercornHero } from '../utils/heroImages'

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
  return (
    <button className={`pp-save${saved ? ' pp-save--done' : ''}`} onClick={onSave}>
      {saved ? 'Saved ✓' : 'Save'}
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
  return (
    <SectionShell
      id="instagram-strategy"
      sectionRef={sectionRef}
      title="Social Presence"
      subtitle="Instagram and Twitter — what each threshold means, and what's worth noticing."
      isOpen={isOpen}
      onToggle={onToggle}
    >
      <div className="pp-analysis-grid">

        <div className="pp-platform-block">
          <div className="pp-platform-header">
            <span className="pp-platform-name">Instagram</span>
            <span className="pp-platform-handle">@gegyjiji</span>
            <span className="pp-platform-count">21k followers</span>
          </div>
          <p className="pp-analysis-note">
            21k means you are visible to the Tokyo illustration community and to print buyers
            doing light research. Gallery directors may glance. Major curators are not yet watching.
          </p>
          <div className="pp-threshold-list">
            <div className="pp-threshold-row">
              <div className="pp-threshold-marker pp-threshold-marker--next">25k</div>
              <p className="pp-threshold-desc">
                Algorithm begins treating the account as established. Print buyer and zine
                collector discovery increases — people who find work through browsing start
                encountering it. The first threshold worth actively pursuing.
              </p>
            </div>
            <div className="pp-threshold-row">
              <div className="pp-threshold-marker">50k</div>
              <p className="pp-threshold-desc">
                Gallery directors begin treating social following as a signal of market viability.
                Consignment conversations become easier to open — checking an artist's Instagram
                before agreeing to a show is standard practice at this level.
              </p>
            </div>
            <div className="pp-threshold-row">
              <div className="pp-threshold-marker">100k</div>
              <p className="pp-threshold-desc">
                Press interest increases organically. Collector attention expands beyond the
                illustration community. Speaking invitations at art events become plausible.
                A medium-term goal, not a near-term one.
              </p>
            </div>
          </div>
          <div className="pp-tactics-block">
            <div className="pp-block-label">What tends to work for this kind of practice</div>
            <ul className="pp-tactics-list">
              <li>Daily diary posts build attachment faster than occasional large posts — the accumulation effect</li>
              <li>Urban architecture, quiet spaces, and cats are high-performing for Japanese audiences</li>
              <li>Consistent Japanese/Chinese bilingual captions reach both communities without fragmenting either</li>
              <li>Story reposts of Tokyo urban observations build local audience faster than feed posts alone</li>
            </ul>
          </div>
        </div>

        <div className="pp-platform-block">
          <div className="pp-platform-header">
            <span className="pp-platform-name">Twitter / X</span>
            <span className="pp-platform-handle">@GegYjiji</span>
            <span className="pp-platform-count">~90k followers</span>
          </div>
          <p className="pp-analysis-note">
            Almost at 100k — a symbolic threshold. The illustration community following built
            through daily diary practice since 2020 is genuine and hard-won.
          </p>
          <div className="pp-threshold-list">
            <div className="pp-threshold-row">
              <div className="pp-threshold-marker pp-threshold-marker--next">100k</div>
              <p className="pp-threshold-desc">
                Symbolic milestone. Credibility marker in curator and gallerist conversations.
                Press mentions increase. Almost there.
              </p>
            </div>
          </div>
          <div className="pp-insight-box">
            Twitter is roughly 4× larger than Instagram. The gap matters because galleries
            and publishers use Instagram for discovery — it's where they look when they
            encounter a name. Twitter's audience doesn't bridge automatically.
          </div>
          <div className="pp-gentle-questions">
            <div className="pp-block-label">Peppercorn was wondering</div>
            <ul className="pp-wondering-list">
              <li>How often do you post to Instagram at the moment?</li>
              <li>Do you want to grow it, or use it mainly as a portfolio archive? The approach is completely different.</li>
              <li>If you can share your Instagram Insights screenshot, Peppercorn can see where your audience actually is.</li>
            </ul>
          </div>
        </div>

      </div>
    </SectionShell>
  )
}

// ── Exhibition pathway section ────────────────────────────────────────────

function ExhibitionPathwaySection({ isOpen, onToggle, sectionRef }) {
  return (
    <SectionShell
      id="exhibition-pathway"
      sectionRef={sectionRef}
      title="Exhibition Pathway"
      subtitle="Where one confirmed show sits on the road to a Tokyo solo."
      isOpen={isOpen}
      onToggle={onToggle}
    >
      <div className="pp-pathway-record">
        <div className="pp-pathway-show-title">Tide from China Part 1</div>
        <div className="pp-pathway-show-meta">ACG_Labo · Harajuku, Tokyo · February 2023 · Group show, 6 Chinese illustrators</div>
        <div className="pp-pathway-show-note">First Japan exhibition on record.</div>
      </div>

      <div className="pp-threshold-list pp-threshold-list--shows">
        <div className="pp-threshold-row pp-threshold-row--done">
          <div className="pp-threshold-marker pp-threshold-marker--done">1 ✓</div>
          <p className="pp-threshold-desc">Established presence. A credible starting point. Not yet a pattern.</p>
        </div>
        <div className="pp-threshold-row">
          <div className="pp-threshold-marker pp-threshold-marker--next">2</div>
          <p className="pp-threshold-desc">
            Pattern begins. The perception of "one lucky group show" dissolves.
            She is someone who exhibits, not someone who exhibited.
          </p>
        </div>
        <div className="pp-threshold-row">
          <div className="pp-threshold-marker pp-threshold-marker--key">3</div>
          <p className="pp-threshold-desc">
            The blocking milestone. Most Tokyo galleries consider 3 group show credits
            the minimum before discussing a solo show. Getting to 3 unlocks the next
            stage of the career arc.
          </p>
        </div>
        <div className="pp-threshold-row">
          <div className="pp-threshold-marker">5</div>
          <p className="pp-threshold-desc">
            Strong exhibition CV. Residency applications become competitive. Institutional
            open calls — TOKAS, BankART1929, Youkobo — become realistic rather than aspirational.
          </p>
        </div>
      </div>

      <div className="pp-next-targets">
        <div className="pp-block-label">Next targets worth watching</div>
        <div className="pp-target-row">
          <div className="pp-target-name">3331 Arts Chiyoda</div>
          <p className="pp-target-desc">Open calls on regular cycle. Artist-run feel. Accessible for international artists based in Tokyo.</p>
        </div>
        <div className="pp-target-row">
          <div className="pp-target-name">Design Festa Gallery</div>
          <p className="pp-target-desc">Active curated program, illustration-adjacent. Harajuku location builds on the ACG_Labo connection.</p>
        </div>
        <div className="pp-target-row">
          <div className="pp-target-name">Gallery IYN</div>
          <p className="pp-target-desc">Smaller, emerging-artist focused. Realistic first repeat venue.</p>
        </div>
      </div>

      <p className="pp-timeline-note">
        At a realistic application pace — 3 to 5 submissions per year, acceptance rate 20–30% —
        reaching 3 confirmed shows takes approximately 2–3 years from mid-2026.
        This is not slow. This is normal.
      </p>
    </SectionShell>
  )
}

// ── Artist statement section ──────────────────────────────────────────────

function StatementExample() {
  const [show, setShow] = useState(false)
  return (
    <div className="pp-stmt-example">
      <button className="pp-example-toggle" onClick={() => setShow(s => !s)}>
        {show ? 'Hide example ↑' : 'Why does this matter? See an example ↓'}
      </button>
      {show && (
        <div className="pp-example-body">
          <div className="pp-example-col">
            <div className="pp-example-label">Generic</div>
            <p className="pp-example-text pp-example-text--generic">
              "I am an artist working with watercolor, exploring themes of memory and urban space."
            </p>
          </div>
          <div className="pp-example-vs">→</div>
          <div className="pp-example-col">
            <div className="pp-example-label">Specific</div>
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
  useEffect(() => { setText(data || '') }, [data])

  return (
    <SectionShell
      id="artist-statement"
      sectionRef={sectionRef}
      title="Artist Statement"
      subtitle="A working draft — edit freely, whenever it feels right."
      isOpen={isOpen}
      onToggle={onToggle}
    >
      <p className="pp-section-note">
        This text feeds every outreach email Mochi drafts, every cover letter, every
        opportunity description the system generates. A specific, true statement produces
        outreach that sounds like you. A generic one produces generic outreach.
      </p>
      <StatementExample />
      <textarea
        className="pp-statement"
        value={text}
        onChange={e => setText(e.target.value)}
        placeholder="Write a short statement about your practice…"
        rows={7}
      />
      <SaveBtn saved={saved} onSave={() => { onSave(text); flash() }} />
    </SectionShell>
  )
}

// ── Saffron's questions section ───────────────────────────────────────────

const QUESTIONS = [
  { key: 'posting_frequency',         text: 'How often do you post to Instagram? Any goals for this?',                              why: 'Posting cadence is the most controllable variable for closing the Instagram/Twitter gap.' },
  { key: 'audience_geography',        text: 'Where are most of your followers — Tokyo, China, or spread globally?',                  why: 'Whether your audience is primarily Chinese-language changes the geographic expansion strategy entirely.' },
  { key: 'has_sold_work',             text: 'Have you sold work before? Through which channels — fairs, online, prints, originals?', why: 'Sales history reveals which formats and price points convert, which shapes which fairs are worth entering.' },
  { key: 'new_publication_planned',   text: 'Is a new publication or zine in the works, even loosely?',                              why: 'If one is already planned, the system should support it — not recommend it as a new idea.' },
  { key: 'has_artist_statement',      text: 'Do you have an artist statement written anywhere — in any language?',                   why: 'Most open calls require one. If none exists, this is the most urgent gap before any submissions.' },
  { key: 'tide_china_contact',        text: 'Are you still in touch with anyone from the Tide from China show?',                     why: 'Those five artists are the most natural group show partners. If they have dispersed, the network needs rebuilding.' },
  { key: 'second_exhibition_planned', text: 'Is there a second Japan exhibition already planned or in conversation?',                 why: 'The system assumes 2–3 more group shows are needed, but one may already be underway.' },
  { key: 'price_points',              text: 'What do you charge for originals and prints?',                                          why: 'Pricing determines which collector tier and which fairs are appropriate. Under-pricing affects how galleries perceive the work.' },
]

function SaffronQuestionsSection({ data, onSave, isOpen, onToggle, sectionRef }) {
  const [answers, setAnswers] = useState(data || {})
  useEffect(() => { setAnswers(data || {}) }, [data])

  const answeredCount    = QUESTIONS.filter(q => answers[q.key]).length
  const allAnswered      = answeredCount === QUESTIONS.length
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

  const subtitle = allAnswered
    ? 'Saffron has everything she needs for now. Check back after your next exhibition.'
    : `Saffron left ${QUESTIONS.length - answeredCount} question${QUESTIONS.length - answeredCount !== 1 ? 's' : ''} — whenever you have a moment.`

  return (
    <SectionShell
      id="saffron-questions"
      sectionRef={sectionRef}
      title="Saffron's Questions"
      subtitle={subtitle}
      isOpen={isOpen}
      onToggle={onToggle}
    >
      {allAnswered ? (
        <p className="pp-section-note pp-section-note--gentle">
          Saffron has everything she needs for now. Come back after your next exhibition or publication.
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
            <div className="pp-q-num">Question {activeIdx + 1}</div>
            <p className="pp-q-text">{currentQ.text}</p>
            <p className="pp-q-why">{currentQ.why}</p>
            <textarea
              className="pp-q-input"
              value={draft}
              onChange={e => setDraft(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && e.metaKey && saveAnswer()}
              placeholder="Your answer…"
              rows={3}
            />
            <div className="pp-q-actions">
              <button className="pp-save pp-save--answer" onClick={saveAnswer} disabled={!draft.trim()}>
                Save answer
              </button>
              {!answers[currentQ.key] && (
                <button className="pp-skip" onClick={skipQ}>Come back to this</button>
              )}
              {answers[currentQ.key] && (
                <button className="pp-skip" onClick={() => clearAnswer(currentQ.key)}>Clear answer</button>
              )}
            </div>
          </div>
        </>
      )}

      {answeredCount > 0 && (
        <div className="pp-q-done-list">
          <div className="pp-block-label">{answeredCount} answered</div>
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
      title="Career Goals"
      subtitle="What are you working toward? No format needed — Peppercorn will figure it out."
      isOpen={isOpen}
      onToggle={onToggle}
    >
      {goals.length === 0 && (
        <p className="pp-section-note">
          Peppercorn hasn't heard your goals yet. What are you working toward?
        </p>
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
        <button className="pp-add-btn" onClick={addGoal}>Add</button>
      </div>

      {shownFirstNote && goals.length === 1 && (
        <p className="pp-first-goal-note">Saffron will use this to sharpen her analysis.</p>
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

const TIERS = [
  { n: 1, label: 'Tier 1 — Ambient Visibility', desc: 'Zine shops, consignment, café prints, book fairs' },
  { n: 2, label: 'Tier 2 — Networking',         desc: 'Group shows, artist-run spaces, community events' },
  { n: 3, label: 'Tier 3 — Credibility',        desc: 'Institutional open calls, juried shows, TOKAS' },
  { n: 4, label: 'Tier 4 — Prestige',           desc: 'RWS, ACC, Cité des Arts — future targets only' },
]
const TRACKS = [
  { id: 'publication', label: 'Publication & illustration ecosystem', desc: 'Zines, artist books, illustration fairs, publishers' },
  { id: 'gallery',     label: 'Gallery & exhibition track',           desc: 'Group shows, open calls, gallery relationships' },
  { id: 'hybrid',      label: 'Both — running in parallel',          desc: 'The natural fit given her existing practice' },
]
const AVOID_OPTIONS = [
  { id: 'photography_calls',    label: 'Photography-heavy open calls' },
  { id: 'high_fees',            label: 'Entry fees over ¥10,000 / $60' },
  { id: 'international_travel', label: 'Opportunities requiring international travel now' },
  { id: 'digital_only',         label: 'Digital-only submissions' },
  { id: 'large_group',          label: 'Group shows with 20+ artists' },
]
const GEO_OPTIONS = [
  { id: 'tokyo',         label: 'Tokyo first',           desc: 'Prioritise opportunities within Tokyo' },
  { id: 'japan',         label: 'Japan (beyond Tokyo)',  desc: 'Include Osaka, Kyoto, Yokohama, etc.' },
  { id: 'international', label: 'International equally', desc: 'Global open calls, overseas fairs, residencies' },
]
const FEE_OPTIONS = [
  { id: 'free',   label: 'Free only' },
  { id: 'low',    label: 'Up to ¥5,000 / $30' },
  { id: 'medium', label: 'Up to ¥15,000 / $80' },
  { id: 'any',    label: 'Any fee — judge case by case' },
]
const SURFACE_OPTIONS = [
  { id: 'zines_books',     label: 'Zines, artist books & publishing' },
  { id: 'gallery_shows',   label: 'Gallery exhibitions & open calls' },
  { id: 'residencies',     label: 'Residencies & fellowships' },
  { id: 'cafes_bookshops', label: 'Café & bookshop spaces' },
  { id: 'art_fairs',       label: 'Art fairs & markets' },
]

function PreferencesSection({ data, onSave, isOpen, onToggle, sectionRef }) {
  const pri  = (data || {}).priorities  || {}
  const pref = (data || {}).preferences || {}

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
      title="Preferences"
      subtitle="Peppercorn's current settings. The defaults are reasonable — only change them if something feels off."
      isOpen={isOpen}
      onToggle={onToggle}
    >
      <p className="pp-section-note">
        The more Peppercorn knows, the sharper Saffron's analysis becomes — but there's no rush.
        Changes take effect on the next pipeline run.
      </p>

      <div className="pp-group">
        <div className="pp-group-label">Active tiers</div>
        <p className="pp-group-hint">Check the tiers you are actively building toward. Tier 1–2 should almost always be checked.</p>
        {TIERS.map(t => (
          <label key={t.n} className="pp-check-row">
            <input type="checkbox" className="pp-check" checked={tiers.includes(t.n)} onChange={() => toggleTier(t.n)} />
            <span className="pp-check-label"><strong>{t.label}</strong><span className="pp-check-desc">{t.desc}</span></span>
          </label>
        ))}
      </div>

      <div className="pp-group">
        <div className="pp-group-label">Primary track</div>
        {TRACKS.map(tr => (
          <label key={tr.id} className="pp-radio-row">
            <input type="radio" className="pp-radio" name="pp-track" value={tr.id} checked={track === tr.id} onChange={() => setTrack(tr.id)} />
            <span className="pp-check-label"><strong>{tr.label}</strong><span className="pp-check-desc">{tr.desc}</span></span>
          </label>
        ))}
      </div>

      <div className="pp-group">
        <div className="pp-group-label">Avoid surfacing</div>
        {AVOID_OPTIONS.map(opt => (
          <label key={opt.id} className="pp-check-row">
            <input type="checkbox" className="pp-check" checked={avoid.includes(opt.id)} onChange={() => toggleAvoid(opt.id)} />
            <span className="pp-check-label">{opt.label}</span>
          </label>
        ))}
      </div>

      <div className="pp-group">
        <div className="pp-group-label">Geographic focus</div>
        {GEO_OPTIONS.map(opt => (
          <label key={opt.id} className="pp-check-row">
            <input type="checkbox" className="pp-check" checked={geo.includes(opt.id)} onChange={() => toggleGeo(opt.id)} />
            <span className="pp-check-label"><strong>{opt.label}</strong>{opt.desc && <span className="pp-check-desc">{opt.desc}</span>}</span>
          </label>
        ))}
      </div>

      <div className="pp-group">
        <div className="pp-group-label">Fee tolerance</div>
        {FEE_OPTIONS.map(opt => (
          <label key={opt.id} className="pp-radio-row">
            <input type="radio" className="pp-radio" name="pp-fee" value={opt.id} checked={fee === opt.id} onChange={() => setFee(opt.id)} />
            <span className="pp-check-label">{opt.label}</span>
          </label>
        ))}
      </div>

      <div className="pp-group">
        <div className="pp-group-label">Category weighting</div>
        <p className="pp-group-hint">Surface more ↑ or less ↓ of each category. Leaving a category blank keeps the pipeline's current weighting.</p>
        <div className="pp-surface-grid">
          <div className="pp-surface-header">
            <span />
            <span className="pp-surface-col-label">More ↑</span>
            <span className="pp-surface-col-label">Less ↓</span>
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

// ── Carousel data builders ────────────────────────────────────────────────

function buildCarouselCards(profile) {
  const answers      = profile.saffron_answers || {}
  const answeredCount= QUESTIONS.filter(q => answers[q.key]).length
  const goalsCount   = (profile.goals || []).filter(g => !g.done).length
  const hasText      = (profile.artist_statement || '').length > 30

  const cards = [
    {
      id: 'tw',
      sectionId: 'instagram-strategy',
      name: 'Twitter / X',
      current: '~90k',
      next: '100k',
      ratio: 90 / 100,
      desc: 'Symbolic milestone — credibility marker in curator conversations',
    },
    {
      id: 'ig',
      sectionId: 'instagram-strategy',
      name: 'Instagram',
      current: '21k',
      next: '25k',
      ratio: 21 / 25,
      desc: 'Algorithm visibility increases at 25k — print buyer discovery begins',
    },
    {
      id: 'pub',
      sectionId: null,
      name: 'Publications',
      current: '2',
      next: '3',
      ratio: 2 / 3,
      desc: 'A third publication establishes a pattern — see Saffron for the full landscape',
    },
    {
      id: 'stmt',
      sectionId: 'artist-statement',
      name: 'Artist Statement',
      current: hasText ? 'draft' : 'none',
      next: 'refined',
      ratio: hasText ? 0.5 : 0,
      desc: 'This text feeds every email Mochi drafts — the better it is, the better everything is',
    },
    {
      id: 'shows',
      sectionId: 'exhibition-pathway',
      name: 'Group Shows',
      current: '1',
      next: '3',
      ratio: 1 / 3,
      desc: 'Tokyo galleries consider 3 shows minimum before solo show conversations',
    },
    {
      id: 'qs',
      sectionId: 'saffron-questions',
      name: "Saffron's Questions",
      current: `${answeredCount}/8`,
      next: '8/8',
      ratio: answeredCount / 8,
      desc: answeredCount === 0 ? 'Saffron is working with incomplete context'
          : answeredCount < 4  ? `${answeredCount} answered — Saffron is building a picture`
          : answeredCount < 8  ? 'Saffron has enough for a partial analysis'
          :                      'Saffron has everything she needs for now',
    },
    {
      id: 'goals',
      sectionId: 'career-goals',
      name: 'Career Goals',
      current: String(goalsCount),
      next: goalsCount < 1 ? '1' : '3',
      ratio: goalsCount === 0 ? 0 : Math.min(goalsCount / 3, 1),
      desc: goalsCount === 0
        ? "Peppercorn hasn't heard your goals yet"
        : 'Saffron uses these to weight recommendations toward what you want',
    },
  ]

  return cards.sort((a, b) => b.ratio - a.ratio)
}

function computeSectionOrder(profile) {
  const answers      = profile.saffron_answers || {}
  const answeredCount= QUESTIONS.filter(q => answers[q.key]).length
  const goalsCount   = (profile.goals || []).length
  const hasText      = (profile.artist_statement || '').length > 30

  const scores = {
    'instagram-strategy': 0.80,
    'artist-statement':   hasText ? 0.50 : 0.05,
    'exhibition-pathway': 0.40,
    'preferences':        0.20,
    'career-goals':       Math.min(goalsCount / 3, 0.75),
    'saffron-questions':  answeredCount / 8,
  }

  return Object.entries(scores)
    .sort((a, b) => b[1] - a[1])
    .map(([id]) => id)
}

// ── Page root ──────────────────────────────────────────────────────────────

export default function PeppercornPage() {
  const [profile,     setProfile]     = useState(null)
  const [statusMsg,   setStatusMsg]   = useState('')
  const [openSections,setOpenSections]= useState(new Set(['instagram-strategy']))
  const [activeCard,  setActiveCard]  = useState(null)

  const sectionRefs   = useRef({})
  const carouselCards = profile ? buildCarouselCards(profile) : []
  const sectionOrder  = profile ? computeSectionOrder(profile) : []

  useEffect(() => {
    fetch('/api/peppercorn')
      .then(r => r.json())
      .then(p => { setProfile(p); setOpenSections(new Set(['instagram-strategy'])) })
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
    setStatusMsg('Saving…')
    await fetch('/api/peppercorn', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(next),
    })
    setStatusMsg('Saved')
    setTimeout(() => setStatusMsg(''), 2000)
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
  }

  return (
    <div className="peppercorn-page">

      {/* Ambient mouse illustration */}
      <div className="pp-mouse-ambient">
        <img src={peppercornHero} alt="Peppercorn" className="pp-mouse-img" />
      </div>

      {/* Status bar */}
      {statusMsg && (
        <div className={`pp-status-bar${statusMsg === 'Saved' ? ' pp-status-bar--saved' : ''}`}>
          {statusMsg}
        </div>
      )}

      {!profile && <div className="pp-loading">Peppercorn is listening…</div>}

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
