// Small display guards.

// True when `candidate` has real text that isn't just a repeat of `other`.
// Used to hide a "why it fits" paragraph that merely duplicates the
// summary/overview (some opportunities have no distinct why-it-fits and fall
// back to the summary text).
export function isDistinct(candidate, other) {
  const a = (candidate ?? '').trim()
  if (!a) return false
  const b = (other ?? '').trim()
  return a !== b
}
