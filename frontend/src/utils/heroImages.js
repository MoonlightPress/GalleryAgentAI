const peppercornGlob = import.meta.glob('../assets/heroes/peppercorn/*.{png,jpg,jpeg,webp}', { eager: true })
const saffronGlob = import.meta.glob('../assets/heroes/saffron/*.{png,jpg,jpeg,webp}', { eager: true })

function pickRandom(globResult) {
  const urls = Object.values(globResult).map(m => m.default)
  if (!urls.length) return ''
  return urls[Math.floor(Math.random() * urls.length)]
}

// Mochi's hero is a single illustration served from a <picture> with a WebP
// preferred and the PNG as fallback — so it's imported explicitly (not globbed)
// to keep the two formats paired and out of the random pool. The PNG is 1920×621;
// pass those intrinsic dims to the <img> to reserve space (no layout shift).
import mochiHeroPngUrl from '../assets/heroes/mochi/mochi_hero.png'
import mochiHeroWebpUrl from '../assets/heroes/mochi/mochi_hero.webp'

export const mochiHeroSources = {
  webp:   mochiHeroWebpUrl,
  png:    mochiHeroPngUrl,
  width:  1920,
  height: 621,
}
// Back-compat default (PNG): existing imports of `mochiHero` keep working.
export const mochiHero = mochiHeroPngUrl

export const peppercornHero = pickRandom(peppercornGlob)
export const saffronHero = pickRandom(saffronGlob)
