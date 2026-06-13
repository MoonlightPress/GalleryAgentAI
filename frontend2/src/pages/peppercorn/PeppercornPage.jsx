// PEPPERCORN — the Reflection page. Built per
// reports/ux_pass_2026-06/02_REDESIGN_SPEC.md §Page 3.
// Order: hero → The Wondering → dismissal insight → What Peppercorn Knows →
// The Record Book → Milestones. Save contract identical to v1:
// POST /api/peppercorn with the full merged profile.
import { Component, useEffect, useRef, useState } from 'react'
import { api } from '../../utils/api'
import { useLanguage } from '../../i18n/LanguageContext'
import { useLocalT } from '../../i18n/local'
import { strings } from './strings'
import Wondering, { QUESTION_KEYS } from './Wondering'
import Knows from './Knows'
import RecordBook from './RecordBook'
import peppercornImg from '../../assets/heroes/peppercorn/peppercorn_hero.png'
import './peppercorn.css'

// ── Small error boundary — one bad shape must not blank the page ───────────

class PepBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { broken: false }
  }
  static getDerivedStateFromError() { return { broken: true } }
  componentDidCatch(err) { console.warn('[peppercorn] section failed:', this.props.name, err) }
  render() {
    if (this.state.broken) {
      return (
        <div className="card card--quiet pep-section-error">
          <p className="voice small">{this.props.fallback}</p>
        </div>
      )
    }
    return this.props.children
  }
}

// ── Dismissal insight banner (simplified port of v1, 3+ threshold) ─────────

function DismissalInsightBanner() {
  const { t } = useLanguage()
  const [insights, setInsights] = useState(null)
  const [hidden, setHidden] = useState(false)

  useEffect(() => {
    api.feedbackInsights().then(setInsights).catch(() => {})
  }, [])

  if (!insights || hidden) return null
  const entries = Object.entries(insights.dismissals || {}).filter(([, n]) => n >= 3)
  if (entries.length === 0) return null

  const [topCategory, topCount] = entries.sort((a, b) => b[1] - a[1])[0]
  const catKey = `cat.${topCategory}`
  const categoryLabel = t(catKey) !== catKey
    ? t(catKey)
    : topCategory.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())

  async function suppress() {
    try { await api.suppressCategory(topCategory) } catch { /* quiet */ }
    setHidden(true)
  }

  return (
    <div className="pep-insight" role="status">
      <span className="pep-insight-mark" aria-hidden="true">·</span>
      <p className="small pep-insight-text">{t('pp.dismissal.text', { n: topCount, cat: categoryLabel })}</p>
      <div className="pep-insight-actions">
        <button className="btn-quiet pep-mini-btn" onClick={suppress}>{t('pp.dismissal.confirm')}</button>
        <button className="btn-ghost pep-mini-btn" onClick={() => setHidden(true)}>{t('pp.dismissal.skip')}</button>
      </div>
    </div>
  )
}

// ── Milestones — one quiet strip of honest counts. No rings. ────────────────

function Milestones({ profile }) {
  const t2 = useLocalT(strings)
  const lc = profile?.live_counts || {}

  const shows  = lc.group_shows ?? 1
  const showsT = lc.group_shows_target ?? 3
  const pubs   = lc.publications ?? 2
  const pubsT  = lc.publications_target ?? 3
  const ig     = lc.instagram_followers || '26k'
  const igGoal = `${Math.round((lc.instagram_target || 50000) / 1000)}k`
  const hasStmt  = (profile?.artist_statement || '').length > 30
  const answered = QUESTION_KEYS.filter(k => profile?.saffron_answers?.[k]).length

  const items = [
    { id: 'shows', count: t2('v2.peppercorn.ms.of', { a: shows, b: showsT }) },
    { id: 'pubs',  count: t2('v2.peppercorn.ms.of', { a: pubs, b: pubsT }) },
    { id: 'ig',    count: `${ig} → ${igGoal}` },
    { id: 'stmt',  count: hasStmt ? t2('v2.peppercorn.ms.stmt.draft') : t2('v2.peppercorn.ms.stmt.none') },
    { id: 'qs',    count: t2('v2.peppercorn.ms.of', { a: answered, b: QUESTION_KEYS.length }) },
  ]

  return (
    <section className="pep-milestones" aria-label={t2('v2.peppercorn.milestones.title')}>
      <div className="sec-head sec-head--rose">
        <h2 className="h-section">{t2('v2.peppercorn.milestones.title')}</h2>
        <p className="sec-sub">{t2('v2.peppercorn.milestones.sub')}</p>
      </div>
      <div className="card pep-ms-strip">
        {items.map(it => (
          <div key={it.id} className="pep-ms-item">
            <div className="tiny pep-ms-label">{t2(`v2.peppercorn.ms.${it.id}.label`)}</div>
            <div className="pep-ms-count">{it.count}</div>
            <p className="small pep-ms-meaning">{t2(`v2.peppercorn.ms.${it.id}.meaning`)}</p>
          </div>
        ))}
      </div>
    </section>
  )
}

// ── Page root ───────────────────────────────────────────────────────────────

export default function PeppercornPage() {
  const { t } = useLanguage()
  const t2 = useLocalT(strings)
  const [profile, setProfile] = useState(null)
  const [fetchError, setFetchError] = useState(false)
  const [toast, setToast] = useState(null)
  const toastTimer = useRef(null)

  useEffect(() => {
    let alive = true
    api.peppercorn()
      .then(p => { if (alive) setProfile(p) })
      .catch(() => { if (alive) setFetchError(true) })
    return () => { alive = false }
  }, [])

  useEffect(() => () => clearTimeout(toastTimer.current), [])

  function showToast(msg) {
    clearTimeout(toastTimer.current)
    setToast(msg)
    toastTimer.current = setTimeout(() => setToast(null), 2400)
  }

  // v1 save contract: optimistic local merge, POST the whole profile.
  async function saveSection(updates) {
    const next = { ...profile, ...updates }
    setProfile(next)
    try {
      await api.savePeppercorn(next)
      showToast(t('pp.saved'))
    } catch {
      showToast(t('pp.saveError'))
    }
  }

  const sectionErr = t2('v2.peppercorn.section.error')

  return (
    <main className="page pep-page">
      {/* ── Hero band ── */}
      <section className="pep-hero">
        <img className="pep-hero-img" src={peppercornImg} alt={t2('v2.peppercorn.hero.alt')} />
        <div className="pep-hero-veil" />
        <div className="pep-hero-text">
          <h1 className="display">Peppercorn</h1>
          <p className="voice pep-hero-voice">{t2('v2.peppercorn.hero.voice')}</p>
        </div>
      </section>

      {fetchError && (
        <div className="card card--quiet pep-section-error">
          <p className="voice">{t('pp.loadError')}</p>
        </div>
      )}

      {!profile && !fetchError && (
        <p className="voice pep-loading">{t2('v2.peppercorn.loading')}</p>
      )}

      {profile && (
        <>
          {/* 1 · The Wondering — the page's opening move */}
          <div id="wondering"><PepBoundary name="wondering" fallback={sectionErr}>
            <Wondering
              data={profile.saffron_answers}
              onSave={v => saveSection({ saffron_answers: v })}
            />
          </PepBoundary></div>

          {/* 2 · Dismissal insight — only when a category has 3+ dismissals */}
          <PepBoundary name="insight" fallback={sectionErr}>
            <DismissalInsightBanner />
          </PepBoundary>

          {/* 3 · What Peppercorn Knows */}
          <div id="knows"><PepBoundary name="knows" fallback={sectionErr}>
            <Knows
              profile={profile}
              onSaveStatement={v => saveSection({ artist_statement: v })}
              onSaveGoals={v => saveSection({ goals: v })}
              onSavePrefs={v => saveSection(v)}
            />
          </PepBoundary></div>

          {/* 4 · The Record Book */}
          <div id="record"><PepBoundary name="recordbook" fallback={sectionErr}>
            <RecordBook />
          </PepBoundary></div>

          {/* 5 · Milestones — honest counts, nothing rounded up */}
          <div id="milestones"><PepBoundary name="milestones" fallback={sectionErr}>
            <Milestones profile={profile} />
          </PepBoundary></div>
        </>
      )}

      {toast && <div className="toast">{toast}</div>}
    </main>
  )
}
