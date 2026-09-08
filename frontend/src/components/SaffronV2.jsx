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
  Futures, BookEconomics, PublisherFork,
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
function MonthPanel({ slot, lang, calMonths, t }) {
  const [expanded, setExpanded] = useState(false)
  const c = cp(lang)
  useEffect(() => { setExpanded(false) }, [slot?.key])
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

  useEffect(() => {
    if (!selected && slots.length) setSelected(slots[0].key)
  }, [slots, selected])

  const slot = slots.find(s => s.key === selected) || slots[0] || null
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
                selected={selected}
                onSelect={(k) => { setSelected(k); track({ type: 'action', action: 'v2_month', name: k }) }}
                lang={lang}
                calMonths={calMonths}
              />
              <MonthPanel slot={slot} lang={lang} calMonths={calMonths} t={t} />
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

        {/* StrategicPathway is deliberately NOT rendered here (2026-09-08, Scott).
            Its computed goal is "Gallery representation and a sustained
            international record" and its eight steps are the institutional
            ladder — publication, group shows, museum shows, solo shows. Sitting
            beside five routes it silently ranks them: one gets a destination and
            a timeline, the other four get described. But she does not have to do
            galleries. Selling direct, licensing, publishing and commissions are
            destinations, not waypoints on the way to a gallery, and each route
            already carries her real standing in it.

            The component and its engine are untouched — it still renders on the
            live Saffron page. Re-adding one line below is the whole of the undo.
            The open question it leaves is whether the OTHER four routes deserve
            the same "where you are on this one" ladder the gallery route got. */}
        {tab === 'forward' && (
          <SectionOpenContext.Provider value={false}>
            {SB('futures', <Futures data={data.futures} t={t} lang={lang}
              components={{
                book_economics: <BookEconomics data={data.book_economics} lang={lang} />,
                publisher_fork: <PublisherFork data={data.book_economics} lang={lang} />,
              }} />)}
          </SectionOpenContext.Provider>
        )}
      </div>
    </div>
  )
}
