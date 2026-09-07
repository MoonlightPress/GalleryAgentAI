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

const PULSE_COPY = {
  en: {
    since: (d) => `Since you last looked · ${d}`,
    fallback: (d) => `In the last month · since ${d}`,
    isNew: 'new', closed: 'closed', closing: 'closing within the month',
    quiet: 'Nothing new this time — the search runs monthly, and the last one was August.',
    coverage: (ahead, served) =>
      `${ahead} of ${served} entries carry a date we can read. The rest are undated or already gone.`,
  },
  zh: {
    since: (d) => `自你上次查看 · ${d}`,
    fallback: (d) => `最近一个月 · 自 ${d}`,
    isNew: '新增', closed: '已截止', closing: '本月内截止',
    quiet: '这次没有新的——检索每月进行一次，上一次是八月。',
    coverage: (ahead, served) =>
      `${served} 条中有 ${ahead} 条带着可读的日期，其余的没有日期，或已经过去。`,
  },
  ja: {
    since: (d) => `前回ご覧になってから · ${d}`,
    fallback: (d) => `この一か月 · ${d} 以降`,
    isNew: '新着', closed: '締切済み', closing: '今月中に締切',
    quiet: '今回は新着なし——検索は月に一度で、前回は八月でした。',
    coverage: (ahead, served) =>
      `${served} 件のうち ${ahead} 件に読み取れる日付があります。残りは日付がないか、すでに過ぎています。`,
  },
}

const V2_COPY = {
  en: {
    tabs: ['What’s moving', 'Where you stand', 'Ways forward'],
    year: 'The year ahead', yearSub: 'Dated entries · dots are doors that open that month',
    keyDoor: 'a door opens', keyNone: 'nothing dated yet',
    dated: (n) => `${n} dated`, nothingDated: 'Nothing dated yet',
    doorsHere: (n) => n === 1 ? '1 door opens this month' : `${n} doors open this month`,
    more: (n) => `Show the other ${n}`, less: 'Show fewer',
    empty: 'Nothing dated this month. The doors below still come round.',
    loading: 'Saffron is looking…',
  },
  zh: {
    tabs: ['正在发生', '你所处的位置', '可以走的路'],
    year: '未来一年', yearSub: '有日期的条目 · 圆点表示当月开放的门',
    keyDoor: '有门开放', keyNone: '暂无日期',
    dated: (n) => `${n} 条有日期`, nothingDated: '暂无有日期的条目',
    doorsHere: (n) => `本月有 ${n} 扇门开放`,
    more: (n) => `显示其余 ${n} 条`, less: '收起',
    empty: '本月暂无有日期的条目。下面的门仍会轮到。',
    loading: 'Saffron 正在观察…',
  },
  ja: {
    tabs: ['動いているもの', '現在地', '進める道'],
    year: 'これからの一年', yearSub: '日付のある項目 · 点はその月に開く扉',
    keyDoor: '扉が開く', keyNone: '日付未定',
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

// ── Pulse: the one genuinely new surface ─────────────────────────────────────
function Pulse({ pulse, lang }) {
  if (!pulse) return null
  const c = pc(lang)
  const head = pulse.since_source === 'visit' ? c.since(pulse.since) : c.fallback(pulse.since)
  const rows = [
    ['new', pulse.new_count, c.isNew],
    ['closed', pulse.closed_count, c.closed],
    ['closing', pulse.closing_count, c.closing],
  ]
  return (
    <div className="v2-pulse">
      <p className="v2-pulse-head">{head}</p>
      {rows.map(([k, n, label]) => (
        <div key={k} className="v2-pulse-row">
          <span className={`v2-pulse-n${n === 0 ? ' v2-pulse-n--zero' : ''}`}>{n}</span>
          <span>{label}</span>
        </div>
      ))}
      {pulse.new_count === 0 && <p className="v2-pulse-say">{c.quiet}</p>}
    </div>
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
  return (
    <div className="v2-year">
      <div className="v2-yearstrip">
        {slots.map((s) => {
          const on = s.key === selected
          const quiet = s.dated === 0 && s.doors.length === 0
          return (
            <button
              key={s.key}
              className={`v2-ys${on ? ' v2-ys--on' : ''}${quiet ? ' v2-ys--quiet' : ''}`}
              onClick={() => onSelect(s.key)}
              aria-pressed={on}
            >
              <span className="v2-ys-m">{calMonths[s.month - 1]}</span>
              <span className={`v2-ys-n${s.dated === 0 ? ' v2-ys-n--none' : ''}`}>
                {s.dated === 0 ? '—' : s.dated}
              </span>
              <span className="v2-ys-doors">
                {s.doors.map((d) => <i key={d.id} className="v2-ys-door" />)}
              </span>
            </button>
          )
        })}
      </div>
      <p className="v2-ys-key">
        <span><i className="v2-ys-door" /> {c.keyDoor}</span>
        <span>— {c.keyNone}</span>
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
  const [tab, setTab] = useState('moving')
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

  const TABS = [['moving', c.tabs[0]], ['standing', c.tabs[1]], ['forward', c.tabs[2]]]
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

        <Pulse pulse={pulse} lang={lang} />

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

        {tab === 'forward' && (
          <SectionOpenContext.Provider value={false}>
            {SB('futures', <Futures data={data.futures} t={t} lang={lang}
              components={{
                book_economics: <BookEconomics data={data.book_economics} lang={lang} />,
                publisher_fork: <PublisherFork data={data.book_economics} lang={lang} />,
              }} />)}
            {SB('pathway', <StrategicPathway data={data.pathway} t={t} />)}
          </SectionOpenContext.Provider>
        )}
      </div>
    </div>
  )
}
