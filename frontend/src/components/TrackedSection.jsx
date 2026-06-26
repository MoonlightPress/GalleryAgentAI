import { useEffect, useRef } from 'react'
import { track } from '../utils/track'

const SECTION_DWELL_MS = 2000
const SECTION_VISIBLE_RATIO = 0.5

// Fires one nav event when the wrapped section is genuinely landed on (visible
// past the ratio for the dwell time), so scrolling past doesn't spam. Once per
// mount. Layout-neutral: a plain block wrapper with no margin of its own.
export default function TrackedSection({ section, children }) {
  const ref = useRef(null)
  const firedRef = useRef(false)
  const timerRef = useRef(null)

  useEffect(() => {
    const el = ref.current
    if (!el || typeof IntersectionObserver === 'undefined') return
    const obs = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && entry.intersectionRatio >= SECTION_VISIBLE_RATIO) {
          if (!firedRef.current && timerRef.current == null) {
            timerRef.current = setTimeout(() => {
              firedRef.current = true
              timerRef.current = null
              track({ type: 'nav', page: 'discover', section })
            }, SECTION_DWELL_MS)
          }
        } else if (timerRef.current != null) {
          clearTimeout(timerRef.current)
          timerRef.current = null
        }
      },
      { threshold: [SECTION_VISIBLE_RATIO] },
    )
    obs.observe(el)
    return () => {
      obs.disconnect()
      if (timerRef.current != null) clearTimeout(timerRef.current)
    }
  }, [section])

  return <div ref={ref} className="tracked-section">{children}</div>
}
