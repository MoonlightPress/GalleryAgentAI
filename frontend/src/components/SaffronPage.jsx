import { useState, useEffect } from 'react'
import './SaffronPage.css'
import { saffronHero } from '../utils/heroImages'

function SectionHeader({ title, subtitle }) {
  return (
    <div className="sf-section-header">
      <h2 className="sf-section-title">{title}</h2>
      {subtitle && <p className="sf-section-subtitle">{subtitle}</p>}
    </div>
  )
}

function CareerPosition({ data }) {
  return (
    <section className="sf-section sf-career">
      <SectionHeader
        title="Career Position"
        subtitle="Where she actually is right now — confirmed facts only."
      />
      <div className="sf-career-grid">

        <div className="sf-career-block">
          <div className="sf-block-label">Exhibitions</div>
          {data.exhibitions.map((ex, i) => (
            <div key={i} className="sf-career-row">
              <span className="sf-check">✓</span>
              <div className="sf-career-row-body">
                <div className="sf-row-title">{ex.title}</div>
                <div className="sf-row-sub">{ex.venue} · {ex.date}</div>
                <div className="sf-row-meta">{ex.type} · {ex.note}</div>
              </div>
            </div>
          ))}
        </div>

        <div className="sf-career-block">
          <div className="sf-block-label">Publications</div>
          {data.publications.map((pub, i) => (
            <div key={i} className="sf-career-row">
              <span className="sf-check">✓</span>
              <div className="sf-career-row-body">
                <div className="sf-row-title">
                  {pub.title}{pub.year ? ` (${pub.year})` : ''}
                </div>
                <div className="sf-row-meta">{pub.type}</div>
              </div>
            </div>
          ))}
        </div>

        <div className="sf-career-block">
          <div className="sf-block-label">Social Presence</div>
          <table className="sf-social-table">
            <tbody>
              {data.social.map((s, i) => (
                <tr key={i}>
                  <td className="sf-social-platform">{s.platform}</td>
                  <td className="sf-social-handle">{s.handle}</td>
                  <td className="sf-social-followers">{s.followers}</td>
                  {s.posts != null
                    ? <td className="sf-social-posts">{s.posts} posts</td>
                    : <td />}
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="sf-career-block">
          <div className="sf-block-label">Education</div>
          <div className="sf-row-title">{data.education.institution}</div>
          <div className="sf-row-meta">{data.education.field} · {data.education.note}</div>
          <div className="sf-block-label" style={{ marginTop: '18px' }}>Base</div>
          <div className="sf-row-title">{data.base}</div>
        </div>

      </div>
    </section>
  )
}

function MarketLandscape({ data }) {
  const maxCat = Math.max(...data.category_breakdown.map(c => c.count), 1)
  const geoTotal = data.tokyo_vs_international.tokyo + data.tokyo_vs_international.international
  const tokyoPct = Math.round((data.tokyo_vs_international.tokyo / geoTotal) * 100)

  return (
    <section className="sf-section sf-market">
      <SectionHeader
        title="Market Landscape"
        subtitle={`${data.total} opportunities in the current pipeline.`}
      />
      <div className="sf-market-grid">

        <div className="sf-market-block">
          <div className="sf-block-label">By category</div>
          <div className="sf-bars">
            {data.category_breakdown.map((cat, i) => (
              <div key={i} className="sf-bar-row">
                <span className="sf-bar-label">{cat.label}</span>
                <div className="sf-bar-track">
                  <div
                    className="sf-bar-fill"
                    style={{ width: `${(cat.count / maxCat) * 100}%` }}
                  />
                </div>
                <span className="sf-bar-count">{cat.count}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="sf-market-block">
          <div className="sf-block-label">Tokyo / Japan vs. international</div>
          <div className="sf-geo-bar">
            <div className="sf-geo-tokyo" style={{ width: `${tokyoPct}%` }} />
            <div className="sf-geo-intl"  style={{ width: `${100 - tokyoPct}%` }} />
          </div>
          <div className="sf-geo-legend">
            <span className="sf-geo-label sf-geo-label-tokyo">
              Tokyo / Japan — {data.tokyo_vs_international.tokyo}
            </span>
            <span className="sf-geo-label sf-geo-label-intl">
              International — {data.tokyo_vs_international.international}
            </span>
          </div>

          <div className="sf-block-label" style={{ marginTop: '28px' }}>By actionability</div>
          <div className="sf-action-list">
            {data.actionability.map((a, i) => (
              <div key={i} className={`sf-action-row sf-action-${a.tier}`}>
                <span className="sf-action-label">{a.label}</span>
                <span className="sf-action-count">{a.count}</span>
              </div>
            ))}
          </div>
        </div>

      </div>
    </section>
  )
}

function ComparableArtists({ artists }) {
  const top = artists.slice(0, 4)
  return (
    <section className="sf-section sf-peers">
      <SectionHeader
        title="Comparable Artists"
        subtitle="Artists working in adjacent territory — orientation points, not direct comparisons."
      />
      <p className="sf-peers-caveat">
        The pipeline finds peers by thematic and formal overlap. Most here are photographers —
        an artifact of shared subjects (quiet observation, memory, domestic space), not a category error.
        The watercolor-specific peer set is underdeveloped and will improve as more targeted data enters the system.
      </p>
      <div className="sf-peers-grid">
        {top.map((a, i) => (
          <div key={i} className="sf-peer-card">
            <div className="sf-peer-name">{a.name}</div>
            <div className="sf-peer-region">{a.region}</div>
            <div className="sf-peer-reason">{a.fit_reason}</div>
            <div className="sf-peer-traits">
              {a.shared_traits.map((t, j) => (
                <span key={j} className="sf-trait">{t}</span>
              ))}
            </div>
            <div className="sf-peer-use">Use as: {a.use_as}</div>
          </div>
        ))}
      </div>
    </section>
  )
}

function StrategicPathway({ data }) {
  return (
    <section className="sf-section sf-pathway">
      <SectionHeader
        title={`Pathway: ${data.goal}`}
        subtitle={`Estimated timeline: ${data.timeline_estimate}`}
      />

      <div className="sf-steps">
        {data.steps.map((step) => (
          <div
            key={step.n}
            className={`sf-step ${step.done ? 'sf-step--done' : step.blocking ? 'sf-step--blocking' : 'sf-step--pending'}`}
          >
            <div className="sf-step-marker">
              {step.done ? '✓' : step.blocking ? '▶' : '○'}
            </div>
            <div className="sf-step-body">
              <div className="sf-step-label">{step.label}</div>
              <div className="sf-step-detail">{step.detail}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="sf-pathway-callout sf-pathway-blocking">
        <div className="sf-callout-label">What's blocking right now</div>
        <p className="sf-callout-text">{data.blocking_now}</p>
      </div>

      <div className="sf-pathway-callout sf-pathway-next">
        <div className="sf-callout-label">Single most important next move</div>
        <p className="sf-callout-text">{data.next_move}</p>
      </div>
    </section>
  )
}

export default function SaffronPage() {
  const [data, setData]   = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/api/saffron')
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json() })
      .then(setData)
      .catch(e => setError(e.message))
  }, [])

  return (
    <div className="saffron-page">
      <section className="saffron-hero">
        <img
          src={saffronHero}
          alt="Saffron's wide view"
          className="saffron-hero-img"
        />
      </section>

      {!data && !error && (
        <div className="sf-loading">Saffron is watching…</div>
      )}

      {error && (
        <div className="sf-error">
          Saffron needs the Mochi API — <code>python api.py</code>
        </div>
      )}

      {data && (
        <div className="sf-content">
          <CareerPosition   data={data.career_position} />
          <MarketLandscape  data={data.market_landscape} />
          <ComparableArtists artists={data.peer_artists} />
          <StrategicPathway data={data.pathway} />
        </div>
      )}
    </div>
  )
}
