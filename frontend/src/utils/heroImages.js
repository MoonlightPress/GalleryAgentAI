const mochiGlob = import.meta.glob('../assets/heroes/mochi/*.{png,jpg,jpeg,webp}', { eager: true })
const peppercornGlob = import.meta.glob('../assets/heroes/peppercorn/*.{png,jpg,jpeg,webp}', { eager: true })
const saffronGlob = import.meta.glob('../assets/heroes/saffron/*.{png,jpg,jpeg,webp}', { eager: true })

function pickRandom(globResult) {
  const urls = Object.values(globResult).map(m => m.default)
  if (!urls.length) return ''
  return urls[Math.floor(Math.random() * urls.length)]
}

export const mochiHero = pickRandom(mochiGlob)
export const peppercornHero = pickRandom(peppercornGlob)
export const saffronHero = pickRandom(saffronGlob)
