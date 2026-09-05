"""Regenerate frontend/src/utils/heroPoemTone.js.

Run after adding or replacing Mochi hero art:

    python scripts/gen_hero_poem_tone.py

The hero poem is white-on-image, and whether it reads depends entirely on what
happens to be behind it. That used to be decided by the clock — night heroes got
cream, day heroes got ink — which held only because the first night illustration
had a dim brown wall behind the verse. Twelve of the fifteen night paintings
added 2026-09-04 are pale in that same corner, so the cream verse disappeared.

So measure it instead: sample the exact rectangle the poem occupies (left 9%,
width 30%, top 12%, height 64% — see HeroSection.css) and pick the tone from its
mean luminance.
"""

import json
from pathlib import Path

from PIL import Image, ImageStat

ROOT = Path(__file__).resolve().parent.parent
HERO_DIR = ROOT / "frontend" / "src" / "assets" / "heroes" / "mochi"
OUT = ROOT / "frontend" / "src" / "utils" / "heroPoemTone.js"

# Above this the patch is pale enough for dark ink; below it, cream reads better.
LUMINANCE_SPLIT = 150


def poem_region_luminance(path: Path) -> float:
    im = Image.open(path).convert("L")
    w, h = im.size
    box = (int(0.09 * w), int(0.12 * h), int(0.39 * w), int(0.76 * h))
    return ImageStat.Stat(im.crop(box)).mean[0]


def main() -> None:
    tone = {}
    for f in sorted(HERO_DIR.glob("*.webp")):
        lum = poem_region_luminance(f)
        tone[f.name] = "ink" if lum > LUMINANCE_SPLIT else "cream"
        print(f"  {lum:6.1f}  {tone[f.name]:5}  {f.name}")

    header = (
        "// GENERATED - do not hand-edit. Regenerate with scripts/gen_hero_poem_tone.py\n"
        "//\n"
        "// Which colour the hero poem needs, measured per image rather than assumed\n"
        "// from the clock. The poem sits at left 9%/width 30%, top 12%/height 64%\n"
        "// (see HeroSection.css); that exact rectangle is sampled for mean luminance.\n"
    )
    fn = (
        "\n\nexport function poemToneFor(url) {\n"
        "  const file = String(url || '').split('/').pop()?.split('?')[0] || ''\n"
        "  // Vite fingerprints filenames (mochi_day_03-B7XEVwCF.webp); match the stem.\n"
        "  const stem = file.replace(/-[A-Za-z0-9_]{8,}\\.webp$/, '.webp')\n"
        "  return HERO_POEM_TONE[stem] || HERO_POEM_TONE[file] || 'ink'\n"
        "}\n"
    )
    OUT.write_text(
        header + "export const HERO_POEM_TONE = " + json.dumps(tone, indent=2) + fn,
        encoding="utf-8",
    )
    ink = sum(1 for v in tone.values() if v == "ink")
    print(f"\nwrote {OUT.relative_to(ROOT)} - {ink} ink, {len(tone) - ink} cream")


if __name__ == "__main__":
    main()
