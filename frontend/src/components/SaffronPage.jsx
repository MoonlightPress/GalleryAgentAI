import { useState, useEffect } from 'react'
import './SaffronPage.css'
import { saffronHero } from '../utils/heroImages'

// ── Shared primitives ──────────────────────────────────────────────────────

function SectionShell({ title, subtitle, summary, defaultOpen = false, children }) {
  const [open, setOpen] = useState(defaultOpen)
  return (
    <section className={`sf-section${open ? '' : ' sf-section--closed'}`}>
      <button className="sf-toggle-header" onClick={() => setOpen(o => !o)}>
        <div className="sf-toggle-text">
          <h2 className="sf-section-title">{title}</h2>
          {open
            ? subtitle && <p className="sf-section-subtitle">{subtitle}</p>
            : summary  && <p className="sf-section-summary">{summary}</p>
          }
        </div>
        <span className={`sf-chevron${open ? ' sf-chevron--open' : ''}`}>▾</span>
      </button>
      {open && <div className="sf-section-body">{children}</div>}
    </section>
  )
}

function EmptyState({ message }) {
  return <p className="sf-empty-state">{message}</p>
}

function MissingTag({ label }) {
  return <span className="sf-missing-tag">{label} — ask Peppercorn</span>
}

// ── Original four sections ─────────────────────────────────────────────────

function CareerPosition({ data }) {
  const ig = data.social.find(s => s.platform === 'Instagram')
  const summary = `${data.exhibitions.length} exhibition · ${data.publications.length} publications · Instagram ${ig?.followers ?? '—'} · ${data.base}`
  return (
    <SectionShell
      title="Career Position"
      subtitle="Where she actually is right now — confirmed facts only."
      summary={summary}
      defaultOpen={true}
    >
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
                <div className="sf-row-title">{pub.title}{pub.year ? ` (${pub.year})` : ''}</div>
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
                  {s.posts != null ? <td className="sf-social-posts">{s.posts} posts</td> : <td />}
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
    </SectionShell>
  )
}

function MarketLandscape({ data }) {
  const maxCat  = Math.max(...data.category_breakdown.map(c => c.count), 1)
  const geoTotal = data.tokyo_vs_international.tokyo + data.tokyo_vs_international.international
  const tokyoPct = Math.round((data.tokyo_vs_international.tokyo / geoTotal) * 100)
  const summary  = `${data.total} opportunities — ${data.tokyo_vs_international.tokyo} Tokyo / Japan, ${data.tokyo_vs_international.international} international`

  return (
    <SectionShell
      title="Market Landscape"
      subtitle={`${data.total} opportunities in the current pipeline.`}
      summary={summary}
    >
      <div className="sf-market-grid">
        <div className="sf-market-block">
          <div className="sf-block-label">By category</div>
          <div className="sf-bars">
            {data.category_breakdown.map((cat, i) => (
              <div key={i} className="sf-bar-row">
                <span className="sf-bar-label">{cat.label}</span>
                <div className="sf-bar-track">
                  <div className="sf-bar-fill" style={{ width: `${(cat.count / maxCat) * 100}%` }} />
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
            <span className="sf-geo-label sf-geo-label-tokyo">Tokyo / Japan — {data.tokyo_vs_international.tokyo}</span>
            <span className="sf-geo-label sf-geo-label-intl">International — {data.tokyo_vs_international.international}</span>
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
    </SectionShell>
  )
}

function ComparableArtists({ artists }) {
  const top     = artists.slice(0, 4)
  const summary = `${top.length} artists working in adjacent territory — orientation points, not direct comparisons`
  return (
    <SectionShell
      title="Comparable Artists"
      subtitle="Artists working in adjacent territory — orientation points, not direct comparisons."
      summary={summary}
    >
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
              {a.shared_traits.map((t, j) => <span key={j} className="sf-trait">{t}</span>)}
            </div>
            <div className="sf-peer-use">Use as: {a.use_as}</div>
          </div>
        ))}
      </div>
    </SectionShell>
  )
}

function StrategicPathway({ data }) {
  const done    = data.steps.filter(s => s.done).length
  const summary = `${data.goal} · ${done} of ${data.steps.length} steps complete`
  return (
    <SectionShell
      title={`Pathway: ${data.goal}`}
      subtitle={`Estimated timeline: ${data.timeline_estimate}`}
      summary={summary}
    >
      <div className="sf-steps">
        {data.steps.map((step) => (
          <div key={step.n} className={`sf-step ${step.done ? 'sf-step--done' : step.blocking ? 'sf-step--blocking' : 'sf-step--pending'}`}>
            <div className="sf-step-marker">{step.done ? '✓' : step.blocking ? '▶' : '○'}</div>
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
    </SectionShell>
  )
}

// ── New sections ───────────────────────────────────────────────────────────

function parseFollowers(str) {
  if (str == null) return null
  const s = String(str).replace(/~/g, '').trim()
  const n = s.toLowerCase().endsWith('k') ? parseFloat(s) * 1000 : parseFloat(s)
  return isNaN(n) ? null : n
}

function InstagramStrategy({ data }) {
  const tw = data.platforms.find(p => p.name.startsWith('Twitter'))
  const ig = data.platforms.find(p => p.name === 'Instagram')
  const twN = parseFollowers(tw?.followers)
  const igN = parseFollowers(ig?.followers)
  const ratio = twN && igN ? Math.round(twN / igN) : null

  return (
    <SectionShell
      title="Instagram Strategy"
      subtitle="Platform presence, the audience gap, and what's needed to close it."
      summary={`Instagram ${ig?.followers ?? '—'} · Twitter ${tw?.followers ?? '—'} — 4× gap to close`}
    >
      <div className="sf-two-col">
        <div>
          <div className="sf-block-label">Platform comparison</div>
          {data.platforms.map((p, i) => (
            <div key={i} className="sf-platform-row">
              <div className="sf-platform-name">{p.name}</div>
              <div className="sf-platform-handle">{p.handle}</div>
              <div className="sf-platform-followers">{p.followers}{p.posts != null ? ` · ${p.posts} posts` : ''}</div>
              <div className="sf-platform-note">{p.note}</div>
            </div>
          ))}
          {ratio && (
            <div className="sf-insight-callout">
              Twitter is {ratio}× larger. Instagram is the platform galleries and publishers use for discovery — the gap matters.
            </div>
          )}
        </div>
        <div>
          <div className="sf-block-label">What's known</div>
          <div className="sf-row-title" style={{ marginBottom: 6 }}>{data.known.diary_practice}</div>
          <div className="sf-row-meta">{data.known.content_type}</div>

          <div className="sf-block-label" style={{ marginTop: 24 }}>What's missing</div>
          {data.missing.map((m, i) => (
            <div key={i} className="sf-missing-row">
              <MissingTag label={m.field} />
              <p className="sf-missing-reason">{m.reason}</p>
            </div>
          ))}
        </div>
      </div>
    </SectionShell>
  )
}

function AudienceGeography({ data }) {
  return (
    <SectionShell
      title="Audience Geography"
      subtitle="Where her followers are, which markets are engaged, where opportunities align."
      summary="No audience location data yet — Peppercorn needs to ask"
    >
      <EmptyState message={data.reason} />
      <div className="sf-info-block">
        <div className="sf-block-label">Why it matters</div>
        <p className="sf-info-text">{data.why_it_matters}</p>
        <div className="sf-block-label" style={{ marginTop: 18 }}>Working hypothesis</div>
        <p className="sf-info-text sf-hypothesis">{data.hypothesis}</p>
        <div className="sf-block-label" style={{ marginTop: 18 }}>What Peppercorn should ask</div>
        <p className="sf-info-text">{data.what_peppercorn_should_ask}</p>
      </div>
    </SectionShell>
  )
}

const ASSESSMENT_STYLE = {
  strong:       { color: '#5a7a30', label: 'Strong' },
  on_track:     { color: '#7a9a40', label: 'On track' },
  below_typical:{ color: '#c47a35', label: 'Below typical' },
  weak:         { color: '#b03020', label: 'Weak' },
}

function CareerBenchmarks({ data }) {
  const rec = data.artist_record
  const summary = `${rec.exhibitions} exhibition · ${rec.publications} publications · Instagram ${rec.instagram} · Twitter ${rec.twitter}`
  return (
    <SectionShell
      title="Career Benchmarks"
      subtitle="Where she sits relative to artists at a comparable stage."
      summary={summary}
    >
      <p className="sf-peers-caveat">{data.summary}</p>
      <div className="sf-benchmark-grid">
        {data.peer_range.map((row, i) => {
          const style = ASSESSMENT_STYLE[row.assessment] || ASSESSMENT_STYLE.on_track
          return (
            <div key={i} className="sf-benchmark-row">
              <div className="sf-benchmark-dimension">{row.dimension}</div>
              <div className="sf-benchmark-artist">{row.artist_value}</div>
              <div className="sf-benchmark-range">
                <span className="sf-range-label">Peers: </span>
                {row.peer_low} → {row.peer_typical} → {row.peer_high}
              </div>
              <div className="sf-benchmark-tag" style={{ color: style.color }}>{style.label}</div>
              <div className="sf-benchmark-note">{row.note}</div>
            </div>
          )
        })}
      </div>
    </SectionShell>
  )
}

function SeasonalCalendar({ data }) {
  const known = data.months.reduce((n, m) => n + m.opportunities.length, 0)
  const summary = `${known} opportunities with confirmed deadlines · ${data.unknown_deadline_count} dates unknown`
  return (
    <SectionShell
      title="Seasonal Opportunity Calendar"
      subtitle="Which opportunities open when, and when to prepare."
      summary={summary}
    >
      {data.months.length === 0 ? (
        <EmptyState message="No confirmed deadline dates in the current pipeline. Most opportunities list deadlines as unknown or rolling — the calendar will fill as verification improves." />
      ) : (
        <div className="sf-calendar">
          {data.months.map((m, i) => (
            <div key={i} className="sf-cal-month">
              <div className="sf-cal-month-name">{m.month}</div>
              <div className="sf-cal-opps">
                {m.opportunities.map((o, j) => (
                  <div key={j} className="sf-cal-opp">
                    <span className="sf-cal-cat">{o.category}</span>
                    <span className="sf-cal-name">{o.name}</span>
                    <span className="sf-cal-dl">{o.deadline}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
      {data.rolling.length > 0 && (
        <div style={{ marginTop: 28 }}>
          <div className="sf-block-label">Rolling / open deadlines ({data.rolling.length})</div>
          <div className="sf-cal-rolling">
            {data.rolling.map((o, i) => (
              <div key={i} className="sf-cal-opp sf-cal-opp--rolling">
                <span className="sf-cal-cat">{o.category}</span>
                <span className="sf-cal-name">{o.name}</span>
              </div>
            ))}
          </div>
        </div>
      )}
      <div className="sf-cal-note">{data.coverage_note}</div>
      <div style={{ marginTop: 24 }}>
        <div className="sf-block-label">Preparation lead times</div>
        <div className="sf-lead-times">
          {Object.entries(data.preparation_lead_times).map(([k, v], i) => (
            <div key={i} className="sf-lead-row">
              <span className="sf-lead-type">{k.replace(/_/g, ' ')}</span>
              <span className="sf-lead-time">{v}</span>
            </div>
          ))}
        </div>
      </div>
    </SectionShell>
  )
}

function PressFeatures({ data }) {
  const total   = data.confirmed.length
  const summary = `${total} online feature${total !== 1 ? 's' : ''} (Bored Panda) — no art press coverage yet`
  return (
    <SectionShell
      title="Press & Features"
      subtitle="Publications and blogs that have featured her work, and who to pitch next."
      summary={summary}
    >
      <div className="sf-two-col">
        <div>
          <div className="sf-block-label">Confirmed features</div>
          {data.confirmed.map((f, i) => (
            <div key={i} className="sf-press-row">
              <div className="sf-press-outlet">{f.outlet}</div>
              <div className="sf-press-type">{f.type}</div>
              <div className="sf-press-note">{f.note}</div>
            </div>
          ))}
          <div style={{ marginTop: 24 }}>
            <div className="sf-block-label">Art press</div>
            <EmptyState message={data.art_press.reason} />
          </div>
          <div style={{ marginTop: 16 }}>
            <div className="sf-block-label">Japanese media</div>
            <EmptyState message={data.japan_coverage.reason} />
          </div>
        </div>
        <div>
          <div className="sf-block-label">Pitch targets</div>
          {data.pitch_targets.map((t, i) => (
            <div key={i} className="sf-pitch-row">
              <div className="sf-pitch-outlet">{t.outlet}</div>
              <div className="sf-pitch-why">{t.why}</div>
            </div>
          ))}
        </div>
      </div>
    </SectionShell>
  )
}

function CollectorEcosystem({ data }) {
  return (
    <SectionShell
      title="Collector Ecosystem"
      subtitle="Who buys illustration and watercolor work at her price point, and through which channels."
      summary="No collector data yet — sales history needed"
    >
      <EmptyState message={data.reason} />
      <div className="sf-info-block">
        <div className="sf-block-label">Why it matters</div>
        <p className="sf-info-text">{data.why_it_matters}</p>
        <div className="sf-block-label" style={{ marginTop: 18 }}>Fairs in the pipeline that attract buyers</div>
        <div className="sf-tag-list">
          {data.fairs_in_pipeline.map((f, i) => <span key={i} className="sf-trait">{f}</span>)}
        </div>
        <p className="sf-info-text" style={{ marginTop: 12 }}>{data.known_gap}</p>
        <div className="sf-block-label" style={{ marginTop: 18 }}>What Peppercorn should ask</div>
        <p className="sf-info-text">{data.what_peppercorn_should_ask}</p>
      </div>
    </SectionShell>
  )
}

function CollaborationMap({ data }) {
  const summary = `${data.known_co_exhibitors.length} known co-exhibitors from Tide from China · peer network data missing`
  return (
    <SectionShell
      title="Collaboration Map"
      subtitle="Tokyo-based artists with complementary practices and potential group show partners."
      summary={summary}
    >
      <div className="sf-two-col">
        <div>
          <div className="sf-block-label">Known co-exhibitors</div>
          {data.known_co_exhibitors.map((a, i) => (
            <div key={i} className="sf-collab-row">
              <span className="sf-collab-name">{a.name}</span>
              <span className="sf-collab-context">{a.context}</span>
              <span className="sf-collab-status">Current status: {a.current_status}</span>
            </div>
          ))}
          <p className="sf-info-text" style={{ marginTop: 14 }}>{data.note}</p>
        </div>
        <div>
          <div className="sf-block-label">Tokyo peer network</div>
          <EmptyState message={data.peer_network.reason} />
          <div className="sf-block-label" style={{ marginTop: 18 }}>Why it matters</div>
          <p className="sf-info-text">{data.peer_network.why_it_matters}</p>
        </div>
      </div>
    </SectionShell>
  )
}

function GeographicExpansion({ data }) {
  const intl = data.regions.find(r => r.name.startsWith('Europe')) || {}
  const summary = `Primary: Tokyo / Beijing · ${data.regions.filter(r => r.status === 'medium_term').length} medium-term expansion markets`
  return (
    <SectionShell
      title="Geographic Expansion"
      subtitle="Beyond Tokyo and Beijing — which ecosystems fit her work and when to enter them."
      summary={summary}
    >
      <div className="sf-geo-regions">
        {data.regions.map((r, i) => (
          <div key={i} className={`sf-geo-region sf-geo-region--${r.status}`}>
            <div className="sf-geo-region-header">
              <span className="sf-geo-region-name">{r.name}</span>
              <span className="sf-geo-region-count">{r.pipeline_count > 0 ? `${r.pipeline_count} in pipeline` : ''}</span>
              <span className="sf-geo-status-tag">{r.status.replace(/_/g, ' ')}</span>
            </div>
            <p className="sf-geo-region-note">{r.note}</p>
            {r.entry_point && (
              <div className="sf-geo-entry">Entry point: {r.entry_point}</div>
            )}
          </div>
        ))}
      </div>
    </SectionShell>
  )
}

function PublicationLandscape({ data }) {
  const summary = `${data.pipeline_count} publication opportunities in pipeline · ${data.artist_publications.length} personal publications`
  return (
    <SectionShell
      title="Publication Landscape"
      subtitle="Full map of publishers, from zines to art books — where she is and where to go."
      summary={summary}
    >
      <div className="sf-two-col">
        <div>
          <div className="sf-block-label">Her publications</div>
          {data.artist_publications.map((p, i) => (
            <div key={i} className="sf-press-row">
              <div className="sf-press-outlet">{p.title}{p.year ? ` · ${p.year}` : ''}</div>
              <div className="sf-press-type">{p.type}</div>
              <div className="sf-press-note">{p.note}</div>
            </div>
          ))}

          <div className="sf-block-label" style={{ marginTop: 24 }}>Publication tiers</div>
          {data.tiers.map((t, i) => (
            <div key={i} className="sf-pub-tier">
              <div className="sf-pub-tier-header">
                <span className="sf-pub-tier-name">{t.tier}</span>
                <span className={`sf-pub-barrier sf-pub-barrier--${t.barrier}`}>{t.barrier} barrier</span>
              </div>
              <div className="sf-pub-examples">{t.examples.join(' · ')}</div>
              <div className="sf-pub-note">{t.note}</div>
            </div>
          ))}
        </div>
        <div>
          <div className="sf-block-label">Top targets in pipeline ({data.top_targets.length})</div>
          {data.top_targets.map((o, i) => (
            <div key={i} className="sf-pub-target">
              <span className="sf-pub-target-name">{o.name}</span>
              <span className="sf-pub-target-cat">{o.category}</span>
            </div>
          ))}
        </div>
      </div>
    </SectionShell>
  )
}

const PROB_STYLE = { high: '#5a7a30', moderate: '#c47a35', low: '#b03020' }

function LongTermScenarios({ data }) {
  const summary = `3 paths at ${data.horizon} — gallery, publication, hybrid`
  return (
    <SectionShell
      title="Long-term Scenarios"
      subtitle={`Three career paths at ${data.horizon}. What each requires starting now.`}
      summary={summary}
    >
      <div className="sf-scenarios">
        {data.scenarios.map((s, i) => (
          <div key={i} className="sf-scenario">
            <div className="sf-scenario-header">
              <div>
                <div className="sf-scenario-name">{s.name}</div>
                <div className="sf-scenario-tagline">{s.tagline}</div>
              </div>
              <span
                className="sf-scenario-prob"
                style={{ color: PROB_STYLE[s.probability] || '#7a5030' }}
              >
                {s.probability} probability
              </span>
            </div>
            <p className="sf-scenario-desc">{s.description}</p>
            <div className="sf-block-label" style={{ marginTop: 14 }}>Requires now</div>
            <ul className="sf-scenario-requires">
              {s.requires_now.map((r, j) => <li key={j}>{r}</li>)}
            </ul>
            <div className="sf-scenario-footer">
              <div className="sf-scenario-bottleneck">
                <strong>Bottleneck:</strong> {s.bottleneck}
              </div>
              <div className="sf-scenario-signal">
                <strong>Right if:</strong> {s.best_fit_signal}
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="sf-pathway-callout sf-pathway-next" style={{ marginTop: 28 }}>
        <div className="sf-callout-label">Saffron's view</div>
        <p className="sf-callout-text">{data.saffron_view}</p>
      </div>
    </SectionShell>
  )
}

const STATUS_LABEL = {
  ready_to_review:  { label: 'Ready to review', color: '#c47a35' },
  ready_to_contact: { label: 'Ready to contact', color: '#5a7a30' },
  contacted:        { label: 'Contacted',         color: '#3a6a20' },
  not_contacted:    { label: 'Not contacted',      color: '#9a7040' },
}

function VenueTracker({ data }) {
  const summary = `${data.total} venue${data.total !== 1 ? 's' : ''} tracked · 0 active relationships`
  return (
    <SectionShell
      title="Venue Relationship Tracker"
      subtitle="Venues she's in contact with, their status, and suggested next actions."
      summary={summary}
    >
      {data.tracked.length === 0 ? (
        <EmptyState message="No venues tracked yet. This section will populate as venues are added to the CRM." />
      ) : (
        <div className="sf-venue-list">
          {data.tracked.map((v, i) => {
            const s = STATUS_LABEL[v.status] || { label: v.status, color: '#9a7040' }
            return (
              <div key={i} className="sf-venue-row">
                <div className="sf-venue-header">
                  <span className="sf-venue-name">{v.name}</span>
                  <span className="sf-venue-type">{v.type} · {v.city}</span>
                  <span className="sf-venue-status" style={{ color: s.color }}>{s.label}</span>
                  {v.priority && <span className="sf-venue-priority">Priority {v.priority}</span>}
                </div>
                <div className="sf-venue-last">
                  {v.last_contacted
                    ? `Last contacted: ${v.last_contacted}`
                    : 'Not yet contacted'}
                </div>
                {v.next_action && (
                  <div className="sf-venue-next">{v.next_action}</div>
                )}
              </div>
            )
          })}
        </div>
      )}
      {data.gap_note && (
        <div className="sf-insight-callout" style={{ marginTop: 20 }}>{data.gap_note}</div>
      )}
    </SectionShell>
  )
}

function OpenQuestions({ data }) {
  const summary = `${data.count} open questions that would change this analysis`
  return (
    <SectionShell
      title="Open Questions"
      subtitle="Things Saffron doesn't know yet that would change the analysis."
      summary={summary}
    >
      <p className="sf-info-text" style={{ marginBottom: 24 }}>{data.note}</p>
      <div className="sf-questions">
        {data.questions.map((q, i) => (
          <div key={i} className="sf-question-row">
            <div className="sf-question-number">{i + 1}</div>
            <div className="sf-question-body">
              <div className="sf-question-text">{q.question}</div>
              <div className="sf-question-why">{q.why_it_matters}</div>
              <div className="sf-question-route">→ {q.routed_to}</div>
            </div>
          </div>
        ))}
      </div>
    </SectionShell>
  )
}

// ── Page root ──────────────────────────────────────────────────────────────

export default function SaffronPage() {
  const [data,  setData]  = useState(null)
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
        <img src={saffronHero} alt="Saffron's wide view" className="saffron-hero-img" />
      </section>

      {!data && !error && <div className="sf-loading">Saffron is watching…</div>}

      {error && (
        <div className="sf-error">
          Saffron needs the Mochi API — <code>python api.py</code>
        </div>
      )}

      {data && (
        <div className="sf-content">
          <CareerPosition     data={data.career_position} />
          <MarketLandscape    data={data.market_landscape} />
          <ComparableArtists  artists={data.peer_artists} />
          <StrategicPathway   data={data.pathway} />
          <InstagramStrategy  data={data.instagram_strategy} />
          <AudienceGeography  data={data.audience_geography} />
          <CareerBenchmarks   data={data.career_benchmarks} />
          <SeasonalCalendar   data={data.seasonal_calendar} />
          <PressFeatures      data={data.press_features} />
          <CollectorEcosystem data={data.collector_ecosystem} />
          <CollaborationMap   data={data.collaboration_map} />
          <GeographicExpansion data={data.geographic_expansion} />
          <PublicationLandscape data={data.publication_landscape} />
          <LongTermScenarios  data={data.long_term_scenarios} />
          <VenueTracker       data={data.venue_tracker} />
          <OpenQuestions      data={data.open_questions} />
        </div>
      )}
    </div>
  )
}
