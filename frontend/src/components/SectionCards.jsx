import './SectionCards.css'
import { useLanguage } from '../i18n/LanguageContext'

const CARD_DEFS = [
  { art: '🚪', artColor: '#d4e8f0', prefix: 'sc.opps'     },
  { art: '🌸', artColor: '#dce8f5', prefix: 'sc.peers'    },
  { art: '🍃', artColor: '#ddf0e4', prefix: 'sc.outreach' },
  { art: '📚', artColor: '#f5ead8', prefix: 'sc.quests'   },
  { art: '📓', artColor: '#f5f0dc', prefix: 'sc.journal'  },
  { art: '🎨', artColor: '#f5e4e4', prefix: 'sc.analytics'},
]

export default function SectionCards() {
  const { t } = useLanguage()

  return (
    <section className="section-cards">
      <div className="cards-row">
        {CARD_DEFS.map((card) => (
          <div key={card.prefix} className="section-card">
            <div
              className="card-art"
              style={{ background: card.artColor }}
            >
              <span className="card-art-emoji">{card.art}</span>
            </div>
            <div className="card-body">
              <h3 className="card-title">{t(`${card.prefix}.title`)}</h3>
              <p className="card-desc">{t(`${card.prefix}.desc`)}</p>
              <button
                className="card-link"
                onClick={e => e.preventDefault()}
                type="button"
              >{t(`${card.prefix}.link`)} →</button>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}
