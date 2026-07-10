// "Has this section been landed on?" — measured against the screen, not the
// section.
//
// The original test compared the intersection to the section's OWN height and
// required 50%. A section taller than the viewport can never be 50% of itself
// on screen, so it never fired. `open_calls` — the long opportunity grid — has
// never once reported a landing from a phone, despite people opening cards
// inside it. We were blind to exactly the scrolling we most wanted to see.
//
// The fix: a section has landed when it fills half of whatever is smaller,
// itself or the screen. A short section must be half visible; a tall one must
// cover half the screen.

export const LANDED_RATIO = 0.5

export function landedRatio({ intersectionHeight, sectionHeight, viewportHeight }) {
  const visible = Math.max(0, intersectionHeight || 0)
  const reference = Math.min(sectionHeight || 0, viewportHeight || 0)
  if (!(reference > 0)) return 0
  return Math.min(1, visible / reference)
}
