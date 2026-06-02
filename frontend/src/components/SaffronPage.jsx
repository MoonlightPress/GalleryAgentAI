import './SaffronPage.css'
import saffronHero from '../assets/saffron_hero.png'

export default function SaffronPage() {
  return (
    <div className="saffron-page">
      <section className="saffron-hero">
        <img
          src={saffronHero}
          alt="Saffron's wide view"
          className="saffron-hero-img"
        />
        <div className="saffron-hero-overlay">
          <div className="saffron-greeting">
            <div className="saffron-greeting-main">Observe</div>
            <div className="saffron-greeting-sub">Saffron, the bird</div>
          </div>
          <div className="saffron-card">
            <div className="saffron-card-title">The Bigger Picture</div>
            <ul className="saffron-card-list">
              <li>Comparable artists doing similar work</li>
              <li>Opportunity landscape &amp; market context</li>
              <li>Score trends and career statistics</li>
              <li>Seasonal patterns in open calls</li>
            </ul>
            <span className="saffron-card-note">
              Saffron describes without judging — she reports, never advises.
            </span>
          </div>
        </div>
      </section>
    </div>
  )
}
