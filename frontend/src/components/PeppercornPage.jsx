import './PeppercornPage.css'
import { peppercornHero } from '../utils/heroImages'

export default function PeppercornPage() {
  return (
    <div className="peppercorn-page">
      <section className="peppercorn-hero">
        <img
          src={peppercornHero}
          alt="Peppercorn's quiet study"
          className="peppercorn-hero-img"
        />
      </section>
    </div>
  )
}
