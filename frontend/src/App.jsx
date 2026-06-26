import { useState, useEffect, useRef, lazy, Suspense } from 'react'
import './App.css'
import { LanguageProvider, useLanguage } from './i18n/LanguageContext'
import HeroSection from './components/HeroSection'
import Nav, { QuickNav } from './components/Nav'
import TodaysFocus from './components/TodaysFocus'
import OpportunitiesSection from './components/OpportunitiesSection'
import DeadlineCalendar from './components/DeadlineCalendar'
import RelationshipTargets from './components/RelationshipTargets'
import TrackerSection from './components/TrackerSection'
import StatusBar from './components/StatusBar'
import TrackedSection from './components/TrackedSection'
import { track } from './utils/track'

const SaffronPage = lazy(() => import('./components/SaffronPage'))
const PeppercornPage = lazy(() => import('./components/PeppercornPage'))

function PageFallback({ page }) {
  const { t } = useLanguage()
  // Each companion gets its own loading line: bird's-eye view (Saffron),
  // looking for crumbs (Peppercorn), find something good (Mochi).
  const key = page === 'observe' ? 'sf.loading' : page === 'refine' ? 'loading.peppercorn' : 'opps.loading'
  return (
    <p className="page-loading" style={{ textAlign: 'center', fontStyle: 'italic', padding: '3rem 1rem', color: 'var(--muted)' }}>
      {t(key)}
    </p>
  )
}

function ViewToggle({ view, setView }) {
  const { t } = useLanguage()
  return (
    <div className={`view-toggle${view === 'calendar' ? ' view-toggle--sticky' : ''}`}>
      <button
        className={`view-toggle-btn${view === 'cards' ? ' active' : ''}`}
        onClick={() => setView('cards')}
      >
        {t('view.cards')}
      </button>
      <button
        className={`view-toggle-btn${view === 'calendar' ? ' active' : ''}`}
        onClick={() => setView('calendar')}
      >
        📅 {t('view.calendar')}
      </button>
    </div>
  )
}

function MochiIntro() {
  const { t } = useLanguage()
  const [dismissed, setDismissed] = useState(() => {
    try { return localStorage.getItem('mochi_intro_dismissed') === '1' } catch { return false }
  })
  if (dismissed) return null
  function close() {
    setDismissed(true)
    try { localStorage.setItem('mochi_intro_dismissed', '1') } catch { /* localStorage unavailable */ }
  }
  return (
    <div className="companion-intro">
      <button className="companion-intro-close" onClick={close} title={t('intro.dismiss')}>×</button>
      <p className="companion-intro-text">{t('mochi.intro.body')}</p>
    </div>
  )
}

// A watercolor band that closes every page with breathing room — and carries a
// per-companion painting (cat = Mochi / bird = Saffron / mouse = Peppercorn), all
// in the same atelier-shelf style so the set stays cohesive. No links, nothing
// about the maker. The CSS wash shows until the painting loads (or if it 404s).
const FOOTER_IMG = {
  discover: '/mochi/footer/footer_mochi.webp',      // Mochi — the cat
  observe:  '/mochi/footer/footer_saffron.webp',    // Saffron — the bird
  refine:   '/mochi/footer/footer_peppercorn.webp', // Peppercorn — the mouse
}
function AtelierFooter({ page }) {
  const src = FOOTER_IMG[page]
  return (
    <footer className="atelier-footer" aria-hidden="true">
      {src && (
        <img
          className="atelier-footer-img"
          src={src}
          alt=""
          onError={(e) => { e.currentTarget.style.display = 'none' }}
        />
      )}
    </footer>
  )
}

export default function App() {
  const [page, setPage] = useState('discover')
  const [view, setView] = useState('cards')

  // UX-research beacon: report the opening page and each page change so they
  // show up live in Discord. Best-effort; never blocks or breaks the UI.
  const prevPage = useRef(null)
  useEffect(() => {
    const from = prevPage.current
    prevPage.current = page
    // Open = first mount; subsequent changes = companion-page navigation. The
    // anonymous visitor_id is attached inside track(). Best-effort; never blocks.
    track(from === null ? { type: 'open', page } : { type: 'nav', page, from })
  }, [page])

  const nav = <Nav activePage={page} onNav={setPage} />

  return (
    <LanguageProvider>
      <div className="app">
        {page === 'discover' && <HeroSection />}
        {page === 'discover' && nav}
        {page === 'discover' && view === 'cards' && <QuickNav />}
        {page === 'discover' && <MochiIntro />}
        {page === 'discover' && <TrackedSection section="today_focus"><TodaysFocus /></TrackedSection>}
        {page === 'discover' && <ViewToggle view={view} setView={setView} />}
        {page === 'discover' && view === 'cards'    && <TrackedSection section="open_calls"><OpportunitiesSection /></TrackedSection>}
        {/* People (RelationshipTargets) mounts INSIDE the same padded .opps-root
            container the opportunity cards use, so its .rt-section inherits the
            normal max-width + 28px gutter instead of going edge-to-edge (the
            section's own max-width:1400px never engaged below 1400px). */}
        {page === 'discover' && view === 'cards'    && (
          <TrackedSection section="people">
            <div className="opps-root">
              <RelationshipTargets />
            </div>
          </TrackedSection>
        )}
        {page === 'discover' && view === 'cards'    && <TrackedSection section="tracker"><TrackerSection /></TrackedSection>}
        {page === 'discover' && view === 'calendar' && <DeadlineCalendar />}
        {(page === 'observe' || page === 'refine') && (
          <Suspense fallback={<PageFallback page={page} />}>
            {page === 'observe' && <SaffronPage nav={nav} onNav={setPage} />}
            {page === 'refine'  && <PeppercornPage nav={nav} />}
          </Suspense>
        )}
        <AtelierFooter page={page} />
        <StatusBar />
      </div>
    </LanguageProvider>
  )
}
