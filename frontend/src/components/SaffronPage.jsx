import './SaffronPage.css'
import { saffronHero } from '../utils/heroImages'

export default function SaffronPage() {
  return (
    <div className="saffron-page">
      <section className="saffron-hero">
        <img
          src={saffronHero}
          alt="Saffron's wide view"
          className="saffron-hero-img"
        />
      </section>
    </div>
  )
}
