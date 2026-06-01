import './App.css'
import HeroSection from './components/HeroSection'
import SectionCards from './components/SectionCards'
import StatusBar from './components/StatusBar'

export default function App() {
  return (
    <div className="app">
      <HeroSection />
      <SectionCards />
      <StatusBar />
    </div>
  )
}
