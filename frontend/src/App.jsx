import { useState, lazy, Suspense } from 'react'
import './App.css'
import { LanguageProvider, useLanguage } from './i18n/LanguageContext'
import HeroSection from './components/HeroSection'
import Nav from './components/Nav'
import TodaysFocus from './components/TodaysFocus'
import OpportunitiesSection from './components/OpportunitiesSection'
import DeadlineCalendar from './components/DeadlineCalendar'
import RelationshipTargets from './components/RelationshipTargets'
import StatusBar from './components/StatusBar'

const SaffronPage = lazy(() => import('./components/SaffronPage'))
const PeppercornPage = lazy(() => import('./components/PeppercornPage'))

function PageFallback() {
  const { t } = useLanguage()
  return (
    <p className="page-loading" style={{ textAlign: 'center', fontStyle: 'italic', padding: '3rem 1rem', color: 'var(--muted)' }}>
      {t('opps.loading')}
    </p>
  )
}

function ViewToggle({ view, setView }) {
  const { t } = useLanguage()
  return (
    <div className="view-toggle">
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

export default function App() {
  const [page, setPage] = useState('discover')
  const [view, setView] = useState('cards')

  const nav = <Nav activePage={page} onNav={setPage} />

  return (
    <LanguageProvider>
      <div className="app">
        {page === 'discover' && <HeroSection />}
        {page === 'discover' && nav}
        {page === 'discover' && <MochiIntro />}
        {page === 'discover' && <TodaysFocus />}
        {page === 'discover' && <ViewToggle view={view} setView={setView} />}
        {page === 'discover' && view === 'cards'    && <OpportunitiesSection />}
        {page === 'discover' && view === 'cards'    && <RelationshipTargets />}
        {page === 'discover' && view === 'calendar' && <DeadlineCalendar />}
        {(page === 'observe' || page === 'refine') && (
          <Suspense fallback={<PageFallback />}>
            {page === 'observe' && <SaffronPage nav={nav} />}
            {page === 'refine'  && <PeppercornPage nav={nav} />}
          </Suspense>
        )}
        <StatusBar />
      </div>
    </LanguageProvider>
  )
}
