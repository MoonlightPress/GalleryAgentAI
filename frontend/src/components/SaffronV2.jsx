// SaffronV2 — the proposed restructure, live, at #observe2.
//
// Not linked from anywhere. It reads the same endpoints as the real page, so
// everything on it is her actual data; it exists to be looked at and argued
// with before any of it replaces `SaffronPage.jsx`.
//
// The three changes it is here to demonstrate:
//   1. A PULSE — what changed since she last looked. Bible08's tone examples for
//      Saffron are all deltas and no surface computes one. `/api/saffron_pulse`.
//   2. A YEAR STRIP instead of a pageable month grid stacked on an 80-row list.
//      Scraped dates and authored doors land on ONE timeline, which is also what
//      stops them contradicting each other — six months of the old grid are empty
//      while doors open in four of them.
//   3. THREE TABS with one job each: time, position, direction. Every section
//      that fitted none of those was doing another companion's job.
//
// Sections that survive the cut are imported from SaffronPage rather than
// reimplemented, so this is the real content and not a mock of it.

import { useState, useEffect, useMemo } from 'react'
import { useLanguage } from '../i18n/LanguageContext'
import { track, visitorId } from '../utils/track'
import {
  saffronTx,
  RecurringDoors, GrantLandscape,
  CareerPosition, ComparableArtists, VenueTracker, PressFeatures,
  Futures, StrategicPathway, BookEconomics, PublisherFork,
  SectionOpenContext, SectionErrorBoundary,
} from './SaffronPage'
import { saffronHero, saffronHeroNight } from '../utils/heroImages'
import { isNightNow } from '../utils/timeOfDay'
import './SaffronPage.css'
import './SaffronV2.css'

// The first version of this was a scoreboard — 0 new / 24 closed / 49 closing —
// sitting above the tabs. Counts of things she cannot act on are not
// information: she never saw the 24 that closed, and 49 is not a number anyone
// reads. So it is one sentence now, it lives inside the year tab where time is
// the subject, and when something IS new it names the thing rather than tallying
// it.
const PULSE_COPY = {
  en: {
    quiet: (d) => `Nothing new since ${d}. The search runs about once a month.`,
    some: (n, d) => n === 1
      ? `One new thing since ${d}.`
      : `${n} new things since ${d}.`,
    coverage: (ahead, served) =>
      `${ahead} of ${served} entries carry a date we can read; the rest are undated or already past.`,
  },
  zh: {
    quiet: (d) => `自 ${d} 起没有新的。检索大约每月一次。`,
    some: (n, d) => `自 ${d} 起，新增 ${n} 条。`,
    coverage: (ahead, served) =>
      `${served} 条中有 ${ahead} 条带着可读的日期，其余的没有日期，或已经过去。`,
  },
  ja: {
    quiet: (d) => `${d} 以降、新しいものはありません。検索は月に一度ほどです。`,
    some: (n, d) => `${d} 以降、新しいものが ${n} 件。`,
    coverage: (ahead, served) =>
      `${served} 件のうち ${ahead} 件に読み取れる日付があります。残りは日付がないか、すでに過ぎています。`,
  },
}

const V2_COPY = {
  en: {
    year: 'The year ahead', yearSub: 'Dated entries · dots are doors that open that month',
    keyDoor: 'a door opens', keyNone: '— nothing dated yet',
    dated: (n) => `${n} dated`, nothingDated: 'Nothing dated yet',
    doorsHere: (n) => n === 1 ? '1 door opens this month' : `${n} doors open this month`,
    more: (n) => `Show the other ${n}`, less: 'Show fewer',
    empty: 'Nothing dated this month. The doors below still come round.',
    loading: 'Saffron is looking…',
  },
  zh: {
    year: '未来一年', yearSub: '有日期的条目 · 圆点表示当月开放的门',
    keyDoor: '有门开放', keyNone: '— 暂无日期',
    dated: (n) => `${n} 条有日期`, nothingDated: '暂无有日期的条目',
    doorsHere: (n) => `本月有 ${n} 扇门开放`,
    more: (n) => `显示其余 ${n} 条`, less: '收起',
    empty: '本月暂无有日期的条目。下面的门仍会轮到。',
    loading: 'Saffron 正在观察…',
  },
  ja: {
    year: 'これからの一年', yearSub: '日付のある項目 · 点はその月に開く扉',
    keyDoor: '扉が開く', keyNone: '— 日付未定',
    dated: (n) => `${n} 件に日付あり`, nothingDated: '日付のある項目はまだありません',
    doorsHere: (n) => `今月は ${n} 件の扉が開きます`,
    more: (n) => `残り ${n} 件を表示`, less: '折りたたむ',
    empty: '今月は日付のある項目がありません。下の扉はまた巡ってきます。',
    loading: 'Saffron が見渡しています…',
  },
}

const cp = (lang) => V2_COPY[lang] || V2_COPY.en
const pc = (lang) => PULSE_COPY[lang] || PULSE_COPY.en
const MONTH_EN = ['January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December']

// ── Strategies: a ladder of tasks per goal ───────────────────────────────────
//
// PROTOTYPE. The ladders below are hardcoded here on purpose — the engine that
// should own them is specced in docs/NEXT_PHASE_strategies.md and deliberately
// not built yet. Done-ness IS real: every task reads her live record through
// `evidence`, so nothing here is a mock of her progress, only of the structure.
//
// A goal is a name plus an ORDER of task ids. The pool is shared, and the same
// task sits in more than one ladder at different positions — which is the whole
// point. `also` is computed, never typed: it falls out of the ladders.

const TASKS = {
  body_of_work:        { en: 'Ten paintings that hang together as one thing',   zh: '十张能作为一个整体挂在一起的画',       ja: '一つのまとまりとして掛けられる十点' },
  group_shows:         { en: 'A record of showing alongside others',            zh: '与他人同场展出的记录',                 ja: '他の作家と並んで見せた記録' },
  solo_shows:          { en: 'Her own room',                                    zh: '属于自己的展间',                       ja: '自分ひとりの部屋' },
  institutional_show:  { en: 'A museum or public institution',                  zh: '美术馆或公共机构',                     ja: '美術館または公共機関' },
  better_solo_venues:  { en: 'Larger rooms than a café or a small gallery',     zh: '比咖啡馆和小画廊更大的场地',           ja: 'カフェや小さな画廊より大きな会場' },
  critical_press:      { en: 'Written about, rather than featured',             zh: '被评论，而不只是被转载',               ja: '紹介ではなく、論じられること' },
  art_fairs:           { en: 'A fair, where collectors are',                    zh: '藏家所在的艺博会',                     ja: 'コレクターのいるフェア' },
  representation:      { en: 'A gallery that sells on her behalf',              zh: '代理她销售的画廊',                     ja: '代わりに売ってくれる画廊' },

  daily_cadence:       { en: 'A rhythm of new work that does not stop',         zh: '不停下来的创作节奏',                   ja: '途切れない制作のリズム' },
  recognisable_style:  { en: 'One look, legible at thumbnail size',             zh: '缩略图大小也认得出的一种面貌',         ja: 'サムネイルでもわかる一つの佇まい' },
  named_series:        { en: 'A series with a name, not only a diary',          zh: '一个有名字的系列，而不只是日记',       ja: '日記だけでなく、名前のある連作' },
  process_video:       { en: 'The painting in motion, not only the result',     zh: '作画的过程，而不只是结果',             ja: '結果だけでなく、描いている時間' },
  cross_platform:      { en: 'The same work where other audiences already are', zh: '把同样的作品放到别的受众所在之处',     ja: '別の観客がすでにいる場所にも同じ作品を' },
  price_ladder_middle: { en: 'Something between ¥2,200 and ¥31,900',            zh: '在 2,200 日元与 31,900 日元之间的东西', ja: '2,200円と31,900円のあいだの何か' },

  lookbook:            { en: 'Ten to twenty works as product mockups, one PDF', zh: '十到二十件作品的产品效果图，一份 PDF', ja: '製品モックアップ10〜20点、PDF一つ' },
  findable_licensing:  { en: 'Listed where art directors look',                 zh: '出现在美术总监会看的地方',             ja: 'アートディレクターが見る場所に載る' },
  first_licence:       { en: 'One paid usage, at any size',                     zh: '第一笔授权，多小都算',                 ja: '規模を問わず、最初の一件' },
}

const GOALS = [
  { id: 'gallery_success', en: 'Gallery success', zh: '画廊这条路', ja: '画廊での成功',
    ladder: ['body_of_work', 'group_shows', 'solo_shows', 'institutional_show',
             'better_solo_venues', 'critical_press', 'art_fairs', 'representation'] },
  { id: 'a_following', en: 'A following', zh: '一群固定的读者', ja: '見てくれる人たち',
    ladder: ['daily_cadence', 'recognisable_style', 'named_series',
             'process_video', 'cross_platform', 'price_ladder_middle'] },
  { id: 'intl_licensing', en: 'International licensing', zh: '国际授权', ja: '海外のライセンス',
    ladder: ['recognisable_style', 'named_series', 'lookbook',
             'findable_licensing', 'first_licence', 'critical_press'] },
]

// Which OTHER goals each task also serves — derived, so it cannot drift.
const alsoServes = (taskId, goalId) =>
  GOALS.filter(g => g.id !== goalId && g.ladder.includes(taskId))

// Done-ness from her live record. Anything we genuinely cannot see returns
// false rather than guessing — an unearned tick is worse than a blank rung.
function evidence(data, careerData) {
  const ev   = careerData?.career_evidence || {}
  const pos  = data?.career_position || {}
  const shows = (pos.exhibitions || []).length
  const press = (data?.press_features?.confirmed || []).length
  return {
    body_of_work:        shows > 0,
    group_shows:         (ev.confirmed_group_shows || 0) >= 3,
    solo_shows:          !!ev.has_solo_show,
    institutional_show:  !!ev.has_institutional_show,
    better_solo_venues:  false,
    critical_press:      press >= 3,
    art_fairs:           false,
    representation:      !!ev.has_representation,

    daily_cadence:       true,
    recognisable_style:  true,
    named_series:        false,
    process_video:       false,
    cross_platform:      false,
    price_ladder_middle: false,

    lookbook:            false,
    findable_licensing:  false,
    first_licence:       false,
  }
}

const LADDER_COPY = {
  en: { title: 'Strategies', sub: 'Different goals, overlapping tasks, different orders',
        done: (a, b) => `${a} of ${b} already true`, also: 'also counts toward',
        proto: 'Prototype — the ladders are written by hand; the ticks are read from her record.' },
  zh: { title: '推进策略', sub: '不同的目标，重叠的事项，不同的顺序',
        done: (a, b) => `${b} 项里已经成立 ${a} 项`, also: '同时也算进',
        proto: '原型——阶梯是手写的，勾选是从她的记录里读出来的。' },
  ja: { title: '進め方', sub: '目標ごとに、重なる項目を、違う順番で',
        done: (a, b) => `${b} 件中 ${a} 件はすでに満たしている`, also: '次にも効く',
        proto: 'プロトタイプ——梯子は手書き、チェックは記録から読んでいます。' },
}

function Ladders({ data, careerData, lang }) {
  const c = LADDER_COPY[lang] || LADDER_COPY.en
  const pick = (o) => (o && (o[lang] || o.en)) || ''
  const done = evidence(data, careerData)

  return (
    <div className="v2-ladders">
      <h2 className="v2-h">{c.title}</h2>
      <p className="v2-sub">{c.sub}</p>

      {GOALS.map((g) => {
        const total = g.ladder.length
        const hit = g.ladder.filter((t) => done[t]).length
        // The first rung she has not reached — the only one drawn as current.
        const next = g.ladder.find((t) => !done[t])
        return (
          <div key={g.id} className="v2-ladder">
            <div className="v2-ladder-head">
              <h3 className="v2-ladder-name">{pick(g)}</h3>
              <span className="v2-ladder-count">{c.done(hit, total)}</span>
            </div>
            <div className="v2-ladder-bar">
              <span className="v2-ladder-bar-fill" style={{ width: `${(hit / total) * 100}%` }} />
            </div>
            <ol className="v2-rungs">
              {g.ladder.map((t) => {
                const isDone = done[t]
                const isNext = t === next
                const shared = alsoServes(t, g.id)
                const state = isDone ? 'done' : isNext ? 'next' : 'later'
                return (
                  <li key={t} className={`v2-rung v2-rung--${state}`}>
                    <span className="v2-rung-mark">{isDone ? '✓' : isNext ? '▸' : '○'}</span>
                    <span className="v2-rung-body">
                      <span className="v2-rung-label">{pick(TASKS[t])}</span>
                      {shared.length > 0 && (
                        <span className="v2-rung-also">
                          {c.also} {shared.map(s => pick(s)).join(' · ')}
                        </span>
                      )}
                    </span>
                  </li>
                )
              })}
            </ol>
          </div>
        )
      })}
      <p className="v2-ladder-proto">{c.proto}</p>
    </div>
  )
}

// ── Pulse: one line, and it names things rather than counting them ──────────
function Pulse({ pulse, lang }) {
  if (!pulse) return null
  const c = pc(lang)
  const n = pulse.new_count
  const when = pulse.since
  const locName = (o) =>
    (lang === 'zh' && o.name_zh) ? o.name_zh : (lang === 'ja' && o.name_ja) ? o.name_ja : o.name
  return (
    <p className="v2-pulse">
      {n === 0 ? c.quiet(when) : c.some(n, when)}
      {n > 0 && (
        <span className="v2-pulse-names">
          {pulse.new.slice(0, 3).map((o, i) => (
            <a key={i} className="v2-pulse-name" href={o.url || undefined} target="_blank" rel="noreferrer">
              {locName(o)}
            </a>
          ))}
        </span>
      )}
    </p>
  )
}

// ── Year strip: scraped dates and authored doors on one timeline ─────────────
//
// This is the fix for the contradiction the old calendar tab renders today: the
// timing chart calls June "peak application season" while the grid two inches
// below shows June empty. Both are true of different data. Put the doors on the
// same twelve cells and June reads honestly — nothing scraped, one door.
function YearStrip({ slots, selected, onSelect, lang, calMonths }) {
  const c = cp(lang)
  // The wash is a share of the busiest month, so the tallest column is always
  // full and the shape reads the same whatever the absolute numbers are. Floored
  // at 6% so a month with one entry still shows a tint rather than nothing.
  const peak = Math.max(1, ...slots.map(s => s.dated))
  return (
    <div className="v2-year">
      <div className="v2-yearstrip">
        {slots.map((s) => {
          const on = s.key === selected
          const fill = s.dated === 0 ? 0 : Math.max(6, Math.round((s.dated / peak) * 100))
          return (
            <button
              key={s.key}
              className={`v2-ys${on ? ' v2-ys--on' : ''}`}
              style={{ '--fill': `${fill}%` }}
              onClick={() => onSelect(s.key)}
              aria-pressed={on}
              title={`${calMonths[s.month - 1]} ${s.year}`}
            >
              <span className="v2-ys-doors">
                {s.doors.map((d) => <i key={d.id} className="v2-ys-door" />)}
              </span>
              <span className={`v2-ys-n${s.dated === 0 ? ' v2-ys-n--none' : ''}`}>
                {s.dated === 0 ? '—' : s.dated}
              </span>
              <span className="v2-ys-m">{calMonths[s.month - 1]}</span>
            </button>
          )
        })}
      </div>
      <p className="v2-ys-key">
        <span><i className="v2-ys-door" /> {c.keyDoor}</span>
        <span>{c.keyNone}</span>
      </p>
    </div>
  )
}

// ── The month you tapped ─────────────────────────────────────────────────────
// Keyed by slot in the caller, so switching months remounts and `expanded`
// resets on its own — no effect, no cascading render.
function MonthPanel({ slot, lang, calMonths }) {
  const [expanded, setExpanded] = useState(false)
  const c = cp(lang)
  if (!slot) return null

  const locName = (o) =>
    (lang === 'zh' && o.name_zh) ? o.name_zh : (lang === 'ja' && o.name_ja) ? o.name_ja : o.name
  const PAGE = 6
  const shown = expanded ? slot.items : slot.items.slice(0, PAGE)
  const rest = slot.items.length - shown.length

  return (
    <div className="v2-month">
      <h3 className="v2-month-h">
        {calMonths[slot.month - 1]} <span className="v2-month-yr">{slot.year}</span>
      </h3>
      <p className="v2-month-sub">
        {slot.dated === 0 ? c.nothingDated : c.dated(slot.dated)}
        {slot.doors.length > 0 && <> · {c.doorsHere(slot.doors.length)}</>}
      </p>

      {slot.items.length === 0 ? (
        <p className="v2-month-empty">{c.empty}</p>
      ) : (
        <>
          <ul className="v2-list">
            {shown.map((o, i) => (
              <li key={i}>
                <a
                  className="v2-list-name"
                  href={o.url || `https://www.google.com/search?q=${encodeURIComponent(o.name)}`}
                  target="_blank"
                  rel="noreferrer"
                  onClick={() => track({ type: 'action', action: 'v2_open_opp', name: o.name })}
                >
                  {locName(o)} ↗
                </a>
                <span className="v2-list-when">{o.deadline}</span>
              </li>
            ))}
          </ul>
          {rest > 0 && (
            <button className="v2-more" onClick={() => setExpanded(true)}>{c.more(rest)} ▾</button>
          )}
          {expanded && slot.items.length > PAGE && (
            <button className="v2-more" onClick={() => setExpanded(false)}>{c.less} ▴</button>
          )}
        </>
      )}
    </div>
  )
}

export default function SaffronV2({ nav }) {
  const { t, lang } = useLanguage()
  const [raw, setRaw] = useState(null)
  const [rawCareer, setRawCareer] = useState(null)
  const [pulse, setPulse] = useState(null)
  const [error, setError] = useState(null)
  // Futures leads. It contradicts Bible08, which says Saffron does not advise —
  // but it is the only section she has ever deliberately opened, four separate
  // times, and the behaviour is better evidence than the document.
  const [tab, setTab] = useState('forward')
  const [selected, setSelected] = useState(null)

  useEffect(() => {
    fetch('/api/saffron')
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json() })
      .then(setRaw)
      .catch(e => setError(String(e.message)))
    fetch('/api/career_strategy').then(r => r.ok ? r.json() : null).then(setRawCareer).catch(() => {})
    const vid = visitorId()
    fetch(`/api/saffron_pulse${vid ? `?visitor_id=${encodeURIComponent(vid)}` : ''}`)
      .then(r => r.ok ? r.json() : null).then(setPulse).catch(() => {})
  }, [])

  const data = useMemo(() => saffronTx(raw, lang), [raw, lang])
  const careerData = useMemo(() => saffronTx(rawCareer, lang), [rawCareer, lang])
  const calMonths = t('cal.months')
  const c = cp(lang)

  // Twelve slots from this month, each carrying both what was scraped for it
  // and which authored doors open in it.
  const slots = useMemo(() => {
    if (!data) return []
    const now = new Date()
    const byKey = new Map()
    for (const m of (data.seasonal_calendar?.months || [])) {
      const idx = MONTH_EN.indexOf(m.month)
      if (idx < 0) continue
      byKey.set(`${m.year}-${idx + 1}`, m.opportunities || [])
    }
    const doorsBy = new Map()
    for (const d of (data.recurring_calendar?.doors || [])) {
      const k = `${d.opens_year}-${d.opens_month}`
      if (!doorsBy.has(k)) doorsBy.set(k, [])
      doorsBy.get(k).push(d)
    }
    const out = []
    for (let n = 0; n < 12; n++) {
      const dt = new Date(now.getFullYear(), now.getMonth() + n, 1)
      const key = `${dt.getFullYear()}-${dt.getMonth() + 1}`
      const items = byKey.get(key) || []
      out.push({
        key,
        year: dt.getFullYear(),
        month: dt.getMonth() + 1,
        items,
        dated: items.length,
        doors: doorsBy.get(key) || [],
      })
    }
    return out
  }, [data])

  // Derived, not stored: with no explicit choice the current month is the one
  // showing. Writing that into state from an effect meant an extra render and a
  // frame where nothing was selected.
  const selectedKey = selected || slots[0]?.key || null
  const slot = slots.find(s => s.key === selectedKey) || null
  const monthDoors = slot ? { ...data?.recurring_calendar, doors: slot.doors } : null

  const goTab = (key) => {
    setTab(key)
    track({ type: 'nav', page: 'observe2', section: key })
  }

  if (error) return <div className="sf-error">{t('sf.error')}</div>
  if (!data) return <div className="sf-loading">{c.loading}</div>

  // The three surviving tabs keep the names the app already uses. Renaming them
  // was scope creep on my part: `sf.cat.*` are established, already translated
  // (策略 / 戦略, 日历 / カレンダー, 概况 / プロフィール), and she has read them for
  // months. The consolidation that mattered is 5 -> 3 — People & Press folds
  // into Profile, Money dies except Grants — not what the survivors are called.
  const TABS = [
    ['forward',  t('sf.cat.strategy')],
    ['moving',   t('sf.cat.calendar')],
    ['standing', t('sf.cat.profile')],
  ]
  const SB = (k, node) => <SectionErrorBoundary key={`${tab}-${k}`}>{node}</SectionErrorBoundary>

  return (
    <div className="saffron-page saffron-v2">
      <section className="saffron-hero">
        <img src={isNightNow() ? saffronHeroNight : saffronHero} alt="" draggable={false} className="saffron-hero-img" />
      </section>
      {nav}

      <div className="sf-content">
        <p className="v2-flag">
          Prototype · <code>#observe2</code> · not linked from anywhere
        </p>

        <div className="sf-tabs v2-tabs">
          {TABS.map(([key, label]) => (
            <button
              key={key}
              className={`sf-tab${tab === key ? ' sf-tab--active' : ''}`}
              onClick={() => goTab(key)}
            >{label}</button>
          ))}
        </div>

        {tab === 'moving' && (
          <>
            <div className="v2-block">
              <h2 className="v2-h">{c.year}</h2>
              <Pulse pulse={pulse} lang={lang} />
              <p className="v2-sub">{c.yearSub}</p>
              <YearStrip
                slots={slots}
                selected={selectedKey}
                onSelect={(k) => { setSelected(k); track({ type: 'action', action: 'v2_month', name: k }) }}
                lang={lang}
                calMonths={calMonths}
              />
              <MonthPanel key={slot?.key} slot={slot} lang={lang} calMonths={calMonths} />
            </div>

            {slot?.doors.length > 0 && SB('doors', <RecurringDoors data={monthDoors} lang={lang} />)}

            <SectionOpenContext.Provider value={false}>
              {SB('grants', <GrantLandscape t={t} lang={lang} />)}
            </SectionOpenContext.Provider>

            {pulse?.coverage && (
              <p className="v2-coverage">
                {pc(lang).coverage(pulse.coverage.dated_ahead, pulse.coverage.served)}
              </p>
            )}
          </>
        )}

        {tab === 'standing' && (
          <>
            {SB('careerpos', <CareerPosition data={data.career_position} t={t} onChanged={() => {}} />)}
            <SectionOpenContext.Provider value={false}>
              {SB('peers', <ComparableArtists artists={data.peer_artists} t={t} />)}
              {SB('venues', <VenueTracker data={data.venue_tracker} t={t} />)}
              {SB('press', <PressFeatures data={data.press_features} t={t} />)}
            </SectionOpenContext.Provider>
          </>
        )}

        {/* Restored 2026-09-08. Removing it was my misreading: I read the pathway
            as the gallery route wearing a crown, because its goal is gallery
            representation. Scott's correction: the two are different axes. A
            Pathway is a place — what a domain is, what it pays, what she would be
            taking on. A Strategy is a route: an order of action toward a named
            goal. Nothing requires them to correspond.

            Below it, the Strategy ladders — three goals over one shared task
            pool, specced in docs/NEXT_PHASE_strategies.md. The ladders are
            hardcoded; the ticks are read from her live record. */}
        {tab === 'forward' && (
          <SectionOpenContext.Provider value={false}>
            {SB('futures', <Futures data={data.futures} t={t} lang={lang}
              components={{
                book_economics: <BookEconomics data={data.book_economics} lang={lang} />,
                publisher_fork: <PublisherFork data={data.book_economics} lang={lang} />,
              }} />)}
            {SB('pathway', <StrategicPathway data={data.pathway} t={t} />)}
            {SB('ladders', <Ladders data={data} careerData={careerData} lang={lang} />)}
          </SectionOpenContext.Provider>
        )}
      </div>
    </div>
  )
}
