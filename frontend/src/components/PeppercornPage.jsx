import { useState, useEffect } from 'react'
import './PeppercornPage.css'
import { peppercornHero } from '../utils/heroImages'

// ── Shared shell ───────────────────────────────────────────────────────────

function Section({ title, subtitle, defaultOpen = true, children }) {
  const [open, setOpen] = useState(defaultOpen)
  return (
    <section className={`pp-section${open ? '' : ' pp-section--closed'}`}>
      <button className="pp-toggle" onClick={() => setOpen(o => !o)}>
        <div className="pp-toggle-text">
          <h2 className="pp-title">{title}</h2>
          {open && subtitle && <p className="pp-subtitle">{subtitle}</p>}
        </div>
        <span className={`pp-chevron${open ? ' pp-chevron--open' : ''}`}>▾</span>
      </button>
      {open && <div className="pp-body">{children}</div>}
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
  function flash() {
    setSaved(true)
    setTimeout(() => setSaved(false), 2200)
  }
  return [saved, flash]
}

// ── Section 1: Priorities ──────────────────────────────────────────────────

const TIERS = [
  { n: 1, label: 'Tier 1 — Ambient Visibility', desc: 'Zine shops, consignment, café prints, book fairs' },
  { n: 2, label: 'Tier 2 — Networking',         desc: 'Group shows, artist-run spaces, community events' },
  { n: 3, label: 'Tier 3 — Credibility',         desc: 'Institutional open calls, juried shows, TOKAS' },
  { n: 4, label: 'Tier 4 — Prestige',            desc: 'RWS, ACC, Cité des Arts — future targets only' },
]

const TRACKS = [
  { id: 'publication', label: 'Publication & illustration ecosystem', desc: 'Zines, artist books, illustration fairs, publishers' },
  { id: 'gallery',     label: 'Gallery & exhibition track',           desc: 'Group shows, open calls, gallery relationships' },
  { id: 'hybrid',      label: 'Both — running in parallel',          desc: 'The natural fit given her existing practice' },
]

const AVOID_OPTIONS = [
  { id: 'photography_calls', label: 'Photography-heavy open calls' },
  { id: 'high_fees',         label: 'Entry fees over ¥10,000 / $60' },
  { id: 'international_travel', label: 'Opportunities requiring international travel now' },
  { id: 'digital_only',     label: 'Digital-only submissions' },
  { id: 'large_group',      label: 'Group shows with 20+ artists' },
]

function PrioritiesSection({ data, onSave }) {
  const [tiers, setTiers] = useState(data.active_tiers || [1, 2])
  const [track, setTrack] = useState(data.primary_track || 'hybrid')
  const [avoid, setAvoid] = useState(data.avoid || [])
  const [saved, flash] = useSaved()

  function toggleTier(n) {
    setTiers(ts => ts.includes(n) ? ts.filter(t => t !== n) : [...ts, n].sort())
  }
  function toggleAvoid(id) {
    setAvoid(av => av.includes(id) ? av.filter(a => a !== id) : [...av, id])
  }

  return (
    <Section
      title="Priorities"
      subtitle="Which career tiers are active right now, and what to focus on."
    >
      <div className="pp-group">
        <div className="pp-group-label">Active tiers</div>
        <p className="pp-group-hint">Check the tiers you are actively building toward. Tier 1–2 should almost always be checked.</p>
        {TIERS.map(t => (
          <label key={t.n} className="pp-check-row">
            <input
              type="checkbox"
              className="pp-check"
              checked={tiers.includes(t.n)}
              onChange={() => toggleTier(t.n)}
            />
            <span className="pp-check-label">
              <strong>{t.label}</strong>
              <span className="pp-check-desc">{t.desc}</span>
            </span>
          </label>
        ))}
      </div>

      <div className="pp-group">
        <div className="pp-group-label">Primary track</div>
        {TRACKS.map(tr => (
          <label key={tr.id} className="pp-radio-row">
            <input
              type="radio"
              className="pp-radio"
              name="track"
              value={tr.id}
              checked={track === tr.id}
              onChange={() => setTrack(tr.id)}
            />
            <span className="pp-check-label">
              <strong>{tr.label}</strong>
              <span className="pp-check-desc">{tr.desc}</span>
            </span>
          </label>
        ))}
      </div>

      <div className="pp-group">
        <div className="pp-group-label">Avoid surfacing</div>
        {AVOID_OPTIONS.map(opt => (
          <label key={opt.id} className="pp-check-row">
            <input
              type="checkbox"
              className="pp-check"
              checked={avoid.includes(opt.id)}
              onChange={() => toggleAvoid(opt.id)}
            />
            <span className="pp-check-label">{opt.label}</span>
          </label>
        ))}
      </div>

      <SaveBtn saved={saved} onSave={() => {
        onSave({ active_tiers: tiers, primary_track: track, avoid })
        flash()
      }} />
    </Section>
  )
}

// ── Section 2: Artist Statement ────────────────────────────────────────────

function StatementSection({ data, onSave }) {
  const [text, setText] = useState(data || '')
  const [saved, flash] = useSaved()

  return (
    <Section
      title="Artist Statement"
      subtitle="A working draft — edit freely. This feeds into submissions, cover letters, and Mochi's recommendations."
    >
      <textarea
        className="pp-statement"
        value={text}
        onChange={e => setText(e.target.value)}
        placeholder="Write a short statement about your practice…"
        rows={7}
      />
      <p className="pp-field-hint">
        Pre-populated from your profile phrases. Edit, expand, or replace entirely — this is your draft, not a final version.
      </p>
      <SaveBtn saved={saved} onSave={() => { onSave(text); flash() }} />
    </Section>
  )
}

// ── Section 3: Goals ───────────────────────────────────────────────────────

function GoalsSection({ data, onSave }) {
  const [goals, setGoals] = useState(data || [])
  const [input, setInput] = useState('')
  const [saved, flash] = useSaved()

  function addGoal() {
    const t = input.trim()
    if (!t) return
    setGoals(gs => [...gs, { id: Date.now(), text: t, done: false }])
    setInput('')
  }

  function removeGoal(id) { setGoals(gs => gs.filter(g => g.id !== id)) }
  function toggleDone(id) { setGoals(gs => gs.map(g => g.id === id ? { ...g, done: !g.done } : g)) }

  return (
    <Section
      title="Goals"
      subtitle="What do you want to accomplish? No timeframe required — just capture it."
    >
      {goals.length === 0 && (
        <p className="pp-empty">No goals yet. Add the first one below.</p>
      )}

      <div className="pp-goal-list">
        {goals.map(g => (
          <div key={g.id} className={`pp-goal-row${g.done ? ' pp-goal-row--done' : ''}`}>
            <button className="pp-goal-toggle" onClick={() => toggleDone(g.id)} title="Mark complete">
              {g.done ? '✓' : '○'}
            </button>
            <span className="pp-goal-text">{g.text}</span>
            <button className="pp-goal-remove" onClick={() => removeGoal(g.id)} title="Remove">×</button>
          </div>
        ))}
      </div>

      <div className="pp-goal-add">
        <input
          className="pp-goal-input"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && addGoal()}
          placeholder="Add a goal and press Enter…"
        />
        <button className="pp-add-btn" onClick={addGoal}>Add</button>
      </div>

      <SaveBtn saved={saved} onSave={() => { onSave(goals); flash() }} />
    </Section>
  )
}

// ── Section 4: Preferences ─────────────────────────────────────────────────

const GEO_OPTIONS = [
  { id: 'tokyo',         label: 'Tokyo first',               desc: 'Prioritise opportunities within Tokyo' },
  { id: 'japan',         label: 'Japan (beyond Tokyo)',       desc: 'Include Osaka, Kyoto, Yokohama, etc.' },
  { id: 'international', label: 'International equally',      desc: 'Global open calls, overseas fairs, residencies' },
]

const FEE_OPTIONS = [
  { id: 'free',    label: 'Free only' },
  { id: 'low',     label: 'Up to ¥5,000 / $30' },
  { id: 'medium',  label: 'Up to ¥15,000 / $80' },
  { id: 'any',     label: 'Any fee — judge case by case' },
]

const SURFACE_OPTIONS = [
  { id: 'zines_books',   label: 'Zines, artist books & publishing' },
  { id: 'gallery_shows', label: 'Gallery exhibitions & open calls' },
  { id: 'residencies',   label: 'Residencies & fellowships' },
  { id: 'cafes_bookshops', label: 'Café & bookshop spaces' },
  { id: 'art_fairs',     label: 'Art fairs & markets' },
]

function PreferencesSection({ data, onSave }) {
  const [geo, setGeo]       = useState(data.geo_focus || ['tokyo', 'international'])
  const [fee, setFee]       = useState(data.fee_tolerance || 'low')
  const [more, setMore]     = useState(data.surface_more || ['zines_books'])
  const [less, setLess]     = useState(data.surface_less || [])
  const [saved, flash]      = useSaved()

  function toggleGeo(id) {
    setGeo(gs => gs.includes(id) ? gs.filter(g => g !== id) : [...gs, id])
  }
  function toggleMore(id) {
    setMore(ms => ms.includes(id) ? ms.filter(m => m !== id) : [...ms, id])
    setLess(ls => ls.filter(l => l !== id))
  }
  function toggleLess(id) {
    setLess(ls => ls.includes(id) ? ls.filter(l => l !== id) : [...ls, id])
    setMore(ms => ms.filter(m => m !== id))
  }

  return (
    <Section
      title="Preferences"
      subtitle="Tune what the pipeline surfaces. Changes take effect on the next pipeline run."
    >
      <div className="pp-group">
        <div className="pp-group-label">Geographic focus</div>
        {GEO_OPTIONS.map(opt => (
          <label key={opt.id} className="pp-check-row">
            <input
              type="checkbox"
              className="pp-check"
              checked={geo.includes(opt.id)}
              onChange={() => toggleGeo(opt.id)}
            />
            <span className="pp-check-label">
              <strong>{opt.label}</strong>
              {opt.desc && <span className="pp-check-desc">{opt.desc}</span>}
            </span>
          </label>
        ))}
      </div>

      <div className="pp-group">
        <div className="pp-group-label">Fee tolerance</div>
        {FEE_OPTIONS.map(opt => (
          <label key={opt.id} className="pp-radio-row">
            <input
              type="radio"
              className="pp-radio"
              name="fee"
              value={opt.id}
              checked={fee === opt.id}
              onChange={() => setFee(opt.id)}
            />
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
              <input
                type="checkbox"
                className="pp-check pp-check--more"
                checked={more.includes(opt.id)}
                onChange={() => toggleMore(opt.id)}
              />
              <input
                type="checkbox"
                className="pp-check pp-check--less"
                checked={less.includes(opt.id)}
                onChange={() => toggleLess(opt.id)}
              />
            </div>
          ))}
        </div>
      </div>

      <SaveBtn saved={saved} onSave={() => {
        onSave({ geo_focus: geo, fee_tolerance: fee, surface_more: more, surface_less: less })
        flash()
      }} />
    </Section>
  )
}

// ── Section 5: Saffron's Questions ─────────────────────────────────────────

const QUESTIONS = [
  {
    key:  'posting_frequency',
    text: 'How often do you post to Instagram? Any goals for this?',
    why:  'Posting cadence is the most controllable variable for closing the gap between Instagram and Twitter.',
  },
  {
    key:  'audience_geography',
    text: 'Where are most of your followers — Tokyo, China, or spread globally?',
    why:  'Whether your audience is mostly Chinese-language changes the geographic expansion strategy entirely.',
  },
  {
    key:  'has_sold_work',
    text: 'Have you sold work before? Through which channels — fairs, online, prints, originals?',
    why:  'Sales history reveals which formats and price points convert, which shapes which fairs are worth entering.',
  },
  {
    key:  'new_publication_planned',
    text: 'Is a new publication or zine in the works, even loosely?',
    why:  'If one is already planned, the system should support it — not recommend it as a new idea.',
  },
  {
    key:  'has_artist_statement',
    text: 'Do you have an artist statement written anywhere — in any language?',
    why:  'Most open calls require one. If none exists, this is the most urgent gap before any submissions.',
  },
  {
    key:  'tide_china_contact',
    text: 'Are you still in touch with anyone from the Tide from China show?',
    why:  "Those five artists are the most natural group show partners. If they've dispersed, that network is dormant.",
  },
  {
    key:  'second_exhibition_planned',
    text: 'Is there a second Japan exhibition already planned or in conversation?',
    why:  "The system assumes you need 2–3 more group shows — but you may already have one underway that isn't in the data.",
  },
  {
    key:  'price_points',
    text: 'What do you charge for originals and prints?',
    why:  'Pricing determines which collector tier and which fairs are appropriate. Under-pricing affects how galleries perceive the work.',
  },
]

function QuestionsSection({ data, onSave }) {
  const [answers, setAnswers] = useState(data || {})
  const firstUnanswered = QUESTIONS.findIndex(q => !answers[q.key])
  const [activeIdx, setActiveIdx] = useState(firstUnanswered === -1 ? 0 : firstUnanswered)
  const [draft, setDraft] = useState(answers[QUESTIONS[firstUnanswered === -1 ? 0 : firstUnanswered]?.key] || '')
  const [saved, flash] = useSaved()

  const answeredCount = QUESTIONS.filter(q => answers[q.key]).length
  const allAnswered   = answeredCount === QUESTIONS.length
  const currentQ      = QUESTIONS[activeIdx]

  function selectQ(idx) {
    setActiveIdx(idx)
    setDraft(answers[QUESTIONS[idx].key] || '')
  }

  function saveAnswer() {
    if (!draft.trim()) return
    const next = { ...answers, [currentQ.key]: draft.trim() }
    setAnswers(next)
    onSave(next)
    flash()
    const nextUnanswered = QUESTIONS.findIndex((q, i) => i > activeIdx && !next[q.key])
    if (nextUnanswered !== -1) {
      setActiveIdx(nextUnanswered)
      setDraft('')
    }
  }

  function clearAnswer(key) {
    const next = { ...answers, [key]: null }
    setAnswers(next)
    onSave(next)
  }

  function skipQ() {
    const next = QUESTIONS.findIndex((q, i) => i > activeIdx && !answers[q.key])
    if (next !== -1) {
      setActiveIdx(next)
      setDraft(answers[QUESTIONS[next].key] || '')
    }
  }

  const subtitle = allAnswered
    ? 'All eight answered — Saffron has everything she needs.'
    : `${answeredCount} of ${QUESTIONS.length} answered — Saffron uses these to sharpen her analysis.`

  return (
    <Section title="Saffron's Questions" subtitle={subtitle}>
      {/* Progress dots */}
      <div className="pp-q-dots">
        {QUESTIONS.map((q, i) => (
          <button
            key={q.key}
            className={[
              'pp-q-dot',
              answers[q.key] ? 'pp-q-dot--done' : '',
              i === activeIdx ? 'pp-q-dot--active' : '',
            ].join(' ').trim()}
            onClick={() => selectQ(i)}
            title={q.text}
          />
        ))}
        <span className="pp-q-count">{answeredCount} / {QUESTIONS.length}</span>
      </div>

      {/* Active question */}
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
            {saved ? 'Saved ✓' : 'Save answer'}
          </button>
          {!answers[currentQ.key] && (
            <button className="pp-skip" onClick={skipQ}>
              Skip for now
            </button>
          )}
          {answers[currentQ.key] && (
            <button className="pp-skip" onClick={() => clearAnswer(currentQ.key)}>
              Clear answer
            </button>
          )}
        </div>
      </div>

      {/* Answered list */}
      {answeredCount > 0 && (
        <div className="pp-q-done-list">
          <div className="pp-group-label">{answeredCount} answered</div>
          {QUESTIONS.filter(q => answers[q.key]).map((q, i) => (
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
    </Section>
  )
}

// ── Page root ──────────────────────────────────────────────────────────────

export default function PeppercornPage() {
  const [profile, setProfile] = useState(null)
  const [statusMsg, setStatusMsg] = useState('')

  useEffect(() => {
    fetch('/api/peppercorn')
      .then(r => r.json())
      .then(setProfile)
  }, [])

  async function saveSection(updates) {
    const next = { ...profile, ...updates }
    setProfile(next)
    setStatusMsg('Saving…')
    await fetch('/api/peppercorn', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(next),
    })
    setStatusMsg('Saved')
    setTimeout(() => setStatusMsg(''), 2000)
  }

  return (
    <div className="peppercorn-page">
      <section className="peppercorn-hero">
        <img src={peppercornHero} alt="Peppercorn's quiet study" className="peppercorn-hero-img" />
      </section>

      {statusMsg && (
        <div className={`pp-status-bar${statusMsg === 'Saving…' ? '' : ' pp-status-bar--saved'}`}>
          {statusMsg}
        </div>
      )}

      {!profile && <div className="pp-loading">Peppercorn is listening…</div>}

      {profile && (
        <div className="pp-content">
          <PrioritiesSection
            data={profile.priorities}
            onSave={v => saveSection({ priorities: v })}
          />
          <StatementSection
            data={profile.artist_statement}
            onSave={v => saveSection({ artist_statement: v })}
          />
          <GoalsSection
            data={profile.goals}
            onSave={v => saveSection({ goals: v })}
          />
          <PreferencesSection
            data={profile.preferences}
            onSave={v => saveSection({ preferences: v })}
          />
          <QuestionsSection
            data={profile.saffron_answers}
            onSave={v => saveSection({ saffron_answers: v })}
          />
        </div>
      )}
    </div>
  )
}
