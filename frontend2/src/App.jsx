import { LanguageProvider } from './i18n/LanguageContext'
import { useHashRoute } from './router'
import CompanionBand from './components/CompanionBand'
import StatusStrip from './components/StatusStrip'
import MochiPage from './pages/mochi/MochiPage'
import SaffronPage from './pages/saffron/SaffronPage'
import PeppercornPage from './pages/peppercorn/PeppercornPage'

const PAGES = {
  mochi:      MochiPage,
  saffron:    SaffronPage,
  peppercorn: PeppercornPage,
}

export default function App() {
  const [page, navigate] = useHashRoute()
  const Page = PAGES[page] || MochiPage

  return (
    <LanguageProvider>
      <div className="app-shell">
        <CompanionBand activePage={page} onNav={navigate} />
        <Page />
        <StatusStrip />
      </div>
    </LanguageProvider>
  )
}
