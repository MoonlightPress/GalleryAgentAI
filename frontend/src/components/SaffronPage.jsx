import './SaffronPage.css'

export default function SaffronPage() {
  return (
    <div className="saffron-page">
      <div className="saffron-swatch" aria-hidden="true">
        <svg viewBox="0 0 200 200" width="140" height="140" fill="none" xmlns="http://www.w3.org/2000/svg">
          {/* Saffron — red/yellow bird perched on a branch, looking out */}
          {/* branch */}
          <path d="M30 148 Q100 140 170 145" stroke="#8B5e3c" strokeWidth="6" strokeLinecap="round" fill="none" opacity="0.7"/>
          {/* tail feathers */}
          <path d="M98 138 Q80 160 68 170" stroke="#c0392b" strokeWidth="4" strokeLinecap="round" fill="none" opacity="0.75"/>
          <path d="M102 140 Q88 162 80 172" stroke="#d44000" strokeWidth="3.5" strokeLinecap="round" fill="none" opacity="0.65"/>
          <path d="M106 142 Q100 165 96 174" stroke="#e67e22" strokeWidth="3" strokeLinecap="round" fill="none" opacity="0.6"/>
          {/* body */}
          <ellipse cx="108" cy="122" rx="22" ry="18" fill="#c0392b" opacity="0.92"/>
          {/* wing highlight */}
          <path d="M90 118 Q98 108 118 112 Q110 128 92 126 Z" fill="#e74c3c" opacity="0.7"/>
          <path d="M92 119 Q99 111 116 114" stroke="#f39c12" strokeWidth="1.5" fill="none" opacity="0.5"/>
          {/* head */}
          <ellipse cx="122" cy="104" rx="16" ry="14" fill="#c0392b" opacity="0.95"/>
          {/* crest */}
          <path d="M122 91 Q118 78 124 70 Q128 80 130 88" fill="#e74c3c" opacity="0.8"/>
          <path d="M124 70 Q126 62 132 58" stroke="#f39c12" strokeWidth="2" strokeLinecap="round" fill="none" opacity="0.7"/>
          {/* eye */}
          <circle cx="129" cy="101" r="4" fill="#fff" opacity="0.95"/>
          <circle cx="130" cy="101" r="2.5" fill="#1a1a1a"/>
          <circle cx="131" cy="100" r="0.8" fill="#fff" opacity="0.8"/>
          {/* beak */}
          <path d="M136 107 L148 108 L136 112 Z" fill="#f39c12" opacity="0.9"/>
          {/* belly */}
          <ellipse cx="108" cy="130" rx="13" ry="9" fill="#f39c12" opacity="0.55"/>
          {/* feet gripping branch */}
          <line x1="100" y1="138" x2="95" y2="147" stroke="#7B4F2E" strokeWidth="2" strokeLinecap="round"/>
          <line x1="95" y1="147" x2="88" y2="149" stroke="#7B4F2E" strokeWidth="1.5" strokeLinecap="round"/>
          <line x1="95" y1="147" x2="93" y2="152" stroke="#7B4F2E" strokeWidth="1.5" strokeLinecap="round"/>
          <line x1="112" y1="139" x2="116" y2="148" stroke="#7B4F2E" strokeWidth="2" strokeLinecap="round"/>
          <line x1="116" y1="148" x2="122" y2="150" stroke="#7B4F2E" strokeWidth="1.5" strokeLinecap="round"/>
          <line x1="116" y1="148" x2="118" y2="153" stroke="#7B4F2E" strokeWidth="1.5" strokeLinecap="round"/>
        </svg>
      </div>

      <div className="saffron-text">
        <h1 className="saffron-title">Observe</h1>
        <p className="saffron-companion">Saffron, the bird</p>
        <p className="saffron-desc">
          Saffron perches high and watches. From up here she can see
          patterns you can't see from the ground — the shape of the
          market, how comparable artists are moving, what the bigger
          picture looks like over time.
        </p>
        <ul className="saffron-coming">
          <li>Comparable artists doing similar work</li>
          <li>Opportunity landscape and market context</li>
          <li>Score trends and career statistics</li>
          <li>Seasonal patterns in open calls</li>
        </ul>
        <p className="saffron-note">
          Coming later. Saffron describes without judging — she reports, never advises.
        </p>
      </div>
    </div>
  )
}
