import './PeppercornPage.css'

export default function PeppercornPage() {
  return (
    <div className="peppercorn-page">
      <div className="peppercorn-swatch" aria-hidden="true">
        <svg viewBox="0 0 200 200" width="140" height="140" fill="none" xmlns="http://www.w3.org/2000/svg">
          {/* Peppercorn — black mouse silhouette, gestural */}
          <ellipse cx="100" cy="118" rx="44" ry="34" fill="#2a2a2a" opacity="0.88"/>
          <ellipse cx="100" cy="108" rx="30" ry="28" fill="#1e1e1e" opacity="0.9"/>
          {/* ears */}
          <ellipse cx="80" cy="85" rx="11" ry="13" fill="#2a2a2a" opacity="0.85"/>
          <ellipse cx="120" cy="85" rx="11" ry="13" fill="#2a2a2a" opacity="0.85"/>
          <ellipse cx="80" cy="85" rx="6" ry="8" fill="#5a4040" opacity="0.5"/>
          <ellipse cx="120" cy="85" rx="6" ry="8" fill="#5a4040" opacity="0.5"/>
          {/* eye */}
          <circle cx="93" cy="104" r="3.5" fill="#fff" opacity="0.9"/>
          <circle cx="93" cy="104" r="2" fill="#111"/>
          {/* nose */}
          <ellipse cx="100" cy="113" rx="4" ry="2.5" fill="#7a5050" opacity="0.7"/>
          {/* tail — curling line */}
          <path d="M144 130 Q170 125 168 145 Q166 158 150 155" stroke="#2a2a2a" strokeWidth="3.5" strokeLinecap="round" fill="none" opacity="0.75"/>
          {/* pencil sketch marks — crosshatching in corner */}
          <line x1="20" y1="168" x2="48" y2="158" stroke="#888" strokeWidth="1" opacity="0.35"/>
          <line x1="25" y1="174" x2="53" y2="164" stroke="#888" strokeWidth="1" opacity="0.35"/>
          <line x1="30" y1="180" x2="58" y2="170" stroke="#888" strokeWidth="1" opacity="0.35"/>
          <line x1="17" y1="171" x2="34" y2="150" stroke="#aaa" strokeWidth="0.8" opacity="0.25"/>
          <line x1="23" y1="177" x2="40" y2="156" stroke="#aaa" strokeWidth="0.8" opacity="0.25"/>
        </svg>
      </div>

      <div className="peppercorn-text">
        <h1 className="peppercorn-title">Refine</h1>
        <p className="peppercorn-companion">Peppercorn, the mouse</p>
        <p className="peppercorn-desc">
          This is where your voice enters the system. Peppercorn keeps
          track of what feels right and what doesn't — your goals, your
          preferences, which recommendations to trust, and which to skip.
        </p>
        <ul className="peppercorn-coming">
          <li>Artist statement & career goals</li>
          <li>Recommendation feedback ("more like this / not this kind")</li>
          <li>Portfolio body definitions</li>
          <li>Private notes</li>
        </ul>
        <p className="peppercorn-note">
          Coming later. Without this page the system is a monologue.
        </p>
      </div>
    </div>
  )
}
