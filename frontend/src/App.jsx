import './App.css'
import HeroSection from './components/HeroSection'
import SectionCards from './components/SectionCards'
import OpportunitiesSection from './components/OpportunitiesSection'
import StatusBar from './components/StatusBar'

export default function App() {
  return (
    <div className="app">
      <HeroSection />
      <SectionCards />
      <OpportunitiesSection />
      <StatusBar />
    </div>
  )
}
