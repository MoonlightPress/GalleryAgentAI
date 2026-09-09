import { useState, useEffect } from 'react'
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
//
// The set is NOT uniformly composed the same way — measuring the alpha-channel
// centroid of all 18 source images (Scott's own reference set) found a clean 9/9
// split between art that hugs the canvas's right edge and art that hugs its
// left. The code used to assume everything hugged the right and mirrored
// (scaleX(-1)) whichever copy went on the left — correct for exactly half the
// set and backwards for the other half, which is what put flowers "on the wrong
// side" after the transparency fix made the bug visible instead of hidden under
// an opaque white canvas. Fixed by keeping two pools and never mirroring: each
// side draws only from images natively drawn to hug that edge.
const BOTANICAL_RIGHT = new Set(['artsupplies-vine', 'bird', 'cream-floral-b', 'fern', 'jasmine-vine', 'lavender'])
const BOTANICAL_LEFT = new Set(['books-vine', 'cream-floral-a', 'cream-floral-c', 'daisy-vine', 'roses', 'wisteria'])

function pick(pool, seed) {
  return pool[Math.abs(seed) % pool.length]
}

function rollAccents() {
  const rightPool = ACCENTS.filter((a) => BOTANICAL_RIGHT.has(a.name))
  const leftPool = ACCENTS.filter((a) => BOTANICAL_LEFT.has(a.name))
  const seed = Math.floor(Math.random() * 100000)
  const result = []
  if (rightPool.length) result.push({ ...pick(rightPool, seed), side: 'right' })
  if (leftPool.length) result.push({ ...pick(leftPool, seed >> 3), side: 'left' })
  return result
}

/**
 * Two botanical strips down the page edges, site-wide (rendered once in
 * App.jsx, not per-companion-page) — re-rolled per companion, so Mochi,
 * Saffron, and Peppercorn each get their own pair instead of showing the
 * identical two flowers everywhere ("they're all using the same images").
 *
 * Hidden below 1100px. On her phone the column already fills the width and an
 * edge strip would sit under the text rather than beside it.
 *
 * `page` drives BOTH the re-roll and the top-of-content re-measurement below —
 * each companion has a different subnav/header height, so both which flowers
 * show and where they sit legitimately differ per page.
 */
export default function PaperAccents({ page }) {
  const [chosen, setChosen] = useState(rollAccents)
  // React's documented pattern for "reset state when a prop changes" without an
  // effect: setState during render, guarded by comparing against a ref-like
  // state value. React re-renders immediately with the new state before
  // committing, so this never paints the stale pair — an effect doing the same
  // setState is flagged by this repo's lint (react-hooks/set-state-in-effect)
  // because it costs an extra full render pass for no benefit here.
  const [lastPage, setLastPage] = useState(page)
  if (page !== lastPage) {
    setLastPage(page)
    setChosen(rollAccents())
  }

  // Both accents pin to the SAME point, just below the page's stable chrome —
  // not a random percentage of the whole scrollable page (put them inside the
  // hero, or halfway down an arbitrarily long page), and not the top of a
  // "content" element whose measured position included conditional, dismissible
  // banners/intros above it (their height comes and goes with localStorage
  // state and async checks, which kept shifting this and reads as "the flowers
  // moved for no reason").
  //
  // Fix: every page marks its LAST unconditional chrome element with
  // .page-content-start — the shared <Nav/> (site-nav) always carries it, and a
  // page with its own always-rendered sub-nav (Mochi's QuickNav, Saffron's
  // .sf-tabs) marks that too, later in the DOM. We take the LAST match and use
  // its BOTTOM edge, so a page with a sub-nav anchors below that, and a page
  // without one (Peppercorn) falls back to just below the shared nav — never
  // dependent on whether a dismissible intro/banner happens to be showing.
  const [contentTop, setContentTop] = useState(null)
  useEffect(() => {
    let debounceId = null
    const measure = () => {
      const root = document.querySelector('.app')
      const markers = document.querySelectorAll('.page-content-start')
      const content = markers[markers.length - 1]
      if (!root || !content) return
      setContentTop(content.getBoundingClientRect().bottom - root.getBoundingClientRect().top)
    }
    const measureDebounced = () => {
      if (debounceId) clearTimeout(debounceId)
      debounceId = setTimeout(measure, 120)
    }
    measure()
    // The target page is lazy-loaded and fetches its own data, and cards below
    // .page-content-start keep arriving/resizing well after it first appears
    // (async opportunity/section data, images), so a one-shot measurement can
    // be taken before the layout settles. A ResizeObserver re-measures instead
    // for as long as things keep moving, and does nothing once settled.
    //
    // This USED to observe(document.body) — the whole page, not just the
    // marker. On a phone, that's what actually caused "flowers follow me while
    // scrolling" and "flowers jump when I switch tabs": the mobile browser's
    // address bar hiding/showing on scroll (and tab visibility changes)
    // resizes the *viewport*, which recomputes `.app`'s 100svh-based height —
    // a real, constant stream of body-level layout changes that has nothing to
    // do with where the marker actually is, but retriggered this on every one
    // of them, at one point badly enough to make the whole page janky. The
    // fix is to only watch the marker element(s) themselves, which resize far
    // less often, plus a short debounce so a burst of events (a scroll-driven
    // toolbar animation, several ResizeObserver callbacks in one frame) only
    // triggers one recalculation instead of one per event.
    const ro = new ResizeObserver(measureDebounced)
    document.querySelectorAll('.page-content-start').forEach((el) => ro.observe(el))
    window.addEventListener('resize', measureDebounced)
    return () => {
      if (debounceId) clearTimeout(debounceId)
      ro.disconnect()
      window.removeEventListener('resize', measureDebounced)
    }
  }, [page])

  if (!chosen.length) return null
  const top = (contentTop ?? 260) + 24
  return (
    <div className="paper-accents" aria-hidden="true">
      {chosen.map((a) => (
        <img
          key={a.side}
          src={a.url}
          alt=""
          draggable={false}
          className={`paper-accent paper-accent--${a.side}`}
          style={{ top: `${top}px` }}
        />
      ))}
    </div>
  )
}
