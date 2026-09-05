// GENERATED - do not hand-edit. Regenerate with scripts/gen_hero_poem_tone.py
//
// Which colour the hero poem needs, measured per image rather than assumed
// from the clock. The poem sits at left 9%/width 30%, top 12%/height 64%
// (see HeroSection.css); that exact rectangle is sampled for mean luminance.
export const HERO_POEM_TONE = {
  "mochi_day_01.webp": "ink",
  "mochi_day_02.webp": "ink",
  "mochi_day_03.webp": "ink",
  "mochi_day_04.webp": "ink",
  "mochi_day_05.webp": "ink",
  "mochi_day_06.webp": "ink",
  "mochi_day_07.webp": "ink",
  "mochi_day_08.webp": "ink",
  "mochi_day_09.webp": "ink",
  "mochi_day_10.webp": "ink",
  "mochi_day_11.webp": "ink",
  "mochi_day_12.webp": "ink",
  "mochi_day_13.webp": "ink",
  "mochi_day_14.webp": "ink",
  "mochi_day_15.webp": "ink",
  "mochi_day_16.webp": "ink",
  "mochi_day_17.webp": "ink",
  "mochi_hero.webp": "ink",
  "mochi_hero_night.webp": "cream",
  "mochi_night_01.webp": "cream",
  "mochi_night_02.webp": "ink",
  "mochi_night_03.webp": "ink",
  "mochi_night_04.webp": "ink",
  "mochi_night_05.webp": "ink",
  "mochi_night_06.webp": "ink",
  "mochi_night_07.webp": "ink",
  "mochi_night_08.webp": "ink",
  "mochi_night_09.webp": "ink",
  "mochi_night_10.webp": "ink",
  "mochi_night_11.webp": "ink",
  "mochi_night_12.webp": "ink",
  "mochi_night_13.webp": "ink",
  "mochi_night_14.webp": "cream"
}

export const HERO_FOCAL_Y = {
  "mochi_day_01.webp": 63,
  "mochi_day_02.webp": 55,
  "mochi_day_03.webp": 51,
  "mochi_day_04.webp": 55,
  "mochi_day_05.webp": 53,
  "mochi_day_06.webp": 52,
  "mochi_day_07.webp": 53,
  "mochi_day_08.webp": 54,
  "mochi_day_09.webp": 54,
  "mochi_day_10.webp": 54,
  "mochi_day_11.webp": 53,
  "mochi_day_12.webp": 53,
  "mochi_day_13.webp": 51,
  "mochi_day_14.webp": 51,
  "mochi_day_15.webp": 54,
  "mochi_day_16.webp": 49,
  "mochi_day_17.webp": 55,
  "mochi_hero.webp": 53,
  "mochi_hero_night.webp": 54,
  "mochi_night_01.webp": 56,
  "mochi_night_02.webp": 53,
  "mochi_night_03.webp": 52,
  "mochi_night_04.webp": 54,
  "mochi_night_05.webp": 51,
  "mochi_night_06.webp": 52,
  "mochi_night_07.webp": 54,
  "mochi_night_08.webp": 53,
  "mochi_night_09.webp": 51,
  "mochi_night_10.webp": 51,
  "mochi_night_11.webp": 50,
  "mochi_night_12.webp": 53,
  "mochi_night_13.webp": 54,
  "mochi_night_14.webp": 55
}

function stemOf(url) {
  const file = String(url || '').split('/').pop()?.split('?')[0] || ''
  // Vite fingerprints filenames (mochi_day_03-B7XEVwCF.webp); match the stem.
  return { file, stem: file.replace(/-[A-Za-z0-9_]{8,}\.webp$/, '.webp') }
}

export function poemToneFor(url) {
  const { file, stem } = stemOf(url)
  return HERO_POEM_TONE[stem] || HERO_POEM_TONE[file] || 'ink'
}

// object-position Y for the hero crop, so a subject low in the frame is not
// cut off at the feet by a box far squarer than the painting.
export function focalYFor(url) {
  const { file, stem } = stemOf(url)
  return HERO_FOCAL_Y[stem] ?? HERO_FOCAL_Y[file] ?? 50
}
