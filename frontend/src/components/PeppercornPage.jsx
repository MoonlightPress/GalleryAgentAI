import './PeppercornPage.css'
import peppercornHero from '../assets/peppercorn_hero.png'

export default function PeppercornPage() {
  return (
    <div className="peppercorn-page">
      <section className="peppercorn-hero">
        <img
          src={peppercornHero}
          alt="Peppercorn's quiet study"
          className="peppercorn-hero-img"
        />
        <div className="peppercorn-hero-overlay">
          <div className="peppercorn-greeting">
            <div className="peppercorn-greeting-main">Refine</div>
            <div className="peppercorn-greeting-sub">Peppercorn, the mouse</div>
          </div>
          <div className="peppercorn-card">
            <div className="peppercorn-card-title">Your Voice</div>
            <ul className="peppercorn-card-list">
              <li>Artist statement &amp; career goals</li>
              <li>Recommendation feedback ("more like this / not this")</li>
              <li>Portfolio body definitions</li>
              <li>Private notes</li>
            </ul>
            <span className="peppercorn-card-note">
              Without this page the system is a monologue.
            </span>
          </div>
        </div>
      </section>
    </div>
  )
}
