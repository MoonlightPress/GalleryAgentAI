// WHAT PEPPERCORN KNOWS — statement + goals (two columns), preferences below.
// Data contracts identical to v1 (POST /api/peppercorn via parent saveSection).
import { useState, useEffect } from 'react'
import { useLanguage } from '../../i18n/LanguageContext'
import { useLocalT } from '../../i18n/local'
import { strings } from './strings'
import { useSaved } from './bits'

// ── Artist statement ───────────────────────────────────────────────────────

function StatementExample() {
  const [show, setShow] = useState(false)
  const { t } = useLanguage()
  return (
    <div className="pep-stmt-example">
      <button className="btn-ghost pep-example-toggle" onClick={() => setShow(s => !s)}>
        {show ? t('pp.exToggle.hide') : t('pp.exToggle.show')}
      </button>
      {show && (
        <div className="pep-example-body">
          <div className="pep-example-col">
            <div className="tiny pep-block-label">{t('pp.ex.generic')}</div>
            <p className="small pep-example-text pep-example-text--generic">{t('pp.ex.generic.text')}</p>
          </div>
          <div className="pep-example-vs" aria-hidden="true">→</div>
          <div className="pep-example-col">
            <div className="tiny pep-block-label">{t('pp.ex.specific')}</div>
            <p className="small pep-example-text pep-example-text--specific">{t('pp.ex.specific.text')}</p>
          </div>
        </div>
      )}
    </div>
  )
}

function StatementCard({ data, onSave }) {
  const { t } = useLanguage()
  const [text, setText] = useState(data || '')
  const [saved, flash] = useSaved()
  useEffect(() => { setText(data || '') }, [data])

  return (
    <div className="card pep-knows-card">
      <h3 className="h-card">{t('pp.sec.statement')}</h3>
      <p className="small pep-note">{t('pp.stmt.note')}</p>
      <StatementExample />
      <textarea
        className="pep-input pep-statement"
        value={text}
        onChange={e => setText(e.target.value)}
        placeholder={t('pp.stmt.placeholder')}
        rows={7}
      />
      <div className="pep-q-actions">
        <button className="btn-warm" onClick={() => { onSave(text); flash() }}>
          {saved ? t('pp.saved.done') : t('pp.save')}
        </button>
      </div>
    </div>
  )
}

// ── Career goals ───────────────────────────────────────────────────────────

const GOAL_PLACEHOLDER_KEYS = ['pp.goal.ph.0', 'pp.goal.ph.1', 'pp.goal.ph.2', 'pp.goal.ph.3', 'pp.goal.ph.4']

function GoalsCard({ data, onSave }) {
  const { t } = useLanguage()
  const [goals, setGoals] = useState(data || [])
  const [input, setInput] = useState('')
  const [phIdx] = useState(() => Math.floor(Math.random() * GOAL_PLACEHOLDER_KEYS.length))
  useEffect(() => { setGoals(data || []) }, [data])

  function addGoal() {
    const trimmed = input.trim()
    if (!trimmed) return
    const next = [...goals, { id: Date.now(), text: trimmed, done: false }]
    setGoals(next); setInput('')
    onSave(next)
  }
  function removeGoal(id) { const n = goals.filter(g => g.id !== id); setGoals(n); onSave(n) }
  function toggleDone(id) {
    const n = goals.map(g => (g.id === id ? { ...g, done: !g.done } : g))
    setGoals(n); onSave(n)
  }

  const active = goals.filter(g => !g.done)
  const done   = goals.filter(g => g.done)

  return (
    <div className="card pep-knows-card">
      <h3 className="h-card">{t('pp.sec.goals')}</h3>
      {goals.length === 0 && <p className="small pep-note">{t('pp.goals.empty')}</p>}

      {active.length > 0 && (
        <ul className="pep-goal-list">
          {active.map(g => (
            <li key={g.id} className="pep-goal-row">
              <button className="pep-goal-toggle" onClick={() => toggleDone(g.id)} title={t('pp.goal.markDone')}>○</button>
              <span className="pep-goal-text">{g.text}</span>
              <button className="pep-goal-remove" onClick={() => removeGoal(g.id)} title={t('pp.goal.remove')}>×</button>
            </li>
          ))}
        </ul>
      )}

      <div className="pep-goal-add">
        <input
          className="pep-input"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && addGoal()}
          placeholder={t(GOAL_PLACEHOLDER_KEYS[phIdx]) + '…'}
        />
        <button className="btn-quiet" onClick={addGoal}>{t('pp.add')}</button>
      </div>

      {goals.length === 1 && <p className="small voice pep-note">{t('pp.goals.firstNote')}</p>}

      {done.length > 0 && (
        <ul className="pep-goal-list pep-goal-list--done">
          {done.map(g => (
            <li key={g.id} className="pep-goal-row pep-goal-row--done">
              <button className="pep-goal-toggle pep-goal-toggle--done" onClick={() => toggleDone(g.id)} title={t('pp.goal.reopen')}>✓</button>
              <span className="pep-goal-text">{g.text}</span>
              <button className="pep-goal-remove" onClick={() => removeGoal(g.id)} title={t('pp.goal.remove')}>×</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

// ── Preferences (tighter layout, one Save, same contract as v1) ────────────

const TIER_NS     = [1, 2, 3, 4]
const TRACK_IDS   = ['publication', 'gallery', 'hybrid']
const AVOID_IDS   = ['photography_calls', 'high_fees', 'international_travel', 'digital_only', 'large_group']
const GEO_IDS     = ['tokyo', 'japan', 'beijing', 'international']
const FEE_IDS     = ['free', 'low', 'medium', 'any']
const SURFACE_IDS = ['zines_books', 'gallery_shows', 'residencies', 'cafes_bookshops', 'art_fairs']

function PreferencesCard({ data, onSave }) {
  const { t } = useLanguage()
  const pri  = (data || {}).priorities  || {}
  const pref = (data || {}).preferences || {}

  const [tiers, setTiers] = useState(pri.active_tiers  || [1, 2])
  const [track, setTrack] = useState(pri.primary_track || 'hybrid')
  const [avoid, setAvoid] = useState(pri.avoid         || [])
  const [geo,   setGeo]   = useState(pref.geo_focus    || ['tokyo', 'international'])
  const [fee,   setFee]   = useState(pref.fee_tolerance|| 'low')
  const [more,  setMore]  = useState(pref.surface_more || ['zines_books'])
  const [less,  setLess]  = useState(pref.surface_less || [])
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

  const toggleTier  = n  => setTiers(ts => (ts.includes(n) ? ts.filter(x => x !== n) : [...ts, n].sort()))
  const toggleAvoid = id => setAvoid(av => (av.includes(id) ? av.filter(a => a !== id) : [...av, id]))
  const toggleGeo   = id => setGeo(gs => (gs.includes(id) ? gs.filter(g => g !== id) : [...gs, id]))
  const toggleMore  = id => { setMore(ms => (ms.includes(id) ? ms.filter(m => m !== id) : [...ms, id])); setLess(ls => ls.filter(l => l !== id)) }
  const toggleLess  = id => { setLess(ls => (ls.includes(id) ? ls.filter(l => l !== id) : [...ls, id])); setMore(ms => ms.filter(m => m !== id)) }

  function handleSave() {
    onSave({
      priorities:  { active_tiers: tiers, primary_track: track, avoid },
      preferences: { geo_focus: geo, fee_tolerance: fee, surface_more: more, surface_less: less },
    })
    flash()
  }

  return (
    <div className="card pep-prefs-card">
      <h3 className="h-card">{t('pp.sec.preferences')}</h3>
      <p className="small pep-note">{t('pp.prefs.note')}</p>

      <div className="pep-prefs-grid">
        <div className="pep-group">
          <div className="tiny pep-block-label">{t('pp.group.activeTiers')}</div>
          <p className="small pep-hint">{t('pp.group.tiersHint')}</p>
          {TIER_NS.map(n => (
            <label key={n} className="pep-check-row">
              <input type="checkbox" checked={tiers.includes(n)} onChange={() => toggleTier(n)} />
              <span className="pep-check-label">
                <strong>{t(`pp.tier.${n}.label`)}</strong>
                <span className="small pep-check-desc">{t(`pp.tier.${n}.desc`)}</span>
              </span>
            </label>
          ))}
        </div>

        <div className="pep-group">
          <div className="tiny pep-block-label">{t('pp.group.primaryTrack')}</div>
          {TRACK_IDS.map(id => (
            <label key={id} className="pep-check-row">
              <input type="radio" name="pep-track" value={id} checked={track === id} onChange={() => setTrack(id)} />
              <span className="pep-check-label">
                <strong>{t(`pp.track.${id}.label`)}</strong>
                <span className="small pep-check-desc">{t(`pp.track.${id}.desc`)}</span>
              </span>
            </label>
          ))}

          <div className="tiny pep-block-label pep-block-label--gap">{t('pp.group.feeTolerance')}</div>
          {FEE_IDS.map(id => (
            <label key={id} className="pep-check-row">
              <input type="radio" name="pep-fee" value={id} checked={fee === id} onChange={() => setFee(id)} />
              <span className="pep-check-label">{t(`pp.fee.${id}`)}</span>
            </label>
          ))}
        </div>

        <div className="pep-group">
          <div className="tiny pep-block-label">{t('pp.group.avoid')}</div>
          {AVOID_IDS.map(id => (
            <label key={id} className="pep-check-row">
              <input type="checkbox" checked={avoid.includes(id)} onChange={() => toggleAvoid(id)} />
              <span className="pep-check-label">{t(`pp.avoid.${id}`)}</span>
            </label>
          ))}

          <div className="tiny pep-block-label pep-block-label--gap">{t('pp.group.geoFocus')}</div>
          {GEO_IDS.map(id => (
            <label key={id} className="pep-check-row">
              <input type="checkbox" checked={geo.includes(id)} onChange={() => toggleGeo(id)} />
              <span className="pep-check-label">
                <strong>{t(`pp.geo.${id}.label`)}</strong>
                {t(`pp.geo.${id}.desc`) !== `pp.geo.${id}.desc` && (
                  <span className="small pep-check-desc">{t(`pp.geo.${id}.desc`)}</span>
                )}
              </span>
            </label>
          ))}
        </div>

        <div className="pep-group">
          <div className="tiny pep-block-label">{t('pp.group.catWeighting')}</div>
          <p className="small pep-hint">{t('pp.group.catHint')}</p>
          <div className="pep-surface-grid">
            <span />
            <span className="tiny pep-surface-col">{t('pp.group.more')}</span>
            <span className="tiny pep-surface-col">{t('pp.group.less')}</span>
            {SURFACE_IDS.map(id => (
              <SurfaceRow
                key={id}
                label={t(`pp.surface.${id}`)}
                more={more.includes(id)}
                less={less.includes(id)}
                onMore={() => toggleMore(id)}
                onLess={() => toggleLess(id)}
              />
            ))}
          </div>
        </div>
      </div>

      <div className="pep-q-actions">
        <button className="btn-warm" onClick={handleSave}>
          {saved ? t('pp.saved.done') : t('pp.save')}
        </button>
      </div>
    </div>
  )
}

function SurfaceRow({ label, more, less, onMore, onLess }) {
  return (
    <>
      <span className="small pep-surface-name">{label}</span>
      <input type="checkbox" checked={more} onChange={onMore} />
      <input type="checkbox" checked={less} onChange={onLess} />
    </>
  )
}

// ── Section root ───────────────────────────────────────────────────────────

export default function Knows({ profile, onSaveStatement, onSaveGoals, onSavePrefs }) {
  const t2 = useLocalT(strings)
  return (
    <section className="pep-knows" aria-label={t2('v2.peppercorn.knows.title')}>
      <div className="sec-head sec-head--leaf">
        <h2 className="h-section">{t2('v2.peppercorn.knows.title')}</h2>
        <p className="sec-sub">{t2('v2.peppercorn.knows.sub')}</p>
      </div>

      <div className="grid-2 pep-knows-grid">
        <StatementCard data={profile?.artist_statement} onSave={onSaveStatement} />
        <GoalsCard data={profile?.goals} onSave={onSaveGoals} />
      </div>

      <PreferencesCard
        data={{ priorities: profile?.priorities, preferences: profile?.preferences }}
        onSave={onSavePrefs}
      />
    </section>
  )
}
