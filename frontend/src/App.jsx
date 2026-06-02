import './App.css'
import HeroSection from './components/HeroSection'
import Nav from './components/Nav'
import OpportunitiesSection from './components/OpportunitiesSection'
import StatusBar from './components/StatusBar'

export default function App() {
  return (
    <div className="app">
      <HeroSection />
      <Nav />
      <OpportunitiesSection />
      <StatusBar />
    </div>
  )
}
