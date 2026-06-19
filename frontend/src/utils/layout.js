// Shared layout helpers.

// How many cards to reveal per batch before the "Show more" button.
// Mirrors the card grid's column count so a batch is ~two rows:
//   > 960px  -> 3 columns -> 6 cards
//   <= 960px -> 2 or 1 column -> 4 cards
// Evaluated at module load (once per page load), which is enough to be correct
// on each device without a resize listener.
export function cardsPerBatch() {
  if (typeof window === 'undefined') return 6
  return window.innerWidth > 960 ? 6 : 4
}
