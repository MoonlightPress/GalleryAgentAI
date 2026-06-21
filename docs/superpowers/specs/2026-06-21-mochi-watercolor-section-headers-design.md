# Mochi Watercolor Section Headers

## Intent

Mochi's browse sections should be recognized as small painted places and working moments, not as emoji labels.
Each heading uses a section-specific watercolor vignette with the live title and item count nested inside its
pale negative space.

## Composition

- Desktop header art is 72px tall; mobile art is 56px tall.
- The scene occupies the left or lower edge and dissolves into paper-colored negative space.
- The localized HTML title and count sit inside the image area, never baked into the bitmap.
- The existing description remains directly below the image strip.
- The existing emoji is hidden once an illustration is available.

## Scene Set

- Today's Focus: a working desk with three selected notes.
- Strongest Picks: a folio with three carefully chosen sheets.
- Immediate Best Moves: a prepared portfolio and an open path forward.
- Open Calls: a welcoming gallery doorway and notice board.
- Publication / Editorial: an editor's desk with proofs and brushes.
- Competitions / Awards: a framed watercolor and a restrained ribbon.
- Zines / Print: an independent bookstore and handmade-zine display.
- Venue Targets: a small neighborhood gallery storefront.
- Watch List: a studio window, calendar, and quietly waiting materials.
- Press / Visibility: editorial clippings and a laid-out arts page.
- People: a quiet cafe table set for a conversation.

## Visual Contract

The assets share textured off-white paper, graphite underdrawing, translucent pigment, muted sage, indigo,
ochre, dusty rose, and walnut. They contain no words, logos, people, UI, or legible signage. The paintings must
feel adult, observant, and handmade rather than cute or decorative.

## Responsive And Accessibility

Images are decorative CSS backgrounds, so the live heading remains the accessible name. Long localized titles
may wrap inside the available negative space. Mobile uses a tighter crop and never increases page width.

## Verification

Run `npm.cmd test`, `npm.cmd run lint`, and `npm.cmd run build` in `frontend/`. Capture desktop and 390px mobile
screenshots, confirm the title remains legible in each scene, and confirm no header exceeds the target height.
