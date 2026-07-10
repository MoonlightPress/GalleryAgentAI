import { useEffect, useRef } from 'react'
import { track } from '../utils/track'
import { landedRatio, LANDED_RATIO } from '../utils/sectionVisibility'

const SECTION_DWELL_MS = 2000

// A tall section's ratio-against-itself tops out well below 0.5, so a single
// [0.5] threshold never even invokes the callback for one. Fine-grained
// thresholds make the browser call us as the section scrolls through; the real
// landed/not-landed decision is landedRatio(), which measures against the
// screen. See utils/sectionVisibility.js.
const THRESHOLDS = Array.from({ length: 21 }, (_, i) => i / 20)

// Fires one nav event when the wrapped section is genuinely landed on (filling
// half the screen, or half of itself if it's shorter, for the dwell time), so
// scrolling past doesn't spam. Once per mount. Layout-neutral: a plain block
// wrapper with no margin of its own.
export default function TrackedSection({ page = 'discover', section, children }) {
  const ref = useRef(null)
  const firedRef = useRef(false)
  const timerRef = useRef(null)

  useEffect(() => {
    const el = ref.current
    if (!el || typeof IntersectionObserver === 'undefined') return
    const obs = new IntersectionObserver(
      ([entry]) => {
        const viewportHeight = entry.rootBounds?.height
          ?? (typeof window !== 'undefined' ? window.innerHeight : 0)
        const landed = entry.isIntersecting && landedRatio({
          intersectionHeight: entry.intersectionRect?.height,
          sectionHeight: entry.boundingClientRect?.height,
          viewportHeight,
        }) >= LANDED_RATIO

        if (landed) {
          if (!firedRef.current && timerRef.current == null) {
            timerRef.current = setTimeout(() => {
              firedRef.current = true
              timerRef.current = null
              track({ type: 'nav', page, section })
            }, SECTION_DWELL_MS)
          }
        } else if (timerRef.current != null) {
          clearTimeout(timerRef.current)
          timerRef.current = null
        }
      },
      { threshold: THRESHOLDS },
    )
    obs.observe(el)
    return () => {
      obs.disconnect()
      if (timerRef.current != null) clearTimeout(timerRef.current)
    }
  }, [page, section])

  return <div ref={ref} className="tracked-section">{children}</div>
}
