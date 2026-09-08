import { useState } from 'react'
import './PaperAccents.css'

// Watercolour accents painted on a WHITE ground (docs/design/saffron_visual_pass_
// 2026-09-08/overlays_vertical). They are composited with mix-blend-mode:multiply,
// which drops pure white to nothing and lets only the paint darken the paper
// underneath — so no cut-out mask is needed and the edges stay soft.
//
// Vite gives every file a hashed URL at build time; the browser only fetches the
// two the page actually renders, so having eighteen on the server costs nothing.
const FILES = import.meta.glob('../assets/accents/*.webp', {
  eager: true,
  query: '?url',
  import: 'default',
})
const ACCENTS = Object.entries(FILES)
  .map(([path, url]) => ({ url, name: path.split('/').pop().replace('.webp', '') }))
  .sort((a, b) => a.name.localeCompare(b.name))

// The still-life pieces (a cat on a shelf, a pegboard of brushes) read as
// illustrations of a scene and pull the eye; the botanical strips read as paper.
// Only the botanicals go behind text.
const BOTANICAL = new Set([
  'artsupplies-vine', 'bird', 'books-vine', 'cream-floral-a', 'cream-floral-b',
  'cream-floral-c', 'daisy-vine', 'fern', 'jasmine-vine', 'lavender', 'roses',
  'wisteria',
])

function pick(pool, seed) {
  return pool[Math.abs(seed) % pool.length]
}

/**
 * Two botanical strips down the page edges, different on each visit.
 *
 * Deliberately NOT random per render. The choice is made once in a lazy state
 * initialiser, so nothing reshuffles under her while she is reading and changing
 * tabs does not redraw the flowers. (useMemo would be the obvious tool, but
 * Math.random() inside one is impure and the React Compiler refuses to preserve
 * it — a state initialiser is the supported way to hold a stable random value.)
 *
 * Hidden below 1100px. On her phone the column already fills the width and an
 * edge strip would sit under the text rather than beside it.
 */
export default function PaperAccents() {
  const [chosen] = useState(() => {
    const pool = ACCENTS.filter((a) => BOTANICAL.has(a.name))
    if (!pool.length) return []
    const seed = Math.floor(Math.random() * 100000)
    const top = pick(pool, seed)
    const rest = pool.filter((a) => a.name !== top.name)
    const bottom = pick(rest.length ? rest : pool, seed >> 3)
    return [
      { ...top, side: 'right', offset: 4 + ((seed >> 5) % 10) },
      { ...bottom, side: 'left', offset: 46 + ((seed >> 7) % 14) },
    ]
  })

  if (!chosen.length) return null
  return (
    <div className="paper-accents" aria-hidden="true">
      {chosen.map((a) => (
        <img
          key={a.side}
          src={a.url}
          alt=""
          draggable={false}
          className={`paper-accent paper-accent--${a.side}`}
          style={{ top: `${a.offset}%` }}
        />
      ))}
    </div>
  )
}
