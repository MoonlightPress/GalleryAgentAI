import { useState, useEffect } from 'react'
import { useLanguage } from '../i18n/LanguageContext'
import './TrackerSection.css'

// "What I've followed / applied to" in one place. Follows (★) come joined to
// opportunity data; applied (✓) are the submission-log entries auto-created when
// she marks an opportunity Applied. Hidden entirely until she has at least one.
export default function TrackerSection() {
  const { t } = useLanguage()
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch('/api/tracker')
      .then(r => (r.ok ? r.json() : null))
      .then(setData)
      .catch(() => {})
  }, [])

  if (!data) return null
  const follows = data.follows || []
  const applied = data.applied || []
  if (follows.length === 0 && applied.length === 0) return null

  return (
    <section className="tracker-section">
      <h2 className="tracker-title">{t('tracker.title')}</h2>
      <div className="tracker-cols">
        <div className="tracker-col">
          <div className="tracker-col-head">★ {t('tracker.following')} · {follows.length}</div>
          {follows.length === 0
            ? <p className="tracker-empty">{t('tracker.noFollows')}</p>
            : follows.map((f, i) => (
              <div key={i} className="tracker-row">
                {f.website
                  ? <a href={f.website} target="_blank" rel="noreferrer" className="tracker-name">{f.name}</a>
                  : <span className="tracker-name">{f.name}</span>}
                {f.deadline && <span className="tracker-meta">{f.deadline}</span>}
              </div>
            ))}
        </div>
        <div className="tracker-col">
          <div className="tracker-col-head">✓ {t('tracker.applied')} · {applied.length}</div>
          {applied.length === 0
            ? <p className="tracker-empty">{t('tracker.noApplied')}</p>
            : applied.map((a, i) => {
              const label = a.venue || a.what || a.id
              return (
                <div key={i} className="tracker-row">
                  {a.website
                    ? <a href={a.website} target="_blank" rel="noreferrer" className="tracker-name">{label}</a>
                    : <span className="tracker-name">{label}</span>}
                  {a.date && <span className="tracker-meta">{a.date}</span>}
                  {a.outcome && <span className="tracker-meta tracker-outcome">{a.outcome}</span>}
                </div>
              )
            })}
        </div>
      </div>
    </section>
  )
}
