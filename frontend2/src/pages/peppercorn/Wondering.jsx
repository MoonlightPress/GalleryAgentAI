// THE WONDERING — one question at a time, eight pebbles of progress.
// Logic ported from v1 SaffronQuestionsSection (same keys, same save contract).
import { useState, useEffect, useRef } from 'react'
import { useLanguage } from '../../i18n/LanguageContext'
import { useLocalT } from '../../i18n/local'
import { strings } from './strings'

// Static keys — language-independent, must match the backend profile fields.
export const QUESTION_KEYS = [
  'posting_frequency',
  'audience_geography',
  'has_sold_work',
  'new_publication_planned',
  'has_artist_statement',
  'tide_china_contact',
  'second_exhibition_planned',
  'price_points',
]

function buildQuestions(t) {
  return QUESTION_KEYS.map((key, i) => ({
    key,
    text: t(`pp.q.${i}.text`),
    why:  t(`pp.q.${i}.why`),
    options: [0, 1, 2, 3].map(j => t(`pp.q.${i}.opt.${j}`)),
  }))
}

export default function Wondering({ data, onSave }) {
  const { t } = useLanguage()
  const t2 = useLocalT(strings)
  const [answers, setAnswers] = useState(data || {})
  const [activeIdx, setActiveIdx] = useState(0)
  const [draft, setDraft] = useState('')
  const initialised = useRef(false)

  const QUESTIONS = buildQuestions(t)

  useEffect(() => { setAnswers(data || {}) }, [data])

  // Once real answers arrive, open on the first unanswered question.
  useEffect(() => {
    if (initialised.current || !data) return
    initialised.current = true
    const first = QUESTION_KEYS.findIndex(k => !data[k])
    if (first !== -1) { setActiveIdx(first); setDraft('') }
  }, [data]) // eslint-disable-line react-hooks/exhaustive-deps

  const answeredCount = QUESTION_KEYS.filter(k => answers[k]).length
  const allAnswered   = answeredCount === QUESTION_KEYS.length
  const currentQ      = QUESTIONS[activeIdx]

  function selectQ(idx) {
    setActiveIdx(idx)
    setDraft(displayAnswer(answers[QUESTIONS[idx].key]) || '')
  }

  function saveAnswer() {
    if (!draft.trim()) return
    const next = { ...answers, [currentQ.key]: draft.trim() }
    setAnswers(next)
    onSave(next)
    const nextUnanswered = QUESTIONS.findIndex((q, i) => i > activeIdx && !next[q.key])
    if (nextUnanswered !== -1) { setActiveIdx(nextUnanswered); setDraft('') }
  }

  function clearAnswer(key) {
    const next = { ...answers, [key]: null }
    setAnswers(next)
    onSave(next)
  }

  function skipQ() {
    const next = QUESTIONS.findIndex((q, i) => i > activeIdx && !answers[q.key])
    if (next !== -1) { setActiveIdx(next); setDraft('') }
  }

  // Booleans come back from the pipeline profile (e.g. has_artist_statement: true).
  function displayAnswer(v) {
    if (v === true) return t2('v2.peppercorn.answer.yes')
    if (v === null || v === undefined || v === false) return ''
    return String(v)
  }

  return (
    <section className="pep-wondering" aria-label={t2('v2.peppercorn.wondering.title')}>
      <div className="sec-head sec-head--leaf">
        <h2 className="h-section">{t2('v2.peppercorn.wondering.title')}</h2>
        <p className="sec-sub">{t2('v2.peppercorn.wondering.sub')}</p>
      </div>

      {/* Eight pebbles */}
      <div className="pep-pebbles" role="tablist" aria-label={t2('v2.peppercorn.wondering.progress', { n: answeredCount })}>
        {QUESTIONS.map((q, i) => (
          <button
            key={q.key}
            role="tab"
            aria-selected={i === activeIdx}
            className={[
              'pep-pebble',
              answers[q.key] ? 'pep-pebble--done' : '',
              i === activeIdx && !allAnswered ? 'pep-pebble--active' : '',
            ].join(' ').trim()}
            onClick={() => selectQ(i)}
            title={q.text}
          />
        ))}
        <span className="pep-pebble-count tiny">{t2('v2.peppercorn.wondering.progress', { n: answeredCount })}</span>
      </div>

      {allAnswered ? (
        <div className="card card--quiet pep-content-card">
          <p className="voice">{t2('v2.peppercorn.wondering.content')}</p>
        </div>
      ) : (
        <div className="card pep-q-card">
          <div className="tiny pep-q-num">{t('pp.question', { n: activeIdx + 1 })}</div>
          <p className="pep-q-text h-card">{currentQ.text}</p>
          <p className="pep-q-why voice small">{currentQ.why}</p>
          <div className="pep-q-options">
            {currentQ.options.map((opt, i) => (
              <button key={i} className="btn-quiet pep-q-option" onClick={() => setDraft(opt)}>{opt}</button>
            ))}
          </div>
          <textarea
            className="pep-input pep-q-input"
            value={draft}
            onChange={e => setDraft(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && (e.metaKey || e.ctrlKey) && saveAnswer()}
            placeholder={t('pp.q.input.placeholder')}
            rows={3}
          />
          <div className="pep-q-actions">
            <button className="btn-warm" onClick={saveAnswer} disabled={!draft.trim()}>
              {t('pp.saveAnswer')}
            </button>
            {!answers[currentQ.key] && (
              <button className="btn-ghost" onClick={skipQ}>{t('pp.comeBack')}</button>
            )}
            {answers[currentQ.key] && (
              <button className="btn-ghost" onClick={() => clearAnswer(currentQ.key)}>{t('pp.clearAnswer')}</button>
            )}
          </div>
        </div>
      )}

      {answeredCount > 0 && (
        <div className="pep-answered">
          <div className="tiny pep-block-label">{t('pp.answered', { n: answeredCount })}</div>
          {QUESTIONS.filter(q => answers[q.key]).map(q => (
            <button key={q.key} className="pep-answered-row" onClick={() => selectQ(QUESTIONS.indexOf(q))}>
              <span className="pep-answered-check" aria-hidden="true">✓</span>
              <span className="pep-answered-body">
                <span className="pep-answered-q small">{q.text}</span>
                <span className="pep-answered-a small">{displayAnswer(answers[q.key])}</span>
              </span>
            </button>
          ))}
        </div>
      )}
    </section>
  )
}
