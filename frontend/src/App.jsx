import { useState } from 'react'
import './App.css'
import { LanguageProvider, useLanguage } from './i18n/LanguageContext'
import HeroSection from './components/HeroSection'
import Nav from './components/Nav'
import TodaysFocus from './components/TodaysFocus'
import OpportunitiesSection from './components/OpportunitiesSection'
import DeadlineCalendar from './components/DeadlineCalendar'
import PeppercornPage from './components/PeppercornPage'
import SaffronPage from './components/SaffronPage'
import StatusBar from './components/StatusBar'

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

export default function App() {
  const [page, setPage] = useState('discover')
  const [view, setView] = useState('cards')

  const nav = <Nav activePage={page} onNav={setPage} />

  return (
    <LanguageProvider>
      <div className="app">
        {page === 'discover' && <HeroSection />}
        {page === 'discover' && nav}
        {page === 'discover' && <TodaysFocus />}
        {page === 'discover' && <ViewToggle view={view} setView={setView} />}
        {page === 'discover' && view === 'cards'    && <OpportunitiesSection />}
        {page === 'discover' && view === 'calendar' && <DeadlineCalendar />}
        {page === 'observe'  && <SaffronPage nav={nav} />}
        {page === 'refine'   && <PeppercornPage nav={nav} />}
        <StatusBar />
      </div>
    </LanguageProvider>
  )
}
