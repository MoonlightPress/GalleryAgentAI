const peppercornGlob = import.meta.glob('../assets/heroes/peppercorn/*.{png,jpg,jpeg,webp}', { eager: true })
const saffronGlob = import.meta.glob('../assets/heroes/saffron/*.{png,jpg,jpeg,webp}', { eager: true })

function pickRandom(globResult) {
  // `*_night.*` files are the evening art, chosen explicitly by time of day —
  // keep them out of the random daytime pool.
  const urls = Object.entries(globResult)
    .filter(([path]) => !path.includes('_night'))
    .map(([, m]) => m.default)
  if (!urls.length) return ''
  return urls[Math.floor(Math.random() * urls.length)]
}

// Mochi's hero is a single illustration served from a <picture> with a WebP
// preferred and the PNG as fallback — so it's imported explicitly (not globbed)
// to keep the two formats paired and out of the random pool. The PNG is 1920×621;
// pass those intrinsic dims to the <img> to reserve space (no layout shift).
import mochiHeroPngUrl from '../assets/heroes/mochi/mochi_hero.png'
import mochiHeroWebpUrl from '../assets/heroes/mochi/mochi_hero.webp'
// Night-time variant (Mochi watching the fireworks) — 1920×640, same <picture> pattern.
import mochiHeroNightPngUrl from '../assets/heroes/mochi/mochi_hero_night.png'
import mochiHeroNightWebpUrl from '../assets/heroes/mochi/mochi_hero_night.webp'
// Night-time Saffron (robin over the town, hanabi in the sky) — webp only, like the daytime one.
import saffronHeroNightWebpUrl from '../assets/heroes/saffron/saffron_hero_night.webp'
// Night-time Peppercorn (mouse in a teacup, lantern + fireworks) — webp only. Kept out of the
// daytime random pool by pickRandom's `_night` filter above.
import peppercornHeroNightWebpUrl from '../assets/heroes/peppercorn/peppercorn_hero_night.webp'

export const mochiHeroSources = {
  webp:   mochiHeroWebpUrl,
  png:    mochiHeroPngUrl,
  width:  1920,
  height: 621,
}
export const mochiHeroNightSources = {
  webp:   mochiHeroNightWebpUrl,
  png:    mochiHeroNightPngUrl,
  width:  1920,
  height: 640,
}
// Back-compat default (PNG): existing imports of `mochiHero` keep working.
export const mochiHero = mochiHeroPngUrl

export const peppercornHero = pickRandom(peppercornGlob)
export const peppercornHeroNight = peppercornHeroNightWebpUrl
export const saffronHero = pickRandom(saffronGlob)
export const saffronHeroNight = saffronHeroNightWebpUrl
