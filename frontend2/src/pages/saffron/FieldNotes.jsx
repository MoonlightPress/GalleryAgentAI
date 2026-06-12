// Field Notes — the library. All remaining v1 Saffron research, reorganized
// under five shelves. Index cards open ONE reading pane at a time.
import { useState, Component } from 'react'
import { loc } from '../../utils/api'
import {
  LICENSING_LANDSCAPE,
  PRESS_PITCH_MAP,
  GRANT_LANDSCAPE,
  REVENUE_STREAMS,
  CAREER_DEPENDENCY_MAP,
  CAREER_TIMELINE,
  PRICING_INTELLIGENCE,
} from './data/saffron_insights'

// ── Per-shelf error boundary (one bad data shape never blanks the page) ─────
export class NoteBoundary extends Component {
  constructor(props) { super(props); this.state = { error: null } }
  static getDerivedStateFromError(err) { return { error: err } }
  render() {
    if (this.state.error) {
      return <div className="card card--quiet sv-failed">{this.props.fallback}</div>
    }
    return this.props.children
  }
}

// ── Tiny shared pieces ──────────────────────────────────────────────────────
const Label = ({ children, style }) => <div className="sfn-label" style={style}>{children}</div>
const Callout = ({ children, rose }) => (
  <div className={`sfn-callout${rose ? ' sfn-callout--rose' : ''}`}>{children}</div>
)
const Empty = ({ msg }) => <p className="sfn-empty">{msg}</p>

// warm token palettes (replaces v1's cold hex values)
const ASSESS = {
  strong: 'var(--leaf-deep)', on_track: 'var(--leaf)', below_typical: 'var(--gold-deep)',
  weak: 'var(--rose-deep)', unknown: 'var(--ink-muted)',
}
const ASSESS_KEYS = {
  strong: 'sf.assess.strong', on_track: 'sf.assess.on_track',
  below_typical: 'sf.assess.below_typical', weak: 'sf.assess.weak', unknown: 'sf.assess.unknown',
}
const TIER = { now: 'var(--leaf-deep)', near_term: 'var(--gold-deep)', medium_term: 'var(--ink-muted)' }
const PROB = { high: 'var(--leaf-deep)', moderate: 'var(--gold-deep)', low: 'var(--rose-deep)' }
const TRAJ = { early: 'var(--gold-deep)', accelerating: 'var(--leaf-deep)', steady: 'var(--gold-deep)', stalling: 'var(--rose-deep)' }
const VSTATUS = {
  ready_to_review: ['sf.status.readyReview', 'var(--gold-deep)'],
  ready_to_contact: ['sf.status.readyContact', 'var(--leaf-deep)'],
  contacted: ['sf.status.contacted', 'var(--leaf)'],
  not_contacted: ['sf.status.notContacted', 'var(--ink-muted)'],
}
const DEPDOT = { current: 'var(--leaf-deep)', next: 'var(--gold-deep)', future: 'var(--ink-muted)', horizon: 'var(--ink-muted)' }

// ── Note renderers (ported from v1, simplified to v2 primitives) ────────────

function RecordNote({ d, t }) {
  return (
    <div className="sfn-twocol">
      <div>
        <Label>{t('sf.label.exhibitions')}</Label>
        {(d.exhibitions || []).map((ex, i) => (
          <div key={i} className="sfn-row">
            <div className="sfn-row-head">
              <span className="sfn-row-title">{ex.title}</span>
              <span className="chip-verified">✓</span>
            </div>
            <div className="sfn-row-sub">{ex.venue} · {ex.date}</div>
            <div className="sfn-row-note">{ex.type} · {ex.note}</div>
          </div>
        ))}
        <Label>{t('sf.label.publications')}</Label>
        {(d.publications || []).map((p, i) => (
          <div key={i} className="sfn-row">
            <span className="sfn-row-title">{p.title}{p.year ? ` (${p.year})` : ''}</span>
            <div className="sfn-row-sub">{p.type}</div>
          </div>
        ))}
      </div>
      <div>
        <Label>{t('sf.label.social')}</Label>
        {(d.social || []).map((s, i) => (
          <div key={i} className="sfn-row">
            <span className="sfn-row-title">{s.platform} · {s.handle}</span>
            <div className="sfn-row-sub">{s.followers}{s.posts != null ? ` · ${s.posts} ${t('sf.label.posts')}` : ''}</div>
          </div>
        ))}
        <Label>{t('sf.label.education')}</Label>
        <div className="sfn-row-title">{d.education?.institution}</div>
        <div className="sfn-row-sub">{d.education?.field} · {d.education?.note}</div>
        <Label>{t('sf.label.base')}</Label>
        <div className="sfn-row-title">{d.base}</div>
      </div>
    </div>
  )
}

function InstagramNote({ d, t }) {
  return (
    <div className="sfn-twocol">
      <div>
        <Label>{t('sf.label.social')}</Label>
        {(d.platforms || []).map((p, i) => (
          <div key={i} className="sfn-row">
            <div className="sfn-row-head">
              <span className="sfn-row-title">{p.name}</span>
              <span className="sfn-row-sub">{p.handle}</span>
            </div>
            <div className="sfn-row-sub">{p.followers ?? '—'}{p.posts != null ? ` · ${p.posts} ${t('sf.label.posts')}` : ''}</div>
            {p.note && <div className="sfn-row-note">{p.note}</div>}
          </div>
        ))}
      </div>
      <div>
        <div className="sfn-row-title" style={{ marginBottom: 4 }}>{d.known?.diary_practice}</div>
        <div className="sfn-row-sub">{d.known?.content_type}</div>
        {d.known?.posting_frequency && (
          <>
            <Label>{t('sf.label.postingFreq')}</Label>
            <span className="sfn-bubble">{d.known.posting_frequency}</span>
          </>
        )}
        {(d.missing || []).length > 0 && (
          <>
            <Label>{t('pp.ig.missing')}</Label>
            {d.missing.map((m, i) => (
              <div key={i} className="sfn-row">
                <span className="sfn-tag">{t('sf.missing.askPepper', { label: m.field })}</span>
                <div className="sfn-row-note">{m.reason}</div>
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  )
}

function AudienceGeoNote({ d, t }) {
  if (d.available && d.artist_report) {
    return (
      <div>
        <Label>{t('sf.label.artistReport')}</Label>
        <span className="sfn-bubble">{d.artist_report}</span>
        <Label>{t('sf.label.whyMatters')}</Label>
        <p className="sfn-row-note">{d.why_it_matters}</p>
      </div>
    )
  }
  return (
    <div>
      <Empty msg={d.reason ?? ''} />
      <Label>{t('sf.label.whyMatters')}</Label>
      <p className="sfn-row-note">{d.why_it_matters}</p>
      <Label>{t('sf.label.hypothesis')}</Label>
      <p className="sfn-row-note">{d.hypothesis}</p>
      <Label>{t('sf.label.askPepper')}</Label>
      <p className="sfn-row-note">{d.what_peppercorn_should_ask}</p>
    </div>
  )
}

function PressNote({ d, t }) {
  return (
    <div className="sfn-twocol">
      <div>
        <Label>{t('sf.label.confirmed')}</Label>
        {(d.confirmed || []).map((f, i) => (
          <div key={i} className="sfn-row">
            <div className="sfn-row-head">
              <span className="sfn-row-title">{f.outlet}</span>
              <span className="sfn-row-sub">{f.type}</span>
            </div>
            <div className="sfn-row-note">{f.note}</div>
          </div>
        ))}
        <Label>{t('sf.label.artPress')}</Label>
        <Empty msg={d.art_press?.reason ?? ''} />
        <Label>{t('sf.label.japanMedia')}</Label>
        <Empty msg={d.japan_coverage?.reason ?? ''} />
      </div>
      <div>
        <Label>{t('sf.label.pitchTargets')}</Label>
        {(d.pitch_targets || []).map((p, i) => (
          <div key={i} className="sfn-row">
            <span className="sfn-row-title">{p.outlet}</span>
            <div className="sfn-row-note">{p.why}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

function PressPitchNote({ t, lang }) {
  const d = PRESS_PITCH_MAP
  const outlets = d.items.filter(it => it.name)
  const discovery = d.items.find(it => it.category_note)
  return (
    <div>
      {outlets.map((it, i) => (
        <div key={i} className="sfn-row">
          <div className="sfn-row-head">
            <span className="sfn-row-title">{it.name}</span>
            <span className="sfn-row-sub">{loc(it, 'type', lang)}</span>
          </div>
          <div className="sfn-row-note">{loc(it, 'why_fits', lang)}</div>
          {it.how_to_pitch && <div className="sfn-meta"><strong>{t('sf.label.pitchColon')}</strong>{loc(it, 'how_to_pitch', lang)}</div>}
          {it.contact && <div className="sfn-meta"><strong>{t('sf.label.contactColon')}</strong>{it.contact}</div>}
          {it.timeline && <div className="sfn-meta"><strong>{t('sf.label.timelineColon')}</strong>{loc(it, 'timeline', lang)}</div>}
        </div>
      ))}
      {discovery && (
        <Callout>
          <strong>{loc(discovery, 'category_note', lang)}</strong> — {loc(discovery, 'how_discovered', lang)}
        </Callout>
      )}
    </div>
  )
}

function PricingNote({ t }) {
  const d = PRICING_INTELLIGENCE
  const { originals, prints, zines } = d.current_range
  return (
    <div>
      <p className="sfn-row-sub">{d.source_note}</p>
      <Label>{t('sf.pricing.currentRanges')}</Label>
      <div className="sfn-ranges">
        {[originals, prints, zines].map((r, i) => (
          <div key={i} className="sfn-range">
            <div className="sfn-row-sub">{r.label}</div>
            <div className="sfn-range-val">¥{r.low.toLocaleString()} – ¥{r.high.toLocaleString()}</div>
            <div className="sfn-row-note">{r.note}</div>
            {r.sweet_spot && <div className="sfn-meta">{r.sweet_spot}</div>}
          </div>
        ))}
      </div>
      <Label>{t('sf.pricing.whatAffectsPrice')}</Label>
      {d.what_affects_price.map((f, i) => (
        <div key={i} className="sfn-row">
          <div className="sfn-row-head">
            <span className="sfn-row-title">{f.factor}</span>
            <span className="sfn-badge" style={{ color: f.impact === 'high' ? 'var(--leaf-deep)' : f.impact === 'medium' ? 'var(--gold-deep)' : 'var(--ink-muted)' }}>
              {t(`sf.pricing.impact.${f.impact}`)}
            </span>
          </div>
          <div className="sfn-row-note">{f.note}</div>
        </div>
      ))}
      <Callout rose>
        <strong>{t('sf.pricing.editionDiscipline')}</strong> — {d.edition_discipline.rule} {d.edition_discipline.current_gap}
      </Callout>
      <Label>{t('sf.pricing.credibilitySignals')}</Label>
      <ul className="sfn-list">
        {d.credibility_signals.map((s, i) => <li key={i}>{s}</li>)}
      </ul>
    </div>
  )
}

function RevenueNote({ t, lang }) {
  const d = REVENUE_STREAMS
  const streams = d.items.filter(it => it.stream !== 'Summary assessment')
  const summary = d.items.find(it => it.stream === 'Summary assessment')
  return (
    <div>
      {streams.map((it, i) => (
        <div key={i} className="sfn-row">
          <div className="sfn-row-head">
            <span className="sfn-row-title">{loc(it, 'stream', lang)}</span>
            {it.realistic_monthly && <span className="sfn-badge" style={{ color: 'var(--gold-deep)' }}>{it.realistic_monthly}</span>}
            {it.leaving_on_table && <span className="chip-caution">{t('sf.label.gapTag')}</span>}
          </div>
          <div className="sfn-row-note">{loc(it, 'description', lang)}</div>
          {it.pricing && <div className="sfn-meta">{loc(it, 'pricing', lang)}</div>}
          {it.why_now && <div className="sfn-meta">{loc(it, 'why_now', lang)}</div>}
          {it.action && <div className="sfn-meta"><strong>{t('sf.label.actionColon')}</strong>{loc(it, 'action', lang)}</div>}
        </div>
      ))}
      {summary && (
        <Callout rose>
          <strong>{t('sf.label.assessmentTitle')}</strong> — {loc(summary, 'description', lang)}
        </Callout>
      )}
    </div>
  )
}

function LicensingNote({ t, lang }) {
  const d = LICENSING_LANDSCAPE
  return (
    <div>
      {d.items.map((group, gi) => (
        <div key={gi}>
          <Label>{loc(group, 'category', lang)}</Label>
          {group.entries.map((e, ei) => (
            <div key={ei} className="sfn-row">
              <div className="sfn-row-head">
                <span className="sfn-row-title">{e.name}</span>
                <span className="sfn-badge" style={{ color: TIER[e.tier] || 'var(--ink-muted)' }}>{t(`sf.tier.${e.tier}`)}</span>
              </div>
              <div className="sfn-row-note">{loc(e, 'note', lang)}</div>
            </div>
          ))}
        </div>
      ))}
    </div>
  )
}

function GrantNote({ t, lang }) {
  const d = GRANT_LANDSCAPE
  const grants = d.items.filter(it => it.name)
  const strategy = d.items.find(it => it.category_note)
  return (
    <div>
      {grants.map((g, i) => (
        <div key={i} className="sfn-row">
          <div className="sfn-row-head">
            <span className="sfn-row-title">{g.name}</span>
            <span className="sfn-row-sub">{g.country}</span>
            <span className="sfn-badge" style={{ color: 'var(--gold-deep)' }}>{g.amount}</span>
          </div>
          <div className="sfn-row-note">{loc(g, 'why_apply', lang)}</div>
          {g.eligibility && <div className="sfn-meta"><strong>{t('sf.label.eligibilityColon')}</strong>{loc(g, 'eligibility', lang)}</div>}
          {g.deadline && <div className="sfn-meta"><strong>{t('sf.label.deadlineColon')}</strong>{g.deadline}</div>}
          {g.competition && <div className="sfn-meta"><strong>{t('sf.label.competitionColon')}</strong>{loc(g, 'competition', lang)}</div>}
          {g.tip && <div className="sfn-meta"><strong>{t('sf.label.tipColon')}</strong>{loc(g, 'tip', lang)}</div>}
        </div>
      ))}
      {strategy && (
        <Callout>
          <strong>{loc(strategy, 'category_note', lang)}</strong> — {loc(strategy, 'note', lang)}
        </Callout>
      )}
    </div>
  )
}

function CollectorNote({ d, t }) {
  return (
    <div>
      <Empty msg={d.reason} />
      <Label>{t('sf.label.whyMatters')}</Label>
      <p className="sfn-row-note">{d.why_it_matters}</p>
      <Label>{t('sf.label.fairsPipeline')}</Label>
      <div>{(d.fairs_in_pipeline || []).map((f, i) => <span key={i} className="sfn-tag">{f}</span>)}</div>
      <p className="sfn-row-note" style={{ marginTop: 8 }}>{d.known_gap}</p>
      <Label>{t('sf.label.askPepper')}</Label>
      <p className="sfn-row-note">{d.what_peppercorn_should_ask}</p>
    </div>
  )
}

function VenueNote({ d, t }) {
  if (!d.tracked?.length) return <Empty msg={t('sf.empty.venues')} />
  return (
    <div>
      <div className="sfn-scroll">
        {d.tracked.map((v, i) => {
          const [key, color] = VSTATUS[v.status] || VSTATUS.not_contacted
          return (
            <div key={i} className="sfn-row">
              <div className="sfn-row-head">
                <span className="sfn-row-title">{v.name}</span>
                <span className="sfn-row-sub">{v.type} · {v.city}</span>
                <span className="sfn-badge" style={{ color }}>{t(key)}</span>
                {v.priority && <span className="sfn-tag">{t('sf.venue.priority', { n: v.priority })}</span>}
              </div>
              <div className="sfn-meta">
                {v.last_contacted ? t('sf.venue.lastContacted', { date: v.last_contacted }) : t('sf.venue.notContacted')}
              </div>
              {v.next_action && <div className="sfn-row-note">{v.next_action}</div>}
            </div>
          )
        })}
      </div>
      {d.gap_note && <Callout>{d.gap_note}</Callout>}
    </div>
  )
}

function CollabNote({ d, t }) {
  return (
    <div className="sfn-twocol">
      <div>
        <Label>{t('sf.label.knownCoExhib')}</Label>
        {(d.known_co_exhibitors || []).map((a, i) => (
          <div key={i} className="sfn-row">
            <div className="sfn-row-head">
              <span className="sfn-row-title">{a.name}</span>
              <span className="sfn-row-sub">{a.context}</span>
            </div>
            <div className="sfn-meta">{t('sf.label.currentStatus')} {a.current_status}</div>
          </div>
        ))}
        <p className="sfn-row-note" style={{ marginTop: 10 }}>{d.note}</p>
      </div>
      <div>
        <Label>{t('sf.label.tokyoPeerNet')}</Label>
        <Empty msg={d.peer_network?.reason ?? ''} />
        <Label>{t('sf.label.whyMatters')}</Label>
        <p className="sfn-row-note">{d.peer_network?.why_it_matters}</p>
      </div>
    </div>
  )
}

function GeoExpansionNote({ d, t }) {
  return (
    <div>
      {(d.regions || []).map((r, i) => (
        <div key={i} className="sfn-row">
          <div className="sfn-row-head">
            <span className="sfn-row-title">{r.name}</span>
            {r.pipeline_count > 0 && <span className="sfn-row-sub">{t('sf.inPipeline', { n: r.pipeline_count })}</span>}
            <span className="sfn-tag">{t(`sf.geo.${r.status}`)}</span>
          </div>
          <div className="sfn-row-note">{r.note}</div>
          {r.entry_point && <div className="sfn-meta"><strong>{t('sf.label.entryPoint')}</strong> {r.entry_point}</div>}
        </div>
      ))}
    </div>
  )
}

function PublicationNote({ d, t }) {
  return (
    <div className="sfn-twocol">
      <div>
        <Label>{t('sf.label.herPubs')}</Label>
        {(d.artist_publications || []).map((p, i) => (
          <div key={i} className="sfn-row">
            <span className="sfn-row-title">{p.title}{p.year ? ` · ${p.year}` : ''}</span>
            <div className="sfn-row-sub">{p.type}</div>
            {p.note && <div className="sfn-row-note">{p.note}</div>}
          </div>
        ))}
        {d.artist_intent && (
          <>
            <Label>{t('sf.label.pubIntent')}</Label>
            <span className="sfn-bubble">{d.artist_intent}</span>
          </>
        )}
        <Label>{t('sf.label.pubTiers')}</Label>
        {(d.tiers || []).map((tier, i) => (
          <div key={i} className="sfn-row">
            <div className="sfn-row-head">
              <span className="sfn-row-title">{tier.tier}</span>
              <span className="sfn-tag">{t(`sf.barrier.${tier.barrier}`)}</span>
            </div>
            <div className="sfn-row-sub">{(tier.examples || []).join(' · ')}</div>
            <div className="sfn-row-note">{tier.note}</div>
          </div>
        ))}
      </div>
      <div>
        <Label>{t('sf.label.topTargets', { n: (d.top_targets || []).length })}</Label>
        <div className="sfn-scroll">
          {(d.top_targets || []).map((o, i) => (
            <div key={i} className="sfn-row">
              <span className="sfn-row-title">{o.name}</span>
              <div className="sfn-row-sub">{o.category}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function CalendarNote({ d, t }) {
  return (
    <div>
      {(d.months || []).length === 0
        ? <Empty msg={t('sf.empty.calendar')} />
        : d.months.map((m, i) => (
          <div key={i}>
            <Label>{m.month}</Label>
            {m.opportunities.map((o, j) => (
              <div key={j} className="sfn-row">
                <div className="sfn-row-head">
                  <span className="sfn-tag">{o.category}</span>
                  <span className="sfn-row-title">{o.name}</span>
                  <span className="sfn-row-sub">{o.deadline}</span>
                </div>
              </div>
            ))}
          </div>
        ))
      }
      {(d.rolling || []).length > 0 && (
        <>
          <Label>{t('sf.label.rolling', { n: d.rolling.length })}</Label>
          <div>{d.rolling.map((o, i) => <span key={i} className="sfn-tag">{o.name}</span>)}</div>
        </>
      )}
      <p className="sfn-row-sub" style={{ marginTop: 12 }}>{d.coverage_note}</p>
      <Label>{t('sf.label.prepLeadTimes')}</Label>
      {Object.entries(d.preparation_lead_times || {}).map(([k, v], i) => (
        <div key={i} className="sfn-meta"><strong>{k.replace(/_/g, ' ')}</strong> — {v}</div>
      ))}
    </div>
  )
}

function TimingNote({ d, t }) {
  const maxCount = Math.max(...(d.monthly_counts || []).map(m => m.count), 1)
  return (
    <div>
      <Callout>{d.key_insight}</Callout>
      <Label>{t('sf.timing.deadlinesByMonth')}</Label>
      <div className="sfn-chart">
        {(d.monthly_counts || []).map((m, i) => (
          <div key={i} className="sfn-chart-col">
            <span className="sfn-chart-n">{m.count || ''}</span>
            <div className="sfn-chart-track">
              <div
                className={`sfn-chart-bar${(d.peak_months || []).includes(m.month) ? ' sfn-chart-bar--peak' : ''}`}
                style={{ height: `${Math.round((m.count / maxCount) * 100)}%` }}
              />
            </div>
            <span className="sfn-chart-x">{m.month.slice(0, 3)}</span>
          </div>
        ))}
      </div>
      <div className="sfn-twocol" style={{ marginTop: 18 }}>
        <div>
          <Label>{t('sf.timing.peakMonths')}</Label>
          {(d.peak_months || []).map((m, i) => (
            <div key={i} className="sfn-meta">
              {m} — {t('sf.timing.deadlineCount', { n: (d.monthly_counts || []).find(x => x.month === m)?.count ?? 0 })}
            </div>
          ))}
          {(d.quiet_months || []).length > 0 && (
            <>
              <Label>{t('sf.timing.quietMonths')}</Label>
              {d.quiet_months.map((m, i) => <div key={i} className="sfn-meta">{m} — {t('sf.timing.quietNote')}</div>)}
            </>
          )}
        </div>
        <div>
          <Label>{t('sf.timing.coverage')}</Label>
          <div className="sfn-meta"><strong>{t('sf.timing.withDeadline')}</strong> {d.with_parsed_deadline}</div>
          <div className="sfn-meta"><strong>{t('sf.timing.rolling')}</strong> {d.rolling_count}</div>
          <div className="sfn-meta"><strong>{t('sf.timing.noDeadline')}</strong> {d.no_deadline_count}</div>
          <Label>{t('sf.timing.prepWindow')}</Label>
          <p className="sfn-row-note">{t('sf.timing.prepWindowNote')}</p>
        </div>
      </div>
    </div>
  )
}

function MomentumNote({ d, t }) {
  const { totals = {}, trajectory, monthly_chart = [], recent_activity = [] } = d
  const maxBar = Math.max(...monthly_chart.map(m => (m.submissions || 0) + (m.contacts || 0)), 1)
  return (
    <div>
      <div className="sfn-stats">
        <div className="sfn-stat"><div className="sfn-stat-n">{totals.submissions ?? 0}</div><div className="sfn-stat-label">{t('sf.mom.totalSubmissions')}</div></div>
        <div className="sfn-stat"><div className="sfn-stat-n">{totals.venues_in_crm ?? 0}</div><div className="sfn-stat-label">{t('sf.mom.venuesInCRM')}</div></div>
        <div className="sfn-stat"><div className="sfn-stat-n">{totals.responses_received ?? 0}</div><div className="sfn-stat-label">{t('sf.mom.responses')}</div></div>
        <div className="sfn-stat"><div className="sfn-stat-n" style={{ color: TRAJ[trajectory] || 'var(--gold-deep)', fontSize: '1.05rem', paddingTop: 8 }}>{t(`sf.mom.traj.${trajectory}`)}</div><div className="sfn-stat-label">{t('sf.mom.trajectory')}</div></div>
      </div>
      <Label>{t('sf.mom.activityChart')}</Label>
      <div className="sfn-chart">
        {monthly_chart.map((m, i) => (
          <div key={i} className="sfn-chart-col">
            <span className="sfn-chart-n">{(m.submissions || 0) + (m.contacts || 0) || ''}</span>
            <div className="sfn-chart-track">
              <div className="sfn-chart-bar" style={{ height: `${Math.round(((m.submissions || 0) / maxBar) * 100)}%` }} />
              <div className="sfn-chart-bar sfn-chart-bar--alt" style={{ height: `${Math.round(((m.contacts || 0) / maxBar) * 100)}%` }} />
            </div>
            <span className="sfn-chart-x">{m.month?.slice(5)}</span>
          </div>
        ))}
      </div>
      <div className="sfn-meta">
        <span className="sfn-tag" style={{ borderColor: 'var(--gold)', color: 'var(--gold-deep)' }}>{t('sf.mom.submissions')}</span>
        <span className="sfn-tag" style={{ borderColor: 'var(--leaf)', color: 'var(--leaf-deep)' }}>{t('sf.mom.contacts')}</span>
      </div>
      {recent_activity.length > 0 && (
        <>
          <Label>{t('sf.mom.recentActivity')}</Label>
          {recent_activity.map((it, i) => (
            <div key={i} className="sfn-row">
              <div className="sfn-row-head">
                <span className="sv-act-dot sv-act-dot--medium" style={{ alignSelf: 'center' }} />
                <span className="sfn-row-title">{it.name}</span>
                <span className="sfn-row-sub">{it.status}</span>
                <span className="sfn-row-sub">{it.date?.slice(0, 10)}</span>
              </div>
            </div>
          ))}
        </>
      )}
      {(totals.submissions ?? 0) === 0 && <Callout>{t('sf.mom.noSubmissionsYet')}</Callout>}
    </div>
  )
}

function ScenariosNote({ d, t }) {
  return (
    <div>
      <div className="sfn-scenarios">
        {(d.scenarios || []).map((s, i) => (
          <div key={i} className="sfn-scenario">
            <div className="sfn-row-head">
              <span className="sfn-row-title">{s.name}</span>
              <span className="sfn-badge" style={{ color: PROB[s.probability] || 'var(--gold-deep)' }}>{t(`sf.prob.${s.probability}`)}</span>
            </div>
            <div className="sfn-row-sub">{s.tagline}</div>
            <div className="sfn-row-note" style={{ marginTop: 6 }}>{s.description}</div>
            <Label>{t('sf.label.requiresNow')}</Label>
            <ul className="sfn-list">
              {(s.requires_now || []).map((r, j) => <li key={j}>{r}</li>)}
            </ul>
            <div className="sfn-meta"><strong>{t('sf.label.bottleneck')}</strong> {s.bottleneck}</div>
            <div className="sfn-meta"><strong>{t('sf.label.rightIf')}</strong> {s.best_fit_signal}</div>
          </div>
        ))}
      </div>
      <Callout><span className="voice">{d.saffron_view}</span></Callout>
    </div>
  )
}

function TimelineNote({ t }) {
  const d = CAREER_TIMELINE
  return (
    <div>
      <Callout>{d.overall_assessment}</Callout>
      <Label>{t('sf.timeline.artistStage')}</Label>
      <div>
        <span className="sfn-tag">{t('sf.timeline.age', { n: d.artist_stage.age })}</span>
        <span className="sfn-tag">{t('sf.timeline.groupShow', { n: d.artist_stage.group_shows, s: d.artist_stage.group_shows !== 1 ? 's' : '' })}</span>
        <span className="sfn-tag">{t('sf.timeline.publications', { n: d.artist_stage.publications, s: d.artist_stage.publications !== 1 ? 's' : '' })}</span>
        {d.artist_stage.instagram && <span className="sfn-tag">Instagram {d.artist_stage.instagram}</span>}
      </div>
      {d.peers.map((p, i) => (
        <div key={i} className="sfn-row">
          <div className="sfn-row-head">
            <span className="sfn-row-title">{p.name}</span>
            <span className="sfn-row-sub">{p.region} · {p.comparable_age}</span>
          </div>
          <Label style={{ margin: '0.4rem 0 0.2rem' }}>{t('sf.timeline.hadAtStage')}</Label>
          <ul className="sfn-list">
            {(p.at_stage?.had || []).map((h, j) => <li key={j}>{h}</li>)}
          </ul>
          <div className="sfn-row-note">{p.comparison}</div>
        </div>
      ))}
    </div>
  )
}

function BenchmarksNote({ d, t }) {
  return (
    <div>
      <p className="sfn-row-note">{d.summary}</p>
      {(d.peer_range || []).map((row, i) => (
        <div key={i} className="sfn-row">
          <div className="sfn-row-head">
            <span className="sfn-row-title">{row.dimension}</span>
            <span className="sfn-badge" style={{ color: ASSESS[row.assessment] || ASSESS.on_track }}>
              {t(ASSESS_KEYS[row.assessment] || 'sf.assess.on_track')}
            </span>
          </div>
          <div className="sfn-meta"><strong>{row.artist_value}</strong> · {t('sf.label.peers')} {row.peer_low} → {row.peer_typical} → {row.peer_high}</div>
          <div className="sfn-row-note">{row.note}</div>
        </div>
      ))}
    </div>
  )
}

function OppGapNote({ d, t }) {
  return (
    <div>
      <Callout>{d.summary}</Callout>
      {(d.gaps || []).length > 0 && (
        <>
          <Label>{t('sf.gap.underrepresented')}</Label>
          {d.gaps.map((g, i) => (
            <div key={i} className="sfn-row">
              <div className="sfn-row-head">
                <span className="sfn-row-title">{g.label}</span>
                <span className="sfn-row-sub">{g.actual_count} {t('sf.gap.vs')} ~{g.expected_count} {t('sf.gap.expected')}</span>
              </div>
              <div className="sfn-row-note">{g.note}</div>
            </div>
          ))}
        </>
      )}
      {(d.strengths || []).length > 0 && (
        <>
          <Label>{t('sf.gap.strengths')}</Label>
          {d.strengths.map((g, i) => (
            <div key={i} className="sfn-meta">{g.label} — {g.actual_count} {t('sf.gap.tracked')}</div>
          ))}
        </>
      )}
      <Label>{t('sf.gap.portfolioFocus')}</Label>
      <div>
        {(d.top_actual_categories || []).map((c, i) => (
          <span key={i} className="sfn-tag">{c.category.replace(/_/g, ' ')} ({c.count})</span>
        ))}
      </div>
    </div>
  )
}

function DepMapNote({ t, lang }) {
  const d = CAREER_DEPENDENCY_MAP
  return (
    <div>
      {d.milestones.map((m, mi) => (
        <div key={mi}>
          <div className="sfn-row-head" style={{ alignItems: 'center' }}>
            <span className="sfn-dep-dot" style={{ background: DEPDOT[m.status] || 'var(--ink-muted)' }} />
            <span className="sfn-row-title">{t(`sf.depmap.${m.status}`)}</span>
          </div>
          {m.items.map((it, ii) => (
            <div key={ii} className="sfn-row" style={{ marginLeft: '1.2rem' }}>
              <div className="sfn-meta"><strong>{t('sf.depmap.completes')}</strong> {loc(it, 'complete', lang)}</div>
              <div className="sfn-meta" style={{ marginTop: 4 }}><strong>{t('sf.depmap.unlocks')}</strong></div>
              <ul className="sfn-list">
                {(loc(it, 'unlocks', lang) || it.unlocks || []).map((u, ui) => <li key={ui}>{u}</li>)}
              </ul>
            </div>
          ))}
          {mi < d.milestones.length - 1 && <div className="sfn-dep-connector" />}
        </div>
      ))}
    </div>
  )
}

function ReadinessNote({ d, t }) {
  const tier3 = (d.readiness_scores?.tier_3_readiness ?? 0) * 100
  const tier4 = (d.readiness_scores?.tier_4_readiness ?? 0) * 100
  return (
    <div>
      <Label>{t('sf.cr.tier3Label')}</Label>
      <div className="sfn-ready-track"><div className="sfn-ready-fill" style={{ width: `${tier3}%` }} /></div>
      <div className="sfn-row-sub">{t('sf.cr.tier3Sublabel')}</div>
      <Label>{t('sf.cr.tier4Label')}</Label>
      <div className="sfn-ready-track"><div className="sfn-ready-fill" style={{ width: `${tier4}%`, opacity: 0.6 }} /></div>
      <div className="sfn-row-sub">{t('sf.cr.tier4Sublabel')}</div>
      {d.months_to_tier3 != null && (
        <div style={{ marginTop: 12 }}><span className="pill pill--count">{t('sf.cr.monthsToTier3', { n: d.months_to_tier3 })}</span></div>
      )}
      {d.next_milestone && <Callout>{d.next_milestone}</Callout>}
      {(d.blocking_gaps || []).length > 0 && (
        <>
          <Label>{t('sf.cr.blockingGaps')}</Label>
          {d.blocking_gaps.map((g, i) => (
            <div key={i} className="sfn-row">
              <span className="sfn-row-title">{g.gap}</span>
              {g.detail && <div className="sfn-row-note">{g.detail}</div>}
              {g.action && <div className="sfn-meta">{g.action}</div>}
            </div>
          ))}
        </>
      )}
    </div>
  )
}

function OpenQsNote({ d, t }) {
  return (
    <div>
      <p className="sfn-row-note" style={{ marginBottom: 12 }}>{t('sf.label.openQNote')}</p>
      {(d.questions || []).map((q, i) => (
        <div key={i} className="sfn-qrow">
          <div className="sfn-qnum">{i + 1}</div>
          <div>
            <div className="sfn-row-title">{q.question}</div>
            <div className="sfn-row-note">{q.why_it_matters}</div>
            <div className="sfn-meta">→ {q.routed_to}</div>
          </div>
        </div>
      ))}
    </div>
  )
}

// ── Shelf configuration ─────────────────────────────────────────────────────
// title/hook are (t, ctx) => string; get pulls the data the renderer needs.
const SHELVES = [
  {
    key: 'audience',
    notes: [
      { id: 'instagram',  title: t => t('sf.sec.instagram'),   hook: t => t('sf.sub.instagram'),    get: c => c.data?.instagram_strategy,  render: (c, d) => <InstagramNote d={d} t={c.t} /> },
      { id: 'audienceGeo',title: t => t('sf.sec.audienceGeo'), hook: t => t('sf.sub.audienceGeo'),  get: c => c.data?.audience_geography,  render: (c, d) => <AudienceGeoNote d={d} t={c.t} /> },
      { id: 'press',      title: t => t('sf.sec.press'),       hook: t => t('sf.sub.press'),        get: c => c.data?.press_features,      render: (c, d) => <PressNote d={d} t={c.t} /> },
      { id: 'pressPitch', title: t => t('sf.press.title'),     hook: t => t('sf.press.summary'),    get: () => true,                       render: c => <PressPitchNote t={c.t} lang={c.lang} /> },
    ],
  },
  {
    key: 'money',
    notes: [
      { id: 'pricing',    title: t => t('sf.sec.pricing'),     hook: t => t('sf.sum.pricing'),      get: () => true,                       render: c => <PricingNote t={c.t} /> },
      { id: 'revenue',    title: t => t('sf.revenue.title'),   hook: t => t('sf.revenue.summary'),  get: () => true,                       render: c => <RevenueNote t={c.t} lang={c.lang} /> },
      { id: 'licensing',  title: t => t('sf.licensing.title'), hook: t => t('sf.licensing.summary'),get: () => true,                       render: c => <LicensingNote t={c.t} lang={c.lang} /> },
      { id: 'grants',     title: t => t('sf.grant.title'),     hook: t => t('sf.grant.summary'),    get: () => true,                       render: c => <GrantNote t={c.t} lang={c.lang} /> },
      { id: 'collectors', title: t => t('sf.sec.collector'),   hook: t => t('sf.sub.collector'),    get: c => c.data?.collector_ecosystem, render: (c, d) => <CollectorNote d={d} t={c.t} /> },
    ],
  },
  {
    key: 'places',
    notes: [
      { id: 'venues',     title: t => t('sf.sec.venues'),      hook: t => t('sf.sub.venues'),       get: c => c.data?.venue_tracker,        render: (c, d) => <VenueNote d={d} t={c.t} /> },
      { id: 'collab',     title: t => t('sf.sec.collab'),      hook: t => t('sf.sub.collab'),       get: c => c.data?.collaboration_map,    render: (c, d) => <CollabNote d={d} t={c.t} /> },
      { id: 'geo',        title: t => t('sf.sec.geoExpansion'),hook: t => t('sf.sub.geoExpansion'), get: c => c.data?.geographic_expansion, render: (c, d) => <GeoExpansionNote d={d} t={c.t} /> },
      { id: 'publication',title: t => t('sf.sec.publication'), hook: t => t('sf.sub.publication'),  get: c => c.data?.publication_landscape,render: (c, d) => <PublicationNote d={d} t={c.t} /> },
    ],
  },
  {
    key: 'timing',
    notes: [
      { id: 'calendar',   title: t => t('sf.sec.calendar'),    hook: t => t('sf.sub.calendar'),     get: c => c.data?.seasonal_calendar,    render: (c, d) => <CalendarNote d={d} t={c.t} /> },
      { id: 'timing',     title: t => t('sf.sec.timing'),      hook: t => t('sf.sub.timing'),       get: c => c.data?.timing_intelligence,  render: (c, d) => <TimingNote d={d} t={c.t} /> },
      { id: 'momentum',   title: t => t('sf.sec.momentum'),    hook: t => t('sf.sub.momentum'),     get: c => c.data?.career_momentum,      render: (c, d) => <MomentumNote d={d} t={c.t} /> },
    ],
  },
  {
    key: 'longview',
    notes: [
      { id: 'record',     title: t => t('sf.sec.careerPosition'), hook: t => t('sf.sub.careerPosition'), get: c => c.data?.career_position, render: (c, d) => <RecordNote d={d} t={c.t} /> },
      { id: 'scenarios',  title: t => t('sf.sec.longTerm'),    hook: (t, c) => t('sf.sub.longTerm', { horizon: c.data?.long_term_scenarios?.horizon ?? '' }), get: c => c.data?.long_term_scenarios, render: (c, d) => <ScenariosNote d={d} t={c.t} /> },
      { id: 'timeline',   title: t => t('sf.sec.careerTimeline'), hook: t => t('sf.sum.careerTimeline'), get: () => true,                  render: c => <TimelineNote t={c.t} /> },
      { id: 'benchmarks', title: t => t('sf.sec.benchmarks'),  hook: t => t('sf.sub.benchmarks'),   get: c => c.data?.career_benchmarks,    render: (c, d) => <BenchmarksNote d={d} t={c.t} /> },
      { id: 'oppGap',     title: t => t('sf.sec.oppGap'),      hook: t => t('sf.sub.oppGap'),       get: c => c.data?.opportunity_gap,      render: (c, d) => <OppGapNote d={d} t={c.t} /> },
      { id: 'depmap',     title: t => t('sf.depmap.title'),    hook: t => t('sf.depmap.summary'),   get: () => true,                        render: c => <DepMapNote t={c.t} lang={c.lang} /> },
      { id: 'readiness',  title: t => t('sf.cr.title'),        hook: t => t('sf.cr.subtitle'),      get: c => c.careerData,                 render: (c, d) => <ReadinessNote d={d} t={c.t} /> },
      { id: 'openQs',     title: t => t('sf.sec.openQs'),      hook: t => t('sf.sub.openQs'),       get: c => c.data?.open_questions,       render: (c, d) => <OpenQsNote d={d} t={c.t} /> },
    ],
  },
]

// ── Library component (single-open accordion across all shelves) ────────────
export default function FieldNotes({ data, careerData, t, t2, lang }) {
  const [openId, setOpenId] = useState(null)
  const ctx = { data, careerData, t, lang }

  return (
    <section>
      <div className="sec-head sec-head--leaf">
        <h2 className="h-section">{t2('v2.saffron.notes.title')}</h2>
        <p className="sec-sub voice">{t2('v2.saffron.notes.sub')}</p>
      </div>

      {SHELVES.map(shelf => {
        const openNote = shelf.notes.find(n => n.id === openId)
        return (
          <NoteBoundary key={shelf.key} fallback={t2('v2.saffron.section.failed')}>
            <div className="sv-shelf">
              <h3 className="sv-shelf-title">{t2(`v2.saffron.shelf.${shelf.key}`)}</h3>
              <div className="sv-note-grid">
                {shelf.notes.map(n => (
                  <button
                    key={n.id}
                    className={`card sv-note-card${openId === n.id ? ' sv-note-card--open' : ''}`}
                    onClick={() => setOpenId(openId === n.id ? null : n.id)}
                    aria-expanded={openId === n.id}
                  >
                    <div className="sv-note-title">{n.title(t, ctx)}</div>
                    <div className="sv-note-hook clamp-2">{n.hook(t, ctx)}</div>
                  </button>
                ))}
              </div>
              {openNote && (
                <div className="card sv-pane">
                  <div className="sv-pane-head">
                    <h4 className="h-card">{openNote.title(t, ctx)}</h4>
                    <button className="btn-ghost" onClick={() => setOpenId(null)}>{t2('v2.saffron.note.close')}</button>
                  </div>
                  <NoteBoundary key={openNote.id} fallback={t2('v2.saffron.section.failed')}>
                    {(() => {
                      const d = openNote.get(ctx)
                      return d ? openNote.render(ctx, d) : <Empty msg={t2('v2.saffron.note.empty')} />
                    })()}
                  </NoteBoundary>
                </div>
              )}
            </div>
          </NoteBoundary>
        )
      })}
    </section>
  )
}
