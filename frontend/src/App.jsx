import { useState } from 'react'
import './App.css'
import HeroSection from './components/HeroSection'
import Nav from './components/Nav'
import OpportunitiesSection from './components/OpportunitiesSection'
import PeppercornPage from './components/PeppercornPage'
import SaffronPage from './components/SaffronPage'
import StatusBar from './components/StatusBar'

export default function App() {
  const [page, setPage] = useState('discover')

  return (
    <div className="app">
      {page === 'discover' && <HeroSection />}
      <Nav activePage={page} onNav={setPage} />
      {page === 'discover' && <OpportunitiesSection />}
      {page === 'refine'   && <PeppercornPage />}
      {page === 'observe'  && <SaffronPage />}
      <StatusBar />
    </div>
  )
}
