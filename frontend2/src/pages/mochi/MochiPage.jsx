// Mochi — the Action page. Hero = Today's Focus (once), then the Hunt Board.
// Built per reports/ux_pass_2026-06/02_REDESIGN_SPEC.md §Page 1.
import { useEffect, useRef, useState } from 'react'
import { api } from '../../utils/api'
import { useLanguage } from '../../i18n/LanguageContext'
import { useLocalT } from '../../i18n/local'
import { strings } from './strings'
import FocusCard from './FocusCard'
import HuntBoard from './HuntBoard'
import mochiImg from '../../assets/heroes/mochi/mochi_hero.png'
import './mochi.css'

const LOCALES = { en: 'en-US', zh: 'zh-CN', ja: 'ja-JP' }

function greetingKey() {
  const h = new Date().getHours()
  if (h < 12) return 'v2.mochi.greeting.morning'
  if (h < 18) return 'v2.mochi.greeting.afternoon'
  return 'v2.mochi.greeting.evening'
}

const FOCUS_SLOTS = ['quick_win', 'high_impact', 'stretch_goal']

export default function MochiPage() {
  const { lang } = useLanguage()
  const t2 = useLocalT(strings)
  const [today, setToday] = useState(null)
  const [opps, setOpps] = useState(null)
  const [loaded, setLoaded] = useState(false)
  const [openFocus, setOpenFocus] = useState(null)
  const [removed, setRemoved] = useState(() => new Set())
  const [toast, setToast] = useState(null)
  const toastTimer = useRef(null)

  useEffect(() => {
    let alive = true
    Promise.allSettled([api.today(), api.opportunities()]).then(([td, op]) => {
      if (!alive) return
      if (td.status === 'fulfilled') setToday(td.value)
      if (op.status === 'fulfilled') setOpps(op.value)
      setLoaded(true)
    })
    return () => { alive = false }
  }, [])

  function showToast(msg) {
    clearTimeout(toastTimer.current)
    setToast(msg)
    toastTimer.current = setTimeout(() => setToast(null), 2600)
  }
  useEffect(() => () => clearTimeout(toastTimer.current), [])

  function handleRemove(id) {
    setRemoved(prev => new Set([...prev, id]))
  }

  const slots = FOCUS_SLOTS.filter(k => today?.[k])
  const dateLine = new Date().toLocaleDateString(LOCALES[lang] || 'en-US', {
    year: 'numeric', month: 'long', day: 'numeric', weekday: 'long',
  })

  return (
    <main className="page mv2-page">
      {/* ── Hero = Today's Focus, once ── */}
      <section className="mv2-hero">
        <img className="mv2-hero-img" src={mochiImg} alt="" />
        <div className="mv2-hero-veil" />
        <div className="mv2-hero-text">
          <div className="tiny mv2-hero-date">{dateLine}</div>
          <h1 className="display">{t2(greetingKey())}</h1>
          <p className="voice mv2-hero-voice">
            {!loaded ? t2('v2.mochi.voice.hunting')
              : slots.length ? t2('v2.mochi.voice.found')
              : t2('v2.mochi.voice.quiet')}
          </p>
        </div>
      </section>

      {loaded && slots.length > 0 && (
        <div id="focus" className="grid-3 mv2-focus-grid">
          {slots.map(key => (
            <FocusCard
              key={key}
              card={today[key]}
              role={today[key].today_role || key}
              isOpen={openFocus === key}
              onDetails={() => setOpenFocus(prev => (prev === key ? null : key))}
              showToast={showToast}
            />
          ))}
        </div>
      )}

      {loaded && slots.length === 0 && (
        <div className="empty mv2-focus-empty">
          <img src="/assets/illustrations/immediate_best_moves.svg" alt="" />
          <p className="voice">{t2('v2.mochi.voice.quiet')}</p>
        </div>
      )}

      {/* ── The Hunt Board ── */}
      {opps?.sections && (
        <HuntBoard
          sections={opps.sections}
          removed={removed}
          onRemove={handleRemove}
          showToast={showToast}
        />
      )}

      {toast && <div className="toast">{toast}</div>}
    </main>
  )
}
