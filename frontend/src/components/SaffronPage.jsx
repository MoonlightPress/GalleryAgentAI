import { useState, useEffect } from 'react'
import './SaffronPage.css'
import { saffronHero } from '../utils/heroImages'
import { useLanguage } from '../i18n/LanguageContext'
import {
  LICENSING_LANDSCAPE,
  PRESS_PITCH_MAP,
  GRANT_LANDSCAPE,
  REVENUE_STREAMS,
  CAREER_DEPENDENCY_MAP,
  CAREER_TIMELINE,
  PRICING_INTELLIGENCE,
} from '../data/saffron_insights'

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

function MissingTag({ label, t }) {
  return <span className="sf-missing-tag">{t('sf.missing.askPepper', { label })}</span>
}

// ── Original four sections ─────────────────────────────────────────────────

function CareerPosition({ data, t }) {
  const ig = data.social.find(s => s.platform === 'Instagram')
  const summary = `${data.exhibitions.length} · ${data.publications.length} · Instagram ${ig?.followers ?? '—'} · ${data.base}`
  return (
    <SectionShell
      title={t('sf.sec.careerPosition')}
      subtitle={t('sf.sub.careerPosition')}
      summary={summary}
      defaultOpen={true}
    >
      <div className="sf-career-grid">
        <div className="sf-career-block">
          <div className="sf-block-label">{t('sf.label.exhibitions')}</div>
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
          <div className="sf-block-label">{t('sf.label.publications')}</div>
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
          <div className="sf-block-label">{t('sf.label.social')}</div>
          <table className="sf-social-table">
            <tbody>
              {data.social.map((s, i) => (
                <tr key={i}>
                  <td className="sf-social-platform">{s.platform}</td>
                  <td className="sf-social-handle">{s.handle}</td>
                  <td className="sf-social-followers">{s.followers}</td>
                  {s.posts != null ? <td className="sf-social-posts">{s.posts} {t('sf.label.posts')}</td> : <td />}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="sf-career-block">
          <div className="sf-block-label">{t('sf.label.education')}</div>
          <div className="sf-row-title">{data.education.institution}</div>
          <div className="sf-row-meta">{data.education.field} · {data.education.note}</div>
          <div className="sf-block-label" style={{ marginTop: '18px' }}>{t('sf.label.base')}</div>
          <div className="sf-row-title">{data.base}</div>
        </div>
      </div>
    </SectionShell>
  )
}

function MarketLandscape({ data, t }) {
  const maxCat  = Math.max(...data.category_breakdown.map(c => c.count), 1)
  const geoTotal = data.tokyo_vs_international.tokyo + data.tokyo_vs_international.international
  const tokyoPct = Math.round((data.tokyo_vs_international.tokyo / geoTotal) * 100)
  const summary  = `${data.total} — ${data.tokyo_vs_international.tokyo} ${t('sf.label.tokyo')}, ${data.tokyo_vs_international.international} ${t('sf.label.international')}`

  return (
    <SectionShell
      title={t('sf.sec.market')}
      subtitle={t('sf.sub.market', { n: data.total })}
      summary={summary}
    >
      <div className="sf-market-grid">
        <div className="sf-market-block">
          <div className="sf-block-label">{t('sf.label.byCategory')}</div>
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
          <div className="sf-block-label">{t('sf.label.tokyoVsIntl')}</div>
          <div className="sf-geo-bar">
            <div className="sf-geo-tokyo" style={{ width: `${tokyoPct}%` }} />
            <div className="sf-geo-intl"  style={{ width: `${100 - tokyoPct}%` }} />
          </div>
          <div className="sf-geo-legend">
            <span className="sf-geo-label sf-geo-label-tokyo">{t('sf.label.tokyo')} — {data.tokyo_vs_international.tokyo}</span>
            <span className="sf-geo-label sf-geo-label-intl">{t('sf.label.international')} — {data.tokyo_vs_international.international}</span>
          </div>
          <div className="sf-block-label" style={{ marginTop: '28px' }}>{t('sf.label.byAction')}</div>
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

function ComparableArtists({ artists, t }) {
  const top     = artists.slice(0, 4)
  const summary = t('sf.sum.peers', { n: top.length })
  return (
    <SectionShell
      title={t('sf.sec.peers')}
      subtitle={t('sf.sub.peers')}
      summary={summary}
    >
      <p className="sf-peers-caveat">{t('sf.label.peersCaveat')}</p>
      <div className="sf-peers-grid">
        {top.map((a, i) => (
          <div key={i} className="sf-peer-card">
            <div className="sf-peer-name">{a.name}</div>
            <div className="sf-peer-region">{a.region}</div>
            <div className="sf-peer-reason">{a.fit_reason}</div>
            <div className="sf-peer-traits">
              {a.shared_traits.map((tr, j) => <span key={j} className="sf-trait">{tr}</span>)}
            </div>
            <div className="sf-peer-use">{t('sf.label.useAs')} {a.use_as}</div>
          </div>
        ))}
      </div>
    </SectionShell>
  )
}

function StrategicPathway({ data, t }) {
  const done    = data.steps.filter(s => s.done).length
  const summary = `${data.goal} · ${done} / ${data.steps.length}`
  return (
    <SectionShell
      title={t('sf.sec.pathway', { goal: data.goal })}
      subtitle={t('sf.sub.pathway', { timeline: data.timeline_estimate })}
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
        <div className="sf-callout-label">{t('sf.label.whatBlocking')}</div>
        <p className="sf-callout-text">{data.blocking_now}</p>
      </div>
      <div className="sf-pathway-callout sf-pathway-next">
        <div className="sf-callout-label">{t('sf.label.nextMove')}</div>
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

function InstagramStrategy({ data, t }) {
  const tw = data.platforms.find(p => p.name.startsWith('Twitter'))
  const ig = data.platforms.find(p => p.name === 'Instagram')
  const twN = parseFollowers(tw?.followers)
  const igN = parseFollowers(ig?.followers)
  const ratio = twN && igN ? Math.round(twN / igN) : null

  return (
    <SectionShell
      title={t('sf.sec.instagram')}
      subtitle={t('sf.sub.instagram')}
      summary={`Instagram ${ig?.followers ?? '—'} · Twitter ${tw?.followers ?? '—'}`}
    >
      <div className="sf-two-col">
        <div>
          <div className="sf-block-label">{t('pp.ig.platComp')}</div>
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
              {t('pp.ig.ratio', { n: ratio })}
            </div>
          )}
        </div>
        <div>
          <div className="sf-block-label">{t('pp.ig.known')}</div>
          <div className="sf-row-title" style={{ marginBottom: 6 }}>{data.known.diary_practice}</div>
          <div className="sf-row-meta">{data.known.content_type}</div>

          <div className="sf-block-label" style={{ marginTop: 24 }}>{t('pp.ig.missing')}</div>
          {data.missing.map((m, i) => (
            <div key={i} className="sf-missing-row">
              <MissingTag label={m.field} t={t} />
              <p className="sf-missing-reason">{m.reason}</p>
            </div>
          ))}
        </div>
      </div>
    </SectionShell>
  )
}

function AudienceGeography({ data, t }) {
  return (
    <SectionShell
      title={t('sf.sec.audienceGeo')}
      subtitle={t('sf.sub.audienceGeo')}
      summary={t('sf.sum.audienceGeo')}
    >
      <EmptyState message={data.reason} />
      <div className="sf-info-block">
        <div className="sf-block-label">{t('sf.label.whyMatters')}</div>
        <p className="sf-info-text">{data.why_it_matters}</p>
        <div className="sf-block-label" style={{ marginTop: 18 }}>{t('sf.label.hypothesis')}</div>
        <p className="sf-info-text sf-hypothesis">{data.hypothesis}</p>
        <div className="sf-block-label" style={{ marginTop: 18 }}>{t('sf.label.askPepper')}</div>
        <p className="sf-info-text">{data.what_peppercorn_should_ask}</p>
      </div>
    </SectionShell>
  )
}

const ASSESSMENT_KEYS = {
  strong:        'sf.assess.strong',
  on_track:      'sf.assess.on_track',
  below_typical: 'sf.assess.below_typical',
  weak:          'sf.assess.weak',
}
const ASSESSMENT_COLORS = {
  strong: '#5a7a30', on_track: '#7a9a40', below_typical: '#c47a35', weak: '#b03020',
}

function CareerBenchmarks({ data, t }) {
  const rec = data.artist_record
  const summary = `${rec.exhibitions} · ${rec.publications} · Instagram ${rec.instagram} · Twitter ${rec.twitter}`
  return (
    <SectionShell
      title={t('sf.sec.benchmarks')}
      subtitle={t('sf.sub.benchmarks')}
      summary={summary}
    >
      <p className="sf-peers-caveat">{data.summary}</p>
      <div className="sf-benchmark-grid">
        {data.peer_range.map((row, i) => {
          const color = ASSESSMENT_COLORS[row.assessment] || ASSESSMENT_COLORS.on_track
          const label = t(ASSESSMENT_KEYS[row.assessment] || 'sf.assess.on_track')
          return (
            <div key={i} className="sf-benchmark-row">
              <div className="sf-benchmark-dimension">{row.dimension}</div>
              <div className="sf-benchmark-artist">{row.artist_value}</div>
              <div className="sf-benchmark-range">
                <span className="sf-range-label">{t('sf.label.peers')} </span>
                {row.peer_low} → {row.peer_typical} → {row.peer_high}
              </div>
              <div className="sf-benchmark-tag" style={{ color }}>{label}</div>
              <div className="sf-benchmark-note">{row.note}</div>
            </div>
          )
        })}
      </div>
    </SectionShell>
  )
}

function SeasonalCalendar({ data, t }) {
  const known = data.months.reduce((n, m) => n + m.opportunities.length, 0)
  const summary = `${known} · ${data.unknown_deadline_count} unknown`
  return (
    <SectionShell
      title={t('sf.sec.calendar')}
      subtitle={t('sf.sub.calendar')}
      summary={summary}
    >
      {data.months.length === 0 ? (
        <EmptyState message={t('sf.empty.calendar')} />
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
          <div className="sf-block-label">{t('sf.label.rolling', { n: data.rolling.length })}</div>
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
        <div className="sf-block-label">{t('sf.label.prepLeadTimes')}</div>
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

function PressFeatures({ data, t }) {
  const total   = data.confirmed.length
  const summary = `${total} online feature${total !== 1 ? 's' : ''}`
  return (
    <SectionShell
      title={t('sf.sec.press')}
      subtitle={t('sf.sub.press')}
      summary={summary}
    >
      <div className="sf-two-col">
        <div>
          <div className="sf-block-label">{t('sf.label.confirmed')}</div>
          {data.confirmed.map((f, i) => (
            <div key={i} className="sf-press-row">
              <div className="sf-press-outlet">{f.outlet}</div>
              <div className="sf-press-type">{f.type}</div>
              <div className="sf-press-note">{f.note}</div>
            </div>
          ))}
          <div style={{ marginTop: 24 }}>
            <div className="sf-block-label">{t('sf.label.artPress')}</div>
            <EmptyState message={data.art_press.reason} />
          </div>
          <div style={{ marginTop: 16 }}>
            <div className="sf-block-label">{t('sf.label.japanMedia')}</div>
            <EmptyState message={data.japan_coverage.reason} />
          </div>
        </div>
        <div>
          <div className="sf-block-label">{t('sf.label.pitchTargets')}</div>
          {data.pitch_targets.map((pt, i) => (
            <div key={i} className="sf-pitch-row">
              <div className="sf-pitch-outlet">{pt.outlet}</div>
              <div className="sf-pitch-why">{pt.why}</div>
            </div>
          ))}
        </div>
      </div>
    </SectionShell>
  )
}

function CollectorEcosystem({ data, t }) {
  return (
    <SectionShell
      title={t('sf.sec.collector')}
      subtitle={t('sf.sub.collector')}
      summary={t('sf.sum.collector')}
    >
      <EmptyState message={data.reason} />
      <div className="sf-info-block">
        <div className="sf-block-label">{t('sf.label.whyMatters')}</div>
        <p className="sf-info-text">{data.why_it_matters}</p>
        <div className="sf-block-label" style={{ marginTop: 18 }}>{t('sf.label.fairsPipeline')}</div>
        <div className="sf-tag-list">
          {data.fairs_in_pipeline.map((f, i) => <span key={i} className="sf-trait">{f}</span>)}
        </div>
        <p className="sf-info-text" style={{ marginTop: 12 }}>{data.known_gap}</p>
        <div className="sf-block-label" style={{ marginTop: 18 }}>{t('sf.label.askPepper')}</div>
        <p className="sf-info-text">{data.what_peppercorn_should_ask}</p>
      </div>
    </SectionShell>
  )
}

function CollaborationMap({ data, t }) {
  const summary = `${data.known_co_exhibitors.length} co-exhibitors`
  return (
    <SectionShell
      title={t('sf.sec.collab')}
      subtitle={t('sf.sub.collab')}
      summary={summary}
    >
      <div className="sf-two-col">
        <div>
          <div className="sf-block-label">{t('sf.label.knownCoExhib')}</div>
          {data.known_co_exhibitors.map((a, i) => (
            <div key={i} className="sf-collab-row">
              <span className="sf-collab-name">{a.name}</span>
              <span className="sf-collab-context">{a.context}</span>
              <span className="sf-collab-status">{t('sf.label.currentStatus')} {a.current_status}</span>
            </div>
          ))}
          <p className="sf-info-text" style={{ marginTop: 14 }}>{data.note}</p>
        </div>
        <div>
          <div className="sf-block-label">{t('sf.label.tokyoPeerNet')}</div>
          <EmptyState message={data.peer_network.reason} />
          <div className="sf-block-label" style={{ marginTop: 18 }}>{t('sf.label.whyMatters')}</div>
          <p className="sf-info-text">{data.peer_network.why_it_matters}</p>
        </div>
      </div>
    </SectionShell>
  )
}

function GeographicExpansion({ data, t }) {
  const summary = `Primary: Tokyo / Beijing`
  return (
    <SectionShell
      title={t('sf.sec.geoExpansion')}
      subtitle={t('sf.sub.geoExpansion')}
      summary={summary}
    >
      <div className="sf-geo-regions">
        {data.regions.map((r, i) => (
          <div key={i} className={`sf-geo-region sf-geo-region--${r.status}`}>
            <div className="sf-geo-region-header">
              <span className="sf-geo-region-name">{r.name}</span>
              <span className="sf-geo-region-count">
                {r.pipeline_count > 0 ? t('sf.inPipeline', { n: r.pipeline_count }) : ''}
              </span>
              <span className="sf-geo-status-tag">{t(`sf.geo.${r.status}`) || r.status.replace(/_/g, ' ')}</span>
            </div>
            <p className="sf-geo-region-note">{r.note}</p>
            {r.entry_point && (
              <div className="sf-geo-entry">{t('sf.label.entryPoint')} {r.entry_point}</div>
            )}
          </div>
        ))}
      </div>
    </SectionShell>
  )
}

function PublicationLandscape({ data, t }) {
  const summary = `${data.pipeline_count} · ${data.artist_publications.length}`
  return (
    <SectionShell
      title={t('sf.sec.publication')}
      subtitle={t('sf.sub.publication')}
      summary={summary}
    >
      <div className="sf-two-col">
        <div>
          <div className="sf-block-label">{t('sf.label.herPubs')}</div>
          {data.artist_publications.map((p, i) => (
            <div key={i} className="sf-press-row">
              <div className="sf-press-outlet">{p.title}{p.year ? ` · ${p.year}` : ''}</div>
              <div className="sf-press-type">{p.type}</div>
              <div className="sf-press-note">{p.note}</div>
            </div>
          ))}

          <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.label.pubTiers')}</div>
          {data.tiers.map((tier, i) => (
            <div key={i} className="sf-pub-tier">
              <div className="sf-pub-tier-header">
                <span className="sf-pub-tier-name">{tier.tier}</span>
                <span className={`sf-pub-barrier sf-pub-barrier--${tier.barrier}`}>
                  {t(`sf.barrier.${tier.barrier}`) || tier.barrier}
                </span>
              </div>
              <div className="sf-pub-examples">{tier.examples.join(' · ')}</div>
              <div className="sf-pub-note">{tier.note}</div>
            </div>
          ))}
        </div>
        <div>
          <div className="sf-block-label">{t('sf.label.topTargets', { n: data.top_targets.length })}</div>
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

function LongTermScenarios({ data, t }) {
  const PROB_COLORS = { high: '#5a7a30', moderate: '#c47a35', low: '#b03020' }
  const summary = `3 paths · ${data.horizon}`
  return (
    <SectionShell
      title={t('sf.sec.longTerm')}
      subtitle={t('sf.sub.longTerm', { horizon: data.horizon })}
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
                style={{ color: PROB_COLORS[s.probability] || '#7a5030' }}
              >
                {t(`sf.prob.${s.probability}`) || s.probability}
              </span>
            </div>
            <p className="sf-scenario-desc">{s.description}</p>
            <div className="sf-block-label" style={{ marginTop: 14 }}>{t('sf.label.requiresNow')}</div>
            <ul className="sf-scenario-requires">
              {s.requires_now.map((r, j) => <li key={j}>{r}</li>)}
            </ul>
            <div className="sf-scenario-footer">
              <div className="sf-scenario-bottleneck">
                <strong>{t('sf.label.bottleneck')}</strong> {s.bottleneck}
              </div>
              <div className="sf-scenario-signal">
                <strong>{t('sf.label.rightIf')}</strong> {s.best_fit_signal}
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="sf-pathway-callout sf-pathway-next" style={{ marginTop: 28 }}>
        <div className="sf-callout-label">{t('sf.label.saffronView')}</div>
        <p className="sf-callout-text">{data.saffron_view}</p>
      </div>
    </SectionShell>
  )
}

const STATUS_KEYS = {
  ready_to_review:  'sf.status.readyReview',
  ready_to_contact: 'sf.status.readyContact',
  contacted:        'sf.status.contacted',
  not_contacted:    'sf.status.notContacted',
}
const STATUS_COLORS = {
  ready_to_review: '#c47a35', ready_to_contact: '#5a7a30',
  contacted: '#3a6a20', not_contacted: '#9a7040',
}

function VenueTracker({ data, t }) {
  const summary = t('sf.sum.venues', { n: data.total, s: data.total !== 1 ? 's' : '' })
  return (
    <SectionShell
      title={t('sf.sec.venues')}
      subtitle={t('sf.sub.venues')}
      summary={summary}
    >
      {data.tracked.length === 0 ? (
        <EmptyState message={t('sf.empty.venues')} />
      ) : (
        <div className="sf-venue-list">
          {data.tracked.map((v, i) => {
            const color = STATUS_COLORS[v.status] || '#9a7040'
            const label = t(STATUS_KEYS[v.status] || 'sf.status.notContacted')
            return (
              <div key={i} className="sf-venue-row">
                <div className="sf-venue-header">
                  <span className="sf-venue-name">{v.name}</span>
                  <span className="sf-venue-type">{v.type} · {v.city}</span>
                  <span className="sf-venue-status" style={{ color }}>{label}</span>
                  {v.priority && <span className="sf-venue-priority">{t('sf.venue.priority', { n: v.priority })}</span>}
                </div>
                <div className="sf-venue-last">
                  {v.last_contacted
                    ? t('sf.venue.lastContacted', { date: v.last_contacted })
                    : t('sf.venue.notContacted')}
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

function OpenQuestions({ data, t }) {
  const summary = `${data.count}`
  return (
    <SectionShell
      title={t('sf.sec.openQs')}
      subtitle={t('sf.sub.openQs')}
      summary={summary}
    >
      <p className="sf-info-text" style={{ marginBottom: 24 }}>{t('sf.label.openQNote')}</p>
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

// ── Licensing Landscape ────────────────────────────────────────────────────

const TIER_COLORS = { now: '#16a34a', near_term: '#d97706', medium_term: '#9ca3af' }

function locF(item, field, lang) {
  if (lang === 'zh' && item[field + '_zh']) return item[field + '_zh']
  if (lang === 'ja' && item[field + '_ja']) return item[field + '_ja']
  return item[field] || ''
}

function LicensingLandscape({ t, lang }) {
  const d = LICENSING_LANDSCAPE
  return (
    <SectionShell title={t(d.titleKey)} summary={t(d.summaryKey)}>
      {d.items.map((group, gi) => (
        <div key={gi} className="sf-insight-group">
          <div className="sf-block-label">{locF(group, 'category', lang)}</div>
          <div className="sf-licensing-entries">
            {group.entries.map((entry, ei) => (
              <div key={ei} className="sf-licensing-entry">
                <div className="sf-licensing-entry-header">
                  <span className="sf-licensing-name">{entry.name}</span>
                  <span className="sf-tier-badge" style={{ color: TIER_COLORS[entry.tier] || '#9ca3af' }}>
                    {t(`sf.tier.${entry.tier}`) || entry.tier}
                  </span>
                </div>
                <p className="sf-licensing-note">{locF(entry, 'note', lang)}</p>
              </div>
            ))}
          </div>
        </div>
      ))}
    </SectionShell>
  )
}

// ── Press & Pitch Map ──────────────────────────────────────────────────────

function PressPitchMap({ t, lang }) {
  const d = PRESS_PITCH_MAP
  const outlets = d.items.filter(item => item.name)
  const discoveryNote = d.items.find(item => item.category_note)
  return (
    <SectionShell title={t(d.titleKey)} summary={t(d.summaryKey)}>
      <div className="sf-press-pitch-list">
        {outlets.map((item, i) => (
          <div key={i} className="sf-press-pitch-row">
            <div className="sf-press-pitch-header">
              <span className="sf-press-pitch-name">{item.name}</span>
              <span className="sf-press-pitch-type">{locF(item, 'type', lang)}</span>
            </div>
            <p className="sf-press-pitch-why">{locF(item, 'why_fits', lang)}</p>
            <div className="sf-press-pitch-meta">
              {item.how_to_pitch && (
                <div className="sf-press-pitch-how">
                  <span className="sf-press-pitch-meta-label">{t('sf.label.pitchColon')}</span>
                  {locF(item, 'how_to_pitch', lang)}
                </div>
              )}
              {item.contact && (
                <div className="sf-press-pitch-contact">
                  <span className="sf-press-pitch-meta-label">{t('sf.label.contactColon')}</span>
                  {item.contact}
                </div>
              )}
              {item.timeline && (
                <div className="sf-press-pitch-timeline">
                  <span className="sf-press-pitch-meta-label">{t('sf.label.timelineColon')}</span>
                  {locF(item, 'timeline', lang)}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
      {discoveryNote && (
        <div className="sf-insight-callout" style={{ marginTop: 24 }}>
          <div className="sf-block-label">{locF(discoveryNote, 'category_note', lang)}</div>
          <p className="sf-info-text">{locF(discoveryNote, 'how_discovered', lang)}</p>
        </div>
      )}
    </SectionShell>
  )
}

// ── Grant Landscape ────────────────────────────────────────────────────────

function GrantLandscape({ t, lang }) {
  const d = GRANT_LANDSCAPE
  const grants = d.items.filter(item => item.name)
  const strategyNote = d.items.find(item => item.category_note)
  return (
    <SectionShell title={t(d.titleKey)} summary={t(d.summaryKey)}>
      <div className="sf-grant-list">
        {grants.map((grant, i) => (
          <div key={i} className="sf-grant-row">
            <div className="sf-grant-header">
              <span className="sf-grant-name">{grant.name}</span>
              <span className="sf-grant-country">{grant.country}</span>
            </div>
            <div className="sf-grant-amount">{grant.amount}</div>
            <p className="sf-grant-why">{locF(grant, 'why_apply', lang)}</p>
            <div className="sf-grant-meta">
              {grant.eligibility && (
                <div className="sf-grant-meta-row">
                  <span className="sf-grant-meta-label">{t('sf.label.eligibilityColon')}</span>
                  {locF(grant, 'eligibility', lang)}
                </div>
              )}
              {grant.deadline && (
                <div className="sf-grant-meta-row">
                  <span className="sf-grant-meta-label">{t('sf.label.deadlineColon')}</span>
                  {grant.deadline}
                </div>
              )}
              {grant.competition && (
                <div className="sf-grant-meta-row">
                  <span className="sf-grant-meta-label">{t('sf.label.competitionColon')}</span>
                  {locF(grant, 'competition', lang)}
                </div>
              )}
              {grant.tip && (
                <div className="sf-grant-tip">{t('sf.label.tipColon')}{locF(grant, 'tip', lang)}</div>
              )}
            </div>
          </div>
        ))}
      </div>
      {strategyNote && (
        <div className="sf-insight-callout" style={{ marginTop: 24 }}>
          <div className="sf-block-label">{locF(strategyNote, 'category_note', lang)}</div>
          <p className="sf-info-text">{locF(strategyNote, 'note', lang)}</p>
        </div>
      )}
    </SectionShell>
  )
}

// ── Revenue Streams ────────────────────────────────────────────────────────

function RevenueStreams({ t, lang }) {
  const d = REVENUE_STREAMS
  const streams = d.items.filter(item => item.stream !== 'Summary assessment')
  const summary_item = d.items.find(item => item.stream === 'Summary assessment')
  return (
    <SectionShell title={t(d.titleKey)} summary={t(d.summaryKey)}>
      <div className="sf-revenue-list">
        {streams.map((item, i) => (
          <div key={i} className={`sf-revenue-row${item.leaving_on_table ? ' sf-revenue-row--gap' : ''}`}>
            <div className="sf-revenue-header">
              <span className="sf-revenue-stream">{locF(item, 'stream', lang)}</span>
              {item.realistic_monthly && (
                <span className="sf-revenue-range">{item.realistic_monthly}</span>
              )}
              {item.leaving_on_table && (
                <span className="sf-revenue-gap-tag">{t('sf.label.gapTag')}</span>
              )}
            </div>
            <p className="sf-revenue-desc">{locF(item, 'description', lang)}</p>
            {item.pricing && (
              <div className="sf-revenue-pricing">{locF(item, 'pricing', lang)}</div>
            )}
            {item.why_now && (
              <div className="sf-revenue-why">{locF(item, 'why_now', lang)}</div>
            )}
            {item.action && (
              <div className="sf-revenue-action">
                <span className="sf-revenue-action-label">{t('sf.label.actionColon')}</span>
                {locF(item, 'action', lang)}
              </div>
            )}
          </div>
        ))}
      </div>
      {summary_item && (
        <div className="sf-pathway-callout sf-pathway-blocking" style={{ marginTop: 24 }}>
          <div className="sf-callout-label">{t('sf.label.assessmentTitle')}</div>
          <p className="sf-callout-text">{locF(summary_item, 'description', lang)}</p>
        </div>
      )}
    </SectionShell>
  )
}

// ── Career Dependency Map ──────────────────────────────────────────────────

const MILESTONE_DOT_COLORS = {
  current: '#16a34a',
  next:    '#d97706',
  future:  '#9ca3af',
  horizon: '#9ca3af',
}

function CareerDependencyMap({ t, lang }) {
  const d = CAREER_DEPENDENCY_MAP
  return (
    <SectionShell title={t(d.titleKey)} summary={t(d.summaryKey)}>
      <div className="sf-depmap">
        {d.milestones.map((milestone, mi) => {
          const dotColor = MILESTONE_DOT_COLORS[milestone.status] || '#9ca3af'
          const phaseKey = `sf.depmap.${milestone.status}`
          const phaseLabel = t(phaseKey) || milestone.label
          return (
            <div key={mi} className={`sf-depmap-milestone sf-depmap-milestone--${milestone.status}`}>
              <div className="sf-depmap-milestone-header">
                <span className="sf-depmap-dot" style={{ background: dotColor }} />
                <span className="sf-depmap-phase-label">{phaseLabel}</span>
              </div>
              <div className="sf-depmap-items">
                {milestone.items.map((item, ii) => (
                  <div key={ii} className="sf-depmap-item">
                    <div className="sf-depmap-complete">
                      <span className="sf-depmap-complete-label">{t('sf.depmap.completes')}</span>
                      {locF(item, 'complete', lang)}
                    </div>
                    <div className="sf-depmap-unlocks">
                      <span className="sf-depmap-unlocks-label">{t('sf.depmap.unlocks')}</span>
                      <ul className="sf-depmap-unlocks-list">
                        {(locF(item, 'unlocks', lang) || item.unlocks || []).map((unlock, ui) => (
                          <li key={ui}>{unlock}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ))}
              </div>
              {mi < d.milestones.length - 1 && (
                <div className="sf-depmap-connector" />
              )}
            </div>
          )
        })}
      </div>
    </SectionShell>
  )
}

// ── Career Momentum Tracker ────────────────────────────────────────────────

const TRAJECTORY_COLORS = {
  early:        '#9a7040',
  accelerating: '#5a7a30',
  steady:       '#3a6a80',
  stalling:     '#b03020',
}

function CareerMomentum({ data, t }) {
  const { this_month, totals, response_rate, trajectory, monthly_chart, recent_activity } = data
  const maxBar = Math.max(...monthly_chart.map(m => m.submissions + m.contacts), 1)
  const trajColor = TRAJECTORY_COLORS[trajectory] || '#9a7040'
  const summary = `${totals.submissions} submissions · ${totals.venues_in_crm} venues · ${response_rate}% response`

  return (
    <SectionShell
      title={t('sf.sec.momentum')}
      subtitle={t('sf.sub.momentum')}
      summary={summary}
    >
      <div className="sf-momentum-stats">
        <div className="sf-momentum-stat">
          <div className="sf-momentum-number">{totals.submissions}</div>
          <div className="sf-momentum-label">{t('sf.mom.totalSubmissions')}</div>
        </div>
        <div className="sf-momentum-stat">
          <div className="sf-momentum-number">{totals.venues_in_crm}</div>
          <div className="sf-momentum-label">{t('sf.mom.venuesInCRM')}</div>
        </div>
        <div className="sf-momentum-stat">
          <div className="sf-momentum-number">{totals.responses_received}</div>
          <div className="sf-momentum-label">{t('sf.mom.responses')}</div>
        </div>
        <div className="sf-momentum-stat">
          <div className="sf-momentum-number" style={{ color: trajColor }}>
            {t(`sf.mom.traj.${trajectory}`) || trajectory}
          </div>
          <div className="sf-momentum-label">{t('sf.mom.trajectory')}</div>
        </div>
      </div>

      <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.mom.activityChart')}</div>
      <div className="sf-mom-chart">
        {monthly_chart.map((m, i) => {
          const total = m.submissions + m.contacts
          const pct   = Math.round((total / maxBar) * 100)
          return (
            <div key={i} className="sf-mom-bar-col">
              <div className="sf-mom-bar-track">
                <div className="sf-mom-bar-subs"
                  style={{ height: `${Math.round((m.submissions / maxBar) * 100)}%` }} />
                <div className="sf-mom-bar-contacts"
                  style={{ height: `${Math.round((m.contacts / maxBar) * 100)}%` }} />
              </div>
              <div className="sf-mom-bar-label">{m.month.slice(5)}</div>
              <div className="sf-mom-bar-total">{total || ''}</div>
            </div>
          )
        })}
      </div>
      <div className="sf-mom-legend">
        <span className="sf-mom-legend-subs">{t('sf.mom.submissions')}</span>
        <span className="sf-mom-legend-contacts">{t('sf.mom.contacts')}</span>
      </div>

      {recent_activity.length > 0 && (
        <div style={{ marginTop: 24 }}>
          <div className="sf-block-label">{t('sf.mom.recentActivity')}</div>
          <div className="sf-mom-activity">
            {recent_activity.map((item, i) => (
              <div key={i} className="sf-mom-activity-row">
                <span className={`sf-mom-type sf-mom-type--${item.type}`}>
                  {item.type === 'submission' ? '📤' : '📋'}
                </span>
                <span className="sf-mom-activity-name">{item.name}</span>
                <span className="sf-mom-activity-status">{item.status}</span>
                <span className="sf-mom-activity-date">{item.date?.slice(0, 10)}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {totals.submissions === 0 && (
        <div className="sf-insight-callout" style={{ marginTop: 20 }}>
          {t('sf.mom.noSubmissionsYet')}
        </div>
      )}
    </SectionShell>
  )
}

// ── Timing Intelligence ────────────────────────────────────────────────────

function TimingIntelligence({ data, t }) {
  const maxCount = Math.max(...data.monthly_counts.map(m => m.count), 1)
  const summary  = `${data.peak_months.slice(0, 2).join(' · ')} peak · ${data.with_parsed_deadline} dated`

  return (
    <SectionShell
      title={t('sf.sec.timing')}
      subtitle={t('sf.sub.timing')}
      summary={summary}
    >
      <div className="sf-insight-callout">{data.key_insight}</div>

      <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.timing.deadlinesByMonth')}</div>
      <div className="sf-timing-grid">
        {data.monthly_counts.map((m, i) => (
          <div key={i} className="sf-timing-month">
            <div className="sf-timing-month-name">{m.month.slice(0, 3)}</div>
            <div className="sf-timing-bar-track">
              <div
                className={`sf-timing-bar${data.peak_months.includes(m.month) ? ' sf-timing-bar--peak' : ''}`}
                style={{ height: `${Math.round((m.count / maxCount) * 100)}%` }}
              />
            </div>
            <div className="sf-timing-count">{m.count || ''}</div>
          </div>
        ))}
      </div>

      <div className="sf-two-col" style={{ marginTop: 28 }}>
        <div>
          <div className="sf-block-label">{t('sf.timing.peakMonths')}</div>
          {data.peak_months.map((m, i) => (
            <div key={i} className="sf-timing-peak-row">
              <span className="sf-timing-peak-dot" />
              <span>{m}</span>
              <span className="sf-timing-peak-count">{data.monthly_counts.find(x => x.month === m)?.count} deadlines</span>
            </div>
          ))}
          {data.quiet_months.length > 0 && (
            <>
              <div className="sf-block-label" style={{ marginTop: 18 }}>{t('sf.timing.quietMonths')}</div>
              {data.quiet_months.map((m, i) => (
                <div key={i} className="sf-timing-quiet-row">{m} — {t('sf.timing.quietNote')}</div>
              ))}
            </>
          )}
        </div>
        <div>
          <div className="sf-block-label">{t('sf.timing.coverage')}</div>
          <div className="sf-timing-stats">
            <div className="sf-timing-stat-row">
              <span>{t('sf.timing.withDeadline')}</span>
              <span className="sf-timing-stat-val">{data.with_parsed_deadline}</span>
            </div>
            <div className="sf-timing-stat-row">
              <span>{t('sf.timing.rolling')}</span>
              <span className="sf-timing-stat-val">{data.rolling_count}</span>
            </div>
            <div className="sf-timing-stat-row">
              <span>{t('sf.timing.noDeadline')}</span>
              <span className="sf-timing-stat-val">{data.no_deadline_count}</span>
            </div>
          </div>
          <div className="sf-block-label" style={{ marginTop: 18 }}>{t('sf.timing.prepWindow')}</div>
          <p className="sf-info-text">{t('sf.timing.prepWindowNote')}</p>
        </div>
      </div>
    </SectionShell>
  )
}

// ── Comparative Career Timeline ────────────────────────────────────────────

function CareerTimeline({ t }) {
  const d = CAREER_TIMELINE
  return (
    <SectionShell title={t(d.titleKey)} summary={t(d.summaryKey)}>
      <div className="sf-insight-callout">{d.overall_assessment}</div>

      <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.timeline.artistStage')}</div>
      <div className="sf-timeline-stage">
        <span className="sf-trait">Age {d.artist_stage.age}</span>
        <span className="sf-trait">{d.artist_stage.group_shows} group show</span>
        <span className="sf-trait">{d.artist_stage.publications} publications</span>
        <span className="sf-trait">Instagram {d.artist_stage.instagram}</span>
        <span className="sf-trait">Twitter {d.artist_stage.twitter}</span>
      </div>

      <div className="sf-peers-grid" style={{ marginTop: 24 }}>
        {d.peers.map((peer, i) => (
          <div key={i} className="sf-peer-card">
            <div className="sf-peer-name">{peer.name}</div>
            <div className="sf-peer-region">{peer.region} · {peer.comparable_age}</div>
            <div className="sf-block-label" style={{ marginTop: 12, fontSize: '0.72rem' }}>{t('sf.timeline.hadAtStage')}</div>
            <ul className="sf-timeline-had-list">
              {peer.at_stage.had.map((h, j) => <li key={j}>{h}</li>)}
            </ul>
            <div className="sf-peer-use" style={{ marginTop: 10 }}>{peer.comparison}</div>
          </div>
        ))}
      </div>
    </SectionShell>
  )
}

// ── Pricing Intelligence ───────────────────────────────────────────────────

const IMPACT_COLORS = { high: '#5a7a30', medium: '#c47a35', low: '#9ca3af' }

function PricingIntelligence({ t }) {
  const d = PRICING_INTELLIGENCE
  const { originals, prints, zines } = d.current_range
  return (
    <SectionShell title={t(d.titleKey)} summary={t(d.summaryKey)}>
      <p className="sf-peers-caveat">{d.source_note}</p>

      <div className="sf-block-label" style={{ marginTop: 16 }}>{t('sf.pricing.currentRanges')}</div>
      <div className="sf-pricing-ranges">
        {[originals, prints, zines].map((range, i) => (
          <div key={i} className="sf-pricing-range-card">
            <div className="sf-pricing-range-label">{range.label}</div>
            <div className="sf-pricing-range-value">
              ¥{range.low.toLocaleString()} – ¥{range.high.toLocaleString()}
            </div>
            <p className="sf-pricing-range-note">{range.note}</p>
            {range.sweet_spot && (
              <div className="sf-pricing-sweet-spot">{range.sweet_spot}</div>
            )}
          </div>
        ))}
      </div>

      <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.pricing.whatAffectsPrice')}</div>
      <div className="sf-pricing-factors">
        {d.what_affects_price.map((f, i) => (
          <div key={i} className="sf-pricing-factor">
            <div className="sf-pricing-factor-header">
              <span className="sf-pricing-factor-name">{f.factor}</span>
              <span className="sf-pricing-impact" style={{ color: IMPACT_COLORS[f.impact] }}>
                {t(`sf.pricing.impact.${f.impact}`) || f.impact}
              </span>
            </div>
            <p className="sf-pricing-factor-note">{f.note}</p>
          </div>
        ))}
      </div>

      <div className="sf-pathway-callout sf-pathway-blocking" style={{ marginTop: 24 }}>
        <div className="sf-callout-label">{t('sf.pricing.editionDiscipline')}</div>
        <p className="sf-callout-text">{d.edition_discipline.rule}</p>
        <p className="sf-callout-text" style={{ marginTop: 8, fontStyle: 'italic' }}>
          {d.edition_discipline.current_gap}
        </p>
      </div>

      <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.pricing.credibilitySignals')}</div>
      <ul className="sf-pricing-signals">
        {d.credibility_signals.map((s, i) => <li key={i}>{s}</li>)}
      </ul>
    </SectionShell>
  )
}

// ── Opportunity Gap Analysis ───────────────────────────────────────────────

const GAP_COLORS = { gap: '#b03020', strength: '#5a7a30', on_track: '#9a7040' }

function OpportunityGap({ data, t }) {
  const summary = `${data.gaps.length} gaps · ${data.strengths.length} strengths`
  return (
    <SectionShell
      title={t('sf.sec.oppGap')}
      subtitle={t('sf.sub.oppGap')}
      summary={summary}
    >
      <div className="sf-insight-callout">{data.summary}</div>

      {data.gaps.length > 0 && (
        <>
          <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.gap.underrepresented')}</div>
          <div className="sf-gap-list">
            {data.gaps.map((g, i) => (
              <div key={i} className="sf-gap-row sf-gap-row--gap">
                <div className="sf-gap-row-header">
                  <span className="sf-gap-label">{g.label}</span>
                  <span className="sf-gap-counts">
                    {g.actual_count} {t('sf.gap.vs')} ~{g.expected_count} {t('sf.gap.expected')}
                  </span>
                </div>
                <p className="sf-gap-note">{g.note}</p>
              </div>
            ))}
          </div>
        </>
      )}

      {data.strengths.length > 0 && (
        <>
          <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.gap.strengths')}</div>
          <div className="sf-gap-list">
            {data.strengths.map((g, i) => (
              <div key={i} className="sf-gap-row sf-gap-row--strength">
                <div className="sf-gap-row-header">
                  <span className="sf-gap-label">{g.label}</span>
                  <span className="sf-gap-counts">
                    {g.actual_count} {t('sf.gap.tracked')}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.gap.portfolioFocus')}</div>
      <div className="sf-tag-list">
        {data.top_actual_categories.map((c, i) => (
          <span key={i} className="sf-trait">{c.category.replace(/_/g, ' ')} ({c.count})</span>
        ))}
      </div>
    </SectionShell>
  )
}

// ── Page root ──────────────────────────────────────────────────────────────

export default function SaffronPage({ nav }) {
  const [data,  setData]  = useState(null)
  const [error, setError] = useState(null)
  const { t, lang } = useLanguage()

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
      {nav}

      {!data && !error && <div className="sf-loading">{t('sf.loading')}</div>}

      {error && (
        <div className="sf-error">
          {t('sf.error')} — <code>python api.py</code>
        </div>
      )}

      {data && (
        <div className="sf-content">
          <CareerPosition      data={data.career_position}    t={t} />
          <MarketLandscape     data={data.market_landscape}   t={t} />
          <ComparableArtists   artists={data.peer_artists}    t={t} />
          <StrategicPathway    data={data.pathway}            t={t} />
          <InstagramStrategy   data={data.instagram_strategy} t={t} />
          <AudienceGeography   data={data.audience_geography} t={t} />
          <CareerBenchmarks    data={data.career_benchmarks}  t={t} />
          <SeasonalCalendar    data={data.seasonal_calendar}  t={t} />
          <PressFeatures       data={data.press_features}     t={t} />
          <CollectorEcosystem  data={data.collector_ecosystem}t={t} />
          <CollaborationMap    data={data.collaboration_map}  t={t} />
          <GeographicExpansion data={data.geographic_expansion} t={t} />
          <PublicationLandscape data={data.publication_landscape} t={t} />
          <LongTermScenarios   data={data.long_term_scenarios} t={t} />
          <VenueTracker        data={data.venue_tracker}      t={t} />
          <OpenQuestions       data={data.open_questions}     t={t} />
          <CareerMomentum      data={data.career_momentum}      t={t} />
          <TimingIntelligence  data={data.timing_intelligence}  t={t} />
          <CareerTimeline      t={t} />
          <PricingIntelligence t={t} />
          <OpportunityGap      data={data.opportunity_gap}      t={t} />
          <LicensingLandscape  t={t} lang={lang} />
          <PressPitchMap       t={t} lang={lang} />
          <GrantLandscape      t={t} lang={lang} />
          <RevenueStreams       t={t} lang={lang} />
          <CareerDependencyMap t={t} lang={lang} />
        </div>
      )}
    </div>
  )
}
