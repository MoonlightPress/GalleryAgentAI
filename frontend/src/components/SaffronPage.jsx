import { useState, useEffect, useMemo, Component } from 'react'
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

// Saffron's analysis body is authored in English in api.py. When the viewer is
// reading in Chinese, we translate every served string client-side via this map
// (unmapped strings pass through unchanged — graceful partial coverage).
function deepTranslate(obj, map) {
  if (typeof obj === 'string') return map[obj] || obj
  if (Array.isArray(obj)) return obj.map(x => deepTranslate(x, map))
  if (obj && typeof obj === 'object') {
    const out = {}
    for (const k in obj) out[k] = deepTranslate(obj[k], map)
    return out
  }
  return obj
}

const SF_ZH = {
  // ── Open questions (she reads + answers these) ──
  "What's your current Instagram posting frequency?": "你目前在 Instagram 上的发布频率是多少？",
  "With a 26k Instagram following, the account is established and growing. Cadence is the most controllable variable for maximising reach on the platform galleries, publishers, and curators actually use for discovery. Without knowing current frequency, no posting strategy can be recommended.": "你已有 2.6 万 Instagram 粉丝，账号已确立并在增长。发布节奏是提升触及最可控的变量——而画廊、出版社与策展人正是用这个平台来发掘新人。在不知道当前频率的情况下，无法给出任何发布策略建议。",
  "Where is your audience located geographically?": "你的受众主要分布在哪些地区？",
  "A primarily Chinese-language following changes the geographic expansion strategy entirely — it suggests China reentry before European expansion.": "如果粉丝以中文受众为主，整个地域拓展策略都会不同——这意味着应先重返中国市场，再考虑欧洲。",
  "Have you sold work, and through which channels?": "你卖出过作品吗？通过哪些渠道？",
  "Sales history reveals which formats and price points convert — this shapes which fairs and platforms are worth prioritising.": "销售记录能揭示哪些形式与价位真正能成交——这决定了哪些博览会与平台值得优先投入。",
  "Is a new publication or zine in progress?": "你目前是否在筹备新的出版物或独立刊物？",
  "If you're already planning one, this should support it — not pitch it as a new idea.": "如果你已经在筹备，系统应当支持它——而不是把它当作一个全新的点子来推荐。",
  "Do you have a current artist statement in any language?": "你是否已有一份（任意语言的）现行艺术家自述？",
  "Most open calls and gallery submissions require one. If none exists, this is the most urgent gap before any submissions.": "大多数公开征集与画廊投递都需要它。如果还没有，这是你开始任何投递前最紧迫的空缺。",
  "Are you still in contact with your Tide from China co-exhibitors?": "你和「潮自中国」联展的其他参展者还有联系吗？",
  "If those 5 artists are Tokyo-based and active, they are the most natural group show partners. If they've dispersed, that network is dormant.": "如果那 5 位艺术家身在东京且仍活跃，他们就是最自然的联展伙伴。如果已各奔东西，这个人脉网络便处于休眠状态。",
  "Do you have a second Japan exhibition in progress?": "你目前是否在筹备第二场日本展览？",
  "There's one show on record, so the read assumes 2–3 more group shows would help — but you may already have one underway. If so, tell me here.": "记录在册的只有一场展览，因此分析假设再参与 2–3 场联展会有帮助——但你也许已经有一场在进行中。如果是，请在这里告诉我。",
  "What price points do you use for originals and prints?": "你的原作和印刷品定价大约是多少？",
  "Pricing determines which collector tier and which fairs are appropriate. Under-pricing is common at this stage and affects how galleries perceive the work.": "定价决定了适合哪一层级的藏家与哪些博览会。在这个阶段定价偏低很常见，并会影响画廊对作品的看法。",

  // ── Career paths (long-term scenarios) ──
  "Gallery Track": "画廊路线",
  "Primary identity as a gallery artist.": "以画廊艺术家为主要身份。",
  "Solo shows, institutional open calls, gallery representation by 30.": "个展、机构公开征集，30 岁前获得画廊代理。",
  "Exhibition history is thin. 2–3 more group shows are required before any gallery will discuss a solo show.": "展览经历尚浅。在任何画廊愿意谈个展之前，还需要 2–3 场联展。",
  "Right if you're primarily motivated by the physical exhibition experience and gallery community.": "如果你最看重实体展览的体验与画廊圈子，这条路最适合你。",
  "Publication Track": "出版路线",
  "Primary identity as an illustrator and artist-book maker.": "以插画家与艺术书创作者为主要身份。",
  "Second solo book, international distribution, major book fairs by 30.": "30 岁前完成第二本个人作品集、国际发行、参与重要书展。",
  "No new publication since 2021. The content exists — it needs packaging.": "自 2021 年以来没有新出版物。内容已经具备——只差整理成册。",
  "Right if you're motivated by the book as object and the publishing community. Your formation already points here.": "如果你着迷于书作为实体，以及出版社群，这条路最适合你。你的成长背景本就指向这里。",
  "Hybrid Track": "复合路线",
  "Artist-publisher: books and gallery shows running in parallel.": "艺术家兼出版者：书与画廊展览并行。",
  "The book practice feeds the gallery presence and vice versa. Bookshop gallery shows bridge both worlds.": "出版实践滋养画廊呈现，反之亦然。书店画廊展览连接两个世界。",
  "Requires more energy and time management than either single track.": "比任何单一路线都更考验精力与时间管理。",
  "The most natural fit given your existing practice. The daily diary is simultaneously publication material and gallery-worthy work.": "鉴于你现有的实践，这是最自然的选择。每日水彩日记既是出版素材，也是值得展出的作品。",
  "The Hybrid Track is the best structural fit. The bookshop gallery show is the single highest-leverage action — it advances both tracks with one move.": "复合路线在结构上最契合。书店画廊展览是单一杠杆最高的行动——一步同时推进两条路线。",
  "Age 30 (approximately 4 years from now)": "30 岁（大约从现在起 4 年后）",
}

class SectionErrorBoundary extends Component {
  constructor(props) { super(props); this.state = { error: null } }
  static getDerivedStateFromError(err) { return { error: err } }
  render() {
    if (this.state.error) {
      return (
        <div style={{ padding: '12px 16px', background: '#fff8ee', border: '1px solid #e8c97a', borderRadius: 6, margin: '8px 0', fontFamily: 'Georgia, serif', fontSize: 13, color: '#7a4a1a' }}>
          A section failed to render: <code style={{ fontSize: 11 }}>{String(this.state.error)}</code>
        </div>
      )
    }
    return this.props.children
  }
}

// ── Shared primitives ──────────────────────────────────────────────────────

function SectionShell({ title, subtitle, summary, defaultOpen = true, children }) {
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

// Any external name (venue, outlet) → a search link so she can look it up.
function sfSearch(name) {
  return `https://www.google.com/search?q=${encodeURIComponent(name || '')}`
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
  const tokyoPct = Math.round((data.tokyo_vs_international.tokyo / (geoTotal || 1)) * 100)
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

// Confirmed Instagram handles for the comparable artists (verified Jun 2026).
// Anyone not listed falls back to a name search.
const PEER_IG = {
  'Chien Chung-Wei (簡忠威)': 'chien_chung_wei',
  'Keiko Tanabe':            'keikotanabewatercolor',
  'Thomas W. Schaller':      'thomaswschaller',
  'Cathy Read':              'cathyreadart',
  'Alvaro Castagnet':        'alvaro.castagnet',
  'Jean Haines':             'jeanhaines',
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
            <a
              className="sf-peer-name sf-peer-link"
              href={PEER_IG[a.name] ? `https://www.instagram.com/${PEER_IG[a.name]}/` : sfSearch(`${a.name} instagram`)}
              target="_blank"
              rel="noreferrer"
            >
              {a.name} ↗
            </a>
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

function InstagramStrategy({ data, t }) {
  const ig = data.platforms.find(p => p.name === 'Instagram')
  const postingFreq = data.known?.posting_frequency

  return (
    <SectionShell
      title={t('sf.sec.instagram')}
      subtitle={t('sf.sub.instagram')}
      summary={`Instagram ${ig?.followers ?? '—'}`}
    >
      <div className="sf-two-col">
        <div>
          <div className="sf-block-label">{t('pp.ig.platform')}</div>
          {data.platforms.map((p, i) => (
            <div key={i} className="sf-platform-row">
              <div className="sf-platform-name">{p.name}</div>
              <div className="sf-platform-handle">{p.handle}</div>
              <div className="sf-platform-followers">{p.followers ?? '—'}{p.posts != null ? ` · ${p.posts} ${t('sf.label.posts')}` : ''}</div>
              <div className="sf-platform-note">{p.note}</div>
            </div>
          ))}
        </div>
        <div>
          <div className="sf-block-label">{t('pp.ig.known')}</div>
          <div className="sf-row-title" style={{ marginBottom: 6 }}>{data.known.diary_practice}</div>
          <div className="sf-row-meta">{data.known.content_type}</div>

          {data.strategy && (
            <div style={{ marginTop: 16 }}>
              <div className="sf-block-label">{t('sf.ig.strategy')}</div>
              <p className="sf-info-text">{data.strategy}</p>
            </div>
          )}

          {postingFreq && (
            <div className="sf-peppercorn-answer" style={{ marginTop: 16 }}>
              <div className="sf-block-label">{t('sf.label.postingFreq')}</div>
              <div className="sf-answer-bubble">{postingFreq}</div>
            </div>
          )}
        </div>
      </div>
    </SectionShell>
  )
}

function AudienceGeography({ data, t }) {
  // Only show when there's a real audience report — no "what's missing" meta.
  if (!data.available || !data.artist_report) return null
  return (
    <SectionShell
      title={t('sf.sec.audienceGeo')}
      subtitle={t('sf.sub.audienceGeo')}
      summary={t('sf.sum.audienceGeo.live')}
    >
      <div className="sf-info-block">
        <div className="sf-block-label">{t('sf.label.artistReport')}</div>
        <div className="sf-answer-bubble sf-answer-bubble--geo">{data.artist_report}</div>
        <div className="sf-block-label" style={{ marginTop: 18 }}>{t('sf.label.whyMatters')}</div>
        <p className="sf-info-text">{data.why_it_matters}</p>
      </div>
    </SectionShell>
  )
}

const ASSESSMENT_KEYS = {
  strong:        'sf.assess.strong',
  on_track:      'sf.assess.on_track',
  below_typical: 'sf.assess.below_typical',
  weak:          'sf.assess.weak',
  unknown:       'sf.assess.unknown',
}
const ASSESSMENT_COLORS = {
  strong: '#5a7a30', on_track: '#7a9a40', below_typical: '#c47a35', weak: '#b03020',
  unknown: '#9a8a70',
}

function CareerBenchmarks({ data, t }) {
  const rec = data.artist_record
  const summary = `${rec.exhibitions} · ${rec.publications} · Instagram ${rec.instagram ?? '—'}`
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
  const summary = t('sf.sum.calendarUnknown', { known, n: data.unknown_deadline_count, s: data.unknown_deadline_count !== 1 ? 's' : '' })
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
  const summary = t('sf.sum.pressFeatures', { n: total, s: total !== 1 ? 's' : '' })
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
              <a className="sf-press-outlet sf-ext-link" href={sfSearch(f.outlet)} target="_blank" rel="noreferrer">{f.outlet} ↗</a>
              <div className="sf-press-type">{f.type}</div>
              <div className="sf-press-note">{f.note}</div>
            </div>
          ))}
        </div>
        <div>
          <div className="sf-block-label">{t('sf.label.pitchTargets')}</div>
          {data.pitch_targets.map((pt, i) => (
            <div key={i} className="sf-pitch-row">
              <a className="sf-pitch-outlet sf-ext-link" href={sfSearch(pt.outlet)} target="_blank" rel="noreferrer">{pt.outlet} ↗</a>
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
      <div className="sf-info-block">
        <div className="sf-block-label">{t('sf.label.whyMatters')}</div>
        <p className="sf-info-text">{data.why_it_matters}</p>
        <div className="sf-block-label" style={{ marginTop: 18 }}>{t('sf.label.fairsPipeline')}</div>
        <div className="sf-tag-list">
          {data.fairs_in_pipeline.map((f, i) => <span key={i} className="sf-trait">{f}</span>)}
        </div>
      </div>
    </SectionShell>
  )
}

function CollaborationMap({ data, t }) {
  const summary = t('sf.sum.coExhibitors', { n: data.known_co_exhibitors.length, s: data.known_co_exhibitors.length !== 1 ? 's' : '' })
  return (
    <SectionShell
      title={t('sf.sec.collab')}
      subtitle={t('sf.sub.collab')}
      summary={summary}
    >
      <div className="sf-block-label">{t('sf.label.knownCoExhib')}</div>
      {data.known_co_exhibitors.map((a, i) => (
        <div key={i} className="sf-collab-row">
          <span className="sf-collab-name">{a.name}</span>
          <span className="sf-collab-context">{a.context}</span>
          <span className="sf-collab-status">{t('sf.label.currentStatus')} {a.current_status}</span>
        </div>
      ))}
      <p className="sf-info-text" style={{ marginTop: 14 }}>{data.note}</p>
    </SectionShell>
  )
}

function GeographicExpansion({ data, t }) {
  const summary = t('sf.label.primaryBase')
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

          {data.artist_intent && (
            <div className="sf-peppercorn-answer" style={{ marginTop: 16 }}>
              <div className="sf-block-label">{t('sf.label.pubIntent')}</div>
              <div className="sf-answer-bubble">{data.artist_intent}</div>
            </div>
          )}

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
  const summary = t('sf.sum.venues', { n: data.total, s: data.total !== 1 ? 's' : '', active: data.active ?? 0 })
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
                  <a className="sf-venue-name sf-ext-link" href={sfSearch(`${v.name} ${v.city || ''}`)} target="_blank" rel="noreferrer">{v.name} ↗</a>
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

// Open questions map 1:1 (in order) to the saffron_answers slots in api.py.
const SF_ANSWER_KEYS = [
  'posting_frequency', 'audience_geography', 'has_sold_work', 'new_publication_planned',
  'has_artist_statement', 'tide_china_contact', 'second_exhibition_planned', 'price_points',
]

function QuestionRow({ q, index, t }) {
  const [value, setValue] = useState('')
  const [saved, setSaved] = useState(false)
  const key = SF_ANSWER_KEYS[index]

  function save() {
    const v = value.trim()
    if (!v || !key) return
    setSaved(true)
    fetch('/api/saffron_answer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key, value: v }),
    }).catch(() => {})
  }

  return (
    <div className="sf-question-row">
      <div className="sf-question-number">{index + 1}</div>
      <div className="sf-question-body">
        <div className="sf-question-text">{q.question}</div>
        <div className="sf-question-why">{q.why_it_matters}</div>
        {saved ? (
          <div className="sf-question-saved">{t('sf.oq.saved')}</div>
        ) : (
          <div className="sf-question-answer">
            <input
              className="sf-question-input"
              value={value}
              onChange={e => setValue(e.target.value)}
              placeholder={t('sf.oq.placeholder')}
              onKeyDown={e => { if (e.key === 'Enter') save() }}
            />
            <button className="sf-question-save" onClick={save} disabled={!value.trim()}>
              {t('sf.oq.save')}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

function OpenQuestions({ data, t }) {
  return (
    <SectionShell
      title={t('sf.sec.openQs')}
      subtitle={t('sf.sub.openQs')}
      summary={`${data.count}`}
    >
      <p className="sf-info-text" style={{ marginBottom: 24 }}>{t('sf.label.openQNote')}</p>
      <div className="sf-questions">
        {data.questions.map((q, i) => <QuestionRow key={i} q={q} index={i} t={t} />)}
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
  const { totals, response_rate, trajectory, monthly_chart, recent_activity } = data
  const maxBar = Math.max(...monthly_chart.map(m => m.submissions + m.contacts), 1)
  const trajColor = TRAJECTORY_COLORS[trajectory] || '#9a7040'
  const summary = t('sf.sum.momentum', { submissions: totals.submissions, venues: totals.venues_in_crm, rate: response_rate })

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
  const summary  = t('sf.sum.timing', { peaks: data.peak_months.slice(0, 2).join(' · '), dated: data.with_parsed_deadline })

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
              <span className="sf-timing-peak-count">{t('sf.timing.deadlineCount', { n: data.monthly_counts.find(x => x.month === m)?.count ?? 0 })}</span>
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
        <span className="sf-trait">{t('sf.timeline.age', { n: d.artist_stage.age })}</span>
        <span className="sf-trait">{t('sf.timeline.groupShow', { n: d.artist_stage.group_shows, s: d.artist_stage.group_shows !== 1 ? 's' : '' })}</span>
        <span className="sf-trait">{t('sf.timeline.publications', { n: d.artist_stage.publications, s: d.artist_stage.publications !== 1 ? 's' : '' })}</span>
        {d.artist_stage.instagram && <span className="sf-trait">Instagram {d.artist_stage.instagram}</span>}
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

// ── Career Readiness ───────────────────────────────────────────────────────

const GAP_DOT_COLORS = {
  HIGH:   '#c47a35',
  MEDIUM: '#d4a855',
  LOW:    '#b0a080',
}

function ReadinessBar({ label, sublabel, pct, color }) {
  return (
    <div className="sf-readiness-bar-row">
      <div className="sf-readiness-bar-header">
        <span className="sf-readiness-bar-label">{label}</span>
        <span className="sf-readiness-bar-pct">{Math.round(pct)}%</span>
      </div>
      <div className="sf-readiness-track">
        <div className="sf-readiness-fill" style={{ width: `${pct}%`, background: color }} />
      </div>
      <div className="sf-readiness-sublabel">{sublabel}</div>
    </div>
  )
}

const CAT_LABELS = {
  'Open Calls & Fairs':      'Open Calls & Fairs',
  'Galleries':               'Galleries',
  'Zines & Books':           'Zines & Books',
  'Residencies & Grants':    'Residencies & Grants',
  'Competitions & Awards':   'Competitions & Awards',
  'Cafes & Bookshop Spaces': 'Cafes & Bookshop Spaces',
  'Other':                   'Other',
}

const MEDIUM_LABELS = {
  watercolor:  'Watercolor',
  painting:    'Painting',
  illustration:'Illustration',
  book_arts:   'Book Arts',
  mixed:       'Mixed / Multi-medium',
  photography: 'Photography',
  unknown:     'Medium unspecified',
}

function MarketStats({ data }) {
  const { t } = useLanguage()
  if (!data) return null
  const cats   = Object.entries(data.by_category || {})
  const maxCat = Math.max(...cats.map(([, v]) => v), 1)
  const { top_tier = 0, mid_tier = 0, lower_tier = 0 } = data.score_distribution || {}
  const scoreTotal = (top_tier + mid_tier + lower_tier) || 1
  const dp = data.deadline_pressure || {}
  const total = data.total_opportunities || 0
  const summary = t('sf.ms.summary', { total, top: top_tier, deadlines: dp.this_month || 0 })
  return (
    <SectionShell title={t('sf.ms.title')} subtitle={t('sf.ms.subtitle')} summary={summary}>
      <div className="sf-block-label">{t('sf.ms.byType')}</div>
      <div className="sf-bars sf-ms-bars">
        {cats.map(([label, count]) => (
          <div key={label} className="sf-bar-row">
            <span className="sf-bar-label">{CAT_LABELS[label] || label}</span>
            <div className="sf-bar-track"><div className="sf-bar-fill sf-ms-bar-fill" style={{ width: `${(count / maxCat) * 100}%` }} /></div>
            <span className="sf-bar-count">{count}</span>
          </div>
        ))}
      </div>
      <div className="sf-ms-two-col" style={{ marginTop: 32 }}>
        <div>
          <div className="sf-block-label">{t('sf.ms.deadlinePressure')}</div>
          <div className="sf-ms-pressure-list">
            <div className="sf-ms-pressure-row sf-ms-pressure--hot"><span className="sf-ms-pressure-num">{dp.this_month || 0}</span><span className="sf-ms-pressure-label">{t('sf.ms.thisMonth')}</span></div>
            <div className="sf-ms-pressure-row sf-ms-pressure--warm"><span className="sf-ms-pressure-num">{dp.next_3_months || 0}</span><span className="sf-ms-pressure-label">{t('sf.ms.next3months')}</span></div>
            <div className="sf-ms-pressure-row sf-ms-pressure--cool"><span className="sf-ms-pressure-num">{dp.open_ongoing || 0}</span><span className="sf-ms-pressure-label">{t('sf.ms.rollingOngoing')}</span></div>
          </div>
          <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.ms.mediumFit')}</div>
          <div className="sf-ms-medium-list">
            {Object.entries(data.by_medium || {}).map(([med, cnt]) => (
              <div key={med} className="sf-ms-medium-row">
                <span className={`sf-ms-medium-label${med === 'watercolor' ? ' sf-ms-medium--wc' : ''}`}>{MEDIUM_LABELS[med] || med}</span>
                <span className="sf-ms-medium-count">{cnt}</span>
              </div>
            ))}
          </div>
        </div>
        <div>
          <div className="sf-block-label">{t('sf.ms.scoreDistrib')}</div>
          <div className="sf-ms-score-tiers">
            <div className="sf-ms-score-row sf-ms-score--high"><div className="sf-ms-score-bar-wrap"><div className="sf-ms-score-bar" style={{ width: `${(top_tier / scoreTotal) * 100}%` }} /></div><span className="sf-ms-score-num">{top_tier}</span><span className="sf-ms-score-label">{t('sf.ms.scoreHigh')}</span></div>
            <div className="sf-ms-score-row sf-ms-score--mid"><div className="sf-ms-score-bar-wrap"><div className="sf-ms-score-bar" style={{ width: `${(mid_tier / scoreTotal) * 100}%` }} /></div><span className="sf-ms-score-num">{mid_tier}</span><span className="sf-ms-score-label">{t('sf.ms.scoreMid')}</span></div>
            <div className="sf-ms-score-row sf-ms-score--low"><div className="sf-ms-score-bar-wrap"><div className="sf-ms-score-bar" style={{ width: `${(lower_tier / scoreTotal) * 100}%` }} /></div><span className="sf-ms-score-num">{lower_tier}</span><span className="sf-ms-score-label">{t('sf.ms.scoreLow')}</span></div>
          </div>
          <div className="sf-block-label" style={{ marginTop: 24 }}>{t('sf.ms.top5')}</div>
          <div className="sf-ms-top-list">
            {(data.top_scored || []).map((opp, i) => (
              <div key={i} className="sf-ms-top-row"><span className="sf-ms-top-rank">{i + 1}</span><span className="sf-ms-top-name">{opp.name}</span><span className="sf-ms-top-score">{opp.score}</span></div>
            ))}
          </div>
        </div>
      </div>
    </SectionShell>
  )
}

function CareerReadiness({ data }) {
  const { t } = useLanguage()
  if (!data) return null

  const tier3Pct = (data.readiness_scores?.tier_3_readiness ?? 0) * 100
  const tier4Pct = (data.readiness_scores?.tier_4_readiness ?? 0) * 100
  const gaps     = data.blocking_gaps ?? []
  const actNow   = (data.immediate_priorities ?? []).slice(0, 3)
  const build    = data.build_toward ?? []
  const watch    = data.watch_list   ?? []
  const months   = data.months_to_tier3

  const summary = data.current_phase
    ? `${data.current_phase}${months ? ` · ${t('sf.cr.monthsToTier3', { n: months })}` : ''}`
    : t('sf.cr.title')

  return (
    <SectionShell
      title={t('sf.cr.title')}
      subtitle={t('sf.cr.subtitle')}
      summary={summary}
    >
      {/* Four-tier ladder */}
      <p className="sf-tiers-intro">{t('sf.cr.tiersIntro')}</p>
      <div className="sf-readiness-bars">
        <div className="sf-tier-done">
          <span className="sf-tier-check">✓</span>
          <span className="sf-tier-name">{t('sf.cr.tier1')}</span>
          <span className="sf-tier-status">{t('sf.cr.tierComplete')}</span>
        </div>
        <div className="sf-tier-done">
          <span className="sf-tier-check">✓</span>
          <span className="sf-tier-name">{t('sf.cr.tier2')}</span>
          <span className="sf-tier-status">{t('sf.cr.tierComplete')}</span>
        </div>
        <ReadinessBar
          label={t('sf.cr.tier3')}
          sublabel={t('sf.cr.tier3Sublabel')}
          pct={tier3Pct}
          color="#c47a35"
        />
        <ReadinessBar
          label={t('sf.cr.tier4')}
          sublabel={t('sf.cr.tier4Sublabel')}
          pct={tier4Pct}
          color="#d4b87a"
        />
      </div>

      {/* Timeline pill + next milestone */}
      <div className="sf-readiness-milestone-row">
        {months != null && (
          <span className="sf-readiness-timeline-pill">{t('sf.cr.monthsToTier3', { n: months })}</span>
        )}
      </div>
      {data.next_milestone && (
        <p className="sf-readiness-milestone">{data.next_milestone}</p>
      )}

      {/* Blocking gaps */}
      {gaps.length > 0 && (
        <div style={{ marginTop: 28 }}>
          <div className="sf-block-label">{t('sf.cr.blockingGaps')}</div>
          <div className="sf-readiness-gaps">
            {gaps.map((g, i) => (
              <div key={i} className="sf-readiness-gap-row">
                <span
                  className="sf-readiness-gap-dot"
                  style={{ background: GAP_DOT_COLORS[g.priority] ?? '#b0a080' }}
                />
                <div className="sf-readiness-gap-body">
                  <span className="sf-readiness-gap-text">{g.gap}</span>
                  {g.action && (
                    <span className="sf-readiness-gap-action">{g.action}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Three columns */}
      <div className="sf-readiness-columns" style={{ marginTop: 28 }}>
        <div className="sf-readiness-col">
          <div className="sf-block-label">{t('sf.cr.actNow')}</div>
          {actNow.length === 0
            ? <p className="sf-readiness-col-empty">{t('sf.cr.noneQueued')}</p>
            : actNow.map((o, i) => (
              <div key={i} className="sf-readiness-col-item">
                <span className="sf-readiness-col-name">{o.name ?? o.title ?? o}</span>
                {o.score != null && (
                  <span className="sf-readiness-col-score">{Math.round(o.score * 10) / 10}</span>
                )}
              </div>
            ))
          }
        </div>
        <div className="sf-readiness-col">
          <div className="sf-block-label">{t('sf.cr.buildToward')}</div>
          {build.length === 0
            ? <p className="sf-readiness-col-empty">{t('sf.cr.noneQueued')}</p>
            : build.map((o, i) => (
              <div key={i} className="sf-readiness-col-item">
                <span className="sf-readiness-col-name">{o.name ?? o.title ?? o}</span>
              </div>
            ))
          }
        </div>
        <div className="sf-readiness-col sf-readiness-col--watch">
          <div className="sf-block-label">{t('sf.cr.watchList')}</div>
          {watch.length === 0
            ? <p className="sf-readiness-col-empty">{t('sf.cr.noneQueued')}</p>
            : watch.map((o, i) => (
              <div key={i} className="sf-readiness-col-item sf-readiness-col-item--muted">
                <span className="sf-readiness-col-name">{o.name ?? o.title ?? o}</span>
              </div>
            ))
          }
        </div>
      </div>
    </SectionShell>
  )
}

// ── Page root ──────────────────────────────────────────────────────────────

export default function SaffronPage({ nav }) {
  const [rawData,    setRawData]    = useState(null)
  const [rawCareer,  setRawCareer]  = useState(null)
  const [error,      setError]      = useState(null)
  const [tab,        setTab]        = useState('profile')
  const { t, lang } = useLanguage()

  useEffect(() => {
    fetch('/api/saffron')
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json() })
      .then(setRawData)
      .catch(e => setError(e.message))
  }, [])

  useEffect(() => {
    fetch('/api/career_strategy')
      .then(r => { if (!r.ok) throw null; return r.json() })
      .then(setRawCareer)
      .catch(() => {})
  }, [])

  // Translate the served (English) analysis into Chinese for 中文 viewers.
  const data       = useMemo(() => (lang === 'zh' ? deepTranslate(rawData,   SF_ZH) : rawData),   [rawData,   lang])
  const careerData = useMemo(() => (lang === 'zh' ? deepTranslate(rawCareer, SF_ZH) : rawCareer), [rawCareer, lang])

  const SF_TABS = [
    ['profile',       t('sf.cat.profile')],
    ['landscape',     t('sf.cat.landscape')],
    ['strategy',      t('sf.cat.strategy')],
    ['calendar',      t('sf.cat.calendar')],
    ['relationships', t('sf.cat.relationships')],
    ['money',         t('sf.cat.money')],
  ]
  function goTab(key) {
    setTab(key)
    requestAnimationFrame(() => document.querySelector('.sf-tabs')?.scrollIntoView({ behavior: 'smooth', block: 'start' }))
  }

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
          <div className="sf-tabs">
            {SF_TABS.map(([key, label]) => (
              <button
                key={key}
                className={`sf-tab${tab === key ? ' sf-tab--active' : ''}`}
                onClick={() => goTab(key)}
              >
                {label}
              </button>
            ))}
          </div>

          <SectionErrorBoundary key={tab}>
            {tab === 'profile' && (
              <>
                {careerData && <CareerReadiness data={careerData} />}
                <CareerPosition     data={data.career_position}    t={t} />
                <CareerMomentum     data={data.career_momentum}    t={t} />
                <CareerBenchmarks   data={data.career_benchmarks}  t={t} />
                <CareerTimeline     t={t} />
                <ComparableArtists  artists={data.peer_artists}    t={t} />
                <InstagramStrategy  data={data.instagram_strategy} t={t} />
                <AudienceGeography  data={data.audience_geography} t={t} />
              </>
            )}
            {tab === 'landscape' && (
              <>
                <MarketStats         data={data.market_stats} />
                <MarketLandscape     data={data.market_landscape}     t={t} />
                <OpportunityGap      data={data.opportunity_gap}      t={t} />
                <GeographicExpansion data={data.geographic_expansion} t={t} />
              </>
            )}
            {tab === 'strategy' && (
              <>
                <StrategicPathway    data={data.pathway}             t={t} />
                <LongTermScenarios   data={data.long_term_scenarios} t={t} />
                <CareerDependencyMap t={t} lang={lang} />
                <OpenQuestions       data={data.open_questions}      t={t} />
              </>
            )}
            {tab === 'calendar' && (
              <>
                <SeasonalCalendar   data={data.seasonal_calendar}   t={t} />
                <TimingIntelligence data={data.timing_intelligence} t={t} />
              </>
            )}
            {tab === 'relationships' && (
              <>
                <PressFeatures      data={data.press_features}      t={t} />
                <PressPitchMap      t={t} lang={lang} />
                <CollaborationMap   data={data.collaboration_map}   t={t} />
                <CollectorEcosystem data={data.collector_ecosystem} t={t} />
                <VenueTracker       data={data.venue_tracker}       t={t} />
              </>
            )}
            {tab === 'money' && (
              <>
                <RevenueStreams       t={t} lang={lang} />
                <PricingIntelligence  t={t} />
                <GrantLandscape       t={t} lang={lang} />
                <LicensingLandscape   t={t} lang={lang} />
                <PublicationLandscape data={data.publication_landscape} t={t} />
              </>
            )}
          </SectionErrorBoundary>
        </div>
      )}
    </div>
  )
}
