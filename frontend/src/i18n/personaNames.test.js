import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'
import { LOCALES } from './translations.js'

// THE RULE (Scott, 2026-06-26): the Chinese UI must never show an English
// persona name, nor an old/renamed one. Companion names in zh are:
//   麻薯 (Mochi) · 山楂 (Saffron) · 胡椒粒 / 花椒 (Peppercorn)
// This guard fails the build the moment a name leaks back in — which is the
// whole class of bug that kept biting (English / stale names in the 中文 view).
const here = dirname(fileURLToPath(import.meta.url))

const FORBIDDEN_IN_ZH = ['Mochi', 'Saffron', 'Peppercorn', '红雀', '猫饼']

test('no persona-name leaks in the zh strings', () => {
  const leaks = []
  for (const [key, val] of Object.entries(LOCALES.zh)) {
    if (typeof val !== 'string') continue
    for (const bad of FORBIDDEN_IN_ZH) {
      if (val.includes(bad)) leaks.push(`${key}: contains "${bad}" -> ${val.slice(0, 60)}`)
    }
  }
  assert.equal(leaks.length, 0, 'zh persona-name leaks found:\n' + leaks.join('\n'))
})

// Stronger regression guard: the OLD zh names must never reappear anywhere in the
// shipped UI source — catches hardcoded strings outside the i18n dict (the
// SaffronPage SF_ZH map, saffron_insights, the nav name map).
const OLD_NAMES = ['红雀', '猫饼']
const SOURCES = [
  '../components/SaffronPage.jsx',
  '../components/Nav.jsx',
  '../data/saffron_insights.js',
]

test('the old zh names never reappear in component / data source', () => {
  const leaks = []
  for (const rel of SOURCES) {
    const text = readFileSync(join(here, rel), 'utf-8')
    for (const bad of OLD_NAMES) {
      if (text.includes(bad)) leaks.push(`${rel}: contains "${bad}"`)
    }
  }
  assert.equal(leaks.length, 0, 'old persona names resurfaced:\n' + leaks.join('\n'))
})
