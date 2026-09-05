// GENERATED — do not hand-edit. Regenerate with scripts/gen_hero_poem_tone.py
//
// Which colour the hero poem needs, measured per image rather than assumed from
// the clock. The poem sits at left 9%/width 30%, top 12%/height 64% (see
// HeroSection.css), so that exact rectangle is sampled for mean luminance:
// a pale patch takes dark ink, a dim one takes cream.
//
// This existed as a time-of-day rule — every night hero got cream, because the
// first night illustration had a dim brown wall behind the verse. Twelve of the
// fifteen night paintings added on 2026-09-04 are pale in that corner, so the
// cream verse vanished into them.
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

export function poemToneFor(url) {
  const file = String(url || '').split('/').pop()?.split('?')[0] || ''
  // Vite fingerprints filenames (mochi_day_03-B7XEVwCF.webp), so match the stem.
  const stem = file.replace(/-[A-Za-z0-9_]{8,}\.webp$/, '.webp')
  return HERO_POEM_TONE[stem] || HERO_POEM_TONE[file] || 'ink'
}
