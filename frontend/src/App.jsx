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
import PaperAccents from './components/PaperAccents'
import NewOpportunitiesBanner from './components/NewOpportunitiesBanner'
import { markFreshSeen } from './utils/newOpportunities'
import TrackedSection from './components/TrackedSection'
import { track } from './utils/track'
import { createVisibilityTracker } from './utils/dwell'
import { setCache, getCache } from './utils/apiCache'
import { isNightNow } from './utils/timeOfDay'
import { prefetchCompanionHeroes } from './utils/heroImages'
import { parseHash, formatHash, sameRoute } from './utils/route'

const PeppercornPage = lazy(() => import('./components/PeppercornPage'))
// The Saffron restructure prototype, reachable only at #observe2 (or /mochi2,
// which nginx redirects here). Lazy like the others so it costs nothing to
// anyone who never opens it.
const SaffronV2 = lazy(() => import('./components/SaffronV2'))

// Scott, 2026-09-10: "i hate that it's fully blank instead of the footer and
// the flowers then it all pops in." Before this, the fallback was a bare
// centered line of italic text — nav, footer and (since neither mounts until
// SaffronV2/PeppercornPage themselves do) even PaperAccents' anchor marker
// were all missing until the lazy chunk resolved, so a slow load really was a
// blank page. nav and the footer are cheap, code-split-free, and the same
// element either way, so rendering them here too means the chrome is already
// in place — and PaperAccents (which anchors to nav's .page-content-start)
// has something to anchor to from the very first paint — and only the middle
// (the part that actually depends on the lazy chunk + her data) pops in later.
function PageFallback({ page, nav }) {
  const { t } = useLanguage()
  // Each companion gets its own loading line: bird's-eye view (Saffron),
  // looking for crumbs (Peppercorn), find something good (Mochi).
  const key = (page === 'observe' || page === 'observe2') ? 'sf.loading'
    : page === 'refine' ? 'loading.peppercorn' : 'opps.loading'
  return (
    <>
      {nav}
      <p className="page-loading" style={{ minHeight: '60vh', display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', fontStyle: 'italic', padding: '3rem 1rem', color: 'var(--muted)' }}>
        {t(key)}
      </p>
      <AtelierFooter page={page} />
    </>
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
  // The URL is the source of truth for which companion is showing, so a link
  // can point at Saffron (#observe) or one of her tabs (#observe/calendar),
  // refresh keeps her place, and back/forward walk the companions she visited.
  // No hash = discover, exactly as before; an unknown hash falls back to it too.
  const [route, setRoute] = useState(() => parseHash(window.location.hash))
  const { page } = route

  // The browser owns the state: every navigation writes the hash, and we only
  // ever read it back out here. One path in, so a click and a back button do
  // precisely the same thing.
  useEffect(() => {
    const onHashChange = () => {
      setRoute(prev => {
        const next = parseHash(window.location.hash)
        return sameRoute(prev, next) ? prev : next
      })
    }
    window.addEventListener('hashchange', onHashChange)
    // A hash can change between first render and this effect attaching.
    onHashChange()
    return () => window.removeEventListener('hashchange', onHashChange)
  }, [])

  const navigate = (nextPage, nextTab = null) => {
    const next = parseHash(formatHash(nextPage, nextTab))
    if (sameRoute(route, next)) return
    // Assigning the hash pushes a history entry, which is what makes back work.
    window.location.hash = formatHash(nextPage, nextTab)
  }
  const setPage = (nextPage) => navigate(nextPage)

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

  // Once Discover is up, warm the other companions in the background — their code
  // chunks, their data into the shared cache, AND their hero art — so switching is
  // instant instead of a blank loading screen (Scott: "load saffron once mochi is
  // done so if she goes there it's already loaded").
  //
  // The hero art was the piece this effect used to miss: chunk and data arrived
  // early, then the page still sat there fetching a cold ~300 KB painting, which
  // is what "3 seconds even when switching sections" actually was.
  useEffect(() => {
    const warm = () => {
      import('./components/SaffronV2')
      import('./components/PeppercornPage')
      prefetchCompanionHeroes(isNightNow())
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
        {/* Paper texture + botanical accents: site-wide (all three companion
            pages), not Saffron-only — rendered once here so it doesn't need
            reimplementing per page. Positions itself against .app and whichever
            .page-content-start marker the active page provides. */}
        <PaperAccents page={page} />
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
        {(page === 'observe' || page === 'observe2' || page === 'refine') && (
          <Suspense fallback={<PageFallback page={page} nav={nav} />}>
            {/* SaffronV2 (the #observe2 restructure prototype) is now the main
                Saffron page too (Scott, 2026-09-09) — both hashes render it so
                existing #observe/#observe2 links keep working. The old 5-tab
                SaffronPage default export is no longer rendered here, but its
                module still stays imported (SaffronV2 pulls its named exports
                from it — see the top-of-file comment there), so nothing there
                needs deleting. */}
            {(page === 'observe' || page === 'observe2') && <SaffronV2 nav={nav} />}
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
