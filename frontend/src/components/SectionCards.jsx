import './SectionCards.css'

const cards = [
  {
    art: '🚪',
    artColor: '#d4e8f0',
    title: 'Opportunities',
    desc: 'Discover galleries, residencies, open calls and more.',
    link: 'View all',
  },
  {
    art: '🌸',
    artColor: '#dce8f5',
    title: 'Suggested Peers',
    desc: 'Artists to follow, connect with, and learn from.',
    link: 'Explore',
  },
  {
    art: '🍃',
    artColor: '#ddf0e4',
    title: 'Outreach',
    desc: 'Track conversations and manage your outreach.',
    link: 'Open',
  },
  {
    art: '📚',
    artColor: '#f5ead8',
    title: 'Quests',
    desc: 'Daily and weekly goals to keep your practice moving.',
    link: 'See quests',
  },
  {
    art: '📓',
    artColor: '#f5f0dc',
    title: 'Journal',
    desc: 'Capture ideas, reflections, and inspiration.',
    link: 'Open',
  },
  {
    art: '🎨',
    artColor: '#f5e4e4',
    title: 'Analytics',
    desc: 'See your progress and patterns over time.',
    link: 'View',
  },
]

export default function SectionCards() {
  return (
    <section className="section-cards">
      <div className="cards-row">
        {cards.map((card) => (
          <div key={card.title} className="section-card">
            <div
              className="card-art"
              style={{ background: card.artColor }}
            >
              <span className="card-art-emoji">{card.art}</span>
            </div>
            <div className="card-body">
              <h3 className="card-title">{card.title}</h3>
              <p className="card-desc">{card.desc}</p>
              <a href="#" className="card-link">{card.link} →</a>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}
