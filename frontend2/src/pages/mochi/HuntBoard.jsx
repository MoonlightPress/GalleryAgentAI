// The Hunt Board — ONE section replacing v1's seven stacked sections.
// Filter chips with painted mini-icons + counts, Cards|Deadlines view toggle
// (equal billing), in-place card expansion, stale drawer at the bottom.
import { useMemo, useState } from 'react'
import { useLanguage } from '../../i18n/LanguageContext'
import { useLocalT } from '../../i18n/local'
import { parseDeadline, splitStale } from '../../utils/deadlines'
import { strings } from './strings'
import OppCardV2 from './OppCardV2'

const ICONS = '/assets/icons/'
const ILLOS = '/assets/illustrations/'

// chips map 1:1 to the API section keys (Galleries & Cafés = relationship_targets)
const FILTERS = [
  { id: 'all',          section: null,                    icon: ICONS + 'icon_international.png', illo: 'immediate_best_moves.svg' },
  { id: 'best',         section: 'immediate_best_moves',  icon: ICONS + 'icon_submission.png',    illo: 'immediate_best_moves.svg' },
  { id: 'open_calls',   section: 'open_calls',            icon: ICONS + 'icon_open_call.png',     illo: 'open_calls.svg' },
  { id: 'publications', section: 'publication_editorial', icon: ICONS + 'icon_bookstore.png',     illo: 'zines_and_print.svg' },
  { id: 'competitions', section: 'competitions_awards',   icon: ICONS + 'icon_prize.png',         illo: 'open_calls.svg' },
  { id: 'zines',        section: 'zines_and_print',       icon: ICONS + 'icon_zines.png',         illo: 'zines_and_print.svg' },
  { id: 'galleries',    section: 'relationship_targets',  icon: ICONS + 'icon_cafe_gallery.png',  illo: 'cafes.svg' },
  { id: 'watch',        section: 'watch_list',            icon: ICONS + 'icon_research.png',      illo: 'watch_list.svg' },
  { id: 'press',        section: '__press__',             icon: ICONS + 'icon_international.png', illo: 'immediate_best_moves.svg' },
]

const SECTION_ORDER = [
  'immediate_best_moves', 'open_calls', 'publication_editorial',
  'competitions_awards', 'zines_and_print', 'relationship_targets', 'watch_list',
]

// Press targets are pitch contacts (magazines/blogs), not dated opportunities —
// v1 gave them their own section; here they get their own chip and stay out of
// the other filters' counts.
function isPress(o) {
  return o.opportunity_type === 'press_target' ||
         o.exclusive_primary_bucket === 'press_target' ||
         o.category === 'press_target'
}

const PAGE = 12

export default function HuntBoard({ sections, removed, onRemove, showToast }) {
  const { t } = useLanguage()
  const t2 = useLocalT(strings)
  const [filter, setFilter] = useState('all')
  const [view, setView] = useState('cards')
  const [openId, setOpenId] = useState(null)
  const [shown, setShown] = useState(PAGE)

  // Split every section into live/stale once (law #1) and drop removed ids.
  const { liveBySection, staleAll } = useMemo(() => {
    const liveBySection = {}
    const staleAll = []
    const press = []
    for (const key of SECTION_ORDER) {
      const items = (sections?.[key] || []).filter(o => !removed.has(o.id))
      press.push(...items.filter(isPress))
      const { live, stale } = splitStale(items.filter(o => !isPress(o)))
      liveBySection[key] = live
      staleAll.push(...stale)
    }
    liveBySection.__press__ = press
    return { liveBySection, staleAll }
  }, [sections, removed])

  const counts = useMemo(() => {
    const c = { all: 0 }
    for (const f of FILTERS) {
      if (!f.section) continue
      c[f.id] = (liveBySection[f.section] || []).length
      if (f.section !== '__press__') c.all += c[f.id]
    }
    return c
  }, [liveBySection])

  const active = FILTERS.find(f => f.id === filter) || FILTERS[0]
  const items = useMemo(() => (
    active.section
      ? (liveBySection[active.section] || [])
      : SECTION_ORDER.flatMap(k => liveBySection[k] || [])
  ), [active, liveBySection])

  function pickFilter(id) { setFilter(id); setShown(PAGE); setOpenId(null) }
  function pickView(v) { setView(v); setOpenId(null) }
  function toggleDetails(id) { setOpenId(prev => (prev === id ? null : id)) }

  return (
    <section id="board" className="mv2-board">
      <div className="sec-head sec-head--amber">
        <h2 className="h-section">{t2('v2.mochi.board.title')}</h2>
        <p className="sec-sub">{t2('v2.mochi.board.sub')}</p>
      </div>

      <div className="mv2-board-controls">
        <div className="chip-row">
          {FILTERS.map(f => (
            <button
              key={f.id}
              className={`chip-filter${filter === f.id ? ' chip-filter--active' : ''}`}
              onClick={() => pickFilter(f.id)}
            >
              <img className="chip-icon" src={f.icon} alt="" />
              {t2(`v2.mochi.filter.${f.id}`)}
              <span className="chip-n">{counts[f.id] ?? 0}</span>
            </button>
          ))}
        </div>
        <div className="mv2-view-toggle" role="tablist" aria-label="view">
          <button
            className={`btn-quiet${view === 'cards' ? ' btn-quiet--active' : ''}`}
            onClick={() => pickView('cards')}
          >
            {t2('v2.mochi.view.cards')}
          </button>
          <button
            className={`btn-quiet${view === 'deadlines' ? ' btn-quiet--active' : ''}`}
            onClick={() => pickView('deadlines')}
          >
            {t2('v2.mochi.view.deadlines')}
          </button>
        </div>
      </div>

      {view === 'cards' ? (
        <CardsView
          items={items} shown={shown} setShown={setShown}
          openId={openId} toggleDetails={toggleDetails}
          onRemove={onRemove} showToast={showToast}
          emptyIllo={active.illo} emptyText={t2('v2.mochi.empty.board')}
          moreLabel={(n) => `${t('opps.showMore')} · ${t('opps.moreCount', { n })}`}
        />
      ) : (
        <DeadlinesView
          items={items}
          openId={openId} toggleDetails={toggleDetails}
          onRemove={onRemove} showToast={showToast}
        />
      )}

      {staleAll.length > 0 && (
        <details className="drawer mv2-stale">
          <summary>{t2('v2.mochi.stale.title', { n: staleAll.length })}</summary>
          <div className="drawer-body">
            <div className="grid-3 mv2-grid">
              {staleAll.map(opp => (
                <OppCardV2
                  key={opp.id} opp={opp} muted
                  isOpen={openId === opp.id}
                  onDetails={() => toggleDetails(opp.id)}
                  onRemove={onRemove} showToast={showToast}
                />
              ))}
            </div>
          </div>
        </details>
      )}
    </section>
  )
}

function CardsView({ items, shown, setShown, openId, toggleDetails, onRemove, showToast, emptyIllo, emptyText, moreLabel }) {
  if (!items.length) {
    return (
      <div className="empty">
        <img src={ILLOS + emptyIllo} alt="" />
        <p className="voice">{emptyText}</p>
      </div>
    )
  }
  const visible = items.slice(0, shown)
  const remaining = items.length - visible.length
  return (
    <>
      <div className="grid-3 mv2-grid">
        {visible.map(opp => (
          <OppCardV2
            key={opp.id} opp={opp}
            isOpen={openId === opp.id}
            onDetails={() => toggleDetails(opp.id)}
            onRemove={onRemove} showToast={showToast}
          />
        ))}
      </div>
      {remaining > 0 && (
        <div className="mv2-more-row">
          <button className="btn-quiet" onClick={() => setShown(s => s + PAGE * 2)}>
            {moreLabel(remaining)}
          </button>
        </div>
      )}
    </>
  )
}

// Deadlines view — port of v1 DeadlineCalendar's date-grouped timeline
// (next 30 days, urgency chips), built on utils/deadlines.js parsing.
function DeadlinesView({ items, openId, toggleDetails, onRemove, showToast }) {
  const { t } = useLanguage()
  const t2 = useLocalT(strings)
  const calWeekdays = t('cal.weekdays')
  const calMonths = t('cal.months')

  const now = new Date(); now.setHours(0, 0, 0, 0)
  const limit = new Date(now); limit.setDate(limit.getDate() + 30)

  const byDate = new Map()
  for (const opp of items) {
    const d = parseDeadline(opp.deadline)
    if (!d || d < now || d >= limit) continue
    const key = d.toISOString().slice(0, 10)
    if (!byDate.has(key)) byDate.set(key, { date: d, opps: [] })
    byDate.get(key).opps.push(opp)
  }
  const entries = [...byDate.entries()].sort(([a], [b]) => a.localeCompare(b))

  if (!entries.length) {
    return (
      <div className="empty">
        <img src={ILLOS + 'open_calls.svg'} alt="" />
        <p className="voice">{t2('v2.mochi.empty.deadlines')}</p>
      </div>
    )
  }

  return (
    <div className="mv2-timeline">
      {entries.map(([key, { date, opps }]) => {
        const days = Math.round((date - now) / 86400000)
        const chip = days === 0 ? t('cal.today')
          : days === 1 ? t('cal.tomorrow')
          : t('cal.daysLeft', { n: days })
        const urgency = days <= 3 ? 'mv2-due--urgent' : days <= 7 ? 'mv2-due--soon' : 'mv2-due--calm'
        return (
          <div key={key} className="mv2-timeline-group">
            <div className="mv2-timeline-head">
              <span className="mv2-timeline-date">
                {calMonths[date.getMonth()]} {date.getDate()} · {calWeekdays[date.getDay()]}
              </span>
              <span className={`pill mv2-due ${urgency}`}>{chip}</span>
              {opps.length > 1 && <span className="pill pill--count">{opps.length}</span>}
            </div>
            <div className="grid-3 mv2-grid">
              {opps.map(opp => (
                <OppCardV2
                  key={opp.id} opp={opp}
                  isOpen={openId === opp.id}
                  onDetails={() => toggleDetails(opp.id)}
                  onRemove={onRemove} showToast={showToast}
                />
              ))}
            </div>
          </div>
        )
      })}
    </div>
  )
}
