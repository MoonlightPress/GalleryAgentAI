// Saffron — the Observatory page. Hero, then ONE synthesis panel, the Journey,
// the Field, the Perch row, then the Field Notes library.
// Built per reports/ux_pass_2026-06/02_REDESIGN_SPEC.md §Page 2.
import { useEffect, useMemo, useState } from 'react'
import { api } from '../../utils/api'
import { useLanguage } from '../../i18n/LanguageContext'
import { useLocalT } from '../../i18n/local'
import { strings } from './strings'
import FieldNotes, { NoteBoundary } from './FieldNotes'
import saffronImg from '../../assets/heroes/saffron/saffron_hero.png'
import './saffron.css'

// ── helpers ─────────────────────────────────────────────────────────────────
function igFollowers(careerPosition) {
  const ig = (careerPosition?.social || []).find(s => /instagram/i.test(s.platform || ''))
  return ig?.followers || '26k'
}

function deadlinesThisMonth(timing, calendar) {
  const now = new Date()
  const byNum = (timing?.monthly_counts || []).find(m => m.month_num === now.getMonth() + 1)
  if (byNum) return byNum.count ?? 0
  const monthName = now.toLocaleDateString('en-US', { month: 'long' })
  const byName = (calendar?.months || []).find(m => m.month === monthName)
  return byName ? (byName.opportunities || []).length : 0
}

// ── 1. Synthesis: "From up here" ────────────────────────────────────────────
function Synthesis({ data, t2 }) {
  const pos = data.career_position || {}
  const ml = data.market_landscape || {}
  const split = ml.tokyo_vs_international || {}
  const ready = (ml.actionability || []).find(a => a.tier === 'high')?.count ?? 0
  const exCount = (pos.exhibitions || []).length
  const pubCount = (pos.publications || []).length
  const monthCount = deadlinesThisMonth(data.timing_intelligence, data.seasonal_calendar)

  return (
    <section>
      <div className="sec-head sec-head--amber">
        <h2 className="h-section">{t2('v2.saffron.synth.title')}</h2>
        <p className="sec-sub voice">{t2('v2.saffron.synth.sub')}</p>
      </div>
      <div className="card sv-synth">
        <div className="sv-synth-prose">
          <div className="sv-beat">
            <div className="sv-beat-label">{t2('v2.saffron.synth.stands.label')}</div>
            <p>{t2('v2.saffron.synth.stands', { ex: exCount, pub: pubCount, ig: igFollowers(pos) })}</p>
          </div>
          {data.pathway?.blocking_now && (
            <div className="sv-beat sv-beat--blocking">
              <div className="sv-beat-label">{t2('v2.saffron.synth.blocking.label')}</div>
              <p>{data.pathway.blocking_now}</p>
            </div>
          )}
          <div className="sv-beat">
            <div className="sv-beat-label">{t2('v2.saffron.synth.field.label')}</div>
            <p>{t2('v2.saffron.synth.field', {
              total: ml.total ?? 0,
              tokyo: split.tokyo ?? 0,
              intl: split.international ?? 0,
              ready,
            })}</p>
          </div>
        </div>
        <div className="sv-synth-nums">
          <div>
            <div className="sv-knum-n">{exCount}</div>
            <div className="sv-knum-label">{t2('v2.saffron.k.shows')}</div>
          </div>
          <div>
            <div className="sv-knum-n">{ready}</div>
            <div className="sv-knum-label">{t2('v2.saffron.k.ready')}</div>
          </div>
          <div>
            <div className="sv-knum-n">{monthCount}</div>
            <div className="sv-knum-label">{t2('v2.saffron.k.month')}</div>
          </div>
        </div>
      </div>
    </section>
  )
}

// ── 2. The Journey: 7 stepping stones ───────────────────────────────────────
function Journey({ pathway, t2 }) {
  const steps = pathway?.steps || []
  const blocking = steps.find(s => s.blocking)
  const [selected, setSelected] = useState(blocking?.n ?? steps[0]?.n ?? null)
  const sel = steps.find(s => s.n === selected)
  if (!steps.length) return null

  return (
    <section>
      <div className="sec-head sec-head--leaf">
        <h2 className="h-section">{t2('v2.saffron.journey.title')}</h2>
        <p className="sec-sub voice">{t2('v2.saffron.journey.sub', { goal: pathway.goal ?? '' })}</p>
      </div>
      <div className="card">
        <div className="sv-journey-detail-head" style={{ marginBottom: '0.2rem' }}>
          <span className="pill pill--count">{pathway.goal}</span>
          {pathway.timeline_estimate && <span className="sfn-row-sub">{pathway.timeline_estimate}</span>}
        </div>
        <div className="sv-journey-path">
          {steps.map(s => (
            <button
              key={s.n}
              className={`sv-stone-btn${selected === s.n ? ' sv-stone-btn--selected' : ''}`}
              onClick={() => setSelected(s.n)}
              aria-pressed={selected === s.n}
            >
              <span className={`sv-stone${s.done ? ' sv-stone--done' : ''}${s.blocking ? ' sv-stone--blocking' : ''}`}>
                {s.done ? '✓' : s.n}
              </span>
              <span className="sv-stone-label">{s.label}</span>
            </button>
          ))}
        </div>
        {sel && (
          <div className="sv-journey-detail">
            <div className="sv-journey-detail-head">
              <span className="tiny" style={{ color: 'var(--gold-deep)', letterSpacing: '0.08em', textTransform: 'uppercase' }}>
                {t2('v2.saffron.journey.step', { n: sel.n })}
              </span>
              <h4 className="h-card">{sel.label}</h4>
            </div>
            <p className="small" style={{ color: 'var(--ink-medium)' }}>{sel.detail}</p>
            {sel.blocking && pathway.blocking_now && (
              <div className="sv-journey-note">
                <div className="sv-beat-label">{t2('v2.saffron.journey.note.label')}</div>
                <p className="small" style={{ color: 'var(--ink-medium)' }}>{pathway.blocking_now}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </section>
  )
}

// ── 3. The Field: warm bars + split + actionability ─────────────────────────
const ACT_DOT = { high: 'high', medium: 'medium', stretch: 'stretch', low: 'low' }

function Field({ ml, t2 }) {
  const cats = ml?.category_breakdown || []
  const maxCount = Math.max(...cats.map(c => c.count), 1)
  const split = ml?.tokyo_vs_international || {}
  const total = (split.tokyo ?? 0) + (split.international ?? 0) || 1
  if (!cats.length && !ml?.actionability?.length) return null

  return (
    <section>
      <div className="sec-head sec-head--amber">
        <h2 className="h-section">{t2('v2.saffron.field.title')}</h2>
        <p className="sec-sub voice">{t2('v2.saffron.field.sub')}</p>
      </div>
      <div className="card sv-field">
        <div>
          <div className="sfn-label">{t2('v2.saffron.field.cats')}</div>
          {cats.map((c, i) => (
            <div key={i} className="sv-bar-row">
              <span className="sv-bar-label">{c.label}</span>
              <div className="sv-bar-track">
                <div className="sv-bar-fill" style={{ width: `${Math.max(Math.round((c.count / maxCount) * 100), 3)}%` }} />
              </div>
              <span className="sv-bar-count">{c.count}</span>
            </div>
          ))}
        </div>
        <div>
          <div className="sfn-label">{t2('v2.saffron.field.split')}</div>
          <div className="sv-split-bar">
            <div className="sv-split-tokyo" style={{ width: `${((split.tokyo ?? 0) / total) * 100}%` }} />
            <div className="sv-split-intl" style={{ width: `${((split.international ?? 0) / total) * 100}%` }} />
          </div>
          <div className="sv-split-legend">
            <span className="tokyo">{t2('v2.saffron.field.tokyo', { n: split.tokyo ?? 0 })}</span>
            <span className="intl">{t2('v2.saffron.field.intl', { n: split.international ?? 0 })}</span>
          </div>
          <div className="sfn-label">{t2('v2.saffron.field.act')}</div>
          <div className="sv-act-pills">
            {(ml?.actionability || []).map((a, i) => (
              <span key={i} className="pill pill--loc">
                <span className={`sv-act-dot sv-act-dot--${ACT_DOT[a.tier] || 'low'}`} style={{ marginRight: '0.35rem' }} />
                {a.label} · {a.count}
              </span>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

// ── 4. Perch row: comparable artists ────────────────────────────────────────
function Perch({ peers, t2 }) {
  if (!peers?.length) return null
  return (
    <section>
      <div className="sec-head sec-head--leaf">
        <h2 className="h-section">{t2('v2.saffron.perch.title')}</h2>
        <p className="sec-sub voice">{t2('v2.saffron.perch.sub')}</p>
      </div>
      <p className="sv-perch-caveat">{t2('v2.saffron.perch.caveat')}</p>
      <div className="sv-perch-grid">
        {peers.slice(0, 4).map((p, i) => (
          <div key={i} className="card">
            <h4 className="h-card sv-peer-name">{p.name}</h4>
            <div className="sv-peer-region">{p.region}</div>
            <p className="sv-peer-fit clamp-2">{p.fit_reason}</p>
            <p className="sv-peer-use">{p.use_as}</p>
          </div>
        ))}
      </div>
    </section>
  )
}

// ── Page root ───────────────────────────────────────────────────────────────
export default function SaffronPage() {
  const { t, lang } = useLanguage()
  const t2 = useLocalT(strings)
  const [data, setData] = useState(null)
  const [careerData, setCareerData] = useState(null)
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    let alive = true
    Promise.allSettled([api.saffron(), api.careerStrategy()]).then(([sf, cs]) => {
      if (!alive) return
      if (sf.status === 'fulfilled') setData(sf.value)
      if (cs.status === 'fulfilled') setCareerData(cs.value)
      setLoaded(true)
    })
    return () => { alive = false }
  }, [])

  const fallback = useMemo(() => t2('v2.saffron.section.failed'), [t2])

  return (
    <main className="page">
      {/* ── Hero band ── */}
      <section className="sv-hero">
        <img src={saffronImg} alt="" />
        <div className="sv-hero-veil">
          <p className="voice">{t2('v2.saffron.hero.line')}</p>
        </div>
      </section>

      {!loaded && <p className="voice" style={{ padding: '2.5rem 0' }}>{t2('v2.saffron.loading')}</p>}

      {loaded && !data && (
        <div className="card card--quiet" style={{ marginTop: '1.6rem' }}>
          <p className="voice">{t2('v2.saffron.error')}</p>
        </div>
      )}

      {data && (
        <>
          <div id="overview"><NoteBoundary fallback={fallback}>
            <Synthesis data={data} t2={t2} />
          </NoteBoundary></div>

          <div id="journey"><NoteBoundary fallback={fallback}>
            <Journey pathway={data.pathway} t2={t2} />
          </NoteBoundary></div>

          <div id="field"><NoteBoundary fallback={fallback}>
            <Field ml={data.market_landscape} t2={t2} />
          </NoteBoundary></div>

          <div id="peers"><NoteBoundary fallback={fallback}>
            <Perch peers={data.peer_artists} t2={t2} />
          </NoteBoundary></div>

          <div id="notes"><NoteBoundary fallback={fallback}>
            <FieldNotes data={data} careerData={careerData} t={t} t2={t2} lang={lang} />
          </NoteBoundary></div>
        </>
      )}
    </main>
  )
}
