import { useState } from 'react'
import './App.css'
import { LanguageProvider } from './i18n/LanguageContext'
import HeroSection from './components/HeroSection'
import Nav from './components/Nav'
import TodaysFocus from './components/TodaysFocus'
import OpportunitiesSection from './components/OpportunitiesSection'
import PeppercornPage from './components/PeppercornPage'
import SaffronPage from './components/SaffronPage'
import StatusBar from './components/StatusBar'

export default function App() {
  const [page, setPage] = useState('discover')
  const nav = <Nav activePage={page} onNav={setPage} />

  return (
    <LanguageProvider>
      <div className="app">
        {page === 'discover' && <HeroSection />}
        {page === 'discover' && nav}
        {page === 'discover' && <TodaysFocus />}
        {page === 'discover' && <OpportunitiesSection />}
        {page === 'observe'  && <SaffronPage nav={nav} />}
        {page === 'refine'   && <PeppercornPage nav={nav} />}
        <StatusBar />
      </div>
    </LanguageProvider>
  )
}
