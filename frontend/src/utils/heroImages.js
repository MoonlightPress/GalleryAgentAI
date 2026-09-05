// Hero art for the three companions. Every companion now works the same way:
// drop a file in that companion's folder and it joins the rotation. Files with
// `_night` in the name are the evening art and are kept out of the daytime pool
// (HeroSection picks the pool by isNightNow(), so the two never mix).
//
// Mochi used to be the exception — a single hardcoded webp/png pair — which
// meant new art couldn't be added without a code change. It's globbed now like
// the other two (2026-09-04).

const mochiGlob      = import.meta.glob('../assets/heroes/mochi/*.webp',      { eager: true })
const peppercornGlob = import.meta.glob('../assets/heroes/peppercorn/*.{png,jpg,jpeg,webp}', { eager: true })
const saffronGlob    = import.meta.glob('../assets/heroes/saffron/*.{png,jpg,jpeg,webp}',    { eager: true })

// Split a glob into the daytime and evening pools by filename.
function pool(globResult, night) {
  return Object.entries(globResult)
    .filter(([path]) => path.includes('_night') === night)
    .map(([, mod]) => mod.default)
}

function pickRandom(urls) {
  if (!urls.length) return ''
  return urls[Math.floor(Math.random() * urls.length)]
}

// Mochi's hero renders through a <picture> with a WebP source and an <img>
// fallback. Every browser that matters has supported WebP since 2020 and the
// PNG twins were ~1.9 MB against ~0.15 MB for the WebP, so the fallback now
// points at the same WebP rather than shipping a second copy of the art — the
// <picture> element stays only because it costs nothing to leave in place.
//
// All current art is 1920×640. The original daytime illustration is 1920×621;
// declaring 640 for it reserves 19px more than it needs (~1%), which is not
// enough shift to be visible and keeps one set of intrinsic dims for the box.
function mochiSources(night) {
  const url = pickRandom(pool(mochiGlob, night))
  return { webp: url, png: url, width: 1920, height: 640 }
}

export const mochiHeroSources      = mochiSources(false)
export const mochiHeroNightSources = mochiSources(true)

// The whole pool, so the hero can be stepped through rather than only sampled.
// Random-per-load is right for her (a different painting each visit); being
// able to advance is what makes the set reviewable — and a tap for the next
// picture is a small pleasure rather than a control she has to understand.
export const mochiDayPool   = pool(mochiGlob, false)
export const mochiNightPool = pool(mochiGlob, true)

export const peppercornHero      = pickRandom(pool(peppercornGlob, false))
export const peppercornHeroNight = pickRandom(pool(peppercornGlob, true))
export const saffronHero         = pickRandom(pool(saffronGlob, false))
export const saffronHeroNight    = pickRandom(pool(saffronGlob, true))
