import test from 'node:test'
import assert from 'node:assert/strict'
import {
  locF,
  isEnglishText,
  parseDeadlineDate,
  formatDeadline,
  localizeDeadline,
  daysUntilDeadline,
  isUrgentDeadline,
} from './localize.js'

// A minimal stand-in for the bound translator: resolves the sentinel keys we
// route through i18n.
const T = (key) => ({
  'loc.unknown': '待确认',
  'loc.verify': '待核实',
  'loc.rolling': '常年开放',
}[key] || key)

// ── isEnglishText ─────────────────────────────────────────────────────────────

test('isEnglishText: Latin-only is English, CJK is not', () => {
  assert.equal(isEnglishText('Twice-yearly (spring/autumn)'), true)
  assert.equal(isEnglishText('每年两次'), false)
  assert.equal(isEnglishText('ZINEフェス東京'), false) // has CJK
  assert.equal(isEnglishText(''), false)
})

// ── locF ──────────────────────────────────────────────────────────────────────

test('locF: prefers the localized _zh field in zh view', () => {
  const opp = { summary: 'English summary', summary_zh: '中文摘要' }
  assert.equal(locF(opp, 'summary', 'zh', T), '中文摘要')
})

test('locF: English view shows the source value', () => {
  const opp = { summary: 'English summary', summary_zh: '中文摘要' }
  assert.equal(locF(opp, 'summary', 'en', T), 'English summary')
})

test('locF: suppresses English free-text with no _zh in zh view (no leak)', () => {
  const opp = { summary: 'Twice-yearly (spring/autumn) — watch @mochi' }
  assert.equal(locF(opp, 'summary', 'zh', T), '')
})

test('locF: routes the "Unknown" sentinel through i18n', () => {
  const opp = { location: 'Unknown' }
  assert.equal(locF(opp, 'location', 'zh', T), '待确认')
})

test('locF: routes "Check source" sentinel through i18n (no internal placeholder)', () => {
  const opp = { location: 'Check source' }
  assert.equal(locF(opp, 'location', 'zh', T), '待核实')
})

test('locF: keeps CJK source text even with no _zh (e.g. ja note in ja view)', () => {
  const opp = { note: '東京の画廊' }
  assert.equal(locF(opp, 'note', 'ja', T), '東京の画廊')
})

test('locF: empty / missing returns empty string', () => {
  assert.equal(locF({}, 'summary', 'zh', T), '')
  assert.equal(locF(null, 'summary', 'zh', T), '')
})

// ── deadlines ──────────────────────────────────────────────────────────────────

test('parseDeadlineDate: parses ISO, returns null for rolling/sentinels', () => {
  assert.equal(parseDeadlineDate('2026-06-27').getFullYear(), 2026)
  assert.equal(parseDeadlineDate('rolling'), null)
  assert.equal(parseDeadlineDate('Unknown'), null)
  assert.equal(parseDeadlineDate(''), null)
})

test('formatDeadline: zh formats as 年月日', () => {
  assert.equal(formatDeadline('2026-06-27', 'zh'), '2026年6月27日')
})

test('localizeDeadline: prefers deadline_zh', () => {
  const opp = { deadline: '2026-06-27', deadline_zh: '2026年6月27日（春季）' }
  assert.equal(localizeDeadline(opp, 'zh', T), '2026年6月27日（春季）')
})

test('localizeDeadline: routes sentinel deadline through i18n', () => {
  assert.equal(localizeDeadline({ deadline: 'Unknown' }, 'zh', T), '待确认')
  assert.equal(localizeDeadline({ deadline: 'rolling' }, 'zh', T), '常年开放')
})

test('localizeDeadline: no English leak for unparseable English deadline in zh', () => {
  assert.equal(localizeDeadline({ deadline: 'Spring or autumn, watch site' }, 'zh', T), '待核实')
})

test('daysUntilDeadline / isUrgentDeadline: relative to today', () => {
  const inThree = new Date()
  inThree.setDate(inThree.getDate() + 3)
  const iso = inThree.toISOString().slice(0, 10)
  assert.equal(daysUntilDeadline(iso), 3)
  assert.equal(isUrgentDeadline(iso), true)

  const inThirty = new Date()
  inThirty.setDate(inThirty.getDate() + 30)
  const isoFar = inThirty.toISOString().slice(0, 10)
  assert.equal(isUrgentDeadline(isoFar), false)

  assert.equal(isUrgentDeadline('2000-01-01'), false) // past
  assert.equal(isUrgentDeadline('rolling'), false)    // no real date
})
