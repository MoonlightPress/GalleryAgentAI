import './HeroSection.css'

const focusItems = [
  { icon: '⭐', text: 'Explore 3 new opportunities' },
  { icon: '✉', text: 'Draft 1 outreach email' },
  { icon: '🔍', text: 'Research 1 artist' },
]

export default function HeroSection() {
  return (
    <section className="hero">
      <img
        src="/mochi_hero.png"
        alt="Mochi's watercolor atelier"
        className="hero-img"
      />
      <div className="hero-overlay">
        <div className="greeting">
          <div className="greeting-main">Good afternoon,</div>
          <div className="greeting-sub">🌱 let's grow today.</div>
        </div>
        <div className="focus-card">
          <div className="focus-card-title">Today's Focus</div>
          <ul className="focus-list">
            {focusItems.map((item, i) => (
              <li key={i} className="focus-item">
                <span className="focus-item-icon">{item.icon}</span>
                <span>{item.text}</span>
              </li>
            ))}
          </ul>
          <a href="#" className="focus-see-all">See all quests →</a>
        </div>
      </div>
    </section>
  )
}
