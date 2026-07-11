import { useState, useEffect, useRef, lazy, Suspense } from 'react'
import './App.css'
import { LanguageProvider, useLanguage } from './i18n/LanguageContext'
import HeroSection from './components/HeroSection'
import Nav, { QuickNav } from './components/Nav'
import TodaysFocus from './components/TodaysFocus'
import OpportunitiesSection from './components/OpportunitiesSection'
import RelationshipTargets from './components/RelationshipTargets'
import TrackerSection from './components/TrackerSection'
import StatusBar from './components/StatusBar'
import NewOpportunitiesBanner from './components/NewOpportunitiesBanner'
import { markFreshSeen } from './utils/newOpportunities'
import TrackedSection from './components/TrackedSection'
import { track } from './utils/track'
import { createVisibilityTracker } from './utils/dwell'
import { setCache, getCache } from './utils/apiCache'
import { isNightNow } from './utils/timeOfDay'

const SaffronPage = lazy(() => import('./components/SaffronPage'))
const PeppercornPage = lazy(() => import('./components/PeppercornPage'))

function PageFallback({ page }) {
  const { t } = useLanguage()
  // Each companion gets its own loading line: bird's-eye view (Saffron),
  // looking for crumbs (Peppercorn), find something good (Mochi).
  const key = page === 'observe' ? 'sf.loading' : page === 'refine' ? 'loading.peppercorn' : 'opps.loading'
  return (
    <p className="page-loading" style={{ minHeight: '80vh', display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', fontStyle: 'italic', padding: '3rem 1rem', color: 'var(--muted)' }}>
      {t(key)}
    </p>
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

  // Real, client-measured foreground time on the current companion page. The
  // server can only infer dwell from gaps between events, and cannot see how
  // long she was on the LAST page before closing the tab.
  //
  // The bookkeeping lives in utils/dwell.js, which debounces Safari's
  // visibility churn — without that, a 200ms hidden/visible flap read as a
  // whole extra 1-3 second visit, and most of her recorded "sessions" were
  // that artefact rather than her.
  const pageRef = useRef(page)
  const trackerRef = useRef(null)

  useEffect(() => {
    pageRef.current = page
    trackerRef.current?.onPageChange()
  }, [page])

  useEffect(() => {
    const tracker = createVisibilityTracker({
      emit: (event) => {
        track({ ...event, page: pageRef.current })
        if (event.type === 'leave') {
          // Session's ending: mark the "new to her" items seen so they clear
          // next visit (she's had this whole visit to see them). Best-effort.
          markFreshSeen()
        }
      },
    })
    trackerRef.current = tracker

    function onVisibilityChange() {
      if (document.visibilityState === 'hidden') tracker.onHidden()
      else if (document.visibilityState === 'visible') tracker.onVisible()
    }
    function onPageHide() { tracker.onPageHide() }
    document.addEventListener('visibilitychange', onVisibilityChange)
    window.addEventListener('pagehide', onPageHide)
    return () => {
      document.removeEventListener('visibilitychange', onVisibilityChange)
      window.removeEventListener('pagehide', onPageHide)
      trackerRef.current = null
    }
  }, [])

  // Once Discover is up, warm the other companions in the background — both their
  // code chunks AND their data into the shared cache — so switching is instant
  // instead of a blank loading screen (Scott: "load saffron once mochi is done so
  // if she goes there it's already loaded").
  useEffect(() => {
    const warm = () => {
      import('./components/SaffronPage')
      import('./components/PeppercornPage')
      for (const url of ['/api/saffron', '/api/career_strategy', '/api/peppercorn']) {
        if (getCache(url)) continue
        fetch(url).then(r => (r.ok ? r.json() : null)).then(d => { if (d) setCache(url, d) }).catch(() => { /* best-effort warm */ })
      }
    }
    const ric = window.requestIdleCallback
    const id = ric ? ric(warm, { timeout: 2500 }) : setTimeout(warm, 1500)
    return () => { ric ? window.cancelIdleCallback(id) : clearTimeout(id) }
  }, [])

  const nav = <Nav activePage={page} onNav={setPage} />

  return (
    <LanguageProvider>
      {/* Night: `app--night` on every page turns just the navigation blue (shared
          companion nav + each page's sub-nav). Page background and content stay in
          their daytime palette everywhere — the light-touch theme. */}
      <div className={`app${isNightNow() ? ' app--night' : ''}`}>
        {page === 'discover' && <HeroSection />}
        {page === 'discover' && nav}
        {page === 'discover' && <QuickNav />}
        {page === 'discover' && <NewOpportunitiesBanner />}
        {page === 'discover' && <MochiIntro />}
        {page === 'discover' && <TrackedSection section="today_focus"><TodaysFocus /></TrackedSection>}
        {page === 'discover' && <TrackedSection section="open_calls"><OpportunitiesSection /></TrackedSection>}
        {/* People (RelationshipTargets) mounts INSIDE the same padded .opps-root
            container the opportunity cards use, so its .rt-section inherits the
            normal max-width + 28px gutter instead of going edge-to-edge (the
            section's own max-width:1400px never engaged below 1400px). */}
        {page === 'discover' && (
          <TrackedSection section="people">
            <div className="opps-root">
              <RelationshipTargets />
            </div>
          </TrackedSection>
        )}
        {page === 'discover' && <TrackedSection section="tracker"><TrackerSection /></TrackedSection>}
        {page === 'discover' && <AtelierFooter page="discover" />}
        {(page === 'observe' || page === 'refine') && (
          <Suspense fallback={<PageFallback page={page} />}>
            {page === 'observe' && <SaffronPage nav={nav} onNav={setPage} />}
            {page === 'refine'  && <PeppercornPage nav={nav} />}
            {/* Footer lives INSIDE Suspense so it stays hidden until the page
                resolves — no footer floating on the blank fallback mid-switch.
                Suspense/fragments add no DOM node, so the footer is still a direct
                flex child of .app and its margin-top:auto bottom-stick still works. */}
            <AtelierFooter page={page} />
          </Suspense>
        )}
        <StatusBar />
      </div>
    </LanguageProvider>
  )
}
